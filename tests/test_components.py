import unittest

from py_rules.components import Condition, Result, Rule


class TestRuleComponents(unittest.TestCase):

    def test_condition(self):
        condition = Condition('number', 'in', [1, 2, 3])
        self.assertEqual(
            condition.to_dict(), {
                'condition': {
                    'metadata': condition.metadata,
                    'variable': 'number',
                    'operator': 'in',
                    'value': {
                        'type': 'list',
                        'value': [{
                            'type': 'int',
                            'value': 1
                        }, {
                            'type': 'int',
                            'value': 2
                        }, {
                            'type': 'int',
                            'value': 3
                        }]
                    }
                }
            })

    def test_result(self):
        result = Result('xyz', 'str', 'Condition met') & Result('result', 'variable', 'xyz')
        self.assertEqual(result.to_dict(), {
            'result': {
                'xyz': {
                    'type': 'str',
                    'value': 'Condition met'
                },
                'result': {
                    'type': 'variable',
                    'value': 'xyz'
                }
            }
        })

    def test_rule(self):
        condition = Condition('number', 'in', [1, 2, 3])
        result = Result('xyz', 'str', 'Condition met') & Result('result', 'variable', 'xyz')
        rule = Rule('rule-one').If(condition).Then(result).Else(result)
        dict_repr = rule.to_dict()
        metadata = dict_repr.pop('metadata')
        self.assertEqual(metadata['name'], 'rule-one')
        self.assertEqual(dict_repr, {'if': condition.to_dict(), 'then': result.to_dict(), 'else': result.to_dict()})
