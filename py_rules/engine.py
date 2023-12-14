from .__version__ import __version__
from .components import Rule
from .condition import RuleCondition
from .errors import InvalidRuleConditionError, InvalidRuleError
from .utils import validate_version


class RuleEngine:
    """
    Class to evaluate a Rule component.
    Takes a `Rule` object and a context (a dictionary) as input. The context is used to evaluate the conditions in the rule.

    - `evaluate`: Evaluates the rule. It checks the 'if' condition and returns the result of the 'then' action if the condition is met, or the result of the 'else' action otherwise.

    Example usage:

        rule = Rule('Temperature Rule').If(Condition('temperature', '>', 30)).Then(Result('message', 'str', 'It is hot!'))
        context = {'temperature': 35}
        engine = RuleEngine(rule, context)
        print(engine.evaluate())  # prints: {'message': 'It is hot!'}

    This will create a rule that checks if the temperature is greater than 30. The context provides the actual temperature. The `RuleEngine` evaluates the rule in the given context and returns the result of the rule.
    """

    def __init__(self, rule: Rule, context: dict) -> None:
        """
        Initialize the RuleEngine with a context dict

        Args:
            rule (Rule): The rule to evaluate
            context (dict): The context in which to evaluate the rule.
        """
        self.version = __version__
        self.context = context
        self.rule = rule
        validate_version(self.rule.version)
        self._validate_context()

    def _validate_context(self) -> None:
        """
        Validate the context.
        """
        if not isinstance(self.context, dict):
            raise InvalidRuleError('Context must be a dict')

        for parameter in self.rule.required_context_parameters:
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
        rule_data = self.rule.to_dict()
        if_condition: dict = rule_data.get('if')
        then_action: dict = rule_data.get('then')
        else_action: dict = rule_data.get('else')

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
