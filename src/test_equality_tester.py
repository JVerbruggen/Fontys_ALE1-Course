from equality_tester import *

def test_equality_tester():
    # Identical propositions
    assert EqualityTester.test_equal_ascii("=(A,B)", "=(A,B)")
    assert EqualityTester.test_equal_ascii(">(A,B)", ">(A,B)")
    assert EqualityTester.test_equal_ascii("&(A,B)", "&(A,B)")
    assert EqualityTester.test_equal_ascii("|(A,B)", "|(A,B)")
    assert EqualityTester.test_equal_ascii("~(A)", "~(A)")
    assert EqualityTester.test_equal_ascii("&(|(P,R),|(Q,R))", "&(|(P,R),|(Q,R))")

    # demorgan
    assert EqualityTester.test_equal_ascii("~(&(P,Q))", "|(~(P),~(Q))")
    assert EqualityTester.test_equal_ascii("~(|(P,Q))", "&(~(P),~(Q))")

    # false check
    assert EqualityTester.test_equal_ascii("~(|(P,Q))", "|(~(P),~(Q))") == False
    assert EqualityTester.test_equal_ascii("~(&(P,Q))", "&(~(P),~(Q))") == False
