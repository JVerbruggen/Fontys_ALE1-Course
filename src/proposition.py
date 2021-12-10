from debugger import *

class Proposition:
    def ascii_operator(self):
        raise NotImplementedError()

    def infix_operator(self):
        raise NotImplementedError()

    def evaluate(self, state):
        raise NotImplementedError()

    def ascii(self) -> str:
        raise NotImplementedError()

    def infix(self) -> str:
        raise NotImplementedError()

    def get_variables(self) -> list[str]:
        raise NotImplementedError()

    def get_literals(self) -> list['Proposition']:
        raise NotImplementedError()

    def get_sub_propositions(self) -> list['Proposition']:
        raise NotImplementedError()

    def cnf(self, debugger=None) -> 'Proposition':
        raise NotImplementedError()

    def concat_sub_propositions(self, other: 'Proposition') -> list['Proposition']:
        return self.get_literals() + other.get_literals()

    def is_literal(self):
        raise NotImplementedError()

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

    def get_literals(self):
        return [self]

    def get_sub_propositions(self):
        return [self]

    def evaluate(self, state):
        if self.value in state.keys():
            return state[self.value]
        return False

    def cnf(self,debugger=None):
        return Variable(self.value)

    def __str__(self):
        return self.value

    def is_literal(self):
        return True

class ExtendedProposition(Proposition):
    def __init__(self, propositions: list[Proposition]):
        super().__init__()
        self.propositions = propositions

    def get_rational_equivalent(self, to_process=None):
        if to_process is None:
            to_process = self.propositions

        take = to_process[0]

        if len(to_process) == 2:
            return CompoundProposition(take, to_process[1])
        elif len(to_process) < 2:
            raise ValueError()

        to_process = to_process[1:]

        return CompoundProposition(take, self.get_rational_equivalent(to_process))
    
    def ascii(self):
        closing_brackets = 1

        operator_ascii = self.ascii_operator()
        ascii_string = operator_ascii + "(" + self.propositions[0].ascii() + ","
        for i in range(1,len(self.propositions)-1):
            prop = self.propositions[i]

            ascii_string += operator_ascii + "(" + prop.ascii() + ","

            closing_brackets += 1
        
        ascii_string += self.propositions[-1].ascii()

        ascii_string += ''.join(')' for _ in range(closing_brackets))

        return ascii_string
    
    def infix(self):
        return "(" + f" {self.infix_operator()} ".join([prop.infix() for prop in self.propositions]) + ")"
    
    def get_variables(self):
        variables = []
        for prop in self.propositions:
            variables += [var for var in prop.get_variables() if var not in variables]
        return sorted(variables)

    def get_literals(self):
        return [self.propositions[:]]

    def get_sub_propositions(self):
        return self.propositions[:]

    # def cnf(self,debugger=None):
    #     if debugger is not None: debugger.analyse(self)
    #     return self.get_rational_equivalent().cnf(debugger)
    #     # raise Exception("CNF not available for extended proposition")

    def __str__(self):
        return self.ascii()
    
    def is_literal(self):
        return False

class MultiAnd(ExtendedProposition):
    def ascii_operator(self):
        return '&'
    
    def infix_operator(self):
        return '∧'

    def evaluate(self, state):
        if len(self.propositions) == 0: return False
        res = self.propositions[0].evaluate(state)
        for i in range(1, len(self.propositions)):
            res = res and self.propositions[i].evaluate(state)
        return res
    
    def cnf(self,debugger=None):
        props = self.get_sub_propositions()
        props = [p.cnf(debugger) for p in props]
        return MultiAnd(props)

class MultiOr(ExtendedProposition):
    def ascii_operator(self):
        return '|'
    
    def infix_operator(self):
        return '∨'

    def evaluate(self, state):
        if len(self.propositions) == 0: return False
        res = self.propositions[0].evaluate(state)
        for i in range(1, len(self.propositions)):
            res = res or self.propositions[i].evaluate(state)
        return res
    
    def cnf(self,debugger=None):
        props = self.get_sub_propositions()
        props = [p.cnf(debugger) for p in props]
        return MultiOr(props)

