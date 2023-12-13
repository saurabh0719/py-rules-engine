"""
Example usage:

# Driver code
condition1 = ConditionBuilder("number", "is_in", [1, 2, 3])
condition2 = ConditionBuilder("number", "=", 1)
condition3 = ConditionBuilder("number", "=", 2)

or_condition = OrCondition(condition2, condition3)
and_condition = AndCondition(condition1, or_condition)

result1 = (ResultBuilder()
           .add('xyz', 'str', 'Condition met')
           .add('result', 'variable', 'xyz'))

result2 = (ResultBuilder()
           .add('xyz', 'str', 'Nested condition met')
           .add('result', 'variable', 'xyz'))


or_condition2 = OrCondition(condition2, condition3, AndCondition(condition2, condition3))

nested_rule = (RuleBuilder("Nested rule")
               .if_condition(or_condition2)
               .then_action(result2)
               .else_action({'result': 'Nested condition not met'}))

rule = (RuleBuilder("Complex rule")
        .if_condition(and_condition)
        .then_action(result1)
        .else_action(nested_rule)
        .build())

print(rule)

"""

class ConditionBuilder:
    def __init__(self, variable, operator, value):
        self.condition = {
            'variable': variable,
            'operator': operator,
            'value': self._build_value(value)
        }

    def _build_value(self, value):
        if isinstance(value, list):
            return {
                'type': 'list',
                'value': [self._build_value(v) for v in value]
            }
        elif isinstance(value, dict):
            return {
                'type': 'dict',
                'value': {k: self._build_value(v) for k, v in value.items()}
            }
        else:
            return {
                'type': type(value).__name__,
                'value': value
            }

    def build(self):
        return {'condition': self.condition}
    

class AndCondition:
    def __init__(self, *conditions):
        self.conditions = conditions

    def build(self):
        result = {"and": []}
        for condition in self.conditions:
            result["and"].append(condition.build())
        return result


class OrCondition:
    def __init__(self, *conditions):
        self.conditions = conditions

    def build(self):
        result = {"or": []}
        for condition in self.conditions:
            result["or"].append(condition.build())
        return result
    

class ResultBuilder:
    def __init__(self):
        self.result = {}

    def add(self, key, type, value):
        self.result[key] = {
            'type': type,
            'value': value
        }
        return self

    def build(self):
        return {'result': self.result}


class RuleBuilder:
    def __init__(self, rule_name):
        self.rule = {'rule': rule_name}

    def if_condition(self, condition):
        self.rule['if'] = condition.build()
        return self

    def then_action(self, action):
        if isinstance(action, ResultBuilder):
            self.rule['then'] = action.build()
        else:
            self.rule['then'] = action
        return self

    def else_action(self, action):
        if isinstance(action, RuleBuilder):
            self.rule['else'] = action.build()
        elif isinstance(action, ResultBuilder):
            self.rule['else'] = action.build()
        else:
            self.rule['else'] = action
        return self

    def build(self):
        return self.rule
