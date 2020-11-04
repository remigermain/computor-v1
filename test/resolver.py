from src.parser import Parser
from src.resolver import Resolver
import unittest


class Test(unittest.TestCase):

    def to_resolver(self, eq):
        parser = Parser(eq)
        self.assertTrue(parser.is_valid())
        return {
            'data': parser.validated_data,
            'no_print': True
        }

    def get_result_from(self, eq):
        resolver = Resolver(**self.to_resolver(eq))
        resolver.resolve()
        return resolver.generate_result()

    def test_division_zero(self):
        result = self.get_result_from("x = x")
        self.assertEqual("ALL", result)

    def test_impossible(self):
        result = self.get_result_from("2x = x")
        self.assertEqual(0, result)

    def test_pdf(self):
        result = self.get_result_from(
            "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
        self.assertEqual(0.905239, round(result[0], 6))
        self.assertEqual(-0.475131, round(result[1], 6))

    def test_pdf2(self):
        result = self.get_result_from("5 * X^0 + 4 * X^1 = 4 * X^0")
        self.assertEqual(-0.25, result)

    def test_pdf3(self):
        result = self.get_result_from("5 + 4 * X + X^2= X^2")
        self.assertEqual(-1.25, result)

    def test_pdf4(self):
        result = self.get_result_from("42 * X ^ 0 = 42 ∗ X ^ 0")
        self.assertEqual("ALL", result)

    def test_eq(self):
        result = self.get_result_from("4 * X^0 + 3 * X^1 + X^2 = 0")
        self.assertEqual("ALL", result)

    def test_eq2(self):
        result = self.get_result_from(
            "1.5 * X ^ 1 + 8.3 * X ^ 2 - 2 * X ^ 0 = -4.1 * X ^ 1 + 2 * X ^ 0")
        self.assertEqual(-1.10919, round(result[0], 5))
        self.assertEqual(0.434488, round(result[1], 6))


if __name__ == '__main__':
    unittest.main()
