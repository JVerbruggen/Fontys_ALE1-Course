from proposition import *
from hashing import *

class TruthTable:
    def parse_variables(variable_sequence: list[str]) -> list[list[int]]:
        variable_sequence_len = len(variable_sequence)
        matrix = [[] for _ in variable_sequence]        # Create empty matrix with correct number of rows
        rows = 2**variable_sequence_len
        
        for i in range(variable_sequence_len):
            variable = variable_sequence[i]
            row = 0
            repeat_length = 2**(variable_sequence_len - i - 1)
            repeating = repeat_length
            printing = 0

            while row < rows:
                if repeating <= 0:
                    repeating = repeat_length
                    printing = 1-printing       # Changes 0 to 1, and 1 to 0

                matrix[i] = matrix[i] + [printing]

                repeating -= 1
                row += 1
        return matrix

    def evaluate_proposition(
            proposition: Proposition, 
            variables: list[str], 
            variable_matrix: list[list[int]]
            ) -> list[int]:
        if len(variable_matrix) == 0: return
        if len(variables) == 0: return
        if proposition == None: return

        rows = len(variable_matrix[0])
        vars = len(variables)

        outputs = []
        
        for i in range(rows):
            state = dict()
            for j in range(vars):
                var = variables[j]
                state[var] = variable_matrix[j][i]
            
            output = proposition.output(state)
            outputs += [1 if output else 0]
        return outputs

    def __init__(self, proposition: Proposition):
        self.variables = proposition.get_variables()
        self.proposition = proposition

        variable_matrix = TruthTable.parse_variables(self.variables)
        evaluated_proposition_matrix = TruthTable.evaluate_proposition(proposition, self.variables, variable_matrix)
        self.matrix = variable_matrix + [evaluated_proposition_matrix]

    def __str__(self) -> str:
        if len(self.matrix) == 0: return

        printed = ""

        printed += " ".join(var for var in self.variables) + " " + self.proposition.ascii() + "\n"
        
        for i in range(len(self.matrix[0])):
            printed += " ".join([str(col[i]) for col in self.matrix]) + "\n"
        
        return printed

    def get_hash(self)->str:
        result_row = self.matrix[-1]
        rows = len(result_row)
        binary_string = ''.join([str(result_row[rows-1-i]) for i in range(rows)])

        return Hashing.get_hash(binary_string)
