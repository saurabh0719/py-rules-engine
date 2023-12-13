from datetime import datetime
from rules.exceptions import InvalidRuleValueError

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

    def get_value(self) -> any:
        """
        Get the value, parsed according to its type.

        Returns:
            The parsed value.
        """
        if self.type == 'bool':
            return bool(self.value)
        elif self.type == 'str':
            return str(self.value)
        elif self.type == 'int':
            return int(self.value)
        elif self.type == 'float':
            return float(self.value)
        elif self.type == 'date':
            return datetime.strptime(self.value, '%Y-%m-%d').date()
        elif self.type == 'datetime':
            return datetime.strptime(self.value, '%Y-%m-%dT%H:%M:%S')
        elif self.type == 'list' and isinstance(self.value, list):
            return [RuleValue(item).get_value() for item in self.value]
        elif self.type == 'dict' and isinstance(self.value, dict):
            return {key: RuleValue(value).get_value() for key, value in self.value.items()}
        elif self.type == 'NoneType' and self.value is None:
            return None
        elif self.type == 'variable':
            return self.context.get(self.value)
        else:
            raise InvalidRuleValueError(f'Invalid type: {self.type}')
