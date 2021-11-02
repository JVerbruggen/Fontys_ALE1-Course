from proposition import *
from proposition_analysis import *

def test_get_variables():
    assert PropositionAnalysis.get_variables(
        Variable('A')) == ['A']
    assert PropositionAnalysis.get_variables(
        CompoundProposition(Operator.AND, Variable('A'), Variable('B'))) == ['A', 'B']
    assert PropositionAnalysis.get_variables(
        CompoundProposition(Operator.AND, Variable('A'), Variable('A'))) == ['A']
    assert PropositionAnalysis.get_variables(
        SingularProposition(Operator.NOT, 
            CompoundProposition(
                Operator.AND, 
                CompoundProposition(Operator.OR, Variable('A'), Variable('C')), 
                Variable('B')
            ))) == ['B', 'A', 'C']