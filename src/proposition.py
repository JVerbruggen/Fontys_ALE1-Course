from enum import Enum

class Operator(Enum):
    NOT = 1
    IMPL = 2
    BIIMPL = 3
    AND = 4
    OR = 5

    def ascii(self):
        operators = {
            Operator.NOT: '~',
            Operator.IMPL: '>',
            Operator.BIIMPL: '=',
            Operator.AND: '&',
            Operator.OR: '|'
        }
        return operators[self]
    
    def is_operator(char):
        chars = ['~', '>', '=', '&', '|']
        return (char in chars)

    def get_operator(char):
        if Operator.is_operator(char) == False: return None
        operators = {
            '~': Operator.NOT,
            '>': Operator.IMPL,
            '=': Operator.BIIMPL,
            '&': Operator.AND,
            '|': Operator.OR
        }
        return operators[char]

    def generate_proposition(operator):
        compound_operators = [2,3,4,5]
        if operator.value in compound_operators:
            return CompoundProposition(operator)
        else:
            return SingularProposition(operator)

class Proposition:
    def ascii(self):
        pass

class Variable(Proposition):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def ascii(self):
        return self.value

    def __str__(self):
        return self.value

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

    def __str__(self):
        return self.operator.ascii() + "(" + str(self.proposition_a) + ")"