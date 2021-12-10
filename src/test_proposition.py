from proposition import *
from proposition_parsing import *
from truthtable import *
from equality_tester import *

and_operator = OperatorFactory.get_operator('&')
or_operator = OperatorFactory.get_operator('|')
not_operator = OperatorFactory.get_operator('~')
impl_operator = OperatorFactory.get_operator('>')
biimpl_operator = OperatorFactory.get_operator('=')

def test_variable():
    assert Variable('A').ascii() == "A"
    assert Variable('ASD').ascii() == "ASD"

def test_compound():
    assert CompoundProposition(and_operator, Variable('A'), Variable('B')).ascii() == "&(A,B)"
    assert CompoundProposition(
            and_operator, 
            CompoundProposition(or_operator, Variable('A'), Variable('C')), 
            Variable('B')
        ).ascii() == "&(|(A,C),B)"

def test_singular():
    assert SingularProposition(not_operator, Variable('A')).ascii() == "~(A)"
    assert SingularProposition(not_operator, 
        CompoundProposition(
            and_operator, 
            CompoundProposition(or_operator, Variable('A'), Variable('C')), 
            Variable('B')
        )).ascii() == "~(&(|(A,C),B))"

def test_extended_or():
    extended = ExtendedProposition(or_operator, [Variable('A'), Variable('B'), CompoundProposition(and_operator, Variable('C'), Variable('D'))])
    assert extended.ascii() == "|(A,|(B,&(C,D)))"
    assert extended.infix() == "(A ∨ B ∨ (C ∧ D))"
    assert extended.output({'A': 0, 'B': 0, 'C': 0, 'D': 0}) == False
    assert extended.output({'A': 1, 'B': 0, 'C': 0, 'D': 0}) == True
    assert extended.output({'A': 0, 'B': 1, 'C': 0, 'D': 0}) == True
    assert extended.output({'A': 0, 'B': 0, 'C': 1, 'D': 0}) == False
    assert extended.output({'A': 0, 'B': 0, 'C': 0, 'D': 1}) == False
    assert extended.output({'A': 0, 'B': 0, 'C': 1, 'D': 1}) == True
    assert extended.output({'A': 1, 'B': 1, 'C': 1, 'D': 1}) == True

def test_extended_and():
    extended = ExtendedProposition(and_operator, [Variable('A'), Variable('B'), CompoundProposition(and_operator, Variable('C'), Variable('D'))])
    assert extended.ascii() == "&(A,&(B,&(C,D)))"
    assert extended.infix() == "(A ∧ B ∧ (C ∧ D))"
    assert extended.output({'A': 0, 'B': 0, 'C': 0, 'D': 0}) == False
    assert extended.output({'A': 1, 'B': 0, 'C': 0, 'D': 0}) == False
    assert extended.output({'A': 0, 'B': 1, 'C': 0, 'D': 0}) == False
    assert extended.output({'A': 0, 'B': 0, 'C': 1, 'D': 0}) == False
    assert extended.output({'A': 0, 'B': 0, 'C': 0, 'D': 1}) == False
    assert extended.output({'A': 0, 'B': 0, 'C': 1, 'D': 1}) == False
    assert extended.output({'A': 0, 'B': 1, 'C': 1, 'D': 1}) == False
    assert extended.output({'A': 1, 'B': 1, 'C': 1, 'D': 1}) == True

def test_generate_proposition():
    assert type(PropositionFactory.generate_proposition(and_operator)) is CompoundProposition
    assert type(PropositionFactory.generate_proposition(or_operator)) is CompoundProposition
    assert type(PropositionFactory.generate_proposition(impl_operator)) is CompoundProposition
    assert type(PropositionFactory.generate_proposition(biimpl_operator)) is CompoundProposition
    assert type(PropositionFactory.generate_proposition(not_operator)) is SingularProposition

def test_get_variables():
    assert Variable('A').get_variables() == ['A']
    assert CompoundProposition(and_operator, Variable('A'), Variable('B')).get_variables() == ['A', 'B']
    assert CompoundProposition(and_operator, Variable('A'), Variable('A')).get_variables() == ['A']
    assert SingularProposition(not_operator, 
            CompoundProposition(
                and_operator, 
                CompoundProposition(or_operator, Variable('A'), Variable('C')), 
                Variable('B')
            )).get_variables() == ['A', 'B', 'C']

def test_get_variables_extended():
    assert ExtendedProposition(and_operator, [Variable('A'), Variable('B'), CompoundProposition(and_operator, Variable('C'), Variable('D'))]).get_variables() == ['A', 'B', 'C', 'D']
    assert ExtendedProposition(and_operator, [Variable('A'), Variable('B'), CompoundProposition(and_operator, Variable('A'), Variable('D'))]).get_variables() == ['A', 'B', 'D']
    assert ExtendedProposition(and_operator, [Variable('A'), Variable('A'), CompoundProposition(and_operator, Variable('A'), Variable('A'))]).get_variables() == ['A']

def test_cnf():
    assert PropositionParser("~(P)").read().cnf().ascii() == "~(P)"
    assert PropositionParser("~(~(P))").read().cnf().ascii() == "P"
    assert PropositionParser("~(~(~(P)))").read().cnf().ascii() == "~(P)"
    assert PropositionParser("~(~(~(~(P))))").read().cnf().ascii() == "P"
    assert PropositionParser("~(&(P,Q))").read().cnf().ascii() == "|(~(P),~(Q))"
    assert PropositionParser("~(|(P,Q))").read().cnf().ascii() == "&(~(P),~(Q))"

    assert PropositionParser("|(P,Q)").read().cnf().ascii() == "|(P,Q)"
    assert PropositionParser("|(|(P,Q),R)").read().cnf().ascii() == "&(|(P,R),|(Q,R))"
    assert PropositionParser("|(|(P,Q),|(R,S))").read().cnf().ascii() == "&(|(P,R),&(|(P,S),&(|(Q,R),|(Q,S))))"
    
    assert PropositionParser(">(P,Q)").read().cnf().ascii() == "|(~(P),Q)"
    assert PropositionParser(">(~(P),Q)").read().cnf().ascii() == "|(P,Q)"
    assert PropositionParser(">(P,~(Q))").read().cnf().ascii() == "|(~(P),~(Q))"
    assert PropositionParser(">(~(P),~(Q))").read().cnf().ascii() == "|(P,~(Q))"

    assert PropositionParser("=(P,Q)").read().cnf().ascii() == "&(|(P,~(P)),&(|(P,~(Q)),&(|(Q,~(P)),|(Q,~(Q)))))"
    assert EqualityTester.test_equal_ascii("=(P,Q)", "&(|(P,~(P)),&(|(P,~(Q)),&(|(Q,~(P)),|(Q,~(Q)))))")

