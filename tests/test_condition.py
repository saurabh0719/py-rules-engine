import unittest
from datetime import datetime

from py_rules.condition import RuleCondition, RuleExpression, RuleValue
from py_rules.constants import Operators, Types
from py_rules.errors import (InvalidRuleConditionError, InvalidRuleExpressionError, InvalidRuleValueError,
                             InvalidRuleValueTypeError)


class TestRuleValue(unittest.TestCase):

    def setUp(self):
        self.context = {'var': 'value'}

    def test_missing_type(self):
        with self.assertRaises(InvalidRuleValueError):
            RuleValue({'value': 'test'}, self.context)

    def test_invalid_type(self):
        with self.assertRaises(InvalidRuleValueTypeError):
            RuleValue({'type': 'invalid', 'value': 'test'}, self.context)

    def test_boolean(self):
        rule_value = RuleValue({'type': Types.BOOLEAN, 'value': 'True'}, self.context)
        self.assertEqual(rule_value.get_value(), True)

    def test_string(self):
        rule_value = RuleValue({'type': Types.STRING, 'value': 'test'}, self.context)
        self.assertEqual(rule_value.get_value(), 'test')

    def test_integer(self):
        rule_value = RuleValue({'type': Types.INTEGER, 'value': '1'}, self.context)
        self.assertEqual(rule_value.get_value(), 1)

    def test_float(self):
        rule_value = RuleValue({'type': Types.FLOAT, 'value': '1.1'}, self.context)
        self.assertEqual(rule_value.get_value(), 1.1)

    def test_date(self):
        rule_value = RuleValue({'type': Types.DATE, 'value': '2022-01-01'}, self.context)
        self.assertEqual(rule_value.get_value(), datetime.strptime('2022-01-01', '%Y-%m-%d').date())

    def test_datetime(self):
        rule_value = RuleValue({'type': Types.DATETIME, 'value': '2022-01-01T12:00:00'}, self.context)
        self.assertEqual(rule_value.get_value(), datetime.strptime('2022-01-01T12:00:00', '%Y-%m-%dT%H:%M:%S'))

    def test_list(self):
        data = {
            'type': Types.LIST,
            'value': [{
                'type': Types.STRING,
                'value': 'one'
            }, {
                'type': Types.STRING,
                'value': 'two'
            }]
        }
        rule_value = RuleValue(data, self.context)
        self.assertEqual(rule_value.get_value(), ['one', 'two'])

    def test_dict(self):
        data = {
            'type': Types.DICTIONARY,
            'value': {
                'key': {
                    'type': Types.STRING,
                    'value': 'one'
                },
                'value': {
                    'type': Types.STRING,
                    'value': 'two'
                }
            }
        }
        rule_value = RuleValue(data, self.context)
        self.assertEqual(rule_value.get_value(), {'key': 'one', 'value': 'two'})

    def test_none(self):
        rule_value = RuleValue({'type': Types.NONETYPE, 'value': 'None'}, self.context)
        self.assertEqual(rule_value.get_value(), None)

    def test_variable(self):
        rule_value = RuleValue({'type': Types.VARIABLE, 'value': 'var'}, self.context)
        self.assertEqual(rule_value.get_value(), 'value')


