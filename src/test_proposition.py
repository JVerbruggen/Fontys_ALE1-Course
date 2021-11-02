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

def test_generate_proposition():
    assert type(Operator.generate_proposition(Operator.AND)) is CompoundProposition
    assert type(Operator.generate_proposition(Operator.OR)) is CompoundProposition
    assert type(Operator.generate_proposition(Operator.IMPL)) is CompoundProposition
    assert type(Operator.generate_proposition(Operator.BIIMPL)) is CompoundProposition
    assert type(Operator.generate_proposition(Operator.NOT)) is SingularProposition