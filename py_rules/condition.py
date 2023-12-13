from .value import RuleValue
from .expression import RuleExpression
from .errors import InvalidRuleConditionError


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
            'value':self.context.get(self.variable)
        }
        left_value = RuleValue(left_value_dict, self.context)
        right_value = RuleValue(self.value, self.context)
        expression = RuleExpression(self.operator, left_value, right_value)
        return expression.evaluate()