class TestRuleExpression(unittest.TestCase):

    def setUp(self):
        self.context = {'var': 'value'}

    def test_invalid_operator(self):
        left_value = RuleValue({'type': Types.STRING, 'value': 'test'}, self.context)
        right_value = RuleValue({'type': Types.STRING, 'value': 'test'}, self.context)
        with self.assertRaises(InvalidRuleExpressionError):
            RuleExpression('invalid', left_value, right_value).evaluate()

    def test_invalid_value_type(self):
        left_value = RuleValue({'type': Types.STRING, 'value': 'test'}, self.context)
        right_value = RuleValue({'type': Types.INTEGER, 'value': '1'}, self.context)
        with self.assertRaises(InvalidRuleValueError):
            RuleExpression(Operators.GREATER_THAN, left_value, right_value).evaluate()

    def test_equal(self):
        left_value = RuleValue({'type': Types.STRING, 'value': 'test'}, self.context)
        right_value = RuleValue({'type': Types.STRING, 'value': 'test'}, self.context)
        self.assertTrue(RuleExpression(Operators.EQUAL, left_value, right_value).evaluate())

    def test_less_than(self):
        left_value = RuleValue({'type': Types.INTEGER, 'value': '1'}, self.context)
        right_value = RuleValue({'type': Types.INTEGER, 'value': '2'}, self.context)
        self.assertTrue(RuleExpression(Operators.LESS_THAN, left_value, right_value).evaluate())

    def test_greater_than(self):
        left_value = RuleValue({'type': Types.INTEGER, 'value': '2'}, self.context)
        right_value = RuleValue({'type': Types.INTEGER, 'value': '1'}, self.context)
        self.assertTrue(RuleExpression(Operators.GREATER_THAN, left_value, right_value).evaluate())

    def test_less_than_equal(self):
        left_value = RuleValue({'type': Types.INTEGER, 'value': '1'}, self.context)
        right_value = RuleValue({'type': Types.INTEGER, 'value': '2'}, self.context)
        self.assertTrue(RuleExpression(Operators.LESS_THAN_OR_EQUAL, left_value, right_value).evaluate())

        left_value = RuleValue({'type': Types.INTEGER, 'value': '2'}, self.context)
        self.assertTrue(RuleExpression(Operators.LESS_THAN_OR_EQUAL, left_value, right_value).evaluate())

        left_value = RuleValue({'type': Types.INTEGER, 'value': '3'}, self.context)
        self.assertFalse(RuleExpression(Operators.LESS_THAN_OR_EQUAL, left_value, right_value).evaluate())

    def test_greater_than_equal(self):
        left_value = RuleValue({'type': Types.INTEGER, 'value': '2'}, self.context)
        right_value = RuleValue({'type': Types.INTEGER, 'value': '1'}, self.context)
        self.assertTrue(RuleExpression(Operators.GREATER_THAN_OR_EQUAL, left_value, right_value).evaluate())

        right_value = RuleValue({'type': Types.INTEGER, 'value': '2'}, self.context)
        self.assertTrue(RuleExpression(Operators.GREATER_THAN_OR_EQUAL, left_value, right_value).evaluate())

        right_value = RuleValue({'type': Types.INTEGER, 'value': '3'}, self.context)
        self.assertFalse(RuleExpression(Operators.GREATER_THAN_OR_EQUAL, left_value, right_value).evaluate())

    def test_not_equal(self):
        left_value = RuleValue({'type': Types.INTEGER, 'value': '2'}, self.context)
        right_value = RuleValue({'type': Types.INTEGER, 'value': '1'}, self.context)
        self.assertTrue(RuleExpression(Operators.NOT_EQUAL, left_value, right_value).evaluate())

    def test_in(self):
        left_value = RuleValue({'type': Types.STRING, 'value': 'test'}, self.context)
        right_value = RuleValue(
            {
                'type': Types.LIST,
                'value': [{
                    'type': Types.STRING,
                    'value': 'test'
                }, {
                    'type': Types.STRING,
                    'value': 'test2'
                }]
            }, self.context)
        self.assertTrue(RuleExpression(Operators.IN, left_value, right_value).evaluate())

        left_value = RuleValue({'type': Types.STRING, 'value': 'test3'}, self.context)
        self.assertFalse(RuleExpression(Operators.IN, left_value, right_value).evaluate())

    def test_not_in(self):
        left_value = RuleValue({'type': Types.STRING, 'value': 'test'}, self.context)
        right_value = RuleValue(
            {
                'type': Types.LIST,
                'value': [{
                    'type': Types.STRING,
                    'value': 'test'
                }, {
                    'type': Types.STRING,
                    'value': 'test2'
                }]
            }, self.context)
        self.assertFalse(RuleExpression(Operators.NOT_IN, left_value, right_value).evaluate())

        left_value = RuleValue({'type': Types.STRING, 'value': 'test3'}, self.context)
        self.assertTrue(RuleExpression(Operators.NOT_IN, left_value, right_value).evaluate())


class TestRuleCondition(unittest.TestCase):

    def setUp(self):
        self.context = {'var': 'value'}

    def test_missing_operator(self):
        condition = {'variable': 'var', 'value': {'type': Types.STRING, 'value': 'test'}}
        with self.assertRaises(InvalidRuleConditionError):
            RuleCondition(self.context).evaluate(condition)

    def test_missing_variable(self):
        condition = {'operator': Operators.EQUAL, 'value': {'type': Types.STRING, 'value': 'test'}}
        with self.assertRaises(InvalidRuleConditionError):
            RuleCondition(self.context).evaluate(condition)

    def test_evaluate(self):
        condition = {'operator': Operators.EQUAL, 'variable': 'var', 'value': {'type': Types.STRING, 'value': 'value'}}
        self.assertTrue(RuleCondition(self.context).evaluate(condition))
