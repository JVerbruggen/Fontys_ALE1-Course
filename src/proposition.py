from enum import Enum

class Operator(Enum):
    NOT = 1
    IMPL = 2
    BIIMPL = 3
    AND = 4
    OR = 5

    def ascii(self) -> str:
        operators = {
            Operator.NOT: '~',
            Operator.IMPL: '>',
            Operator.BIIMPL: '=',
            Operator.AND: '&',
            Operator.OR: '|'
        }
        return operators[self]
    
    def infix(self) -> str:
        operators = {
            Operator.NOT: '¬',
            Operator.IMPL: '=>',
            Operator.BIIMPL: '<=>',
            Operator.AND: '∧',
            Operator.OR: '∨'
        }
        return operators[self]
    
    def is_operator(char: str) -> bool:
        chars = ['~', '>', '=', '&', '|']
        return (char in chars)

    def get_operator(char: str) -> 'Operator':
        if Operator.is_operator(char) == False: return None
        operators = {
            '~': Operator.NOT,
            '>': Operator.IMPL,
            '=': Operator.BIIMPL,
            '&': Operator.AND,
            '|': Operator.OR
        }
        return operators[char]

    def generate_proposition(operator: 'Operator') -> 'Proposition':
        compound_operators = [2,3,4,5]
        if operator.value in compound_operators:
            return CompoundProposition(operator)
        else:
            return SingularProposition(operator)

    def evaluate(self, a, b = False) -> bool:
        if self.value == 1:
            return not a
        elif self.value == 2:
            return not a or (a and b)
        elif self.value == 3:
            return a == b
        elif self.value == 4:
            return a and b
        else:
            return a or b

    def evaluate_extended(self, props: list[int]) -> bool:
        state = props[0] == 1
        for i in range(1, len(props)):
            state = self.evaluate(state, props[i])
        return state

class Proposition:
    def ascii(self) -> str:
        pass

    def infix(self) -> str:
        pass

    def get_variables(self) -> list[str]:
        pass

    def output(self, state: dict) -> bool:
        pass

    def cnf(self) -> 'Proposition':
        pass

class Variable(Proposition):
    def __init__(self, value: str):
        super().__init__()
        self.value = value
    
    def ascii(self):
        return self.value

    def infix(self):
        return self.value

    def get_variables(self):
        return [self.value]

    def output(self, state: dict):
        if self.value in state.keys():
            return state[self.value]
        return False

    def cnf(self):
        return Variable(self.value)

    def __str__(self):
        return self.value

class ExtendedProposition(Proposition):
    def __init__(self, operator: Operator, propositions: list[Proposition]):
        super().__init__()
        self.operator = operator
        self.propositions = propositions
    
    def ascii(self):
        return self.operator.ascii() + "(" + ",".join([prop.ascii() for prop in self.propositions]) + ")"
    
    def infix(self):
        return "(" + f" {self.operator.infix()} ".join([prop.infix() for prop in self.propositions]) + ")"

    def output(self, state):
        evaluated_props = []
        for prop in self.propositions:
            evaluated_props += [prop.output(state)]
        return self.operator.evaluate_extended(evaluated_props)
    
    def get_variables(self):
        variables = []
        for prop in self.propositions:
            variables += [var for var in prop.get_variables() if var not in variables]
        return sorted(variables)

    def cnf(self):
        raise Exception("CNF not available for extended proposition")

    def __str__(self):
        return self.ascii()

class CompoundProposition(Proposition):
    def __init__(self, operator: Operator, proposition_a: Proposition = None, proposition_b: Proposition = None):
        super().__init__()
        self.operator = operator
        self.proposition_a = proposition_a
        self.proposition_b = proposition_b
    
    def ascii(self):
        if self.proposition_a == None or self.proposition_b == None:
            return self.operator.ascii() + "(incomplete proposition)"
        return self.operator.ascii() + "(" + self.proposition_a.ascii() + "," + self.proposition_b.ascii() + ")"
    
    def infix(self):
        return "(" + self.proposition_a.infix() + " " + self.operator.infix() + " " + self.proposition_b.infix() + ")"

    def get_variables(self):
        if self.proposition_a == None or self.proposition_b == None:
            return []
        variables = self.proposition_a.get_variables()
        variables += [var for var in self.proposition_b.get_variables() if var not in variables]
        return sorted(variables)

    def output(self, state):
        return self.operator.evaluate(self.proposition_a.output(state), self.proposition_b.output(state))

    def __str__(self):
        return self.operator.ascii() + "(" + str(self.proposition_a) + "," + str(self.proposition_b) + ")"

class SingularProposition(Proposition):
    def __init__(self, operator: Operator, proposition_a: Proposition = None):
        super().__init__()
        self.operator = operator
        self.proposition_a = proposition_a

    def ascii(self):
        if self.proposition_a == None:
            return self.operator.ascii() + "(incomplete proposition)"
        return self.operator.ascii() + "(" + self.proposition_a.ascii() + ")"

    def infix(self):
        return self.operator.infix() + self.proposition_a.infix()

    def get_variables(self):
        if self.proposition_a == None:
            return []
        return self.proposition_a.get_variables()

    def output(self, state):
        return self.operator.evaluate(self.proposition_a.output(state))

    def __str__(self):
        return self.operator.ascii() + "(" + str(self.proposition_a) + ")"

# Implementations

