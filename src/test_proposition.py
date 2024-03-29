from proposition import *
from proposition_parsing import *
from truthtable import *
from equality_tester import *

def test_variable():
    assert Variable('A').ascii() == "A"
    assert Variable('ASD').ascii() == "ASD"

def test_compound():
    assert AndProposition(Variable('A'), Variable('B')).ascii() == "&(A,B)"
    assert AndProposition(
            OrProposition(Variable('A'), Variable('C')), 
            Variable('B')
        ).ascii() == "&(|(A,C),B)"

def test_singular():
    assert NotProposition(Variable('A')).ascii() == "~(A)"
    assert NotProposition(
        AndProposition(
            OrProposition(Variable('A'), Variable('C')), 
            Variable('B')
        )).ascii() == "~(&(|(A,C),B))"

def test_extended_or():
    extended = MultiOr([Variable('A'), Variable('B'), AndProposition(Variable('C'), Variable('D'))])
    assert extended.ascii() == "|(A,|(B,&(C,D)))"
    assert extended.infix() == "(A ∨ B ∨ (C ∧ D))"
    assert extended.evaluate({'A': 0, 'B': 0, 'C': 0, 'D': 0}) == False
    assert extended.evaluate({'A': 1, 'B': 0, 'C': 0, 'D': 0}) == True
    assert extended.evaluate({'A': 0, 'B': 1, 'C': 0, 'D': 0}) == True
    assert extended.evaluate({'A': 0, 'B': 0, 'C': 1, 'D': 0}) == False
    assert extended.evaluate({'A': 0, 'B': 0, 'C': 0, 'D': 1}) == False
    assert extended.evaluate({'A': 0, 'B': 0, 'C': 1, 'D': 1}) == True
    assert extended.evaluate({'A': 1, 'B': 1, 'C': 1, 'D': 1}) == True

def test_extended_and():
    extended = MultiAnd([Variable('A'), Variable('B'), AndProposition(Variable('C'), Variable('D'))])
    assert extended.ascii() == "&(A,&(B,&(C,D)))"
    assert extended.infix() == "(A ∧ B ∧ (C ∧ D))"
    assert extended.evaluate({'A': 0, 'B': 0, 'C': 0, 'D': 0}) == False
    assert extended.evaluate({'A': 1, 'B': 0, 'C': 0, 'D': 0}) == False
    assert extended.evaluate({'A': 0, 'B': 1, 'C': 0, 'D': 0}) == False
    assert extended.evaluate({'A': 0, 'B': 0, 'C': 1, 'D': 0}) == False
    assert extended.evaluate({'A': 0, 'B': 0, 'C': 0, 'D': 1}) == False
    assert extended.evaluate({'A': 0, 'B': 0, 'C': 1, 'D': 1}) == False
    assert extended.evaluate({'A': 0, 'B': 1, 'C': 1, 'D': 1}) == False
    assert extended.evaluate({'A': 1, 'B': 1, 'C': 1, 'D': 1}) == True

# def test_generate_proposition():
    # assert type(PropositionFactory.generate_proposition(and_operator)) is CompoundProposition
    # assert type(PropositionFactory.generate_proposition(or_operator)) is CompoundProposition
    # assert type(PropositionFactory.generate_proposition(impl_operator)) is CompoundProposition
    # assert type(PropositionFactory.generate_proposition(biimpl_operator)) is CompoundProposition
    # assert type(PropositionFactory.generate_proposition(not_operator)) is SingularProposition

def test_get_variables():
    assert Variable('A').get_variables() == ['A']
    assert AndProposition(Variable('A'), Variable('B')).get_variables() == ['A', 'B']
    assert AndProposition(Variable('A'), Variable('A')).get_variables() == ['A']
    assert NotProposition(AndProposition(
                OrProposition(Variable('A'), Variable('C')), 
                Variable('B')
            )).get_variables() == ['A', 'B', 'C']

def test_get_variables_extended():
    assert MultiAnd([Variable('A'), Variable('B'), AndProposition(Variable('C'), Variable('D'))]).get_variables() == ['A', 'B', 'C', 'D']
    assert MultiAnd([Variable('A'), Variable('B'), AndProposition(Variable('A'), Variable('D'))]).get_variables() == ['A', 'B', 'D']
    assert MultiAnd([Variable('A'), Variable('A'), AndProposition(Variable('A'), Variable('A'))]).get_variables() == ['A']

def test_cnf():
    assert PropositionParser("~(P)").read().cnf().ascii_complex() == "~(P)"
    assert PropositionParser("~(~(P))").read().cnf().ascii_complex() == "P"
    assert PropositionParser("~(~(~(P)))").read().cnf().ascii_complex() == "~(P)"
    assert PropositionParser("~(~(~(~(P))))").read().cnf().ascii_complex() == "P"
    assert PropositionParser("~(&(P,Q))").read().cnf().ascii_complex() == "*&([*|([~(P),~(Q)])])"
    assert PropositionParser("~(|(P,Q))").read().cnf().ascii_complex() == "*&([~(P),~(Q)])"

    assert PropositionParser("|(P,Q)").read().cnf().ascii_complex() == "*&([*|([P,Q])])"
    assert PropositionParser("|(|(P,Q),R)").read().cnf().ascii_complex() == "*&([*|([P,Q,R])])"
    assert PropositionParser("|(|(P,Q),|(R,S))").read().cnf().ascii_complex() == "*&([*|([P,Q,R,S])])"
    
    assert PropositionParser(">(P,Q)").read().cnf().ascii_complex() == "*&([*|([~(P),Q])])"
    assert PropositionParser(">(~(P),Q)").read().cnf().ascii_complex() == "*&([*|([P,Q])])"
    assert PropositionParser(">(P,~(Q))").read().cnf().ascii_complex() == "*&([*|([~(P),~(Q)])])"
    assert PropositionParser(">(~(P),~(Q))").read().cnf().ascii_complex() == "*&([*|([P,~(Q)])])"

    assert PropositionParser("=(P,Q)").read().cnf().ascii_complex() == "*&([*|([P,~(Q)]),*|([Q,~(P)])])"
    assert PropositionParser("=(&(A,C),B)").read().cnf().ascii_complex() == "*&([*|([A,~(B)]),*|([C,~(B)]),*|([B,~(A),~(C)])])"
    # assert PropositionParser("=(=(A,C),B)").read().cnf().ascii() == ""

    assert PropositionParser("=(&(A,C),B)").read().cnf().cnf_notation() == "[ Ab , Cb , Bac ]"
    assert PropositionParser("=(P,Q)").read().cnf().cnf_notation() == "[ Pq , Qp ]"

    assert PropositionParser("=(P,~(Q))").read().cnf().cnf_notation() == "[ PQ , qp ]"
    assert PropositionParser("=(P,&(Q,R))").read().cnf().cnf_notation() == "[ Pqr , Qp , Rp ]"
    assert PropositionParser("=(P,|(Q,R))").read().cnf().cnf_notation() == "[ Pq , Pr , QRp ]"
    assert PropositionParser("&(E,=(A,|(&(B,C),&(D,~(C)))))").read().cnf().cnf_notation() == "[ E , Abc , AdC , BDa , Bca , CDa ]"


def test_get_literals():
    assert [lit.ascii() for lit in PropositionParser("&(P,~(Q))").read().get_literals()] == ['P', '~(Q)']
    assert [lit.ascii() for lit in PropositionParser("|(~(&(A,C)),B)").read().get_literals()] == ['A', 'C', 'B']

def test_cnf_notation():
    pass

