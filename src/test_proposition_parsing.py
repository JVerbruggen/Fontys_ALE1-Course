from proposition import *
from proposition_parsing import PropositionParser

def test_set_childposition():
    empty_and = AndProposition()
    PropositionParser.set_childproposition(empty_and, "b", Variable("Y"))
    assert empty_and.ascii() == "&(incomplete proposition)"

    empty_or = OrProposition()
    PropositionParser.set_childproposition(empty_or, "a", Variable("X"))
    PropositionParser.set_childproposition(empty_or, "b", Variable("Y"))
    assert empty_or.ascii() == "|(X,Y)"

def test_read():
    prop = PropositionParser("&(A,B)").read()
    assert prop.ascii() == "&(A,B)"

    prop = PropositionParser("   & (    A , B  )  ").read()
    assert prop.ascii() == "&(A,B)"

    prop = PropositionParser("&(|(A,C),B)").read()
    assert prop.ascii() == "&(|(A,C),B)"

    prop = PropositionParser("&(|(A,C),~(=(B,D)))").read()
    assert prop.ascii() == "&(|(A,C),~(=(B,D)))"

    prop = PropositionParser("A").read()
    assert prop.ascii() == "A"