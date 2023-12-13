import unittest
from py_rules.builder import Condition, Result, Rule
from py_rules.engine import RuleEngine

class TestEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.context = {"number": 5, "str_var": "py_rules"}

    def test_builder(self):
        condition = Condition('number', 'in', [1, 5, 3]) & Condition('number', '=', 5) & Condition('number', '>', 1) | Condition('number', '=', 2)
        result = Result().add('xyz', 'str', 'Condition met').add('abc', 'variable', 'str_var')
        rule = Rule('Complex rule').If(condition).Then(result).Else(result)

        engine = RuleEngine(rule.to_dict(), self.context)
        self.assertEqual(engine.evaluate(), {"xyz": "Condition met", "abc": "py_rules"})
        

