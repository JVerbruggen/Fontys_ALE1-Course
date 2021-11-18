from proposition import *

def test_operator_ascii():
    assert Operator.NOT.ascii() == "~"
    assert Operator.AND.ascii() == "&"

def test_operator_isoperator():
    assert Operator.is_operator('~') == True
    assert Operator.is_operator('&') == True
    assert Operator.is_operator('>') == True
    assert Operator.is_operator('s') == False

def test_operator_getoperator():
    assert Operator.get_operator('~') == Operator.NOT
    assert Operator.get_operator('|') == Operator.OR
    assert Operator.get_operator('=') == Operator.BIIMPL
    assert Operator.get_operator('s') == None

def test_variable():
    assert Variable('A').ascii() == "A"
    assert Variable('ASD').ascii() == "ASD"

def test_compound():
    assert CompoundProposition(Operator.AND, Variable('A'), Variable('B')).ascii() == "&(A,B)"
    assert CompoundProposition(
            Operator.AND, 
            CompoundProposition(Operator.OR, Variable('A'), Variable('C')), 
            Variable('B')
        ).ascii() == "&(|(A,C),B)"

def test_singular():
    assert SingularProposition(Operator.NOT, Variable('A')).ascii() == "~(A)"
    assert SingularProposition(Operator.NOT, 
        CompoundProposition(
            Operator.AND, 
            CompoundProposition(Operator.OR, Variable('A'), Variable('C')), 
            Variable('B')
        )).ascii() == "~(&(|(A,C),B))"

def test_extended_or():
    extended = ExtendedProposition(Operator.OR, [Variable('A'), Variable('B'), CompoundProposition(Operator.AND, Variable('C'), Variable('D'))])
    assert extended.ascii() == "|(A,B,&(C,D))"
    assert extended.infix() == "(A ∨ B ∨ (C ∧ D))"
    assert extended.output({'A': 0, 'B': 0, 'C': 0, 'D': 0}) == False
    assert extended.output({'A': 1, 'B': 0, 'C': 0, 'D': 0}) == True
    assert extended.output({'A': 0, 'B': 1, 'C': 0, 'D': 0}) == True
    assert extended.output({'A': 0, 'B': 0, 'C': 1, 'D': 0}) == False
    assert extended.output({'A': 0, 'B': 0, 'C': 0, 'D': 1}) == False
    assert extended.output({'A': 0, 'B': 0, 'C': 1, 'D': 1}) == True
    assert extended.output({'A': 1, 'B': 1, 'C': 1, 'D': 1}) == True

def test_extended_and():
    extended = ExtendedProposition(Operator.AND, [Variable('A'), Variable('B'), CompoundProposition(Operator.AND, Variable('C'), Variable('D'))])
    assert extended.ascii() == "&(A,B,&(C,D))"
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
    assert type(Operator.generate_proposition(Operator.AND)) is CompoundProposition
    assert type(Operator.generate_proposition(Operator.OR)) is CompoundProposition
    assert type(Operator.generate_proposition(Operator.IMPL)) is CompoundProposition
    assert type(Operator.generate_proposition(Operator.BIIMPL)) is CompoundProposition
    assert type(Operator.generate_proposition(Operator.NOT)) is SingularProposition

def test_get_variables():
    assert Variable('A').get_variables() == ['A']
    assert CompoundProposition(Operator.AND, Variable('A'), Variable('B')).get_variables() == ['A', 'B']
    assert CompoundProposition(Operator.AND, Variable('A'), Variable('A')).get_variables() == ['A']
    assert SingularProposition(Operator.NOT, 
            CompoundProposition(
                Operator.AND, 
                CompoundProposition(Operator.OR, Variable('A'), Variable('C')), 
                Variable('B')
            )).get_variables() == ['A', 'B', 'C']

def test_get_variables_extended():
    assert ExtendedProposition(Operator.AND, [Variable('A'), Variable('B'), CompoundProposition(Operator.AND, Variable('C'), Variable('D'))]).get_variables() == ['A', 'B', 'C', 'D']
    assert ExtendedProposition(Operator.AND, [Variable('A'), Variable('B'), CompoundProposition(Operator.AND, Variable('A'), Variable('D'))]).get_variables() == ['A', 'B', 'D']
    assert ExtendedProposition(Operator.AND, [Variable('A'), Variable('A'), CompoundProposition(Operator.AND, Variable('A'), Variable('A'))]).get_variables() == ['A']