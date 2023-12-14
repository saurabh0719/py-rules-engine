import datetime
import unittest

from py_rules.components import Condition, Result, Rule
from py_rules.engine import RuleEngine


class TestEngine(unittest.TestCase):

    def setUp(self) -> None:
        self.context = {"number": 5, "str_var": "py_rules"}

    def test_builder(self):
        condition = Condition('number', 'in', [1, 5, 3]) & Condition('number', '=', 5) & Condition(
            'number', '>', 1) | Condition('number', '=', 2)
        result = Result('xyz', 'str', 'Condition met') & Result('abc', 'variable', 'str_var')
        rule = Rule('Complex rule').If(condition).Then(result).Else(result)
        engine = RuleEngine(self.context)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met", "abc": "py_rules"})

    def test_required_parameters(self):
        condition = Condition('a', '=', 2) & Condition('b', '=', 5) & Condition('c', '>', 1)
        result = Result('abc', 'variable', 'str_var')
        rule = Rule('Complex rule').If(condition).Then(result).Else(result)
        self.assertEqual(len(rule.required_context_parameters), 4)

    def test_basic_rules(self):
        condition = Condition('number', '=', 5)
        result = Result('xyz', 'str', 'Condition met')
        rule = Rule('Basic rule').If(condition).Then(result).Else(result)
        engine = RuleEngine(self.context)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met"})

        rule = Rule('Basic rule').If(condition)
        self.assertEqual(engine.evaluate(rule), True)

        condition = Condition('number', '=', 6)
        rule = Rule('Basic rule').If(condition)
        self.assertEqual(engine.evaluate(rule), False)

    def test_multiple_conditions(self):
        condition = Condition('number', '=', 5) & Condition('number', '>', 1)
        result = Result('xyz', 'str', 'Condition met')
        rule = Rule('Multiple conditions').If(condition).Then(result).Else(result)
        engine = RuleEngine(self.context)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met"})

        condition = Condition('number', '=', 5) & Condition('number', '>', 10)
        rule = Rule('Multiple conditions').If(condition).Then(result).Else(result)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met"})

        condition = Condition('number', '=', 5) & Condition('number', '<', 10)
        rule = Rule('Multiple conditions').If(condition).Then(result).Else(result)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met"})

        condition = Condition('number', '=', 5) & Condition('number', '<', 1)
        rule = Rule('Multiple conditions').If(condition).Then(result).Else(result)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met"})

    def test_datetime_expressions(self):
        """
        The condition to compare 'date' with is a 'date' object
        """

        context = {"date": datetime.date(2020, 1, 1)}
        condition = Condition('date', '=', datetime.date(2020, 1, 1))
        result = Result('xyz', 'str', 'Condition met')
        rule = Rule('Datetime rule').If(condition).Then(result).Else(result)
        engine = RuleEngine(context)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met"})

        condition = Condition('date', '=', datetime.date(2020, 1, 2))
        rule = Rule('Datetime rule').If(condition).Then(result).Else(result)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met"})

        condition = Condition('date', '=', datetime.date(2019, 1, 1))
        rule = Rule('Datetime rule').If(condition).Then(result).Else(result)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met"})

        condition = Condition('date', '=', datetime.date(2019, 1, 2))
        rule = Rule('Datetime rule').If(condition).Then(result).Else(result)
        self.assertEqual(engine.evaluate(rule), {"xyz": "Condition met"})
