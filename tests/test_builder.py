import unittest
from py_rules.builder import Condition, Result, Rule

class TestBuilder(unittest.TestCase):
    def test_condition(self):
        condition = Condition('number', 'in', [1, 2, 3])
        self.assertEqual(
            condition.to_dict(), 
            {'condition': {'variable': 'number', 'operator': 'in', 'value': {'type': 'list', 'value': [{'type': 'int', 'value': 1}, {'type': 'int', 'value': 2}, {'type': 'int', 'value': 3}]}}})

    def test_result(self):
        result = Result().add('xyz', 'str', 'Condition met').add('result', 'variable', 'xyz')
        self.assertEqual(result.to_dict(), {'result': {'xyz': {'type': 'str', 'value': 'Condition met'}, 'result': {'type': 'variable', 'value': 'xyz'}}})

    def test_rule(self):
        condition = Condition('number', 'in', [1, 2, 3])
        result = Result().add('xyz', 'str', 'Condition met').add('result', 'variable', 'xyz')
        rule = Rule('Complex rule').If(condition).Then(result).Else(result)
        self.assertEqual(rule.to_dict(), {'rule': 'Complex rule', 'if': condition.to_dict(), 'then': result.to_dict(), 'else': result.to_dict()})
