"""
This module, `value.py`, contains the `RuleValue` class which is used to parse and handle the 'value' field of a condition.

The `RuleValue` class takes a value dictionary and a context dictionary as input. The value dictionary should contain 'type' and 'value' properties.

The `RuleValue` class provides several methods:

- `__init__`: Initializes the `RuleValue` with a value dictionary and a context. It also validates the value type.
- `_parse_list`: Parses a list value. It recursively parses each item in the list.
- `_parse_dict`: Parses a dictionary value. It recursively parses each value in the dictionary.
- `get_value`: Returns the parsed value according to its type.

Example usage:

    value_dict = {
        'type': 'int',
        'value': 30
    }
    context = {}
    value = RuleValue(value_dict, context)
    print(value.get_value())  # prints: 30

This will create a `RuleValue` object that represents an integer value of 30. The `get_value` method returns the parsed value.
"""

from datetime import date, datetime

from .constants import Types
from .errors import InvalidRuleValueError, InvalidRuleValueTypeError


class RuleValue:
    """
    Class to parse and handle the 'value' field of a condition.
    """

    def __init__(self, value: dict, context: dict) -> None:
        """
        Initialize the RuleValue with a value object.

        Args:
            value (dict): The value object, which should have 'type' and 'value' properties.
        """
        self.context = context
        self.vtype = value.get('type')
        self.value = value.get('value')
        if not self.vtype:
            raise InvalidRuleValueError('Missing type in rule value')

        self.type_map = {
            Types.BOOLEAN: bool,
            Types.STRING: str,
            Types.INTEGER: int,
            Types.FLOAT: float,
            Types.DATE: lambda x: datetime.strptime(x, '%Y-%m-%d').date() if not isinstance(x, date) else x,
            Types.DATETIME: lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S') if not isinstance(x, datetime) else x,
            Types.LIST: self._parse_list,
            Types.DICTIONARY: self._parse_dict,
            Types.NONETYPE: lambda x: None,
            Types.VARIABLE: self.context.get
        }

        if self.vtype not in self.type_map:
            raise InvalidRuleValueTypeError(f'Invalid type in rule value: {self.vtype}')

    def _parse_list(self, value):
        return [RuleValue(item, self.context).get_value() for item in value]

    def _parse_dict(self, value):
        return {key: RuleValue(value, self.context).get_value() for key, value in value.items()}

    def get_value(self) -> any:
        """
        Get the value, parsed according to its type.

        Returns:
            The parsed value.
        """
        parse_func = self.type_map.get(self.vtype)
        if parse_func:
            return parse_func(self.value)
        else:
            raise InvalidRuleValueError(f'Invalid type: {self.vtype}')
