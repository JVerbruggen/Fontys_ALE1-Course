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

    def __init__(self, proposition: Proposition, variables: list[str] = None, matrix: list[list[int]] = None):
        self.proposition = proposition

        if variables is None:
            self.variables = proposition.get_variables()
        else:
            self.variables = variables

        if matrix is None:
            variable_matrix = TruthTable.parse_variables(self.variables)
            evaluated_proposition_matrix = TruthTable.evaluate_proposition(self.proposition, self.variables, variable_matrix)
            self.matrix = variable_matrix + [evaluated_proposition_matrix]
        else:
            self.matrix = matrix

    def __str__(self) -> str:
        if len(self.matrix) == 0: return

        printed = ""

        printed += " ".join(var for var in self.variables) + " " + self.proposition.ascii() + "\n"
        
        for i in range(len(self.matrix[0])):
            printed += " ".join([(str(col[i]) if col[i] >= 0 else "*") for col in self.matrix]) + "\n"
        
        return printed

    def __repr__(self):
        return f"matrix: {self.matrix}"

    def get_binary_string(self)->str:
        result_row = self.matrix[-1]
        rows = len(result_row)
        return ''.join([str(result_row[rows-1-i]) for i in range(rows)])

    def get_hash(self)->str:
        return Hashing.get_hash(self.get_binary_string())

    def _results_similar(self, result_row: list[int], nr_checking: int, col: list[int], simplified_rows: int = 0) -> list[int]:
        col_length = len(result_row)
        nrs_indices = [i for i in range(col_length) if col[i]==nr_checking]
        nrs_results = [result_row[i] for i in nrs_indices]
        nrs_apply = 0
        for res in nrs_results:
            nrs_apply += abs(res)
        
        similar = nrs_apply == 0 or nrs_apply == (col_length-simplified_rows)/2

        if not similar:
            return []
        else:
            return nrs_indices

    def _matrix_insert_row(self, index: int, value: [int]):
        for i in range(len(self.matrix)):
            col = self.matrix[i]
            col.insert(index, value[i])

    def _matrix_remove_row(self, indices: [int]):
        indices = sorted(indices, reverse=True)
        for col in self.matrix:
            for i in indices:
                del col[i]

    def _get_dontcare_values(self, col_i: int, cols_count: int, set: int, result_set: int) -> list[int]:
        dontcare_values = [-1 for ii in range(cols_count)]
        dontcare_values[col_i] = set
        dontcare_values[-1] = result_set
        return dontcare_values

    def _get_replacement_preparation(self, indices: list[int], col_i: int, cols_count: int, set: int) -> (int, list[int], list[int]):
        insert_index = indices[0]
        result_set = self.matrix[-1][insert_index]
        inserting = self._get_dontcare_values(col_i, cols_count, set, result_set)

        return (inserting, indices)

    def _replace_by_dontcare(self, indices: list[int], col_i: int, cols_count: int, set: int):
        insert_index = indices[0]
        result_set = self.matrix[-1][insert_index]
        inserting = self._get_dontcare_values(col_i, cols_count, set, result_set)

        self._matrix_remove_row(indices)
        self._matrix_insert_row(insert_index, inserting)

    def simplify(self):
        length_variable_cols = len(self.matrix[0:-1])
        
        replacements = []
        for i in range(length_variable_cols):
            result_col = self.matrix[-1]
            row_i = length_variable_cols-1-i # Work from right to left
            col = self.matrix[0:-1][row_i]

            zeros_similar_nrs = self._results_similar(result_col, 0, col, 0)
            ones_similar_nrs = self._results_similar(result_col, 1, col, 0)

            zeros_similar = len(zeros_similar_nrs) > 1
            ones_similar = len(ones_similar_nrs) > 1

            if zeros_similar and ones_similar:
                self.matrix = [[-1] for _ in range(length_variable_cols)]
                break
            elif zeros_similar:
                replacement = self._get_replacement_preparation(zeros_similar_nrs, row_i, len(self.matrix), 0)
                replacements += [replacement]
            elif ones_similar:
                replacement = self._get_replacement_preparation(ones_similar_nrs, row_i, len(self.matrix), 1)
                replacements += [replacement]

        del_indices_final = []
        for (dontcare_values, del_indices) in replacements:
            del_indices_final += [del_index for del_index in del_indices if del_index not in del_indices_final]
            
            self._matrix_insert_row(len(self.matrix[0]), dontcare_values)
        
        self._matrix_remove_row(del_indices_final)

        return self
