class Operator:
    def ascii(self) -> str:
        raise NotImplementedError()

    def infix(self) -> str:
        raise NotImplementedError()

    def is_compound(self) -> bool:
        raise NotImplementedError()

class SingularOperator(Operator):
    def evaluate(self, a) -> bool:
        raise NotImplementedError()

class CompoundOperator(Operator):
    def evaluate(self, a, b) -> bool:
        raise NotImplementedError()
    
    def evaluate_extended(self, props: list[int]) -> bool:
        if len(props) == 0: return False
        state = props[0] == 1
        for i in range(1, len(props)):
            state = self.evaluate(state, props[i])
        return state
        
class AndOperator(CompoundOperator):
    def ascii(self):
        return '&'

    def infix(self):
        return '∧'

    def is_compound(self):
        return True

    def evaluate(self, a, b) -> bool:
        return a and b

class OrOperator(CompoundOperator):
    def ascii(self):
        return '|'
    
    def infix(self):
        return '∨'

    def is_compound(self):
        return True
    
    def evaluate(self, a, b) -> bool:
        return a or b

class ImplicationOperator(CompoundOperator):
    def ascii(self):
        return '>'

    def infix(self):
        return '=>'

    def is_compound(self):
        return True

    def evaluate(self, a, b) -> bool:
        return not a or (a and b)
    
    def evaluate_extended(self, _):
        raise NotImplementedError()

class BiimplicationOperator(CompoundOperator):
    def ascii(self):
        return '='

    def infix(self):
        return '<=>'

    def is_compound(self):
        return True
    
    def evaluate(self, a, b) -> bool:
        return a == b

    def evaluate_extended(self, _):
        raise NotImplementedError()
    
class NotOperator(SingularOperator):
    def ascii(self):
        return '~'

    def infix(self):
        return '¬'

    def is_compound(self):
        return False

    def evaluate(self, a) -> bool:
        return not a

    def evaluate_extended(self, _):
        raise NotImplementedError()
