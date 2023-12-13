import unittest

from py_rules.builder import Condition, Result, Rule
from py_rules.engine import RuleEngine


class TestEngine(unittest.TestCase):

    def setUp(self) -> None:
        self.context = {"number": 5, "str_var": "py_rules"}

    def test_builder(self):
        condition = Condition('number', 'in', [1, 5, 3]) & Condition(
            'number', '=', 5) & Condition('number', '>', 1) | Condition(
                'number', '=', 2)
        result = Result('xyz', 'str', 'Condition met') & Result(
            'abc', 'variable', 'str_var')
        rule = Rule('Complex rule').If(condition).Then(result).Else(result)
        engine = RuleEngine(rule, self.context)
        self.assertEqual(engine.evaluate(), {
            "xyz": "Condition met",
            "abc": "py_rules"
        })

    def test_required_parameters(self):
        condition = Condition('a', '=', 2) & Condition(
            'b', '=', 5) & Condition('c', '>', 1)
        result = Result('abc', 'variable', 'str_var')
        rule = Rule('Complex rule').If(condition).Then(result).Else(result)
        self.assertEqual(
            len(set(rule.rule_metadata.get('required_context_parameters',
                                           []))), 3)
