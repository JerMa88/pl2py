import unittest
from src.internal.syntax import _convert_operators, _convert_print, _convert_oneline_if

class TestSyntaxConversion(unittest.TestCase):
    def test_convert_operators(self):
        self.assertEqual(_convert_operators("if $a eq $b"), "if $a == $b")
        self.assertEqual(_convert_operators("$a =~ /pattern/"), "$a re.match('pattern',")
        self.assertEqual(_convert_operators("$a x $b"), "$a * $b")
        self.assertEqual(_convert_operators("$a && $b"), "$a and $b")

    def test_convert_print(self):
        self.assertEqual(_convert_print("print 'Hello';"), "print(f'Hello');")

    def test_convert_oneline_if(self):
        self.assertEqual(_convert_oneline_if("do_something if condition;"), "if condition: do_something;")
        with self.assertRaises(ValueError):
            _convert_oneline_if("invalid syntax here")