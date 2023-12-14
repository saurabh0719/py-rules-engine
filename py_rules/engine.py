from .__version__ import __version__
from .components import Rule
from .condition import RuleCondition
from .errors import InvalidRuleConditionError, InvalidRuleError


class RuleEngine:
    """
    Class to evaluate a Rule component.
    Takes a context dictionary as input. The context is used to evaluate the conditions in the rule.

    - `evaluate(rule)`: Evaluates the rule. It checks the 'if' condition and returns the result of the 'then' action if the condition is met, or the result of the 'else' action otherwise.

    Example usage:

        rule = Rule('Temperature Rule').If(Condition('temperature', '>', 30)).Then(Result('message', 'str', 'It is hot!'))
        context = {'temperature': 35}
        engine = RuleEngine(context)
        print(engine.evaluate(rule))  # prints: {'message': 'It is hot!'}

    This will evaluate a rule that checks if the temperature is greater than 30. The context provides the actual temperature. The `RuleEngine` evaluates the rule in the given context and returns the result of the rule.
    """

    def __init__(self, context: dict) -> None:
        """
        Initialize the RuleEngine with a context dict

        Args:
            context (dict): The context against which it will evaluate any rules
        """
        self.version = __version__
        self.context = context

        if not isinstance(self.context, dict):
            raise InvalidRuleError('Context must be a dict')

    def _validate_rule_with_context(self, rule: Rule) -> None:
        """
        Validate the context.
        """
        for parameter in rule.required_context_parameters:
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
        if action and 'result' in action:
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
                return RuleCondition(self.context).evaluate(value)

    def evaluate(self, rule: Rule) -> any:
        """
        Evaluate a rule.

        Args:
            rule (Rule): The rule to evaluate.

        Returns:
            any: The result of the rule.

        NOTE: In a rule, 'if' is required while 'then' and 'else' are optional.

        - If 'then' is absent, the rule returns True if the condition is met, else False.
        - If 'else' is absent, the rule returns the result of 'then' if the condition is met, else False.
        """
        self._validate_rule_with_context(rule)
        if_action = rule.if_action
        then_action = rule.then_action
        else_action = rule.else_action

        if if_action and self.evaluate_condition_block(if_action.to_dict()):
            if then_action:
                if isinstance(then_action, Rule):
                    return self.evaluate(then_action)
                else:
                    return self.evaluate_result(then_action.to_dict(), default=True)
            else:
                return True
        else:
            if else_action:
                if isinstance(else_action, Rule):
                    return self.evaluate(else_action)
                else:
                    return self.evaluate_result(else_action.to_dict(), default=False)
            else:
                return False
