from datetime import date, datetime

from .components import Condition
from .constants import Operators, Types
from .errors import (InvalidRuleConditionError, InvalidRuleExpressionError, InvalidRuleValueError,
                     InvalidRuleValueTypeError)


class RuleValue:
    """
    Class to parse and handle the 'value' field of a condition.
    Takes a value dictionary and a context dictionary as input. The value dictionary should contain 'type' and 'value' properties.

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

        self.type_to_parser_map = {
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

        if self.vtype not in self.type_to_parser_map:
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
        parser = self.type_to_parser_map.get(self.vtype)
        if parser:
            return parser(self.value)
        else:
            raise InvalidRuleValueError(f'Invalid type: {self.vtype}')


class RuleExpression:
    """
    Class to handle different types of operands in a rule.
    Takes an operator and two `RuleValue` objects as input. The operator should be one of '<', '>', '<=', '>=', '==', '!=', 'in', 'not in'.

    Example usage:

        operator = '>'
        left_value = RuleValue({'type': 'int', 'value': 30}, {})
        right_value = RuleValue({'type': 'int', 'value': 20}, {})
        expression = RuleExpression(operator, left_value, right_value)
        print(expression.evaluate())  # prints: True

    This will create an expression that checks if 30 is greater than 20. The `evaluate` method evaluates the expression and returns the result.
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
            Operators.EQUAL: lambda left, right: left == right,
            Operators.DOUBLE_EQUAL: lambda left, right: left == right,
            Operators.LESS_THAN: lambda left, right: left < right,
            Operators.GREATER_THAN: lambda left, right: left > right,
            Operators.LESS_THAN_OR_EQUAL: lambda left, right: left <= right,
            Operators.GREATER_THAN_OR_EQUAL: lambda left, right: left >= right,
            Operators.NOT_EQUAL: lambda left, right: left != right,
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

    def in_(self, left_value, right_value) -> bool:
        if not isinstance(right_value, list):
            raise InvalidRuleValueError('Invalid value for in operator')
        return left_value in right_value

    def not_in(self, left_value, right_value) -> bool:
        if not isinstance(right_value, list):
            raise InvalidRuleValueError('Invalid value for not in operator')
        return left_value not in right_value


class RuleCondition:
    """
    Class to parse and handle a condition in a rule.
    Takes a a context dictionary as input.

    Example usage:

        condition = Condition('number', '>', 30)
        context = {'temperature': 35}
        condition_evaluator = RuleCondition(context)
        print(condition_evaluator.evaluate(condition))  # prints: True

    This will evaluate the condition if the temperature is greater than 30. The context provides the actual temperature.
    The `evaluate` method evaluates the condition in the given context and returns the result.
    """

    def __init__(self, context: dict) -> None:
        """
        Initialize the RuleCondition with a condition object.

        Args:
            condition (dict): The condition object, which should have 'type', 'operator', 'operand', and 'value' properties.
        """
        self.context = context

    def evaluate(self, condition_dict: Condition) -> bool:
        """
        Evaluate the condition against a context.

        Args:
            condition_dict (dict): The dict representation of the condition.

        Returns:
            bool: The result of the evaluation.
        """

        operator = condition_dict.get('operator')
        variable = condition_dict.get('variable')
        value = condition_dict.get('value')
        if not operator or not variable:
            raise InvalidRuleConditionError('Missing type in condition')

        left_value_dict = {'type': type(self.context.get(variable)).__name__, 'value': self.context.get(variable)}
        left_value = RuleValue(left_value_dict, self.context)
        right_value = RuleValue(value, self.context)
        expression = RuleExpression(operator, left_value, right_value)
        return expression.evaluate()
