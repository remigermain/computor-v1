from src.parser import Parser
import unittest


class Test(unittest.TestCase):

    def assertParseEqual(self, l1, l2):
        for el1, el2 in zip(l1, l2):
            if el1.is_operande:
                self.assertEqual(el1.value, el2['value'])
            else:
                self.assertEqual(el1.num, el2['num'])
                self.assertEqual(el1.degres, el2['degres'])

    def test_maj_indefinite(self):
        parser = Parser("1x^1 = 1X^1")
        self.assertTrue(parser.is_valid())

    def test_maj_indefinite2(self):
        parser = Parser("1X^1 = 1X^1")
        self.assertTrue(parser.is_valid())

    def test_maj_indefinite3(self):
        parser = Parser("1O^1 = 1O^1", indefinite="O")
        self.assertTrue(parser.is_valid())

    def test_maj_indefinite4(self):
        parser = Parser("1o^1 = 1o^1", indefinite="O")
        self.assertTrue(parser.is_valid())

    def test_only_num(self):
        parser = Parser("5 + 5 - -5 = 55 + 48")
        self.assertTrue(parser.is_valid())
        vd_b, vd_a = parser.validated_data
        self.assertParseEqual(vd_b, [
            {'num': 5, 'degres': 0},
            {'value': '+'},
            {'num': 5, 'degres': 0},
            {'value': '-'},
            {'num': -5, 'degres': 0},
        ])
        self.assertParseEqual(vd_a, [
            {'num': 55, 'degres': 0},
            {'value': '+'},
            {'num': 48, 'degres': 0},
        ])

    def test_only_exposant(self):
        parser = Parser("X + X - X = X + X")
        parser.is_valid()
        self.assertTrue(parser.is_valid())
        vd_b, vd_a = parser.validated_data
        self.assertParseEqual(vd_b, [
            {'num': 1, 'degres': 1},
            {'value': '+'},
            {'num': 1, 'degres': 1},
            {'value': '-'},
            {'num': 1, 'degres': 1},
        ])
        self.assertParseEqual(vd_a, [
            {'num': 1, 'degres': 1},
            {'value': '+'},
            {'num': 1, 'degres': 1},
        ])

    def test_only_num_with_exposant(self):
        parser = Parser("1X + 5X - -9X = 48X + -18X")
        self.assertTrue(parser.is_valid())
        vd_b, vd_a = parser.validated_data
        self.assertParseEqual(vd_b, [
            {'num': 1, 'degres': 1},
            {'value': '+'},
            {'num': 5, 'degres': 1},
            {'value': '-'},
            {'num': -9, 'degres': 1},
        ])
        self.assertParseEqual(vd_a, [
            {'num': 48, 'degres': 1},
            {'value': '+'},
            {'num': -18, 'degres': 1},
        ])

    def test_only_num_with_exposant_with_num(self):
        parser = Parser("1X^1 + 5X ^  1 - -9X ^ 0 = 48X ^2 + -18X ^  2")
        self.assertTrue(parser.is_valid())
        vd_b, vd_a = parser.validated_data
        self.assertParseEqual(vd_b, [
            {'num': 1, 'degres': 1},
            {'value': '+'},
            {'num': 5, 'degres': 1},
            {'value': '-'},
            {'num': -9, 'degres': 0},
        ])
        self.assertParseEqual(vd_a, [
            {'num': 48, 'degres': 2},
            {'value': '+'},
            {'num': -18, 'degres': 2},
        ])

    def test_only_exposant_with_num(self):
        parser = Parser("X^1 + X ^  1 - X ^ 0 = X ^2 + X ^  2")
        self.assertTrue(parser.is_valid())
        vd_b, vd_a = parser.validated_data
        self.assertParseEqual(vd_b, [
            {'num': 1, 'degres': 1},
            {'value': '+'},
            {'num': 1, 'degres': 1},
            {'value': '-'},
            {'num': 1, 'degres': 0},
        ])
        self.assertParseEqual(vd_a, [
            {'num': 1, 'degres': 2},
            {'value': '+'},
            {'num': 1, 'degres': 2},
        ])

    def test_only_num_with_exposant_with_num_with_multiple(self):
        parser = Parser(
            "1 * X^1 + 5 * X ^  1 - -9 * X ^ 0 = 48 * X ^2 + -18X ^  2")
        self.assertTrue(parser.is_valid())
        vd_b, vd_a = parser.validated_data
        self.assertParseEqual(vd_b, [
            {'num': 1, 'degres': 1},
            {'value': '+'},
            {'num': 5, 'degres': 1},
            {'value': '-'},
            {'num': -9, 'degres': 0},
        ])
        self.assertParseEqual(vd_a, [
            {'num': 48, 'degres': 2},
            {'value': '+'},
            {'num': -18, 'degres': 2},
        ])

    def test_only_num_with_exposant_with_num_with_multiple2(self):
        parser = Parser(
            "1 * X^1 + 5 * X ^  1 - -9 * X ^ 0  - 1 * X^1 + 5 * X ^  1 - -9 * X ^ 0 = 1 * X^1 + 5 * X ^  1 - -9 * X ^ 0 + 48 * X ^2 + -18X ^  2")
        self.assertTrue(parser.is_valid())
        vd_b, vd_a = parser.validated_data
        self.assertParseEqual(vd_b, [
            {'num': 1, 'degres': 1},
            {'value': '+'},
            {'num': 5, 'degres': 1},
            {'value': '-'},
            {'num': -9, 'degres': 0},
            {'value': '-'},
            {'num': 1, 'degres': 1},
            {'value': '+'},
            {'num': 5, 'degres': 1},
            {'value': '-'},
            {'num': -9, 'degres': 0},
        ])
        self.assertParseEqual(vd_a, [
            {'num': 1, 'degres': 1},
            {'value': '+'},
            {'num': 5, 'degres': 1},
            {'value': '-'},
            {'num': -9, 'degres': 0},
            {'value': '+'},
            {'num': 48, 'degres': 2},
            {'value': '+'},
            {'num': -18, 'degres': 2},
        ])

    def test_wrong(self):
        parser = Parser("1 * = 1")
        self.assertFalse(parser.is_valid())

    def test_wrong2(self):
        parser = Parser("1 / = 1")
        self.assertFalse(parser.is_valid())

    def test_wrong3(self):
        parser = Parser("1  = X 1")
        self.assertFalse(parser.is_valid())

    def test_wrong4(self):
        parser = Parser("1  =")
        self.assertFalse(parser.is_valid())

    def test_wrong5(self):
        parser = Parser("1  =")
        self.assertFalse(parser.is_valid())

    def test_wrong6(self):
        parser = Parser("= 1")
        self.assertFalse(parser.is_valid())

    def test_wrong7(self):
        parser = Parser("=")
        self.assertFalse(parser.is_valid())

    def test_wrong8(self):
        parser = Parser("X = -9=")
        self.assertFalse(parser.is_valid())

    def test_negative_number(self):
        parser = Parser("1= -9X")
        self.assertTrue(parser.is_valid())

    def test_float(self):
        parser = Parser("5.6 * X^2 = -9X")
        self.assertTrue(parser.is_valid())
        vd_b, vd_a = parser.validated_data
        self.assertParseEqual(vd_b, [{'num': 5.6, 'degres': 2}])
        self.assertParseEqual(vd_a, [{'num': -9.0, 'degres': 1}])

    def test_multiple_equal(self):
        parser = Parser("1x^1 =1x^1 1x^1")
        self.assertFalse(parser.is_valid())

    def test_no_equal(self):
        parser = Parser("1x^1 1x^1 1x^1 ")
        self.assertFalse(parser.is_valid())


if __name__ == '__main__':
    unittest.main()
