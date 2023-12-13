"""
Example usage:

condition = Condition('number', 'is_in', [1, 2, 3]) & Condition('number', '=', 1) & Condition('number', '=', 1) | Condition('number', '=', 2)
result = Result().add('xyz', 'str', 'Condition met').add('result', 'variable', 'xyz')
rule = Rule('Complex rule').If(condition).Then(result).Else(result)

print(rule.to_dict())
"""
from py_rules.constants import Operators
from py_rules.errors import InvalidRuleConditionError
from py_rules.utils import save_dict_to_json


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
        
    def __str__(self) -> str:
        return str(self.condition)

    def __and__(self, other):
        """
        Combine this condition and another condition with 'and'.
        """
        new_condition = {'and': self._get_conditions('and', other)}
        return Condition(condition=new_condition)

    def __or__(self, other):
        """
        Combine this condition and another condition with 'or'.
        """
        new_condition = {'or': self._get_conditions('or', other)}
        return Condition(condition=new_condition)

    def _get_conditions(self, operator, other):
        """
        Get a list of conditions combined with a specified operator.
        """
        return self.condition.get(operator, [self.condition]) + other.condition.get(operator, [other.condition])

    def to_dict(self):
        return self.condition


class Result:
    def __init__(self):
        self.result = {}

    def __str__(self):
        return str(self.to_dict())

    def add(self, key, type, value):
        self.result[key] = {
            'type': type,
            'value': value
        }
        return self
    
    def to_dict(self):
        return {"result": self.result}


class Rule:
    """
    A class to represent a rule.
    """

    def __init__(self, rule):
        """
        Initialize Rule with a rule name.
        """
        self.rule = {
            'rule': rule
        }
        self.current_operator = "__init__"

    def __str__(self):
        return str(self.rule)

    def If(self, condition: Condition):
        """
        Set the 'if' condition of the rule.
        """
        if self.current_operator == "__init__":
            self.rule['if'] = condition.to_dict()
        else:
            raise Exception('If must be the first condition in the rule')
        
        self.current_operator = "If"
        return self

    def Then(self, result: Result):
        """
        Set the 'then' result of the rule.
        """
        if self.current_operator == "If":
            self.rule['then'] = result.to_dict()
        else:
            raise Exception('Then must be after If in the rule')
        
        self.current_operator = "Then"
        return self

    def Else(self, obj):
        """
        Set the 'else' result of the rule.
        """
        if self.current_operator == "Then":
            if isinstance(obj, (Rule, Result)):
                self.rule['else'] = obj.to_dict()
            else:
                raise Exception('Else must be a Rule or Result type object')
        else:
            raise Exception('Else must be after Then in the rule')
        
        self.current_operator = "Else"
        return self
    
    def to_dict(self):
        return self.rule
    
    def to_file(self, filename):
        save_dict_to_json(self.rule, filename)

