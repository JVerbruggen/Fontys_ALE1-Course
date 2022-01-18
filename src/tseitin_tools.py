
class VariableNamer:
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        self.last = -1

    def from_variables(variables: list[str]) -> 'VariableNamer':
        vn = VariableNamer()
        vn.process_variables(variables)
        return vn

    def process_variables(self, variables: list[str]):
        for var in variables:
            if var.isalpha() == False:
                raise ValueError(f"Cannot process variable '{var}'")
            if var.isupper() == False: continue
            i = VariableNamer.LETTERS.index(var)
            if i > self.last:
                self.last = i

    def next(self) -> str:
        new_i = self.last + 1

        if new_i >= len(VariableNamer.LETTERS):
            raise ValueError(f"New variable for index {new_i} out of bounds")
        
        new_letter = VariableNamer.LETTERS[new_i]

        self.last = new_i
        return new_letter