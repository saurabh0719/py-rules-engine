<!-- ![py_rules](https://github.com/saurabh0719/py-rules/assets/42310348/fff20963-e144-44d0-bfde-3b9c7eb0c6ee) -->
![Screenshot from 2023-12-14 01-53-59](https://github.com/saurabh0719/py-rules/assets/42310348/6c8830a7-0625-4b34-8bec-b4b450db7955)

## Introduction

`py-rules-engine` is a simple, yet powerful rules engine written in pure Python. It allows you to define complex logical conditions and actions, either via a json file or through pythonic functions.

- **Complex Logical Conditions**: It allows you to define complex logical conditions using and, or, and not operations.

- **Pythonic Rule Builder**: It provides a Pythonic interface for building rules, making it easy to define rules in your Python code.

- **File storage & serialization support**: It allows you to define rules in JSON/YAML format and load them for evaluation. This makes it easy to store, configure, and share rules.

- **Ease of Shifting**: One of the standout features of py-rules is the ease of shifting between a Python rule builder and storing/configuring rules in other formats. This flexibility allows you to choose the most convenient way to define and manage your rules.

- **Nested Rules**: It supports nested rules, allowing you to create complex rule structures with multiple levels of conditions.

- **Rule Evaluation**: It provides a rule engine for evaluating rules in a given context.

- **0 dependencies**: It is written in pure Python, making it easy to install and use without any 3rd-party dependency.

<span id="contents"></span>

## Table of Contents :
* [Installation](#installation)
* [Rule structure & definition](#basics)
* [Rule builder](#builder)
* [Rule storage and parsing](#storage)
* [Rule engine and evaluation](#engine)
* [Tests](#tests)
* [To do](#todo)


<span id="installation"></span>

## Installation
You can install `py-rules-engine` using pip:

```bash
pip install py-rules-engine
```

**NOTE** - this library is currently in Beta, and things may break between version bumps pre 1.0.0.


<span id="basics"></span>

## Rule structure & definition

This rule-engine follows the `IF-THEN-ELSE` pattern.

The `IF-THEN-ELSE` structure is a fundamental part of the rule engine. It allows you to define a condition and specify the results based on whether the condition is met or not. Here's a breakdown of each part:

- `IF`: This is the condition that will be evaluated. It can be a simple condition (like "temperature > 30") or a complex condition involving multiple variables and logical operators (like "temperature > 30 AND humidity < 50"). The condition is evaluated against a given context, which is a dictionary of variables and their values.

- `THEN`: This part specifies the result or action that should be returned or performed if the IF condition is met (i.e., if it evaluates to True). It can be a simple value (like "It's hot") or a complex object. It can also be another rule, allowing for nested rules.

- `ELSE`: This part specifies the result or action that should be returned or performed if the IF condition is not met (i.e., if it evaluates to False). Like the THEN part, it can be a simple value, a complex object, or another rule. The ELSE part is optional; if it's not provided and the IF condition is not met, the rule engine will return False.


Every `Rule` object contains the following

- `metadata`: This section contains metadata about the rule.

  - `version`: The version of the rule.
  - `id`: A unique identifier for the rule.
  - `parent_id`: The id of the parent rule if this rule is nested, otherwise null.
  - `created`: The UTC timestamp when the rule was created.
  - `name`: The name of the rule.
  - `required_context_parameters`: A list of context parameters that are required for this rule. These variables/parameters are passed to the `RuleEngine` via a `context` dictionary


- `if`: This section contains the condition to be evaluated.

  - `condition` or `and` or `or`: The condition to be evaluated. It can be a single condition or a logical combination (`and`, `or`) of multiple conditions. Each condition consists of a `variable`, an `operator`, and a `value`.

- `then`: This section contains the result to be returned if the `if` condition evaluates to `True`.

- `result`: The result to be returned. It consists of a type and a value.

- `else`: This section contains the result to be returned if the `if` condition evaluates to `False`, or a nested rule with its own `if`, `then`, and `else` sections.

All the `Rule`(s) are evaluated against a `context` dictionary. The `context` is key-value dictionary of `facts` we use to evaluate all conditions and prepare return statements.


Some more facts about `Rule` objects -

- Rules can be nested within one another.

- Rules can be built using the python builder or be loaded from a `Storage` class (json/yaml etc.)

- Rules can be nested within one another

- A single Rule can be composed of `multiple conditions`

See the `examples/` directory for more.


[Go back to top](#table-of-contents)
<br>

<span id="builder"></span>

## Rule Builder

- `Condition`: This class represents a condition in a rule. It can be initialized with a variable, operator, and value, or with a condition dictionary. It supports logical `and` and `or` operations to combine conditions. The `to_dict` method returns a dictionary representation of the condition.

- `Result`: This class represents a result in a rule. It can be initialized with a key, type, and value, or with a result dictionary. It supports the `and` operation to combine results. The `to_dict` method returns a dictionary representation of the result.

- `Rule`: This class represents a rule. It can be initialized with a name and optional keyword arguments. It supports the `If`, `Then`, and `Else` methods to set the condition and results of the rule. The `to_dict` method returns a dictionary representation of the rule.


```python

from py_rules.components import Condition, Result, Rule

# Create a condition
condition = Condition('temperature', '>', 30)

# Create a result
result = Result('message', 'str', 'It is hot!')

# Create a rule
rule = Rule('Temperature Rule').If(condition).Then(result)

# Print the rule
print(rule.to_dict())

```

Output -

```json

{
    "metadata": {
        "version": "0.2.0",
        "type": "Rule",
        "id": "5dbca846-5e59-4b6c-bdbf-9602d68c79ff",
        "created": "2023-12-15 04:49:45.183531",
        "required_context_parameters": ["temperature"],
        "name": "Temperature Rule",
        "parent_id": null,
    },
    "if": {
        "condition": {
            "metadata": {
                "version": "0.2.0",
                "type": "Condition",
                "id": "14950c65-3741-40da-ac13-e5cf1a0c49ce",
                "created": "2023-12-15 04:49:45.183438",
                "required_context_parameters": ["temperature"],
            },
            "variable": "temperature",
            "operator": ">",
            "value": {"type": "int", "value": 30},
        }
    },
    "then": {"result": {"message": {"type": "str", "value": "It is hot!"}}},
}

```

This will create a rule that checks if the temperature is greater than 30 and returns the message "It is hot!" if the condition is met.


[Go back to top](#table-of-contents)
<br>


<span id="storage"></span>

## Rule parsing and storage


You can also save a `Rule` object to a `Storage` class of your choice, and load it back into a `Rule` object.

Out of the box, JSON, YAML and Pickle are supported.

```python

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

# Load the complex rule from each format
json_rule = JSONRuleStorage('rule.json').load()
yaml_rule = YAMLRuleStorage('rule.yaml').load()

assert complex_rule == json_rule == yaml_rule

```


`rule.json` -

```json

{
    "metadata": {
        "version": "0.2.0",
        "type": "Rule",
        "id": "8330dd39-a0a4-4f21-aab4-0f8e35924c74",
        "created": "2023-12-15 04:54:00.349206",
        "required_context_parameters": [
            "xyz",
            "number"
        ],
        "name": "Complex rule",
        "parent_id": null
    },
    "if": {
        "and": [
            {
                "condition": {
                    "metadata": {
                        "version": "0.2.0",
                        "type": "Condition",
                        "id": "16a74acf-3dfd-4c8f-a280-50dc3970455c",
                        "created": "2023-12-15 04:54:00.349063",
                        "required_context_parameters": [
                            "number"
                        ]
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
                            }
                        ]
                    }
                }
            },
            {
                "condition": {
                    "metadata": {
                        "version": "0.2.0",
                        "type": "Condition",
                        "id": "137af61f-16af-44b9-8c49-a1c61912704b",
                        "created": "2023-12-15 04:54:00.349134",
                        "required_context_parameters": [
                            "number"
                        ]
                    },
                    "variable": "number",
                    "operator": "=",
                    "value": {
                        "type": "int",
                        "value": 1
                    }
                }
            }
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
            }
        }
    },
    "else": {
        "metadata": {
            "version": "0.2.0",
            "type": "Rule",
            "id": "41ad9aa7-d072-49d1-9336-4186a3a6b69c",
            "created": "2023-12-15 04:54:00.349189",
            "required_context_parameters": [
                "number"
            ],
            "name": "Nested rule",
            "parent_id": null
        },
        "if": {
            "condition": {
                "metadata": {
                    "version": "0.2.0",
                    "type": "Condition",
                    "id": "16a74acf-3dfd-4c8f-a280-50dc3970455c",
                    "created": "2023-12-15 04:54:00.349063",
                    "required_context_parameters": [
                        "number"
                    ]
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
                        }
                    ]
                }
            }
        },
        "then": {
            "result": {
                "xyz": {
                    "type": "str",
                    "value": "Condition met"
                }
            }
        }
    }
}

```


`rule.yaml`


```yaml

metadata:
    version: 0.2.0
    type: Rule
    id: 8330dd39-a0a4-4f21-aab4-0f8e35924c74
    created: '2023-12-15 04:54:00.349206'
    required_context_parameters:
    - xyz
    - number
    name: Complex rule
    parent_id: null
if:
    and:
    -   condition:
            metadata:
                version: 0.2.0
                type: Condition
                id: 16a74acf-3dfd-4c8f-a280-50dc3970455c
                created: '2023-12-15 04:54:00.349063'
                required_context_parameters:
                - number
            variable: number
            operator: in
            value:
                type: list
                value:
                -   type: int
                    value: 1
                -   type: int
                    value: 2
                -   type: int
                    value: 3
    -   condition:
            metadata:
                version: 0.2.0
                type: Condition
                id: 137af61f-16af-44b9-8c49-a1c61912704b
                created: '2023-12-15 04:54:00.349134'
                required_context_parameters:
                - number
            variable: number
            operator: '='
            value:
                type: int
                value: 1
then:
    result:
        xyz:
            type: str
            value: Condition met
        result:
            type: variable
            value: xyz
else:
    metadata:
        version: 0.2.0
        type: Rule
        id: 41ad9aa7-d072-49d1-9336-4186a3a6b69c
        created: '2023-12-15 04:54:00.349189'
        required_context_parameters:
        - number
        name: Nested rule
        parent_id: null
    if:
        condition:
            metadata:
                version: 0.2.0
                type: Condition
                id: 16a74acf-3dfd-4c8f-a280-50dc3970455c
                created: '2023-12-15 04:54:00.349063'
                required_context_parameters:
                - number
            variable: number
            operator: in
            value:
                type: list
                value:
                -   type: int
                    value: 1
                -   type: int
                    value: 2
                -   type: int
                    value: 3
    then:
        result:
            xyz:
                type: str
                value: Condition met


```

[Go back to top](#table-of-contents)
<br>

### Nested rules -

```python

from py_rules.components import Condition, Result, Rule

# Create conditions
condition1 = Condition('temperature', '>', 30)
condition2 = Condition('humidity', '<', 50)

# Create results
result1 = Result('message', 'str', 'It is hot!')
result2 = Result('message', 'str', 'It is dry!')

# Create rules
rule1 = Rule('Temperature Rule').If(condition1).Then(result1)
rule2 = Rule('Humidity Rule').If(condition2).Then(result2)

# Create a nested rule
nested_rule = Rule('Nested Rule').If(condition1).Then(rule2).Else(result1)

# Print the nested rule
print(nested_rule.to_dict())

```

This will create a nested rule that checks if the temperature is greater than 30. If the condition is met, it evaluates another rule that checks if the humidity is less than 50. If the nested condition is met, it returns the message "It is dry!". If the nested condition is not met, it returns the message "It is hot!".

Here's the equivalent rule in JSON format:

```json
{
    "metadata": {
        "version": "0.2.0",
        "type": "Rule",
        "id": "7f2a4893-322c-4973-8e41-c3930e37648b",
        "created": "2023-12-15 04:57:33.071026",
        "required_context_parameters": ["temperature", "humidity"],
        "name": "Nested Rule",
        "parent_id": null,
    },
    "if": {
        "condition": {
            "metadata": {
                "version": "0.2.0",
                "type": "Condition",
                "id": "515a3a0e-6a45-4848-9ea9-8202e66372cf",
                "created": "2023-12-15 04:57:33.070916",
                "required_context_parameters": ["temperature"],
            },
            "variable": "temperature",
            "operator": ">",
            "value": {"type": "int", "value": 30},
        }
    },
    "then": {
        "metadata": {
            "version": "0.2.0",
            "type": "Rule",
            "id": "7c045ec9-c262-4c6c-8b0f-34cc773d4f41",
            "created": "2023-12-15 04:57:33.071017",
            "required_context_parameters": ["humidity"],
            "name": "Humidity Rule",
            "parent_id": null,
        },
        "if": {
            "condition": {
                "metadata": {
                    "version": "0.2.0",
                    "type": "Condition",
                    "id": "ddc1e0f2-54a5-4c4f-aedd-2f6db69741dc",
                    "created": "2023-12-15 04:57:33.070964",
                    "required_context_parameters": ["humidity"],
                },
                "variable": "humidity",
                "operator": "<",
                "value": {"type": "int", "value": 50},
            }
        },
        "then": {"result": {"message": {"type": "str", "value": "It is dry!"}}},
    },
    "else": {"result": {"message": {"type": "str", "value": "It is hot!"}}},
}

```

[Go back to top](#table-of-contents)
<br>

<span id="engine"></span>

## Rule engine and evaluation

The `RuleEngine` class is used to evaluate a parsed rule. It takes a `Rule` object and a context (a dictionary) as input. The context is used to evaluate the conditions in the rule.

Here's a breakdown of the methods in the RuleEngine class:

- `__init__`: Initializes the RuleEngine with a `context: dict`; a dictionary of `facts`

    - The `context` dictionary MUST contain all the `variable`(s) being used, either in results or in conditions. The `required_context_parameters` set() of the `Rule` maintains a list of all unique context parameters required to evaluate the rule.

- `evaluate(rule: Rule)`: Evaluates the rule. It checks the 'if' condition and returns the result of the 'then' action if the condition is met, or the result of the 'else' action otherwise.

Here's an example of how to use the RuleEngine class:

```python

from py_rules.builder import Condition, Result, Rule
from py_rules.engine import RuleEngine

# Create a condition
condition = Condition('temperature', '>', 30)

# Create a result
result = Result('message', 'str', 'It is hot!')

# Create a rule
rule = Rule('Temperature Rule').If(condition).Then(result)

# Create a context
context = {'temperature': 35}

# Create a rule engine
engine = RuleEngine(context)

# Evaluate the rule
print(engine.evaluate(rule))  # prints: {'message': 'It is hot!'}

```

In this example, the rule checks if the temperature is greater than 30. The context provides the actual temperature. The rule engine evaluates the rule in the given context and returns the result of the rule.

You can also use the `RuleEngine` class with complex rules that have nested conditions and multiple results. Here's an example:

```python

# Create conditions
condition1 = Condition('temperature', '>', 30)
condition2 = Condition('humidity', '<', 50)

# Create results
result1 = Result('message', 'str', 'It is hot!')
result2 = Result('message', 'str', 'It is dry!')

# Create rules
rule1 = Rule('Temperature Rule').If(condition1).Then(result1)
rule2 = Rule('Humidity Rule').If(condition2).Then(result2)

# Create a context
context = {'temperature': 35, 'humidity': 45}

# Create a rule engine
engine = RuleEngine(context)

# Evaluate the rules
print(engine.evaluate(rule1))  # prints: {'message': 'It is hot!'}
print(engine.evaluate(rule2))  # prints: {'message': 'It is dry!'}

```

In this example, the first rule checks if the temperature is greater than 30, and the second rule checks if the humidity is less than 50. The context provides the actual temperature and humidity. The rule engines evaluate the rules in the given context and return the results of the rules.

[Go back to top](#table-of-contents)
<br>

<span id="tests"></span>

## Tests

Install all dev dependencies

```sh
$ pip install dev-requirements.txt
```

Run tests -

```sh
python -m unittest -v
```


<span id="todo"></span>

## To do

- Pass a global config dictionary from `RuleEngine` to control the following -
    - Date parsing functions
    - Rule metadata creation


[Go back to top](#table-of-contents)
<br>
<hr>
