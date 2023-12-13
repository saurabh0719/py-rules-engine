<!-- ![py_rules](https://github.com/saurabh0719/py-rules/assets/42310348/fff20963-e144-44d0-bfde-3b9c7eb0c6ee) -->
![Screenshot from 2023-12-14 01-53-59](https://github.com/saurabh0719/py-rules/assets/42310348/6c8830a7-0625-4b34-8bec-b4b450db7955)

## Introduction

`py-rules` is a simple, yet powerful rules engine written in pure Python. It allows you to define complex logical conditions and actions, either via a json file or through pythonic functions.

- **Complex Logical Conditions**: It allows you to define complex logical conditions using and, or, and not operations.

- **Pythonic Rule Builder**: It provides a Pythonic interface for building rules, making it easy to define rules in your Python code.

- **JSON Support**: It allows you to define rules in JSON format. This makes it easy to store, configure, and share rules.

- **Ease of Shifting**: One of the standout features of py-rules is the ease of shifting between a Python rule builder and storing/configuring rules in JSON. This flexibility allows you to choose the most convenient way to define and manage your rules.

- **Nested Rules**: It supports nested rules, allowing you to create complex rule structures with multiple levels of conditions.

- **Rule Evaluation**: It provides a rule engine for evaluating rules in a given context.

- **Pure Python**: It is written in pure Python, making it easy to install and use without any dependency.

<span id="contents"></span>

## Table of Contents :
* [Installation](#installation)
* [Rule & Evaluation basics](#basics)
* [Rule builder](#builder)
* [Rule Engine](#engine)
* [Tests](#tests)
* [To do](#todo)


<span id="installation"></span>

## Installation
You can install `py-rules` using pip:

```bash
pip install py-rules
```


<span id="basics"></span>

### Rule & Evaluation basics

- `rule_metadata`: This section contains metadata about the rule.

  - `__version__`: The version of the rule.
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

See the `examples/rule_json/` directory for some JSON rule files.


<span id="builder"></span>

## Rule Builder

- `Condition`: This class represents a condition in a rule. It can be initialized with a variable, operator, and value, or with a condition dictionary. It supports logical `and` and `or` operations to combine conditions. The `to_dict` method returns a dictionary representation of the condition.

- `Result`: This class represents a result in a rule. It can be initialized with a key, type, and value, or with a result dictionary. It supports the `and` operation to combine results. The `to_dict` method returns a dictionary representation of the result.

- `Rule`: This class represents a rule. It can be initialized with a name and optional keyword arguments. It supports the `If`, `Then`, and `Else` methods to set the condition and results of the rule. The `to_dict` method returns a dictionary representation of the rule.


```python

from py_rules.builder import Condition, Result, Rule

# Create a condition
condition = Condition('temperature', '>', 30)

# Create a result
result = Result('message', 'str', 'It is hot!')

# Create a rule
rule = Rule('Temperature Rule').If(condition).Then(result)

# Print the rule
print(rule.to_dict())

```

This will create a rule that checks if the temperature is greater than 30 and returns the message "It is hot!" if the condition is met.

You can also save a rule to a JSON file and load it back:

```python

# Save the rule to a JSON file
rule.save_to_file('rule.json')

# Load the rule from the JSON file
loaded_rule = Rule('Loaded Rule').load_from_file('rule.json')

# Print the loaded rule
print(loaded_rule.to_dict())

```


`rule.json` -

```json

{
    "rule_metadata": {
        "__version__": "0.1.0",
        "id": "043cd3ef-6e48-46a5-85fb-c4c305b82d4e",
        "parent_id": null,
        "created": "2023-12-14 02:44:51.229765",
        "name": "Temperature Rule",
        "required_context_parameters": ["temperature"],
    },
    "if": {
        "condition": {
            "variable": "temperature",
            "operator": ">",
            "value": {"type": "int", "value": 30},
        }
    },
    "then": {"result": {"message": {"type": "str", "value": "It is hot!"}}},
}

```

This will save the rule to a file named rule.json and then load it back into a new Rule object.


### Nested rules -

```python

from py_rules.builder import Condition, Result, Rule

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
    "rule_metadata": {
        "__version__": "0.1.0",
        "id": "e43afea4-15d7-4bac-ab51-3384b78eb99a",
        "parent_id": null,
        "created": "2023-12-14 02:47:39.893801",
        "name": "Nested Rule",
        "required_context_parameters": ["temperature"],
    },
    "if": {
        "condition": {
            "variable": "temperature",
            "operator": ">",
            "value": {"type": "int", "value": 30},
        }
    },
    "then": {
        "rule_metadata": {
            "__version__": "0.1.0",
            "id": "24e1fd04-9cbd-4da3-90ad-d78bd7546e42",
            "parent_id": "e43afea4-15d7-4bac-ab51-3384b78eb99a",
            "created": "2023-12-14 02:47:39.882982",
            "name": "Humidity Rule",
            "required_context_parameters": ["humidity"],
        },
        "if": {
            "condition": {
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


<span id="engine"></span>

### Rule Engine

The `RuleEngine` class is used to evaluate a parsed rule. It takes a `Rule` object and a context (a dictionary) as input. The context is used to evaluate the conditions in the rule.

Here's a breakdown of the methods in the RuleEngine class:

- `__init__`: Initializes the RuleEngine with a `rule` (`Rule` type) and a `context: dict`. It also validates the context.

    - The `context` dictionary MUST contain all the `variable`(s) being used, either in results or in conditions. The `required_context_parameters` in `rule_metadata` of the `Rule` maintains a list of all unique context parameters required to evaluate the rule.

- `evaluate`: Evaluates the rule. It checks the 'if' condition and returns the result of the 'then' action if the condition is met, or the result of the 'else' action otherwise.

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
engine = RuleEngine(rule, context)

# Evaluate the rule
print(engine.evaluate())  # prints: {'message': 'It is hot!'}

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
engine1 = RuleEngine(rule1, context)
engine2 = RuleEngine(rule2, context)

# Evaluate the rules
print(engine1.evaluate())  # prints: {'message': 'It is hot!'}
print(engine2.evaluate())  # prints: {'message': 'It is dry!'}

```

In this example, the first rule checks if the temperature is greater than 30, and the second rule checks if the humidity is less than 50. The context provides the actual temperature and humidity. The rule engines evaluate the rules in the given context and return the results of the rules.

<span id="tests"></span>

### Tests

Install all dev dependencies

```sh
$ pip install dev-requirements.txt
```

Run tests -

```sh
python -m unittest -v
```


<span id="todo"></span>

### To do

- Pass a global config dictionary from `RuleEngine` to control the following -
    - Date parsing functions
    - Rule metadata creation


[Go back to top](#table-of-contents)
<br>
<hr>
