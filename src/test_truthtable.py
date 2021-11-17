from proposition import *
from truthtable import *

def test_parse_variables():
    prop = SingularProposition(Operator.NOT, 
    CompoundProposition(
        Operator.AND, 
        CompoundProposition(Operator.OR, Variable('A'), Variable('C')), 
        Variable('B')
    ))

    variable_matrix = TruthTable.parse_variables(prop.get_variables())
    assert variable_matrix == [[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1]]

def test_evaluate_proposition():
    prop = SingularProposition(Operator.NOT, 
    CompoundProposition(
        Operator.AND, 
        CompoundProposition(Operator.OR, Variable('A'), Variable('C')), 
        Variable('B')
    ))

    variable_matrix = TruthTable.parse_variables(prop.get_variables())
    evaluated_matrix = TruthTable.evaluate_proposition(prop, prop.get_variables(), variable_matrix)
    assert evaluated_matrix == [1,1,1,0,1,1,0,0]

def test_get_truthtable():
    prop = SingularProposition(Operator.NOT, 
    CompoundProposition(
        Operator.AND, 
        CompoundProposition(Operator.OR, Variable('A'), Variable('C')), 
        Variable('B')
    ))

    truthtable = TruthTable(prop)
    assert truthtable.matrix == [[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1],[1,1,1,0,1,1,0,0]]
    assert truthtable.get_binary_string() == "00110111"
    assert truthtable.get_hash() == "37"

def test_predefined_truthtable():
    prop = CompoundProposition(Operator.AND,
        CompoundProposition(Operator.OR, Variable('A'), SingularProposition(Operator.NOT, Variable('B'))),
        Variable('C')
    )

    truthtable = TruthTable(prop)
    assert truthtable.matrix == [[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1],[0,1,0,0,0,1,0,1]]
    assert truthtable.get_binary_string() == "10100010"
    assert truthtable.get_hash() == "A2"

# Simplifying
prop = CompoundProposition(Operator.OR,
    CompoundProposition(Operator.OR, Variable('A'), Variable('B')),
    Variable('C')
)

def test_simplification_results_similar():
    truthtable = TruthTable(prop)
    result_row = truthtable.matrix[-1]
    
    assert truthtable._results_similar(result_row, 0, truthtable.matrix[0]) == []
    assert truthtable._results_similar(result_row, 1, truthtable.matrix[0]) == [4,5,6,7]

    assert truthtable._results_similar(result_row, 0, truthtable.matrix[1]) == []
    assert truthtable._results_similar(result_row, 1, truthtable.matrix[1]) == [2,3,6,7]

    assert truthtable._results_similar(result_row, 0, truthtable.matrix[2]) == []
    assert truthtable._results_similar(result_row, 1, truthtable.matrix[2]) == [1,3,5,7]

def test_simplification_results_similar_withflow():
    truthtable = TruthTable(prop)
    result_row = truthtable.matrix[-1]

    similar = truthtable._results_similar(result_row, 1, truthtable.matrix[2])
    assert similar == [1,3,5,7]
    (inserting, del_indices) = truthtable._get_replacement_preparation(similar, 2, len(truthtable.matrix), 1)

    truthtable._matrix_remove_row(del_indices)
    truthtable._matrix_insert_row(len(truthtable.matrix), inserting)
    assert truthtable.matrix == [[0,0,1,1,-1],[0,1,0,1,-1],[0,0,0,0,1],[0,1,1,1,1]]

    similar = truthtable._results_similar(result_row, 1, truthtable.matrix[1], simplified_rows=1)
    assert similar == [1,3]

def test_matrix_manipulation():
    truthtable = TruthTable(prop)

    truthtable._matrix_insert_row(1, [-1, -1, 1, 0])
    assert truthtable.matrix == [[0,-1,0,0,0,1,1,1,1],[0,-1,0,1,1,0,0,1,1],[0,1,1,0,1,0,1,0,1],[0,0,1,1,1,1,1,1,1]]

    truthtable._matrix_remove_row([0,2,3,4])
    assert truthtable.matrix == [[-1,1,1,1,1],[-1,0,0,1,1],[1,0,1,0,1],[0,1,1,1,1]]

def test_dontcare_values():
    truthtable = TruthTable(prop)

    assert truthtable._get_dontcare_values(1, 4, 0, 1) == [-1, 0, -1, 1]
    assert truthtable._get_dontcare_values(2, 4, 1, 1) == [-1, -1, 1, 1]
    assert truthtable._get_dontcare_values(2, 5, 1, 0) == [-1, -1, 1, -1, 0]

def test_get_replacement_preparation():
    truthtable = TruthTable(prop)

    replacement = truthtable._get_replacement_preparation([1,3,5,7], 2, 4, 1)
    assert replacement == ([-1,-1,1,1], [1,3,5,7])

def test_simplified_truthtable():
    truthtable = TruthTable(prop).simplify()
    assert truthtable.matrix == [[0,-1,-1,1],[0,-1,1,-1],[0,1,-1,-1],[0,1,1,1]]
    assert truthtable.get_binary_string() == "1110"
    assert truthtable.get_hash() == "E"