import pytest
from proposition_operator import *

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
    assert AndOperator().evaluate(True, True) == True
    assert AndOperator().evaluate(False, True) == False
    assert AndOperator().evaluate(True, False) == False
    assert AndOperator().evaluate(False, False) == False

def test_or_operator():
    assert OrOperator().evaluate(True, True) == True
    assert OrOperator().evaluate(False, True) == True
    assert OrOperator().evaluate(True, False) == True
    assert OrOperator().evaluate(False, False) == False

def test_impl_operator():
    assert ImplicationOperator().evaluate(True, True) == True
    assert ImplicationOperator().evaluate(False, True) == True
    assert ImplicationOperator().evaluate(True, False) == False
    assert ImplicationOperator().evaluate(False, False) == True

def test_biimpl_operator():
    assert BiimplicationOperator().evaluate(True, True) == True
    assert BiimplicationOperator().evaluate(False, True) == False
    assert BiimplicationOperator().evaluate(True, False) == False
    assert BiimplicationOperator().evaluate(False, False) == True

def test_not_operator():
    assert NotOperator().evaluate(True, True) == False
    assert NotOperator().evaluate(False, True) == True
    assert NotOperator().evaluate(True, False) == False
    assert NotOperator().evaluate(False, False) == True

def test_extended_evaluation_not_operator():
    with pytest.raises(NotImplementedError):
        NotOperator().evaluate_extended([0,0,1])

def test_extended_evaluation():
    assert AndOperator().evaluate_extended([1,1,1]) == 1
    assert AndOperator().evaluate_extended([1,1,0]) == 0
    assert AndOperator().evaluate_extended([0,0,0]) == 0
    assert AndOperator().evaluate_extended([1,0]) == 0
    assert AndOperator().evaluate_extended([1]) == 1
    assert AndOperator().evaluate_extended([]) == 0

def test_ascii():
    assert AndOperator().ascii() == '&'
    assert OrOperator().ascii() == '|'
    assert ImplicationOperator().ascii() == '>'
    assert BiimplicationOperator().ascii() == '='
    assert NotOperator().ascii() == '~'

def test_infix():
    assert AndOperator().infix() == '∧'
    assert OrOperator().infix() == '∨'
    assert ImplicationOperator().infix() == '=>'
    assert BiimplicationOperator().infix() == '<=>'
    assert NotOperator().infix() == '¬'