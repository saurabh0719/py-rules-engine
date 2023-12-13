import unittest
from datetime import datetime
from py_rules.value import RuleValue
from py_rules.errors import InvalidRuleValueError, InvalidRuleValueTypeError
from py_rules.constants import Types

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
            'value': [
                {
                    'type': Types.STRING,
                    'value': 'one'
                },
                {
                    'type': Types.STRING,
                    'value': 'two'
                }
            ]
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
