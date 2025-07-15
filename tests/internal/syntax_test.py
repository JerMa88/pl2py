import unittest
from src.internal.syntax import _convert_operators, _convert_print, _convert_oneline_if, _delete_semicolon

class TestSyntaxConversion(unittest.TestCase):
    def test_convert_operators(self):
        assert _convert_operators(' $a eq $b ') == ' $a == $b '
        assert _convert_operators(' $a ne $b ') == ' $a != $b '
        assert _convert_operators(' $a lt $b ') == ' $a < $b '
        assert _convert_operators(' $a gt $b ') == ' $a > $b '
        assert _convert_operators(' $a le $b ') == ' $a <= $b '
        assert _convert_operators(' $a ge $b ') == ' $a >= $b '

        # Regex matching
        assert _convert_operators('$a =~ /abc/') == '$a = re.match(r"abc", $a)'
        assert _convert_operators('$a !~ /abc/') == '$a = re.search(r"abc", $a)'

        # String repetition and concatenation
        assert _convert_operators(' "a" x 3 ') == ' "a" * 3 '
        assert _convert_operators(' "a" . "b" ') == ' "a" + "b" '

        # Logical operators
        assert _convert_operators(' $a && $b ') == ' $aand$b '
        assert _convert_operators(' $a || $b ') == ' $aor$b '
        assert _convert_operators(' ! $a ') == ' not $a '

        # Compound assignment operators
        assert _convert_operators(' $a ||= $b ') == ' $a |= $b '
        assert _convert_operators(' $a &&= $b ') == ' $a &= $b '
        assert _convert_operators(' $a .+= $b ') == ' $a += $b '

        # Loop controls
        assert _convert_operators('last') == 'break'
        assert _convert_operators('next') == 'continue'
        assert _convert_operators('redo') == 'pass'

        # File operations
        assert _convert_operators('open("file.txt", "r")') == 'open(file.txt, "r")'
        assert _convert_operators('close("file.txt")') == 'file.txt.close()'

        # Error handling
        assert _convert_operators('die "something went wrong";') == 'raise Exception("something went wrong")'
        assert _convert_operators('die "error"') == 'raise Exception("error")'

        # Warnings
        assert _convert_operators('warn "be careful";') == 'warnings.warn("be careful")'
        assert _convert_operators('warn "oops"') == 'warnings.warn("oops")'

        # System command
        assert _convert_operators('system("ls -la")') == 'os.system("ls -la")'

    def test_convert_print(self):
        self.assertEqual(_convert_print("print 'Hello';"), "print(f'Hello');")
        self.assertEqual(_convert_print("printf 'Hello';"), "printf 'Hello';")

    def test_convert_oneline_if(self):
        self.assertEqual(_convert_oneline_if("do_something if condition;"), "if condition: do_something;")
        self.assertEqual(_convert_oneline_if("do_something if (condition);"), "if (condition): do_something;")

    def test_remove_semicolon(self):
        self.assertEqual(_delete_semicolon("print 'Hello';"), "print 'Hello'")
        self.assertEqual(_delete_semicolon("my $var = 5; print $var;"), "my $var = 5\nprint $var")