import unittest
from src.internal.remove_sigils import _remove_final_sigils, _convert_shift, _convert_declarations, _array_hash_init, remove_sigils

class TestRemoveSigil(unittest.TestCase):
    def test_remove_sigils(self):
        self.assertEqual(_remove_final_sigils("$scalar @array %hash &subroutine *typeblob"), "scalar array hash subroutine typeblob")

    def test_no_sigils(self):
        self.assertEqual(_remove_final_sigils("variable"), "variable")

    def test_empty_string(self):
        self.assertEqual(_remove_final_sigils(""), "")

    def test_sigils_with_numbers(self):
        self.assertEqual(_remove_final_sigils("$var123 @arr456 %hash789"), "var123 arr456 hash789")

    def test_sigils_with_underscores(self):
        self.assertEqual(_remove_final_sigils("$var_name @arr_name %hash_name"), "var_name arr_name hash_name")

    def test_invalid_sigil(self):
        self.assertEqual(_remove_final_sigils("^invalid_sigil"), "^invalid_sigil")

    def test_sigils_in_function_call(self):
        self.assertEqual(_remove_final_sigils("$result = $func_name($arg1, $arg2);"), "result = func_name(arg1, arg2);")

    def test_sigils_in_array_access(self):
        self.assertEqual(_remove_final_sigils("$value = $array[0];"), "value = array[0];")
    
    def test_sigils_in_subroutine_call(self):
        self.assertEqual(_remove_final_sigils("&subroutine($arg1, $arg2);"), "subroutine(arg1, arg2);")
    
    def test_declaration_with_shift(self):
        self.assertEqual(_convert_shift("my $var = shift;"), "my $var = args.pop(0);")
    
    def test_declaration_without_shift(self):
        self.assertEqual(_convert_shift("my $var;"), "my $var;")

    def test_sigils_in_local_declaration(self):
        self.assertEqual(_convert_declarations("my $var = shift;"), "var: Any = shift;")

    def test_sigils_in_global_declaration(self):
        self.assertEqual(_convert_declarations("our $global_var = 42;"), "GLOBAL_VAR: Any = 42;")
    
    def test_sigils_in_function_declaration(self):
        self.assertEqual(_convert_declarations("sub $func_name {"), "def func_name(**args): Callable[..., Any] {")

    def test_group_global_declaration(self):
        self.assertEqual(_convert_declarations("our (var1, var2);"), "global var1, var2")
        self.assertEqual(_convert_declarations("our(var1, var2);"), "global var1, var2")
        self.assertEqual(remove_sigils("our (var1, var2);"), "global var1, var2")

    def test_sigils_in_function_declaration_with_shift(self):
        self.assertEqual(_convert_declarations("sub $func_name { my $var = shift; }"), "def func_name(**args): Callable[..., Any] { var: Any = shift; }")
        self.assertEqual(remove_sigils("sub $func_name { my $var = shift; }"), "def func_name(*args): Callable[..., Any] { var: Any = args.pop(0); }")
    
    def test_sigils_in_function_definition_multiple_shifts(self):
        self.assertEqual(remove_sigils("sub $func_name { my $var1 = shift; my $var2 = shift; }"), "def func_name(*args): Callable[..., Any] { var1: Any = args.pop(0); var2: Any = args.pop(0); }")

    def test_sigils_in_array_declaration(self):
        self.assertEqual(_array_hash_init("my @array = (1, 2, 3);"), "array: List[Any] = [1, 2, 3];")
    
    def test_sigils_in_hash_declaration(self):
        self.assertEqual(_array_hash_init("my %hash = ('key' => 'value');"), "hash: Dict[Any, Any] = {'key' : 'value'};")
    
    def test_sigils_in_hash_access(self):
        self.assertEqual(_array_hash_init("$value = $hash{'key'};"), "$value = hash['key'];")
    

if __name__ == "__main__":
    unittest.main()