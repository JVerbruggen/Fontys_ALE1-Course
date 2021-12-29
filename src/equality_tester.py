from proposition import *
from truthtable import *
from proposition_parsing import *

class EqualityTester:

    def test_cnf(ascii: str, raise_error=True):
        prop_one = PropositionParser(ascii).read()
        prop_cnf = prop_one.cnf()

        return EqualityTester.test_equal(prop_one, prop_cnf, raise_error=raise_error)

    def test_equal_ascii(ascii_one: str, ascii_other: str, raise_error=True) -> bool:
        prop_one = PropositionParser(ascii_one).read()
        prop_other = PropositionParser(ascii_other).read()

        return EqualityTester.test_equal(prop_one, prop_other, raise_error=raise_error)

    def test_equal(one: Proposition, other: Proposition, raise_error=True) -> bool:
        tt_one = TruthTable(one)
        tt_other = TruthTable(other)
        
        binary_string_equal = tt_one.get_binary_string() == tt_other.get_binary_string()
        hash_equal = tt_one.get_hash() == tt_other.get_hash()

        res = binary_string_equal and hash_equal

        if res == False and raise_error:
            raise ValueError(f"Equality test failed: {one} and {other} are not equal\n"
            + f"bin_string: {tt_one.get_binary_string()} vs {tt_other.get_binary_string()}\n"
            + f"hash: {tt_one.get_hash()} vs {tt_other.get_hash()}")

        return res
