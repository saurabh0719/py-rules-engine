import unittest

from py_rules.constants import Operators
from py_rules.errors import InvalidRuleExpressionError, InvalidRuleValueError
from py_rules.expression import RuleExpression
from py_rules.value import RuleValue, Types


class TestRuleExpression(unittest.TestCase):

    def setUp(self):
        self.context = {'var': 'value'}

    def test_invalid_operator(self):
        left_value = RuleValue({
            'type': Types.STRING,
            'value': 'test'
        }, self.context)
        right_value = RuleValue({
            'type': Types.STRING,
            'value': 'test'
        }, self.context)
        with self.assertRaises(InvalidRuleExpressionError):
            RuleExpression('invalid', left_value, right_value).evaluate()

    def test_invalid_value_type(self):
        left_value = RuleValue({
            'type': Types.STRING,
            'value': 'test'
        }, self.context)
        right_value = RuleValue({
            'type': Types.INTEGER,
            'value': '1'
        }, self.context)
        with self.assertRaises(InvalidRuleValueError):
            RuleExpression(Operators.GREATER_THAN, left_value,
                           right_value).evaluate()

    def test_equal(self):
        left_value = RuleValue({
            'type': Types.STRING,
            'value': 'test'
        }, self.context)
        right_value = RuleValue({
            'type': Types.STRING,
            'value': 'test'
        }, self.context)
        self.assertTrue(
            RuleExpression(Operators.EQUAL, left_value,
                           right_value).evaluate())

    def test_less_than(self):
        left_value = RuleValue({
            'type': Types.INTEGER,
            'value': '1'
        }, self.context)
        right_value = RuleValue({
            'type': Types.INTEGER,
            'value': '2'
        }, self.context)
        self.assertTrue(
            RuleExpression(Operators.LESS_THAN, left_value,
                           right_value).evaluate())

    def test_greater_than(self):
        left_value = RuleValue({
            'type': Types.INTEGER,
            'value': '2'
        }, self.context)
        right_value = RuleValue({
            'type': Types.INTEGER,
            'value': '1'
        }, self.context)
        self.assertTrue(
            RuleExpression(Operators.GREATER_THAN, left_value,
                           right_value).evaluate())

    def test_less_than_equal(self):
        left_value = RuleValue({
            'type': Types.INTEGER,
            'value': '1'
        }, self.context)
        right_value = RuleValue({
            'type': Types.INTEGER,
            'value': '2'
        }, self.context)
        self.assertTrue(
            RuleExpression(Operators.LESS_THAN_OR_EQUAL, left_value,
                           right_value).evaluate())

        left_value = RuleValue({
            'type': Types.INTEGER,
            'value': '2'
        }, self.context)
        self.assertTrue(
            RuleExpression(Operators.LESS_THAN_OR_EQUAL, left_value,
                           right_value).evaluate())

        left_value = RuleValue({
            'type': Types.INTEGER,
            'value': '3'
        }, self.context)
        self.assertFalse(
            RuleExpression(Operators.LESS_THAN_OR_EQUAL, left_value,
                           right_value).evaluate())

    def test_greater_than_equal(self):
        left_value = RuleValue({
            'type': Types.INTEGER,
            'value': '2'
        }, self.context)
        right_value = RuleValue({
            'type': Types.INTEGER,
            'value': '1'
        }, self.context)
        self.assertTrue(
            RuleExpression(Operators.GREATER_THAN_OR_EQUAL, left_value,
                           right_value).evaluate())

        right_value = RuleValue({
            'type': Types.INTEGER,
            'value': '2'
        }, self.context)
        self.assertTrue(
            RuleExpression(Operators.GREATER_THAN_OR_EQUAL, left_value,
                           right_value).evaluate())

        right_value = RuleValue({
            'type': Types.INTEGER,
            'value': '3'
        }, self.context)
        self.assertFalse(
            RuleExpression(Operators.GREATER_THAN_OR_EQUAL, left_value,
                           right_value).evaluate())

    def test_not_equal(self):
        left_value = RuleValue({
            'type': Types.INTEGER,
            'value': '2'
        }, self.context)
        right_value = RuleValue({
            'type': Types.INTEGER,
            'value': '1'
        }, self.context)
        self.assertTrue(
            RuleExpression(Operators.NOT_EQUAL, left_value,
                           right_value).evaluate())

    def test_in(self):
        left_value = RuleValue({
            'type': Types.STRING,
            'value': 'test'
        }, self.context)
        right_value = RuleValue(
            {
                'type':
                Types.LIST,
                'value': [{
                    'type': Types.STRING,
                    'value': 'test'
                }, {
                    'type': Types.STRING,
                    'value': 'test2'
                }]
            }, self.context)
        self.assertTrue(
            RuleExpression(Operators.IN, left_value, right_value).evaluate())

        left_value = RuleValue({
            'type': Types.STRING,
            'value': 'test3'
        }, self.context)
        self.assertFalse(
            RuleExpression(Operators.IN, left_value, right_value).evaluate())

    def test_not_in(self):
        left_value = RuleValue({
            'type': Types.STRING,
            'value': 'test'
        }, self.context)
        right_value = RuleValue(
            {
                'type':
                Types.LIST,
                'value': [{
                    'type': Types.STRING,
                    'value': 'test'
                }, {
                    'type': Types.STRING,
                    'value': 'test2'
                }]
            }, self.context)
        self.assertFalse(
            RuleExpression(Operators.NOT_IN, left_value,
                           right_value).evaluate())

        left_value = RuleValue({
            'type': Types.STRING,
            'value': 'test3'
        }, self.context)
        self.assertTrue(
            RuleExpression(Operators.NOT_IN, left_value,
                           right_value).evaluate())
