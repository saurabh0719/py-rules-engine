from .value import RuleValue
from .exceptions import InvalidRuleExpressionError, InvalidRuleValueError


class RuleExpression:
    """
    Class to handle different types of operands in a rule.
    """

    def __init__(self, operator: str, left_value: RuleValue, right_value: RuleValue) -> None:
        """
        Initialize the RuleExpression with an operator and two values.

        Args:
            operator (str): The operator, which should be one of '<', '>', '<=', '>=', '==', '!=', 'between', 'in', 'not in'.
            left_value (RuleValue): The left value.
            right_value (RuleValue): The right value.
        """
        self.operator = operator
        self.left_value = left_value
        self.right_value = right_value

        self.operators = {
            '==': self.equal,
            '=': self.equal,
            '<': self.less_than,
            '>': self.greater_than,
            '<=': self.less_than_equal,
            '>=': self.greater_than_equal,
            '!=': self.not_equal,
            'between': self.between,
            'in': self.in_,
            'not in': self.not_in,
        }

    def evaluate(self) -> bool:
        """
        Evaluate the operand.

        Returns:
            bool: The result of the evaluation.
        """
        try:
            left_value = self.left_value.get_value()
            right_value = self.right_value.get_value()

            if self.operator != '==' and self.operator != '=':
                if not isinstance(left_value, type(right_value)):
                    raise InvalidRuleValueError('Values are not comparable')

            return self.operators[self.operator](left_value, right_value)

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
    
    def between(self, left_value, right_value) -> bool:
        if not isinstance(right_value, list) or len(right_value) != 2:
            raise InvalidRuleValueError('Invalid value for between operator')
        return left_value <= right_value[0] and left_value >= right_value[1]
    
    def in_(self, left_value, right_value) -> bool:
        if not isinstance(right_value, list):
            raise InvalidRuleValueError('Invalid value for in operator')
        return left_value in right_value
    
    def not_in(self, left_value, right_value) -> bool:
        if not isinstance(right_value, list):
            raise InvalidRuleValueError('Invalid value for not in operator')
        return left_value not in right_value
