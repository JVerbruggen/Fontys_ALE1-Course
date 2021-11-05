from proposition import *
from truthtable import *

prop = SingularProposition(Operator.NOT, 
    CompoundProposition(
        Operator.AND, 
        CompoundProposition(Operator.OR, Variable('A'), Variable('C')), 
        Variable('B')
    ))

def test_parse_variables():
    variable_matrix = TruthTable.parse_variables(prop.get_variables())
    assert variable_matrix == [[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1]]

def test_evaluate_proposition():
    variable_matrix = TruthTable.parse_variables(prop.get_variables())
    evaluated_matrix = TruthTable.evaluate_proposition(prop, prop.get_variables(), variable_matrix)
    assert evaluated_matrix == [1,1,1,0,1,1,0,0]

def test_get_truthtable():
    truthtable = TruthTable(prop)
    assert truthtable.matrix == [[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1],[1,1,1,0,1,1,0,0]]
    assert truthtable.get_hash() == "37"
