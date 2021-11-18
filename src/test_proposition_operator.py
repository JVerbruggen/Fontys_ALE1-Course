import pytest
from proposition_operator import *

and_operator = OperatorFactory.get_operator('&')
or_operator = OperatorFactory.get_operator('|')
impl_operator = OperatorFactory.get_operator('>')
biimpl_operator = OperatorFactory.get_operator('=')
not_operator = OperatorFactory.get_operator('~')

def test_abstract_operator():
    with pytest.raises(NotImplementedError):
        Operator().ascii()
    with pytest.raises(NotImplementedError):
        Operator().infix()
    with pytest.raises(NotImplementedError):
        Operator().is_compound()
    with pytest.raises(NotImplementedError):
        Operator().evaluate(True, False)

def test_is_operator():
    assert OperatorFactory.is_operator('&') == True
    assert OperatorFactory.is_operator('|') == True
    assert OperatorFactory.is_operator('>') == True
    assert OperatorFactory.is_operator('=') == True
    assert OperatorFactory.is_operator('~') == True
    assert OperatorFactory.is_operator('%') == False
    assert OperatorFactory.is_operator('(') == False
    assert OperatorFactory.is_operator(',') == False
    assert OperatorFactory.is_operator(')') == False
    assert OperatorFactory.is_operator('*') == False
    assert OperatorFactory.is_operator('/') == False
    assert OperatorFactory.is_operator('A') == False
    assert OperatorFactory.is_operator('B') == False

def test_get_operator():
    assert type(OperatorFactory.get_operator('&')) == AndOperator
    assert type(OperatorFactory.get_operator('|')) == OrOperator
    assert type(OperatorFactory.get_operator('>')) == ImplicationOperator
    assert type(OperatorFactory.get_operator('=')) == BiimplicationOperator
    assert type(OperatorFactory.get_operator('~')) == NotOperator

def test_get_operator_by_type():
    assert type(OperatorFactory.get_operator_by_type(AndOperator)) == AndOperator
    assert type(OperatorFactory.get_operator_by_type(OrOperator)) == OrOperator
    assert type(OperatorFactory.get_operator_by_type(ImplicationOperator)) == ImplicationOperator
    assert type(OperatorFactory.get_operator_by_type(BiimplicationOperator)) == BiimplicationOperator
    assert type(OperatorFactory.get_operator_by_type(NotOperator)) == NotOperator

def test_and_operator():
    assert and_operator.evaluate(True, True) == True
    assert and_operator.evaluate(False, True) == False
    assert and_operator.evaluate(True, False) == False
    assert and_operator.evaluate(False, False) == False

def test_or_operator():
    assert or_operator.evaluate(True, True) == True
    assert or_operator.evaluate(False, True) == True
    assert or_operator.evaluate(True, False) == True
    assert or_operator.evaluate(False, False) == False

def test_impl_operator():
    assert impl_operator.evaluate(True, True) == True
    assert impl_operator.evaluate(False, True) == True
    assert impl_operator.evaluate(True, False) == False
    assert impl_operator.evaluate(False, False) == True

def test_biimpl_operator():
    assert biimpl_operator.evaluate(True, True) == True
    assert biimpl_operator.evaluate(False, True) == False
    assert biimpl_operator.evaluate(True, False) == False
    assert biimpl_operator.evaluate(False, False) == True

def test_not_operator():
    assert not_operator.evaluate(True, True) == False
    assert not_operator.evaluate(False, True) == True
    assert not_operator.evaluate(True, False) == False
    assert not_operator.evaluate(False, False) == True

def test_extended_evaluation_error():
    with pytest.raises(NotImplementedError):
        not_operator.evaluate_extended([0,0,1])
    with pytest.raises(NotImplementedError):
        impl_operator.evaluate_extended([0,0,1])
    with pytest.raises(NotImplementedError):
        biimpl_operator.evaluate_extended([0,0,1])

def test_extended_evaluation():
    assert and_operator.evaluate_extended([1,1,1]) == 1
    assert and_operator.evaluate_extended([1,1,0]) == 0
    assert and_operator.evaluate_extended([0,0,0]) == 0
    assert and_operator.evaluate_extended([1,0]) == 0
    assert and_operator.evaluate_extended([1]) == 1
    assert and_operator.evaluate_extended([]) == 0

    assert or_operator.evaluate_extended([1,1,1]) == 1
    assert or_operator.evaluate_extended([1,1,0]) == 1
    assert or_operator.evaluate_extended([0,0,0]) == 0
    assert or_operator.evaluate_extended([1,0]) == 1
    assert or_operator.evaluate_extended([1]) == 1
    assert or_operator.evaluate_extended([]) == 0

def test_ascii():
    assert and_operator.ascii() == '&'
    assert or_operator.ascii() == '|'
    assert impl_operator.ascii() == '>'
    assert biimpl_operator.ascii() == '='
    assert not_operator.ascii() == '~'

def test_infix():
    assert and_operator.infix() == '∧'
    assert or_operator.infix() == '∨'
    assert impl_operator.infix() == '=>'
    assert biimpl_operator.infix() == '<=>'
    assert not_operator.infix() == '¬'