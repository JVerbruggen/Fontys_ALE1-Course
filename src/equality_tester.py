from proposition import *
from truthtable import *
from proposition_parsing import *

class EqualityTester:

    def test_cnf(ascii: str):
        prop_one = PropositionParser(ascii).read()
        prop_cnf = prop_one.cnf()

        return EqualityTester.test_equal(prop_one, prop_cnf)

    def test_equal_ascii(ascii_one: str, ascii_other: str) -> bool:
        prop_one = PropositionParser(ascii_one).read()
        prop_other = PropositionParser(ascii_other).read()

        return EqualityTester.test_equal(prop_one, prop_other)

    def test_equal(one: Proposition, other: Proposition) -> bool:
        tt_one = TruthTable(one)
        tt_other = TruthTable(other)
        
        binary_string_equal = tt_one.get_binary_string() == tt_other.get_binary_string()
        hash_equal = tt_one.get_hash() == tt_other.get_hash()

        return binary_string_equal and hash_equal
