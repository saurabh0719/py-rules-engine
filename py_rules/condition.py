"""
This module, `condition.py`, contains the `RuleCondition` class which is used to parse and handle a condition in a rule.

The `RuleCondition` class takes a condition dictionary and a context dictionary as input. The condition dictionary should contain 'operator', 'variable', and 'value' properties.

The `RuleCondition` class provides an `evaluate` method which evaluates the condition against the context. The `evaluate` method uses the `RuleExpression` class to evaluate the expression formed by the operator, variable, and value of the condition.

Example usage:

    condition_dict = {
        'operator': '>',
        'variable': 'temperature',
        'value': {
            'type': 'int',
            'value': 30
        }
    }
    context = {'temperature': 35}
    condition = RuleCondition(condition_dict, context)
    print(condition.evaluate())  # prints: True

This will create a condition that checks if the temperature is greater than 30. The context provides the actual temperature. The `evaluate` method evaluates the condition in the given context and returns the result.
"""

from .errors import InvalidRuleConditionError
from .expression import RuleExpression
from .value import RuleValue


class RuleCondition:
    """
    Class to parse and handle a condition in a rule.
    """

    def __init__(self, condition: dict, context: dict) -> None:
        """
        Initialize the RuleCondition with a condition object.

        Args:
            condition (dict): The condition object, which should have 'type', 'operator', 'operand', and 'value' properties.
        """
        self.context = context
        self.operator = condition.get('operator')
        self.variable = condition.get('variable')
        self.value = condition.get('value')
        if not self.operator or not self.variable:
            raise InvalidRuleConditionError('Missing type in condition')

    def evaluate(self) -> bool:
        """
        Evaluate the condition against a context.

        Args:
            context (dict): The context to evaluate the condition against.

        Returns:
            bool: The result of the evaluation.
        """
        left_value_dict = {
            'type': type(self.context.get(self.variable)).__name__,
            'value': self.context.get(self.variable)
        }
        left_value = RuleValue(left_value_dict, self.context)
        right_value = RuleValue(self.value, self.context)
        expression = RuleExpression(self.operator, left_value, right_value)
        return expression.evaluate()
