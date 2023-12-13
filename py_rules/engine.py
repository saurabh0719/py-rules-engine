from .builder import Rule
from .condition import RuleCondition
from .errors import InvalidRuleConditionError, InvalidRuleError


class RuleEngine:
    """
    Class to evaluate a parsed rule.
    """
    def __init__(self, rule: Rule, context: dict) -> None:
        """
        Initialize the RuleEngine with a context
        
        Args:
            rule (Rule): The rule to evaluate
            context (dict): The context in which to evaluate the rule.
        """
        self.context = context
        self.rule = rule
        self._validate_context()
        
    def _validate_context(self) -> None:
        """
        Validate the context.
        """
        if not isinstance(self.context, dict):
            raise InvalidRuleError('Context must be a dict')
        
        if 'required_context_parameters' in self.rule.rule_metadata:
            for parameter in self.rule.rule_metadata.get('required_context_parameters'):
                if parameter not in self.context:
                    raise InvalidRuleError(f'Context is missing required parameter: {parameter}')
                
    def evaluate_result(self, action: dict, default=False) -> dict:
        """
        Build a result dict from the schema or return the default value bool value

        Args:
            result_schema (dict): The schema of result dict to build.

        Returns:
            dict: The built result dict.
        """
        result = {}
        if 'result' in action:
            schema = action.get('result', {})
            for name, data in schema.items():
                if data.get('type') == 'variable':
                    result[name] = self.context.get(data.get('value'))
                else:
                    result[name] = data.get('value')

        if not result:
            return default
        
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
        if_condition: dict = self.rule.data.get('if')
        then_action: dict = self.rule.data.get('then')
        else_action: dict = self.rule.data.get('else')

        if self.evaluate_condition_block(if_condition):
            if then_action and then_action.get('if'):
                return self.evaluate(then_action) 
            else:
                return self.evaluate_result(then_action, default=True)
        else:
            if else_action and else_action.get('if'):
                return self.evaluate(else_action)
            else:
                return self.evaluate_result(else_action, default=False)
