from py_rules.components import Condition, Result, Rule
from py_rules.engine import RuleEngine
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
json_rule = JSONRuleStorage('rule.json').load()
yaml_rule = YAMLRuleStorage('rule.yaml').load()
pickle_rule = PickledRuleStorage('rule.pkl').load()

# Assert that the loaded rules are equal to the original rule
assert complex_rule == json_rule == yaml_rule == pickle_rule

# Print the dictionary representation of each rule
print("\nOriginal rule:", complex_rule.to_dict())
print("\nJSON loaded rule:", json_rule.to_dict())
assert complex_rule == json_rule  #== yaml_rule == pickle_rule
print("\nYAML loaded rule:", yaml_rule.to_dict())
print("\nPickle loaded rule:", pickle_rule.to_dict())

# Hide metadata in the dictionary representation of the rule
complex_rule.kwargs['hide_metadata'] = True
complex_rule.load_metadata()
print("\nComplex rule - ", complex_rule.to_dict())
print("\nJSON rule - ", json_rule.to_dict())
assert complex_rule != json_rule

complex_rule.kwargs['hide_metadata'] = False
complex_rule.load_metadata()
print("\nComplex rule - ", complex_rule.to_dict())
print("\nJSON rule - ", json_rule.to_dict())
assert complex_rule == json_rule

# Create a RuleEngine and add the complex rule
context = {'number': 1, 'xyz': 5}  # Define a context
engine = RuleEngine(context)

# Evaluate the rules against the contexts
print("\nEvaluation of context1:", engine.evaluate(complex_rule))
print("\nEvaluation of context1 with JSON rule:", engine.evaluate(json_rule))

context = {'number': 4, 'xyz': 5}  # Update the context
engine = RuleEngine(context)  # Create a new RuleEngine with the updated context
print("\nEvaluation of context2:", engine.evaluate(complex_rule))
