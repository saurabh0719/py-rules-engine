from .condition import RuleCondition
from .errors import InvalidRuleConditionError, InvalidRuleError


class RuleEngine:
    """
    Class to evaluate a parsed rule.
    """
    def __init__(self, rule: dict, context: dict) -> None:
        """
        Initialize the RuleEngine with a context
        
        Args:
            context (dict): The context in which to evaluate the rule.
            func_map (dict): A map of function names to functions.
        """
        self.context = context
        self.rule = rule
        self.rule_name = rule.get('rule')
        self._validate_rule()
        self._validate_context()
        
    def _validate_rule(self) -> None:
        """
        Validate the rule.
        """
        if not isinstance(self.rule, dict):
            raise InvalidRuleError('Rule must be a dict')
        if not self.rule.get('if'):
            raise InvalidRuleError('Rule must have an "if" property')
        if not self.rule.get('then'):
            raise InvalidRuleError('Rule must have a "then" property')
        
    def _validate_context(self) -> None:
        """
        Validate the context.
        """
        if not isinstance(self.context, dict):
            raise InvalidRuleError('Context must be a dict')
        
        if 'required_context_parameters' in self.rule:
            for parameter in self.rule['required_context_parameters']:
                if parameter not in self.context:
                    raise InvalidRuleError(f'Context is missing required parameter: {parameter}')
                
    def _build_result(self, action: dict) -> dict:
        """
        Build a result dict from the schema.

        Args:
            result_schema (dict): The schema of result dict to build.

        Returns:
            dict: The built result dict.
        """
        result_schema = action.get('result', {})
        result = {}
        for name, data in result_schema.items():
            if data.get('type') == 'variable':
                result[name] = self.context.get(data.get('value'))
            else:
                result[name] = data.get('value')
        return result

    def evaluate_condition_block(self, condition_block: dict) -> bool:
        """
        Evaluate a condition.

        Args:
            condition (dict): The condition to evaluate.

        Returns:
            bool: The result of the condition.
        """
        if not isinstance(condition_block, dict):
            raise InvalidRuleConditionError('Condition block must be a dict')

        for key, value in condition_block.items():
            if key in ['and', 'or']:
                results = [self.evaluate_condition_block(sub_condition) for sub_condition in value]
                return all(results) if key == 'and' else any(results)
            elif key == 'condition':
                return RuleCondition(value, self.context).evaluate()

    def evaluate(self) -> any:
        """
        Evaluate a rule.

        Args:
            rule (dict): The rule to evaluate.

        Returns:
            any: The result of the rule.

        NOTE: In a rule, 'if' is required while 'then' and 'else' are optional. 
        
        - If 'then' is absent, the rule returns True if the condition is met, else False. 
        - If 'else' is absent, the rule returns the result of 'then' if the condition is met, else False.
        """
        if_condition = self.rule.get('if')
        then_action = self.rule.get('then')
        else_action = self.rule.get('else')

        if self.evaluate_condition_block(if_condition):
            return self._build_result(then_action) if then_action else True
        else:
            return self._build_result(else_action) if else_action else False
