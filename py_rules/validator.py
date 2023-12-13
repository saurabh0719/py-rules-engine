from rules.exceptions import InvalidRuleError, InvalidRuleConditionError


class RuleValidator:
    """
    Class to validate a rule.

    Args:
        rule (dict): The rule to validate.
    
    Raises:
        InvalidRuleError: If the rule is invalid.
    
    """
    def __init__(self, rule):
        self.rule = rule

    def validate(self):
        if not isinstance(self.rule, dict):
            raise InvalidRuleError("Rule must be a dictionary")

        if 'if' not in self.rule:
            raise InvalidRuleConditionError("Rule must contain an 'if' condition")

        self.validate_condition(self.rule['if']) 

        if 'then' in self.rule:
            self.validate_action(self.rule['then'])

        if 'else' in self.rule:
            self.validate_action(self.rule['else'])

    def validate_condition(self, condition):
        if not isinstance(condition, dict):
            raise InvalidRuleConditionError("Condition must be a dictionary")

        if 'and' in condition:
            for sub_condition in condition['and']:
                self.validate_condition(sub_condition)
        elif 'or' in condition:
            for sub_condition in condition['or']:
                self.validate_condition(sub_condition)
        else:
            if 'condition' not in condition:
                raise InvalidRuleConditionError("Condition dict must contain a 'condition' field")

            if 'operator' not in condition['condition']:
                raise InvalidRuleConditionError("Condition must contain an 'operator' field")

            if 'value' not in condition['condition']:
                raise InvalidRuleConditionError("Condition must contain a 'value' field")

    def validate_action(self, action):
        if not isinstance(action, dict):
            raise InvalidRuleError("Action must be a dictionary")
