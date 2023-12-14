"""
This module, `components.py`, contains component classes for building rules, conditions, and results for a rule engine.

Classes:
    - Condition: Represents a condition in a rule. It supports logical `and` and `or` operations.
    - Result: Represents a result of a rule. It supports the `and` operation.
    - Rule: Represents a rule. A rule consists of an 'if' condition and 'then' and 'else' results. The 'then' and 'else' results are executed when the 'if' condition is met or not met, respectively.

Each class provides a `to_dict` method for converting the object to a dictionary, which can be useful for storing the object in a database or file, or for converting the object to JSON.

The `Rule` class also provides `save_to_file` and `load_from_file` methods for saving the rule to a file and loading the rule from a file, respectively.

Example usage:
    condition = Condition('number', 'in', [1, 2, 3]) & Condition('number', '=', 1) & \
    Condition('number', '=', 1) | Condition('number', '=', 2)
    result = Result('xyz', 'str', 'Condition met') & Result('result', 'variable', 'xyz')
    rule1 = Rule('Complex rule').If(condition).Then(result).Else(result)
    print(rule1.to_dict())
"""

import datetime
import uuid
from abc import ABC, abstractmethod

from .__version__ import __version__
from .constants import Operators, Types
from .errors import InvalidRuleConditionError


class RuleComponent(ABC):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.id = kwargs.get('id') if kwargs.get('id') else str(uuid.uuid4())
        self.version = kwargs.get('version') if kwargs.get('version') else __version__
        self.required_context_parameters = set()
        self.metadata = None

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError

    def load_metadata(self):
        return {
            'version': self.version,
            'type': self.__class__.__name__,
            'id': self.id,
            'created': str(datetime.datetime.now()),
            'required_context_parameters': list(self.required_context_parameters)
        }


class Condition(RuleComponent):

    def __init__(self, variable=None, operator=None, value=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if operator and operator not in Operators.list_all():
            raise InvalidRuleConditionError(f'Invalid operator - {operator}')

        self.variable = variable
        self.operator = operator
        self.value = self._build_value(value)
        if self.variable is not None:
            self.required_context_parameters.add(variable)
        self.metadata = self.load_metadata()

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
        return {
            'condition': {
                'metadata': self.metadata,
                'variable': self.variable,
                'operator': self.operator,
                'value': self.value,
            }
        }


class AndCondition(RuleComponent):

    def __init__(self, condition1: Condition, condition2: Condition):
        super().__init__()
        self.condition1 = condition1
        self.condition2 = condition2
        self.required_context_parameters = condition1.required_context_parameters.union(
            condition2.required_context_parameters)

    def __and__(self, other):
        return AndCondition(self, other)

    def __or__(self, other):
        return OrCondition(self, other)

    def to_dict(self):
        return {'and': [self.condition1.to_dict(), self.condition2.to_dict()]}


class OrCondition(RuleComponent):

    def __init__(self, condition1: Condition, condition2: Condition):
        super().__init__()
        self.condition1 = condition1
        self.condition2 = condition2
        self.required_context_parameters = condition1.required_context_parameters.union(
            condition2.required_context_parameters)

    def __and__(self, other):
        return AndCondition(self, other)

    def __or__(self, other):
        return OrCondition(self, other)

    def to_dict(self):
        return {'or': [self.condition1.to_dict(), self.condition2.to_dict()]}


class Result(RuleComponent):

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

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.parent_id = kwargs.get('parent_id') if kwargs.get('parent_id') else None
        self.if_action: RuleComponent = None
        self.then_action: RuleComponent = None
        self.else_action: RuleComponent = None
        self.metadata = self.load_metadata()

    def load_metadata(self) -> dict:
        metadata = super().load_metadata()
        metadata['name'] = str(self.name)
        metadata['parent_id'] = self.parent_id
        return metadata

    def set_parent_id(self, parent_id):
        self.parent_id = parent_id
        return self

    def If(self, condition: Condition) -> 'Rule':
        self.if_action = condition
        self.required_context_parameters.update(condition.required_context_parameters)
        return self

    def Then(self, obj) -> 'Rule':
        self.then_action = obj
        if isinstance(obj, Rule):
            self.then_action.set_parent_id(self.id)
        self.required_context_parameters.update(self.then_action.required_context_parameters)
        return self

    def Else(self, obj) -> 'Rule':
        self.else_action = obj
        if isinstance(obj, Rule):
            self.else_action.set_parent_id(self.id)
        self.required_context_parameters.update(self.else_action.required_context_parameters)
        return self

    def to_dict(self):
        return {
            'metadata': self.metadata,
            'if': self.if_action.to_dict() if self.if_action is not None else None,
            'then': self.then_action.to_dict() if self.then_action is not None else None,
            'else': self.else_action.to_dict() if self.else_action is not None else None
        }
