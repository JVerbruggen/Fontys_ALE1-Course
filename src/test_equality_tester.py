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
    assert EqualityTester.test_equal_ascii("~(|(P,Q))", "|(~(P),~(Q))", raise_error=False) == False
    assert EqualityTester.test_equal_ascii("~(&(P,Q))", "&(~(P),~(Q))", raise_error=False) == False

    # cnf equality
    assert EqualityTester.test_equal_ascii("=(P,Q)", "&(|(~(P),Q),|(P,~(Q)))")
    assert EqualityTester.test_equal_ascii("=(&(A,C),B)", "&(|(~(&(A,C)),B),|(&(A,C),~(B)))")

    # Cnf implied equality
    assert EqualityTester.test_cnf("~(P)")
    assert EqualityTester.test_cnf("~(~(P))")
    assert EqualityTester.test_cnf("~(~(~(P)))")
    assert EqualityTester.test_cnf("~(~(~(~(P))))")
    assert EqualityTester.test_cnf("~(&(P,Q))")
    assert EqualityTester.test_cnf("~(|(P,Q))")

    assert EqualityTester.test_cnf("|(P,Q)")
    assert EqualityTester.test_cnf("|(|(P,Q),R)")
    assert EqualityTester.test_cnf("|(|(P,Q),|(R,S))")

    assert EqualityTester.test_cnf(">(P,Q)")
    assert EqualityTester.test_cnf(">(~(P),Q)")
    assert EqualityTester.test_cnf(">(P,~(Q))")
    assert EqualityTester.test_cnf(">(~(P),~(Q))")

    assert EqualityTester.test_cnf("=(P,Q)")
    assert EqualityTester.test_cnf("=(&(A,C),B)")
    assert EqualityTester.test_cnf("=(=(A,C),B)")

    # CNF notation
    assert EqualityTester.test_equal_ascii(
        PropositionCNFFormatParser("[ E , Abc , AdC , BDa , Bca , CDa ]").read().ascii(), 
        PropositionParser("&(E,=(A,|(&(B,C),&(D,~(C)))))").read().cnf().ascii())
    assert EqualityTester.test_equal_ascii(
        PropositionCNFFormatParser("[ Pqr , Qp , Rp ]").read().ascii(), 
        PropositionParser("=(P,&(Q,R))").read().cnf().ascii())
    assert EqualityTester.test_equal_ascii(
        PropositionCNFFormatParser("[ Pq , Pr , QRp ]").read().ascii(), 
        PropositionParser("=(P,|(Q,R))").read().cnf().ascii())



