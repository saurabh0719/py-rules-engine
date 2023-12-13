from datetime import datetime

from .constants import Types
from .errors import InvalidRuleValueError

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
        self.type = value.get('type')
        self.value = value.get('value')
        if not self.type:
            raise InvalidRuleValueError('Missing type in value')
        
        self.type_map = {
            Types.BOOLEAN: bool,
            Types.STRING: str,
            Types.INTEGER: int,
            Types.FLOAT: float,
            Types.DATE: lambda x: datetime.strptime(x, '%Y-%m-%d').date(),
            Types.DATETIME: lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'),
            Types.LIST: self.parse_list,
            Types.DICTIONARY: self.parse_dict,
            Types.NONETYPE: lambda x: None,
            Types.VARIABLE: self.context.get
        }

    def _parse_list(self, value):
        return [RuleValue(self.context, item).get_value() for item in value]

    def _parse_dict(self, value):
        return {key: RuleValue(self.context, value).get_value() for key, value in value.items()}

    def get_value(self) -> any:
        """
        Get the value, parsed according to its type.

        Returns:
            The parsed value.
        """
        parse_func = self.type_map.get(self.type)
        if parse_func:
            return parse_func(self.value)
        else:
            raise InvalidRuleValueError(f'Invalid type: {self.type}')
