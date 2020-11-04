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

    def test_division_zero(self):
        resolver = Resolver(**self.to_resolver("x = x"))
        resolver.resolve()
        result = resolver.generate_result()
        self.assertEqual(0, result)


if __name__ == '__main__':
    unittest.main()
