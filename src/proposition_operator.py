class Operator:
    def ascii(self) -> str:
        raise NotImplementedError()

    def infix(self) -> str:
        raise NotImplementedError()

    def is_compound(self) -> bool:
        raise NotImplementedError()

    def evaluate(self, a, b = False) -> bool:
        raise NotImplementedError()
    
    def evaluate_extended(self, props: list[int]) -> bool:
        if len(props) == 0: return False
        state = props[0] == 1
        for i in range(1, len(props)):
            state = self.evaluate(state, props[i])
        return state

class AndOperator(Operator):
    def ascii(self):
        return '&'

    def infix(self):
        return '∧'

    def is_compound(self):
        return True

    def evaluate(self, a, b = False) -> bool:
        return a and b

class OrOperator(Operator):
    def ascii(self):
        return '|'
    
    def infix(self):
        return '∨'

    def is_compound(self):
        return True
    
    def evaluate(self, a, b = False) -> bool:
        return a or b

class ImplicationOperator(Operator):
    def ascii(self):
        return '>'

    def infix(self):
        return '=>'

    def is_compound(self):
        return True

    def evaluate(self, a, b = False) -> bool:
        return not a or (a and b)

class BiimplicationOperator(Operator):
    def ascii(self):
        return '='

    def infix(self):
        return '<=>'

    def is_compound(self):
        return True
    
    def evaluate(self, a, b = False) -> bool:
        return a == b
    
class NotOperator(Operator):
    def ascii(self):
        return '~'

    def infix(self):
        return '¬'

    def is_compound(self):
        return False

    def evaluate(self, a, b = False) -> bool:
        return not a

    def evaluate_extended(self, _):
        raise NotImplementedError()

class OperatorFactory:
    known_operators = {'&': AndOperator, '|': OrOperator, '>': ImplicationOperator, '=': BiimplicationOperator, '~': NotOperator}
    operator_storage = {AndOperator: AndOperator(), OrOperator: OrOperator(), ImplicationOperator: ImplicationOperator(), BiimplicationOperator: BiimplicationOperator(), NotOperator: NotOperator()}

    def is_operator(char: str) -> bool:
        return char in OperatorFactory.known_operators.keys()

    def get_operator_by_type(operator_type: type) -> Operator:
        return OperatorFactory.operator_storage[operator_type]

    def get_operator(char: str) -> Operator:
        if OperatorFactory.is_operator(char) == False: 
            return None
        return OperatorFactory.get_operator_by_type(OperatorFactory.known_operators[char])