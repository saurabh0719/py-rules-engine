from py_rules.components import Condition, Result, Rule
from py_rules.storages import JSONRuleStorage, PickledRuleStorage, YAMLRuleStorage

# Define conditions
condition1 = Condition('number', 'in', [1, 2, 3])
condition2 = Condition('number', '=', 1)

# Combine conditions using logical 'and'
combined_condition = condition1 & condition2

# Define results
result1 = Result('xyz', 'str', 'Condition met')
result2 = Result('result', 'variable', 'xyz')

# Combine results using logical 'and'
combined_result = result1 & result2

# Define a nested rule
nested_rule = Rule('Nested rule').If(condition1).Then(result1)

# Define a complex rule with nested conditions and rules
complex_rule = Rule('Complex rule').If(combined_condition).Then(combined_result).Else(nested_rule)

# Store the complex rule in different formats
JSONRuleStorage('rule.json').store(complex_rule)
YAMLRuleStorage('rule.yaml').store(complex_rule)
PickledRuleStorage('rule.pkl').store(complex_rule)

# Load the complex rule from each format
json_rule_loaded = JSONRuleStorage('rule.json').load()
yaml_rule_loaded = YAMLRuleStorage('rule.yaml').load()
pickle_rule_loaded = PickledRuleStorage('rule.pkl').load()

# Assert that the loaded rules are equal to the original rule
assert complex_rule.to_dict() == json_rule_loaded.to_dict() == yaml_rule_loaded.to_dict() == pickle_rule_loaded.to_dict(
)

# Print the dictionary representation of each rule
print("\nOriginal rule:", complex_rule.to_dict())
print("\nJSON loaded rule:", json_rule_loaded.to_dict())
print("\nYAML loaded rule:", yaml_rule_loaded.to_dict())
print("\nPickle loaded rule:", pickle_rule_loaded.to_dict())
assert complex_rule.to_dict() == {
    "metadata": {
        "version": "0.1.0",
        "type": "Rule",
        "id": "cfb77a2b-a05d-4f9d-be9d-ce442c51b624",
        "created": "2023-12-14 21:27:01.828293",
        "required_context_parameters": [],
        "name": "Complex rule",
        "parent_id": None,
    },
    "if": {
        "and": [
            {
                "condition": {
                    "metadata": {
                        "version": "0.1.0",
                        "type": "Condition",
                        "id": "3173872f-404d-467b-aef3-507d28a5f53d",
                        "created": "2023-12-14 21:27:01.828222",
                        "required_context_parameters": ["number"],
                    },
                    "variable": "number",
                    "operator": "in",
                    "value": {
                        "type":
                            "list",
                        "value": [
                            {
                                "type": "int",
                                "value": 1
                            },
                            {
                                "type": "int",
                                "value": 2
                            },
                            {
                                "type": "int",
                                "value": 3
                            },
                        ],
                    },
                }
            },
            {
                "condition": {
                    "metadata": {
                        "version": "0.1.0",
                        "type": "Condition",
                        "id": "b31483ed-e103-474f-b04e-70b2aad71beb",
                        "created": "2023-12-14 21:27:01.828252",
                        "required_context_parameters": ["number"],
                    },
                    "variable": "number",
                    "operator": "=",
                    "value": {
                        "type": "int",
                        "value": 1
                    },
                }
            },
        ]
    },
    "then": {
        "result": {
            "xyz": {
                "type": "str",
                "value": "Condition met"
            },
            "result": {
                "type": "variable",
                "value": "xyz"
            },
        }
    },
    "else": {
        "metadata": {
            "version": "0.1.0",
            "type": "Rule",
            "id": "00757c4b-cae1-4b9c-8480-927a48bcc4a8",
            "created": "2023-12-14 21:27:01.828282",
            "required_context_parameters": [],
            "name": "Nested rule",
            "parent_id": None,
        },
        "if": {
            "condition": {
                "metadata": {
                    "version": "0.1.0",
                    "type": "Condition",
                    "id": "3173872f-404d-467b-aef3-507d28a5f53d",
                    "created": "2023-12-14 21:27:01.828222",
                    "required_context_parameters": ["number"],
                },
                "variable": "number",
                "operator": "in",
                "value": {
                    "type": "list",
                    "value": [
                        {
                            "type": "int",
                            "value": 1
                        },
                        {
                            "type": "int",
                            "value": 2
                        },
                        {
                            "type": "int",
                            "value": 3
                        },
                    ],
                },
            }
        },
        "then": {
            "result": {
                "xyz": {
                    "type": "str",
                    "value": "Condition met"
                }
            }
        },
        "else": None,
    },
}
