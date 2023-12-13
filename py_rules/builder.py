import datetime
import uuid
from .__version__ import __version__ as version
from py_rules.constants import Operators, Types
from py_rules.errors import InvalidRuleConditionError
from py_rules.utils import load_from_json, save_dict_to_json


class Condition:
    """
    A class to represent a condition.
    """

    def __init__(self, variable=None, operator=None, value=None, condition=None):
        """
        Initialize Condition with either a condition dictionary or variable, operator, and value.
        """
        if operator and operator not in Operators.list_all():
            raise InvalidRuleConditionError(f'Invalid operator - {operator}')

        if condition:
            self.condition = condition
        else:
            self.condition = {
                'condition': {
                    'variable': variable,
                    'operator': operator,
                    'value': self._build_value(value)
                }
            }

        self.required_context_parameters = set()
        if variable is not None:
            self.required_context_parameters.add(variable)

    def _build_value(self, value):
        """
        Build a dictionary representation of a value.
        """
        if isinstance(value, list):
            return {'type': 'list', 'value': [self._build_value(v) for v in value]}
        elif isinstance(value, dict):
            return {'type': 'dict', 'value': {k: self._build_value(v) for k, v in value.items()}}
        else:
            return {'type': type(value).__name__, 'value': value}
        
    def _create_new_condition(self, condition_dict, total_context_params=set()):
        """
        Create a new condition by passing in a condition dictionary.
        """
        condition = Condition(condition=condition_dict)
        condition.required_context_parameters = condition.required_context_parameters.union(total_context_params)
        return condition
        
    def __str__(self) -> str:
        return str(self.condition)

    def __and__(self, other):
        """
        Combine this condition and another condition with 'and'.
        """
        new_condition_dict = {'and': self._get_conditions('and', other)}
        total_context_params = self.required_context_parameters.union(other.required_context_parameters)
        return self._create_new_condition(new_condition_dict, total_context_params)

    def __or__(self, other):
        """
        Combine this condition and another condition with 'or'.
        """
        new_condition_dict = {'or': self._get_conditions('or', other)}
        total_context_params = self.required_context_parameters.union(other.required_context_parameters)
        return self._create_new_condition(new_condition_dict, total_context_params)

    def _get_conditions(self, operator, other):
        """
        Get a list of conditions combined with a specified operator.
        """
        return self.condition.get(operator, [self.condition]) + other.condition.get(operator, [other.condition])
    
    def get_required_context_parameters(self):
        return list(self.required_context_parameters)

    def to_dict(self):
        return self.condition


class Result:
    def __init__(self, key=None, vtype=None, value=None, result=None):
        if result:
            self.data = result
        else:
            self.data = {}
            self.data[key] = {
                'type': vtype,
                'value': value
            }

        self.required_context_parameters = set()

        if vtype == Types.VARIABLE and value is not None:
            self.required_context_parameters.add(value)

    def __str__(self):
        return str(self.to_dict())
    
    def __and__(self, other):
        merged = {**self.data, **other.data}
        total_context_params = self.required_context_parameters.union(other.required_context_parameters)
        return self._create_new_result(merged, total_context_params)
    
    def __or__(self, other):
        raise NotImplementedError
    
    def _create_new_result(self, result_dict, total_context_params=set()):
        """
        Create a new result by passing in a result dictionary.
        """
        result = Result(result=result_dict)
        result.required_context_parameters = result.required_context_parameters.union(total_context_params)
        return result
    
    def to_dict(self):
        return {"result": self.data}


class Rule:
    """
    A class to represent a rule.

    Example usage:

    A)
    condition = Condition('number', 'in', [1, 2, 3]) & Condition('number', '=', 1) & \
    Condition('number', '=', 1) | Condition('number', '=', 2)
    result = Result('xyz', 'str', 'Condition met') & Result('result', 'variable', 'xyz')
    rule1 = Rule('Complex rule').If(condition).Then(result).Else(result) 
    print(rule1.to_dict())

    B)
    rule = Rule('new-user-subscription').If(
        Condition('number', 'in', [1, 2, 3]) & Condition('number', '=', 1) | Condition('number', '=', 2)).Then(
            Result('result', 'variable', 'number')).Else(
                Rule('new-user-subscription').If(Condition('number', 'in', [1, 2, 3])).Then(
                    Result().add('result', 'variable', 'number')))
    print(rule.to_dict())
    """

    def __init__(self, name, **kwargs):
        """
        Initialize Rule with a rule name.
        """
        self.name = name
        self.kwargs = kwargs
        self.id = kwargs.get('id') if kwargs.get('id') else str(uuid.uuid4())
        self.parent_id = kwargs.get('parent_id') if kwargs.get('parent_id') else None
        self.rule_metadata = self.load_rule_metadata()
        self.data = {'rule_metadata': self.rule_metadata}

    def __str__(self) -> str:
        return str(self.data)
    
    def load_rule_metadata(self) -> dict:
        return {
            '__version__': version,
            'id': self.id,
            'parent_id': self.parent_id,
            'created': str(datetime.datetime.now()),
            'name': str(self.name),
            'required_context_parameters': []
        }
    
    def add_required_context_parameter(self, parameter):
        current_context_params: list = self.rule_metadata.get('required_context_parameters', [])
        if parameter not in current_context_params:
            current_context_params.append(parameter)
    
    def set_parent_id(self, parent_id):
        self.data['rule_metadata']['parent_id'] = parent_id
        return self

    def If(self, condition: Condition) -> 'Rule':
        """
        Set the 'if' condition of the rule.
        """
        self.data['if'] = condition.to_dict()
        for parameter in condition.required_context_parameters:
            self.add_required_context_parameter(parameter)
        return self

    def Then(self, result: Result) -> 'Rule':
        """
        Set the 'then' result of the rule.
        """
        self.data['then'] = result.to_dict()
        return self

    def Else(self, obj) -> 'Rule':
        """
        Set the 'else' result of the rule.
        """
        if isinstance(obj, Rule):
            self.data['else'] = obj.set_parent_id(self.id).to_dict()
        elif isinstance(obj, Result):
            self.data['else'] = obj.to_dict()
        else:
            raise Exception('Else must be a Rule or Result type object')
        return self
    
    def to_dict(self) -> dict:
        return self.data
    
    def save_to_file(self, filename) -> 'Rule':
        save_dict_to_json(self.data, filename)
        return self

    def load_from_file(self, filename) -> 'Rule':
        self.data = load_from_json(filename)
        return self
