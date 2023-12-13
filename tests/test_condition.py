import unittest

from py_rules.condition import RuleCondition
from py_rules.constants import Operators, Types
from py_rules.errors import InvalidRuleConditionError


class TestRuleCondition(unittest.TestCase):

    def setUp(self):
        self.context = {'var': 'value'}

    def test_missing_operator(self):
        condition = {
            'variable': 'var',
            'value': {
                'type': Types.STRING,
                'value': 'test'
            }
        }
        with self.assertRaises(InvalidRuleConditionError):
            RuleCondition(condition, self.context)

    def test_missing_variable(self):
        condition = {
            'operator': Operators.EQUAL,
            'value': {
                'type': Types.STRING,
                'value': 'test'
            }
        }
        with self.assertRaises(InvalidRuleConditionError):
            RuleCondition(condition, self.context)

    def test_evaluate(self):
        condition = {
            'operator': Operators.EQUAL,
            'variable': 'var',
            'value': {
                'type': Types.STRING,
                'value': 'value'
            }
        }
        self.assertTrue(RuleCondition(condition, self.context).evaluate())
