from src.parser import Parser
from src.resolver import Resolver
from src.poly import Result
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
        self.assertTrue(resolver.is_valid())
        return resolver.resolve()

    def test_division_zero(self):
        result = self.get_result_from("x = x")
        self.assertEqual(Result.ANY_POSSIBILITY, result)

    def test_any2(self):
        result = self.get_result_from("1x^0 = 1x^0")
        self.assertEqual(Result.ANY_POSSIBILITY, result)

    def test_any3(self):
        result = self.get_result_from(
            "-1*x ^ 1 - -1*x ^ 1 = 2*x ^ 1 + - 1*x ^ 1 - 1*x ^ 1")
        self.assertEqual(Result.ANY_POSSIBILITY, result)

    def test_real3(self):
        result = self.get_result_from(
            "1*x ^ 1 - -1*x ^ 1 = 2*x ^ 1 + - 1*x ^ 1 - 1*x ^ 1")
        self.assertEqual(0.0, result)

    def test_impossible2(self):
        result = self.get_result_from("1x^0 = 2x^0")
        self.assertEqual(Result.NO_SOLUTION, result)

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
        self.assertEqual(Result.ANY_POSSIBILITY, result)

    def test_eq(self):
        result = self.get_result_from("4 * X^0 + 3 * X^1 + X^2 = 0")
        self.assertEqual(Result.IMAGINAIRE_SOLUTION, result)

    def test_eq2(self):
        result = self.get_result_from(
            "1.5 * X ^ 1 + 8.3 * X ^ 2 - 2 * X ^ 0 = -4.1 * X ^ 1 + 2 * X ^ 0")
        self.assertEqual(-1.10919, round(result[0], 5))
        self.assertEqual(0.434488, round(result[1], 6))

    def test_eq3(self):
        result = self.get_result_from("6 * X ^ 0 + -4 * X ^ 2=1 * X ^ 0")
        self.assertEqual(1.118, round(result[0], 3))
        self.assertEqual(-1.118, round(result[1], 3))

    def test_eq4(self):
        result = self.get_result_from("2x = x")
        self.assertEqual(0, result)

    def test_eq5(self):
        result = self.get_result_from("4*x^2 = 4*x^2 + 1*x^1 - 1*x^1")
        self.assertEqual(Result.ANY_POSSIBILITY, result)

    def test_eq6(self):
        result = self.get_result_from("2x + 4 = x - 3")
        self.assertEqual(-7.0, result)

    def test_loiberti_deg_one(self):
        result = self.get_result_from("40*x^0 - 12*x^1 = 4*x^0")
        self.assertEqual(3.0, result)

    def test_loiberti_delta_greater(self):
        result = self.get_result_from("5*x ^ 0 + 4*x ^ 1 - 9.3*x ^ 2=1*x ^ 0")
        self.assertEqual(0.905239, round(result[0], 6))
        self.assertEqual(-0.475131, round(result[1], 6))

    def test_loiberti_delta_smaller(self):
        result = self.get_result_from(
            "-2*x ^ 0 + 17*x ^ 1 - 4*x ^ 2 = 13*x ^ 1")
        self.assertEqual(Result.IMAGINAIRE_SOLUTION, result)

    def test_loiberti_delta_zero(self):
        result = self.get_result_from("1*x^0 + 17*x^1 + 4*x^2 = 13*x^1")
        self.assertEqual(-0.5, result)

    def test_loiberti_float_prob_1(self):
        result = self.get_result_from(
            "0.9 * x^2 = 0.2 * x^1 + 0.1 * x^1 - 0.3 * x^1")
        self.assertEqual(0.0, result)

    def test_loiberti_float_prob_2(self):
        result = self.get_result_from(
            "0.1 * X ^ 0 + 0.2 * X ^ 0 = 0.3 * X ^ 0")
        self.assertEqual(Result.ANY_POSSIBILITY, result)

    def test_loiberti_float_prob_3(self):
        result = self.get_result_from(
            "4*x ^ 2 = 4*x ^ 2 + 1*x ^ 1 - 1*x ^ 1")
        self.assertEqual(Result.ANY_POSSIBILITY, result)

    def test_loiberti_special(self):
        result = self.get_result_from("4*x^2 + 43*x^1 = 4*x^2 + 43*x^1")
        self.assertEqual(Result.ANY_POSSIBILITY, result)

    def test_loiberti_special2(self):
        result = self.get_result_from("5 * X^0 + 0 * X^1 = 4 * X^0")
        self.assertEqual(Result.NO_SOLUTION, result)

    def test_loiberti_special3(self):
        result = self.get_result_from("-0*x^0 = 0")
        self.assertEqual(Result.ANY_POSSIBILITY, result)

    def test_degres_upper(self):
        result = self.get_result_from("3x^3 + 44x^2 = 3x^3")
        self.assertEqual(0, result)

    def test_loiberti_float_prob3(self):
        result = self.get_result_from(
            "0.9 * x^2 = 0.000000000000000000000000000000001 * x^3")
        self.assertEqual(0, result)


class Test2(unittest.TestCase):

    def test_degres_upper2(self):
        parser = Parser("3x^3 + 44x^2 = 4x^3")
        self.assertTrue(parser.is_valid())
        resolver = Resolver(parser.validated_data, no_print=True)
        self.assertFalse(resolver.is_valid())


if __name__ == '__main__':
    unittest.main()
