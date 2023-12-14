class InvalidRuleValueError(ValueError):
    """
    Exception raised when a rule's value is invalid or inappropriate.
    """
    pass


class InvalidRuleConditionError(ValueError):
    """
    Exception raised when a rule's condition is invalid or inappropriate.
    """
    pass


class InvalidRuleExpressionError(ValueError):
    """
    Exception raised when a rule's expression (combination of conditions and results) is invalid or inappropriate.
    """
    pass


class InvalidRuleError(ValueError):
    """
    Exception raised when a rule is invalid or inappropriate. This is a general exception for rule-related errors.
    """
    pass


class InvalidRuleValueTypeError(ValueError):
    """
    Exception raised when a rule's value type is invalid or inappropriate.
    """
