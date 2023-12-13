"""
This module, `expression.py`, contains the `RuleExpression` class which is used to evaluate an expression in a rule.

The `RuleExpression` class takes an operator and two `RuleValue` objects as input. The operator should be one of '<', '>', '<=', '>=', '==', '!=', 'in', 'not in'.

The `RuleExpression` class provides several methods:

- `__init__`: Initializes the `RuleExpression` with an operator and two `RuleValue` objects. It also validates the operator.
- `evaluate`: Evaluates the expression. It gets the values of the `RuleValue` objects and applies the operator to them.
- `equal`, `less_than`, `greater_than`, `less_than_equal`, `greater_than_equal`, `not_equal`, `in_`, `not_in`: These methods implement the logic for each operator.

Example usage:

    operator = '>'
    left_value = RuleValue({'type': 'int', 'value': 30}, {})
    right_value = RuleValue({'type': 'int', 'value': 20}, {})
    expression = RuleExpression(operator, left_value, right_value)
    print(expression.evaluate())  # prints: True

This will create an expression that checks if 30 is greater than 20. The `evaluate` method evaluates the expression and returns the result.
"""

from .constants import Operators
from .errors import InvalidRuleExpressionError, InvalidRuleValueError
from .value import RuleValue


class RuleExpression:
    """
    Class to handle different types of operands in a rule.
    """

    def __init__(self, operator: str, left_value: RuleValue, right_value: RuleValue) -> None:
        """
        Initialize the RuleExpression with an operator and two values.

        Args:
            operator (str): The operator, which should be one of '<', '>', '<=', '>=', '==', '!=', 'in', 'not in'.
            left_value (RuleValue): The left value.
            right_value (RuleValue): The right value.
        """
        self.operator = operator
        self.left_value = left_value
        self.right_value = right_value

        self.operator_to_handler_map = {
            Operators.EQUAL: self.equal,
            Operators.DOUBLE_EQUAL: self.equal,
            Operators.LESS_THAN: self.less_than,
            Operators.GREATER_THAN: self.greater_than,
            Operators.LESS_THAN_OR_EQUAL: self.less_than_equal,
            Operators.GREATER_THAN_OR_EQUAL: self.greater_than_equal,
            Operators.NOT_EQUAL: self.not_equal,
            Operators.IN: self.in_,
            Operators.NOT_IN: self.not_in,
        }

        if self.operator not in self.operator_to_handler_map:
            raise InvalidRuleExpressionError(f'Invalid operator type - {self.operator}')

    def evaluate(self) -> bool:
        """
        Evaluate the operand.

        Returns:
            bool: The result of the evaluation.
        """
        try:
            left_value = self.left_value.get_value()
            right_value = self.right_value.get_value()

            if self.operator not in [Operators.EQUAL, Operators.NOT_EQUAL, Operators.IN, Operators.NOT_IN]:
                if not isinstance(left_value, type(right_value)):
                    raise InvalidRuleValueError('Values are not comparable')

            return self.operator_to_handler_map[self.operator](left_value, right_value)
        except KeyError:
            raise InvalidRuleExpressionError(
                f'Invalid expression: {self.left_value} {self.operator} {self.right_value}')

    def equal(self, left_value, right_value) -> bool:
        return left_value == right_value

    def less_than(self, left_value, right_value) -> bool:
        return left_value < right_value

    def greater_than(self, left_value, right_value) -> bool:
        return left_value > right_value

    def less_than_equal(self, left_value, right_value) -> bool:
        return left_value <= right_value

    def greater_than_equal(self, left_value, right_value) -> bool:
        return left_value >= right_value

    def not_equal(self, left_value, right_value) -> bool:
        return left_value != right_value

    def in_(self, left_value, right_value) -> bool:
        if not isinstance(right_value, list):
            raise InvalidRuleValueError('Invalid value for in operator')
        return left_value in right_value

    def not_in(self, left_value, right_value) -> bool:
        if not isinstance(right_value, list):
            raise InvalidRuleValueError('Invalid value for not in operator')
        return left_value not in right_value
