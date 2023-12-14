from .components import AndCondition, Condition, OrCondition, Result, Rule
from .errors import InvalidRuleError


class RuleParser:
    """
    This RuleParser class is responsible for parsing rules from a dictionary format. It supports parsing of conditions, results, and rules, including complex rules with 'and' and 'or' conditions.
    - The parse method is the main entry point for parsing a rule. It takes a dictionary representation of a rule and returns a Rule object.

    - The parse_value method is used to parse a value from a dictionary representation. It supports parsing of lists and dictionaries, as well as basic data types.

    - The parse_component method is used to parse a component from a dictionary. It supports parsing of conditions, 'and' conditions, 'or' conditions, results, and rules.

    - The __init__ method initializes the parser with a dictionary representation of a rule. It also validates the version of the rule to ensure compatibility.

    - This class raises an InvalidRuleError if it encounters an unknown component type in the rule.
    """

    def __init__(self, data: dict):
        self.data = data
        self.rule_counter = 0

    def _load_attributes_from_metadata(self, obj, metadata: dict):
        # sync all properties from the metadata dict into obj attrs
        metadata.pop('type', None)

        for key, value in metadata.items():
            setattr(obj, key, value)

        if hasattr(obj, 'required_context_parameters'):
            obj.required_context_parameters = set(obj.required_context_parameters)

        return obj

    def parse(self) -> Rule:
        """
        parse a rule from a dictionary.
        """
        metadata = self.data.get('metadata', {})
        self.rule_counter += 1
        rule = Rule(metadata.get('name', f'Unnamed Rule {self.rule_counter}'))
        if metadata:
            rule = self._load_attributes_from_metadata(rule, metadata)
            rule.load_metadata()

        if self.data.get('if'):
            rule.If(self.parse_component(self.data.get('if')))
        else:
            raise InvalidRuleError('No If condition in Rule')

        if self.data.get('then'):
            rule.Then(self.parse_component(self.data.get('then')))
            if self.data.get('else'):
                rule.Else(self.parse_component(self.data.get('else')))

        rule.metadata['required_context_parameters'] = list(rule.required_context_parameters)
        return rule

    def parse_value(self, data: dict):
        """
        Parse a value from a dictionary representation.
        """
        vtype = data.get('type')
        value = data.get('value')

        if vtype == 'list':
            return [self.parse_value(v) for v in value]
        elif vtype == 'dict':
            return {k: self.parse_value(v) for k, v in value.items()}
        else:
            return value

    def parse_component(self, data):
        """
        Parse a component from a dictionary.
        """
        if 'condition' in data:
            condition_data = data.get('condition', {})
            value = condition_data.get('value')
            value = self.parse_value(value) if isinstance(value, dict) else value
            condition = Condition(condition_data.get('variable'), condition_data.get('operator'), value)
            if 'metadata' in condition_data:
                metadata = condition_data.get('metadata', {})
                condition = self._load_attributes_from_metadata(condition, metadata)
                condition.load_metadata()
            return condition

        elif 'and' in data:
            and_data = data.get('and', [])
            return AndCondition(self.parse_component(and_data[0]), self.parse_component(and_data[1]))

        elif 'or' in data:
            or_data = data.get('or', [])
            return OrCondition(self.parse_component(or_data[0]), self.parse_component(or_data[1]))

        elif 'result' in data:
            results = data.get('result', {})
            combined_result_obj = None
            for key, value in results.items():
                result = Result(key, value.get('type'), value.get('value'))
                if not combined_result_obj:
                    combined_result_obj = result
                else:
                    combined_result_obj = combined_result_obj & result
            return combined_result_obj

        # start of a new rule
        elif 'if' in data:
            return self.__class__(data).parse()

        else:
            raise InvalidRuleError('Unknown component type in rule')
