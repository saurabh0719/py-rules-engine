import datetime
import uuid
from abc import ABC, abstractmethod

from .__version__ import __version__
from .constants import Operators, Types
from .errors import InvalidRuleConditionError, InvalidRuleError
from .utils import is_equal_dict


class RuleComponent(ABC):
    """
    Abstract base class for all rule components.
    Each component has a unique ID, a version, a set of required context parameters, and optional metadata.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.id = kwargs.get('id') if kwargs.get('id') else str(uuid.uuid4())
        self.created = str(datetime.datetime.now())
        self.version = kwargs.get('version') if kwargs.get('version') else __version__
        self.required_context_parameters = set()
        self.metadata = None

    def __eq__(self, other: 'RuleComponent') -> bool:
        return is_equal_dict(self.to_dict(), other.to_dict())

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError

    def load_metadata(self):
        if self.kwargs.get('hide_metadata') is True:
            self.metadata = None
        else:
            self.metadata = {
                'version': self.version,
                'type': self.__class__.__name__,
                'id': self.id,
                'created': self.created,
                'required_context_parameters': list(self.required_context_parameters)
            }


class RuleConditionComponent(RuleComponent):
    """
    Abstract base class for all rule condition components.
    Each condition component has a unique ID, a version, a set of required context parameters, and optional metadata.
    """

    def __and__(self, other):
        return AndCondition(self, other)

    def __or__(self, other):
        return OrCondition(self, other)


class Condition(RuleConditionComponent):
    """
    Represents a condition in a rule.
    A condition has a variable, an operator, and a value.
    The variable is a string that represents a parameter in the context.
    The operator is a string that represents a comparison operator.
    The value is the value to compare the variable to.
    """

    def __init__(self, variable=None, operator=None, value=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if operator and operator not in Operators.list_all():
            raise InvalidRuleConditionError(f'Invalid operator - {operator}')

        self.variable = variable
        self.operator = operator
        self.value = self._build_value(value)
        if self.variable is not None:
            self.required_context_parameters.add(variable)
        self.load_metadata()

    def __and__(self, other):
        return AndCondition(self, other)

    def __or__(self, other):
        return OrCondition(self, other)

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

    def to_dict(self):
        condition_dict = {'condition': {}}
        if self.metadata:
            condition_dict['condition']['metadata'] = self.metadata
        condition_dict['condition'].update({
            'variable': self.variable,
            'operator': self.operator,
            'value': self.value,
        })
        return condition_dict


class AndCondition(RuleConditionComponent):
    """
    Represents a logical 'and' of two conditions.
    An AndCondition has two conditions, and evaluates to True if both conditions are True.
    """

    def __init__(self, condition1: Condition, condition2: Condition):
        super().__init__()
        self.condition1 = condition1
        self.condition2 = condition2
        self.required_context_parameters = condition1.required_context_parameters.union(
            condition2.required_context_parameters)

    def to_dict(self):
        return {'and': [self.condition1.to_dict(), self.condition2.to_dict()]}


class OrCondition(RuleConditionComponent):
    """
    Represents a logical 'or' of two conditions.
    An OrCondition has two conditions, and evaluates to True if either condition is True.
    """

    def __init__(self, condition1: Condition, condition2: Condition):
        super().__init__()
        self.condition1 = condition1
        self.condition2 = condition2
        self.required_context_parameters = condition1.required_context_parameters.union(
            condition2.required_context_parameters)

    def to_dict(self):
        return {'or': [self.condition1.to_dict(), self.condition2.to_dict()]}


class Result(RuleComponent):
    """
    Represents a result of a rule.
    A result has a key, a type, and a value.
    The key is a string that represents a parameter in the context.
    The type is a string that represents the type of the value.
    The value is the value to set the parameter to if the rule is applied.
    """

    def __init__(self, key=None, vtype=None, value=None, result=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key
        self.vtype = vtype
        self.value = value
        self.result = result

        if self.vtype == Types.VARIABLE and self.value is not None:
            self.required_context_parameters.add(self.value)

    def __and__(self, other):
        return AndResult(self, other)

    def to_dict(self):
        return {'result': {self.key: {'type': self.vtype, 'value': self.value}}}


class AndResult(RuleComponent):
    """
    Represents a logical 'and' of two results.
    An AndResult has two results, and evaluates to a combined result if both results are True.
    """

    def __init__(self, result1, result2):
        super().__init__()
        self.result1 = result1
        self.result2 = result2
        self.required_context_parameters = result1.required_context_parameters.union(
            result2.required_context_parameters)

    def __and__(self, other):
        return AndResult(self, other)

    def to_dict(self):
        res1_data = self.result1.to_dict()['result']
        res2_data = self.result2.to_dict()['result']
        res1_data.update(res2_data)
        return {'result': res1_data}


class Rule(RuleComponent):
    """
    Represents a rule.
    A rule has a name, an 'if' condition, a 'then' result, and an optional 'else' result.
    The 'if' condition is a Condition that is evaluated to determine whether to apply the rule.
    The 'then' result is a Result that is applied if the 'if' condition is True.
    The 'else' result is a Result that is applied if the 'if' condition is False.
    """

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.parent_id = kwargs.get('parent_id') if kwargs.get('parent_id') else None
        self.if_action: RuleComponent = None
        self.then_action: RuleComponent = None
        self.else_action: RuleComponent = None
        self.load_metadata()

    def load_metadata(self) -> dict:
        super().load_metadata()
        if self.metadata:
            self.metadata['name'] = str(self.name)
            self.metadata['parent_id'] = self.parent_id

    def set_parent_id(self, parent_id):
        self.parent_id = parent_id
        return self

    def If(self, condition: Condition) -> 'Rule':
        self.if_action = condition
        self.required_context_parameters.update(condition.required_context_parameters)
        self.load_metadata()
        return self

    def Then(self, obj) -> 'Rule':
        self.then_action = obj
        if isinstance(obj, Rule):
            self.then_action.set_parent_id(self.id)
        self.required_context_parameters.update(self.then_action.required_context_parameters)
        self.load_metadata()
        return self

    def Else(self, obj) -> 'Rule':
        self.else_action = obj
        if isinstance(obj, Rule):
            self.else_action.set_parent_id(self.id)
        self.required_context_parameters.update(self.else_action.required_context_parameters)
        self.load_metadata()
        return self

    def to_dict(self):
        rule_dict = {}
        if self.metadata:
            rule_dict['metadata'] = self.metadata

        if not self.if_action:
            raise InvalidRuleError('No If action present in rule')
        rule_dict['if'] = self.if_action.to_dict()

        if self.then_action:
            rule_dict['then'] = self.then_action.to_dict()
            if self.else_action:
                rule_dict['else'] = self.else_action.to_dict()

        return rule_dict
