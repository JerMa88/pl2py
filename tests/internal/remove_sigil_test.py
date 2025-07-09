import unittest
from src.internal.remove_sigil import remove_sigils

class TestRemoveSigil(unittest.TestCase):
    def test_remove_scalar_sigil(self):
        self.assertEqual(remove_sigils("$variable"), "variable")

    def test_remove_array_sigil(self):
        self.assertEqual(remove_sigils("@array"), "array")

    def test_remove_hash_sigil(self):
        self.assertEqual(remove_sigils("%hash"), "hash")

    def test_remove_ampersand_sigil(self):
        self.assertEqual(remove_sigils("&subroutine"), "subroutine")

    def test_remove_asterisk_sigil(self):
        self.assertEqual(remove_sigils("*glob"), "glob")

    def test_mixed_sigils(self):
        self.assertEqual(remove_sigils("$var1 @var2 %var3 &var4 *var5"), "var1 var2 var3 var4 var5")

    def test_no_sigils(self):
        self.assertEqual(remove_sigils("variable"), "variable")

    def test_empty_string(self):
        self.assertEqual(remove_sigils(""), "")

    def test_multiple_variables(self):
        self.assertEqual(remove_sigils("$var1 $var2 @array %hash"), "var1 var2 array hash")

    def test_sigils_with_numbers(self):
        self.assertEqual(remove_sigils("$var123 @arr456 %hash789"), "var123 arr456 hash789")

    def test_sigils_with_underscores(self):
        self.assertEqual(remove_sigils("$var_name @arr_name %hash_name"), "var_name arr_name hash_name")

    def test_declaration_with_shift(self):
        self.assertEqual(remove_sigils("my $var = shift;"), "var: Any = args.pop(0);")
    
    def test_sigils_in_function_declaration(self):
        self.assertEqual(remove_sigils("sub $func_name {"), "def func_name: Callable[..., Any] {")

    def test_sigils_in_function_declaration_with_shift(self):
        self.assertEqual(remove_sigils("sub $func_name { my $var = shift; }"), "def func_name: Callable[..., Any] { var: Any = args.pop(0); }")
    
    def test_sigils_in_function_definition_multiple_shifts(self):
        self.assertEqual(remove_sigils("sub $func_name { my $var1 = shift; my $var2 = shift; }"), "def func_name: Callable[..., Any] { var1: Any = args.pop(0); var2: Any = args.pop(0); }")

    def test_sigils_in_global_declaration(self):
        self.assertEqual(remove_sigils("our $global_var = 42;"), "GLOBAL_VAR: Any = 42;")
    
    def test_sigils_in_local_declaration(self):
        self.assertEqual(remove_sigils("my $local_var = 'hello';"), "local_var: Any = 'hello';")
    
    def test_sigils_in_array_declaration(self):
        self.assertEqual(remove_sigils("my @array = (1, 2, 3);"), "array: List[Any] = [1, 2, 3];")
    
    def test_sigils_in_hash_declaration(self):
        self.assertEqual(remove_sigils("my %hash = ('key' => 'value');"), "hash: Dict[Any, Any] = {'key' : 'value'};")

    def test_sigils_in_function_call(self):
        self.assertEqual(remove_sigils("$result = $func_name($arg1, $arg2);"), "result = func_name(arg1, arg2);")

    def test_sigils_in_array_access(self):
        self.assertEqual(remove_sigils("$value = $array[0];"), "value = array[0];")
    
    def test_sigils_in_hash_access(self):
        self.assertEqual(remove_sigils("$value = $hash{'key'};"), "value = hash['key'];")
    
    def test_sigils_in_subroutine_call(self):
        self.assertEqual(remove_sigils("&subroutine($arg1, $arg2);"), "subroutine(arg1, arg2);")
    
    def test_invalid_sigil(self):
        self.assertEqual(remove_sigils("^invalid_sigil"), "^invalid_sigil")
    
if __name__ == "__main__":
    unittest.main()