class CompoundProposition(Proposition):
    def __init__(self, proposition_a: Proposition = None, proposition_b: Proposition = None):
        super().__init__()
        self.proposition_a = proposition_a
        self.proposition_b = proposition_b

    def ascii(self):
        if self.proposition_a == None or self.proposition_b == None:
            return self.ascii_operator() + "(incomplete proposition)"
        return self.ascii_operator() + "(" + self.proposition_a.ascii() + "," + self.proposition_b.ascii() + ")"
    
    def infix(self):
        return "(" + self.proposition_a.infix() + " " + self.infix_operator() + " " + self.proposition_b.infix() + ")"

    def get_variables(self):
        if self.proposition_a == None or self.proposition_b == None:
            return []
        variables = self.proposition_a.get_variables()
        variables += [var for var in self.proposition_b.get_variables() if var not in variables]
        return sorted(variables)

    def get_literals(self):
        return self.proposition_a.get_literals() + self.proposition_b.get_literals()

    def get_sub_propositions(self):
        return [self.proposition_a, self.proposition_b]

    def __str__(self):
        return self.ascii_operator() + "(" + str(self.proposition_a) + "," + str(self.proposition_b) + ")"

    def is_literal(self):
        return False

class AndProposition(CompoundProposition):
    def ascii_operator(self):
        return '&'

    def infix_operator(self):
        return '∧'

    def evaluate(self, state):
        return self.proposition_a.evaluate(state) and self.proposition_b.evaluate(state)
    
    def cnf(self,debugger=None):
        if self.proposition_a == None or self.proposition_b == None:
            raise ValueError("Propositions in strategies not defined")

        return self
        # pa_items = self.proposition_a.cnf(debugger).get_literals()
        # pb_items = self.proposition_b.cnf(debugger).get_literals()
        # res = MultiAnd(pa_items + pb_items)
        # if debugger is not None: 
        #     debugger.trace(res.ascii())
        #     debugger.analyse(res)
        # return res

class OrProposition(CompoundProposition):
    def ascii_operator(self):
        return '|'
    
    def infix_operator(self):
        return '∨'
    
    def evaluate(self, state):
        return self.proposition_a.evaluate(state) or self.proposition_b.evaluate(state)


    def cnf(self,debugger=None):
        and_props = []

        prop_a = self.proposition_a.cnf(debugger)
        prop_b = self.proposition_b.cnf(debugger)

        p_items = prop_a.get_literals()
        q_items = prop_b.get_literals()

        if debugger is not None:
            debugger.analyse(self)
            debugger.trace("OR1: " + str(prop_a.ascii()))
            debugger.trace("OR2: " + str(prop_b.ascii()))
            debugger.trace("LIT: " + str([x.ascii() for x in p_items + q_items]))
            debugger.trace("OR2: " + str(prop_b.ascii()))


        for p_item in p_items:
            for q_item in q_items:
                and_props += [OrProposition( p_item, q_item)]

        if len(and_props) == 1:
            return and_props[0]

        res = MultiAnd(and_props)
        # Dont CNF this, only CNF its children
        if debugger is not None: 
            debugger.trace(res.ascii())
            debugger.analyse(res)
        return res

class ImplicationProposition(CompoundProposition):
    def ascii_operator(self):
        return '>'
    
    def infix_operator(self):
        return '=>'
    
    def evaluate(self, state):
        pa_evaluated = self.proposition_a.evaluate(state)
        return not pa_evaluated or (pa_evaluated and self.proposition_b.evaluate(state))
    
    def cnf(self,debugger=None):
        res = OrProposition(NotProposition(self.proposition_a), 
            self.proposition_b
            )
        res_cnf = res.cnf(debugger)
        if debugger is not None: 
            debugger.trace(res.ascii())
            debugger.analyse(res)
            debugger.trace(res_cnf.ascii())
            debugger.analyse(res_cnf)
        # return res
        return res_cnf

