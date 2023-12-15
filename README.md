<!-- ![py_rules](https://github.com/saurabh0719/py-rules/assets/42310348/fff20963-e144-44d0-bfde-3b9c7eb0c6ee) -->
![Screenshot from 2023-12-14 01-53-59](https://github.com/saurabh0719/py-rules/assets/42310348/6c8830a7-0625-4b34-8bec-b4b450db7955)

## Introduction

`py-rules-engine` is a robust, Python-based rules engine that enables the creation of intricate logical conditions and actions. Key features include:

- **Complex Logical Conditions**: Define intricate conditions using logical operators.

- **Pythonic Rule Builder**: Utilize a Pythonic interface for easy rule definition.
- **Flexible Rule Management**: Store, configure, and share rules in JSON/YAML format, with seamless shifting between Python rule builder and other formats.
- **Nested Rules**: Create multi-level rule structures.
- **Rule Evaluation**: Evaluate rules in a given context with a built-in rule engine.
- **Zero Dependencies**: Pure Python implementation for easy installation and use.


Example usage -


```python

from py_rules.components import Condition, Result, Rule
from py_rules.engine import RuleEngine

# Create a condition
condition = Condition('temperature', '>', 40) & Condition('day_of_week', 'in', [1, 2, 3, 4, 5])

# Create a result
result = Result('message', 'str', 'Unfavourable weather conditions for work!')

# Create a rule
rule = Rule('Temperature Rule').If(condition).Then(result)

# initialise a new instance of RuleEngine with context
context = {'temperature': 40, 'day_of_week': 5}
engine = RuleEngine(context)

print(engine.evaluate(rule))
# 'Unfavourable weather conditions for work!'

# if a Rule is used without a Result, it simply returns True/False
rule = Rule('Bool Temperature Rule').If(condition)
print(engine.evaluate(rule))
# True

```

<span id="table-of-contents"></span>

## Table of Contents :
* [Installation](#installation)
* [Rule structure](#structure)
  * [Basics](#basics)
  * [Representation](#repr)
* [Rule builder & parser](#builder)
  * [Components](#components)
  * [Nested rules](#nested)
  * [Parser](#parser)
* [Rule engine and evaluation](#engine)
* [Rule storage and parsing](#storage)
* [Tests](#tests)
* [To do](#todo)


<span id="installation"></span>

## Installation
You can install `py-rules-engine` using pip:

```bash
pip install py-rules-engine
```

**NOTE** - this library is currently in Beta, and things may break between version bumps pre-1.0.0.


<span id="structure"></span>

## Rule structure

This section covers the basics of this library, including the structure of the `Rule` object.

<span id="basics"></span>

### Basics

The `If-Then-Else` structure is a fundamental part of the rule engine. It allows you to define a condition and specify the results based on whether the condition is met or not. Here's a breakdown of each part:

- `If`: This is the condition that will be evaluated. It can be a simple condition (like "temperature > 30") or a complex condition involving multiple variables and logical operators (like "temperature > 30 AND humidity < 50"). The condition is evaluated against a given `context`, which is a dictionary of variables and their values.

- `Then`: This part specifies the result or action that should be returned or performed if the IF condition is met (i.e., if it evaluates to True). It can be a simple value (like "It's hot") or a complex object. It can also be another `Rule`, allowing for `nested rules`.

- `Else`: This part specifies the result or action that should be returned or performed if the IF condition is not met (i.e., if it evaluates to False). Like the THEN part, it can be a simple value, a complex object, or another `Rule`. The ELSE part is optional; if it's not provided and the IF condition is not met, the rule engine will return False.


Every `Rule` object's `dict` representation (rule.to_dict()) contains the following

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

- `else`: This section contains the result to be returned if the `if` condition evaluates to `False`, or a nested rule with its own `if`, `then`, and `else` sections.

All the `Rule`(s) are evaluated against a `context` dictionary. The `context` is key-value dictionary of `facts` we use to evaluate all conditions and prepare return statements.

See the `examples/` directory for more.

[Go back to top](#table-of-contents)
<br>

<span id="repr"></span>

### Representation

Every `Rule` object and it's conditions is represented as a `dictionary` structure. Ev

For example-

```python

from py_rules.components import Condition, Result, Rule
from py_rules.engine import RuleEngine

# Create a condition
condition = Condition('temperature', '>', 40) | Condition('wind_speed', '>', 50)
no_work = Result('message', 'str', 'Unfavourable weather conditions for work!')
work = Result('message', 'str', 'Favourable weather conditions for work!')
rule = Rule('Temperature Rule').If(condition).Then(no_work).Else(work)

print(rule.to_dict())

"""
{
    "metadata": {
        "version": "0.3.0",
        "type": "Rule",
        "id": "a605f337-7d60-4a65-a361-96c282e3fc74",
        "created": "2023-12-15 12:53:48.492187",
        "required_context_parameters": ["wind_speed", "temperature"],
        "name": "Temperature Rule",
        "parent_id": None,
    },
    "if": {
        "or": [
            {
                "condition": {
                    "metadata": {
                        "version": "0.3.0",
                        "type": "Condition",
                        "id": "10346a0c-3934-4ed9-b393-053b871ab17d",
                        "created": "2023-12-15 12:53:48.492090",
                        "required_context_parameters": ["temperature"],
                    },
                    "variable": "temperature",
                    "operator": ">",
                    "value": {"type": "int", "value": 40},
                }
            },
            {
                "condition": {
                    "metadata": {
                        "version": "0.3.0",
                        "type": "Condition",
                        "id": "0f3e660e-01a6-41d1-849c-e5b27088ccb4",
                        "created": "2023-12-15 12:53:48.492140",
                        "required_context_parameters": ["wind_speed"],
                    },
                    "variable": "wind_speed",
                    "operator": ">",
                    "value": {"type": "int", "value": 50},
                }
            },
        ]
    },
    "then": {
        "result": {
            "message": {
                "type": "str",
                "value": "Unfavourable weather conditions for work!",
            }
        }
    },
    "else": {
        "result": {
            "message": {
                "type": "str",
                "value": "Favourable weather conditions for work!",
            }
        }
    },
}
"""

```

This `dictionary` is what is used for evaluation.


[Go back to top](#table-of-contents)
<br>

<span id="builder"></span>

## Rule builder & parser


<span id="components"></span>

### Rule components

The following components can be used to build complex Rules.

- `Condition`: This class represents a condition in a rule. It can be initialized with a variable, operator, and value, or with a condition dictionary. It supports logical `and` and `or` operations to combine conditions. The `to_dict` method returns a dictionary representation of the condition.

- `Result`: This class represents a result in a Rule. It can be initialized with a key, type, and value, or with a result dictionary. It supports the `and` operation to combine results. The `to_dict` method returns a dictionary representation of the result.

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

```python

{
    "metadata": {
        "version": "0.3.0",
        "type": "Rule",
        "id": "5dbca846-5e59-4b6c-bdbf-9602d68c79ff",
        "created": "2023-12-15 04:49:45.183531",
        "required_context_parameters": ["temperature"],
        "name": "Temperature Rule",
        "parent_id": None,
    },
    "if": {
        "condition": {
            "metadata": {
                "version": "0.3.0",
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

<span id='nested'></span>

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
        "version": "0.3.0",
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
                "version": "0.3.0",
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
            "version": "0.3.0",
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
                    "version": "0.3.0",
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


<span id="parser"></span>

### Rule Parser

The `RuleParser` class is a utility class that is used to parse a rule from a `python dictionary` into a `Rule` object. This is useful when you want to define rules in a another format (JSON, YAML, etc.) and then load them into your Python code.

```python

from py_rules.components import Rule
from py_rules.parser import RuleParser

# Define a rule as a dictionary
rule_dict = {
    "metadata": {
        "version": "0.3.0",
        "type": "Rule",
        "id": "9911bf90-b6a1-490f-ae5a-3fa9409529f8",
        "created": "2023-12-15 13:09:59.411292",
        "required_context_parameters": ["temperature"],
        "name": "Unnamed Rule 1",
        "parent_id": None,
    },
    "if": {
        "condition": {
            "metadata": {
                "version": "0.3.0",
                "type": "Condition",
                "id": "a4b678f7-44f3-4818-8a72-298880263703",
                "created": "2023-12-15 13:09:59.411350",
                "required_context_parameters": ["temperature"],
            },
            "variable": "temperature",
            "operator": ">",
            "value": {"type": "int", "value": 30},
        }
    },
    "then": {"result": {"message": {"type": "str", "value": "It's hot"}}},
    "else": {"result": {"message": {"type": "str", "value": "It's not hot"}}},
}


# Parse the rule
rule = RuleParser().parse(rule_dict)

print(type(rule))
# <class 'py_rules.components.Rule'>

assert isinstance(rule, Rule)

print(rule.metadata)
# {'version': '0.3.0', 'type': 'Rule', 'id': '9911bf90-b6a1-490f-ae5a-3fa9409529f8', 'created': '2023-12-15 13:09:59.411292', 'required_context_parameters': ['temperature'], 'name': 'Unnamed Rule 1', 'parent_id': None}

```

[Go back to top](#table-of-contents)
<br>


<span id="engine"></span>

## Rule engine and evaluation

The `RuleEngine` class is used to evaluate a rules. It takes a `Rule` object and a context (a dictionary) as input. The `Rule` is then evaluated against the `context`

Here's a breakdown of the methods in the RuleEngine class:

- `__init__`: Initializes the RuleEngine with a `context: dict`; a dictionary of `facts`.

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

<span id="storage"></span>

## Rule parsing and storage

Storing & loading rules from persistent storage enable reuse of rules across different sessions and sharing of rules between different systems.

The `RuleStorage` class is an abstract base class that defines the common interface for all storage classes. It has two abstract methods: `load` and `store`. Any class that inherits from `RuleStorage` must implement these methods. The `RuleStorage` class also has a RuleParser object that is used to parse a rule **after it is loaded into a `dictionary`** format.

The `JSONRuleStorage` and `PickledRuleStorage` classes are concrete classes that inherit from RuleStorage and implement the load and store methods. Each class is designed to work with a specific file format.

Each class also validates the file type in its constructor to ensure that it matches the expected file type. If the file type is not valid, it raises an `InvalidRuleError`.

You can also create your own `RuleStorage` class, as shown in the example below for `yaml` files -

```python
import yaml

from py_rules.components import Condition, Result, Rule
from py_rules.storages import RuleStorage, JSONRuleStorage, PickledRuleStorage

yaml.Dumper.ignore_aliases = lambda *args: True

# CUSTOM Yaml Storage
class YAMLRuleStorage(RuleStorage):
    """
    RuleStorage class for YAML files.
    """

    format = 'yaml'

    def __init__(self, file_path):
        """
        Initialize the loader with a file_path.
        """
        super().__init__()
        self.file_path = file_path
        # validate that the file_path is valid and is a yaml file
        if not self.file_path.endswith('.yaml'):
            raise InvalidRuleError('Invalid file type. Only YAML files are supported.')

    def load(self):
        """
        Load a rule from a YAML file.
        """
        data = {}
        with open(self.file_path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return self.parser.parse(data)

    def store(self, rule):
        """
        Store a rule in a YAML file.
        """
        data = rule.to_dict()
        with open(self.file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, indent=4, sort_keys=False)


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
        "version": "0.3.0",
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
                        "version": "0.3.0",
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
                        "version": "0.3.0",
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
            "version": "0.3.0",
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
                    "version": "0.3.0",
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
    version: 0.3.0
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
                version: 0.3.0
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
                version: 0.3.0
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
        version: 0.3.0
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
                version: 0.3.0
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