class BiimplicationProposition(CompoundProposition):
    def ascii_operator(self):
        return '='
    
    def infix_operator(self):
        return '<=>'
    
    def evaluate(self, state):
        return self.proposition_a.evaluate(state) == self.proposition_b.evaluate(state)
    
    def cnf(self,debugger=None):
        prop_a_cnfed = self.proposition_a.cnf(debugger)
        prop_b_cnfed = self.proposition_b.cnf(debugger)

        res = AndProposition(
            OrProposition(NotProposition(prop_a_cnfed).cnf(debugger), prop_b_cnfed),
            OrProposition(prop_a_cnfed, NotProposition(prop_b_cnfed).cnf(debugger))
        )
        res_cnf = res.cnf(debugger)
        if debugger is not None: 
            debugger.trace(res.ascii())
            debugger.analyse(res)
            debugger.trace(res_cnf.ascii())
            debugger.analyse(res_cnf)
        return res_cnf

class SingularProposition(Proposition):
    def __init__(self, proposition_a: Proposition = None):
        super().__init__()
        self.proposition_a = proposition_a

    def ascii(self):
        if self.proposition_a == None:
            return self.ascii_operator() + "(incomplete proposition)"
        return self.ascii_operator() + "(" + self.proposition_a.ascii() + ")"

    def infix(self):
        return self.infix_operator() + self.proposition_a.infix()

    def get_variables(self):
        if self.proposition_a == None:
            return []
        return self.proposition_a.get_variables()

    def get_sub_propositions(self):
        return [self.proposition_a]

    def __str__(self):
        return self.ascii_operator() + "(" + str(self.proposition_a) + ")"

    def is_literal(self):
        return self.proposition_a.is_literal() # ~(A) is also a literal

class NotProposition(SingularProposition):
    def ascii_operator(self):
        return '~'
    
    def infix_operator(self):
        return '¬'
    
    def evaluate(self, state):
        return not self.proposition_a.evaluate(state)
    
    def cnf(self,debugger=None):
        # Very not OOP, but if delegated to operator we would have circular import?
        pa_type = type(self.proposition_a)
        if pa_type is Variable:
            return self
        elif issubclass(pa_type, SingularProposition):
            return self.proposition_a.proposition_a.cnf(debugger)
        elif issubclass(pa_type, CompoundProposition):
            if pa_type is AndProposition:
                pa = self.proposition_a.proposition_a
                pb = self.proposition_a.proposition_b
                res = OrProposition(
                    NotProposition(pa),
                    NotProposition(pb)
                    )
                res_cnf = res.cnf(debugger)
                if debugger is not None: 
                    debugger.trace(res.ascii())
                    debugger.analyse(res)
                    debugger.trace(res_cnf.ascii())
                    debugger.analyse(res_cnf)
                return res_cnf
            elif pa_type is OrProposition:
                pa = self.proposition_a.proposition_a
                pb = self.proposition_a.proposition_b
                res = AndProposition(
                    NotProposition(pa),
                    NotProposition(pb)
                    )
                res_cnf = res.cnf(debugger)
                if debugger is not None: 
                    debugger.trace(res.ascii())
                    debugger.analyse(res)
                    debugger.trace(res_cnf.ascii())
                    debugger.analyse(res_cnf)
                return res_cnf
            # else:
            #     return NotProposition(self.proposition_a.cnf(debugger)).cnf(debugger)
            raise Exception("Unsupported operator")
        elif issubclass(pa_type, ExtendedProposition): 
            old_props = self.proposition_a.get_sub_propositions()
            props = [NotProposition(p) for p in old_props]
            res = MultiAnd(props) if pa_type == MultiOr else MultiOr(props)
            res_cnf = res.cnf()

            if debugger is not None: 
                debugger.trace(res.ascii())
                debugger.analyse(res)
                debugger.trace(res_cnf.ascii())
                debugger.analyse(res_cnf)
            
            return res_cnf
        raise Exception("Unsupported operator")     

    def get_literals(self):
        if type(self.proposition_a) is Variable:
            return [self]
        elif type(self.proposition_a) is NotProposition:
            return self.proposition_a.proposition_a.get_literals()
        raise NotImplementedError()