from debugger import *
from ascii_inflictor import *
from tseitin_tools import *

class Proposition:
    def ascii_operator(self):
        raise NotImplementedError()

    def infix_operator(self):
        raise NotImplementedError()

    def evaluate(self, state):
        raise NotImplementedError()

    def ascii(self, ascii_func=AsciiInflictor.ascii_normal) -> str:
        raise NotImplementedError()

    def ascii_complex(self) -> str:
        return self.ascii(ascii_func=AsciiInflictor.ascii_complex)

    def infix(self) -> str:
        raise NotImplementedError()

    def get_variables(self) -> list[str]:
        raise NotImplementedError()

    def get_literals(self) -> list['Proposition']:
        raise NotImplementedError()

    def get_proper_literals(self) -> list['Proposition']:
        raise NotImplementedError()

    def get_sub_propositions(self) -> list['Proposition']:
        raise NotImplementedError()

    def remove_biimpl(self, debugger: Debugger=NoDebug()) -> 'Proposition':
        raise NotImplementedError(repr(self))

    def remove_impl(self, debugger: Debugger=NoDebug()) -> 'Proposition':
        raise NotImplementedError(repr(self))

    def remove_nots(self, debugger: Debugger=NoDebug()) -> 'Proposition':
        raise NotImplementedError(repr(self))

    def distribute_elements(self, debugger: Debugger=NoDebug()) -> 'Proposition':
        raise NotImplementedError(repr(self))

    def merge_ors(self, debugger: Debugger=NoDebug()) -> 'Proposition':
        raise NotImplementedError(repr(self))

    def tseitin_replace(self, variable_namer: VariableNamer, debugger: Debugger=NoDebug()):
        raise NotImplementedError(repr(self))

    def tseitin(self, debugger: Debugger=NoDebug()) -> 'Proposition':
        res = self
        debugger.trace("tseitin start with: " + res.ascii_complex())
        debugger.analyse(res)

        (rename, ands) = res.tseitin_replace(VariableNamer.from_variables(res.get_variables()), debugger)
        res = MultiAnd([rename] + ands)

        debugger.trace("after tseitin repl: " + res.ascii_complex())
        debugger.analyse(res)

        return res

    def cnf(self, debugger: Debugger=NoDebug()) -> 'Proposition':
        res = self
        debugger.trace("start with: " + res.ascii_complex())
        debugger.analyse(res)

        res = res.remove_biimpl(debugger)
        debugger.trace("removed biimpl: " + res.ascii_complex())
        debugger.analyse(res)

        res = res.remove_impl(debugger)
        debugger.trace("removed impl: " + res.ascii_complex())
        debugger.analyse(res)

        res = res.remove_nots(debugger)
        debugger.trace("removed nots: " + res.ascii_complex())
        debugger.analyse(res)

        res = res.distribute_elements(debugger)
        debugger.trace("after distribution: " + res.ascii_complex())
        debugger.analyse(res)

        res = res.merge_ors()
        debugger.trace("merged ors: " + res.ascii_complex())
        debugger.analyse(res)

        res = res.remove_contradictions()
        debugger.trace("removed contradictions: " + res.ascii_complex())
        debugger.analyse(res)

        return res

    def cnf_notation(self) -> str:
        raise ValueError("This proposition type is not a CNF root")

    def remove_contradictions(self, debugger: Debugger=NoDebug()):
        return self

    def is_always_same(self, debugger: Debugger=NoDebug()) -> bool:
        return False

    def concat_sub_propositions(self, other: 'Proposition') -> list['Proposition']:
        return self.get_literals() + other.get_literals()

    def is_literal(self):
        raise NotImplementedError()

    def cnf_notation(self):
        raise NotImplementedError()

class Variable(Proposition):
    def __init__(self, value: str):
        super().__init__()
        self.value = value
    
    def ascii(self, ascii_func=AsciiInflictor.ascii_normal):
        return self.value

    def infix(self):
        return self.value

    def get_variables(self):
        return [self.value]

    def get_literals(self):
        return [self]

    def get_proper_literals(self):
        return [self]

    def get_sub_propositions(self):
        return [self]

    def evaluate(self, state):
        if self.value in state.keys():
            return state[self.value]
        return False

    def remove_biimpl(self, debugger: Debugger=NoDebug()):
        return self

    def remove_impl(self, debugger: Debugger=NoDebug()):
        return self

    def remove_nots(self, debugger: Debugger=NoDebug()):
        return self

    def distribute_elements(self, debugger: Debugger=NoDebug()):
        return self

    def merge_ors(self, debugger: Debugger=NoDebug()):
        return self

    def cnf_notation(self):
        return self.value

    def __str__(self):
        return self.value

    def is_literal(self):
        return True

    def tseitin_replace(self, variable_namer: VariableNamer, debugger: Debugger=NoDebug()):
        return (self, self)

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
    
    def ascii(self, ascii_func=AsciiInflictor.ascii_normal):
        closing_brackets = 1

        operator_ascii = self.ascii_operator()
        ascii_string = operator_ascii + "(" + ascii_func(self.propositions[0]) + ","
        for i in range(1,len(self.propositions)-1):
            prop = self.propositions[i]

            ascii_string += operator_ascii + "(" + ascii_func(prop) + ","

            closing_brackets += 1
        
        ascii_string += ascii_func(self.propositions[-1])

        ascii_string += ''.join(')' for _ in range(closing_brackets))

        return ascii_string

    def ascii_complex(self):
        operator_ascii = self.ascii_operator()
        ascii_string = '*' + operator_ascii + "([" + ",".join([prop.ascii_complex() for prop in self.propositions]) + "])"
        
        return ascii_string
    
    def infix(self):
        return "(" + f" {self.infix_operator()} ".join([prop.infix() for prop in self.propositions]) + ")"
    
    def get_variables(self):
        variables = []
        for prop in self.propositions:
            variables += [var for var in prop.get_variables() if var not in variables]
        return sorted(variables)

    def get_literals(self):
        return self.propositions[:]

    def get_proper_literals(self):
        literals = []
        for p in self.propositions:
            if p.is_literal():
                literals += [p]
            else:
                raise ValueError(f"Encountered a non-literal in {str(self)} {repr(self)}: {repr(p)}")
        return literals

    def get_sub_propositions(self):
        return self.propositions[:]

    def new_self(self, props: list[Proposition]):
        raise NotImplementedError()

    def remove_biimpl(self, debugger: Debugger=NoDebug()):
        return self.new_self([p.remove_biimpl(debugger) for p in self.get_sub_propositions()])

    def remove_impl(self, debugger: Debugger=NoDebug()):
        return self.new_self([p.remove_impl(debugger) for p in self.get_sub_propositions()])

    def remove_nots(self, debugger: Debugger=NoDebug()):
        return self.new_self([p.remove_nots(debugger) for p in self.get_sub_propositions()])

    def distribute_elements(self, debugger: Debugger=NoDebug()):
        return self

    def merge_ors(self, debugger: Debugger=NoDebug()) -> 'Proposition':
        return self.new_self([p.merge_ors(debugger) for p in self.get_sub_propositions()])

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

    def cnf_notation(self):
        raise NotImplementedError()

    def remove_contradictions(self, debugger: Debugger=NoDebug()):
        return MultiAnd([p for p in self.propositions if p.is_always_same() == False])
    
    def absorb(self, other: 'MultiAnd'):
        return MultiAnd(self.propositions + other.propositions)

    def cnf_notation(self):
        return "[ " + " , ".join([prop.cnf_notation() for prop in self.propositions]) + " ]"
    
    def new_self(self, props: list[Proposition]):
        return MultiAnd(props)

    def distribute_elements(self, debugger: Debugger=NoDebug()):
        ands = []
        for p in self.propositions:
            el = p.distribute_elements(debugger)
            if type(el) is MultiAnd:
                ands += el.get_sub_propositions()
            else:
                ands += [el]

        return MultiAnd(ands)

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

    def is_always_same(self, debugger: Debugger=NoDebug()) -> bool:
        always_same = False

        for i in range(len(self.propositions)):
            pi = self.propositions[i]
            if pi.is_literal():
                for j in range(i+1, len(self.propositions)):
                    pj = self.propositions[j]
                    if pj.is_literal():
                        always_same_here = (
                            (type(pi) is NotProposition and type(pj) is Variable
                                and type(pi.get_sub_propositions()[0]) is Variable
                                and pi.get_sub_propositions()[0].value==pj.value
                            ) 
                            or 
                            (type(pi) is Variable and type(pj) is NotProposition
                                and type(pj.get_sub_propositions()[0]) is Variable
                                and pi.value==pj.get_sub_propositions()[0].value
                            )) 
                        if always_same_here:
                            always_same = True
                            break

        return always_same
    
    def cnf_notation(self):
        notation = ""

        for prop in self.propositions:
            if type(prop) is Variable:
                notation += prop.value.upper()
            elif type(prop) is NotProposition and type(prop.proposition_a) is Variable:
                notation += prop.proposition_a.value.lower()
            else:
                raise ValueError(f"CNF format is not correct. Expected variable or not(variable), but got {prop}")
        
        return notation
    
    def new_self(self, props: list[Proposition]):
        return MultiOr(props)

class CompoundProposition(Proposition):
    def __init__(self, proposition_a: Proposition = None, proposition_b: Proposition = None):
        super().__init__()
        self.proposition_a = proposition_a
        self.proposition_b = proposition_b

    def ascii(self, ascii_func=AsciiInflictor.ascii_normal):
        if self.proposition_a == None or self.proposition_b == None:
            return self.ascii_operator() + "(incomplete proposition)"
        return self.ascii_operator() + "(" + ascii_func(self.proposition_a) + "," + ascii_func(self.proposition_b) + ")"
    
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

    def new_self(self, prop_a: Proposition, prop_b: Proposition):
        return AndProposition(prop_a, prop_b)

    def remove_impl(self, debugger: Debugger=NoDebug()):
        return self.new_self(self.proposition_a.remove_impl(debugger), self.proposition_b.remove_impl(debugger))

    def remove_biimpl(self, debugger: Debugger=NoDebug()):
        return self.new_self(self.proposition_a.remove_biimpl(debugger), self.proposition_b.remove_biimpl(debugger))

    def remove_nots(self, debugger: Debugger=NoDebug()):
        return self.new_self(self.proposition_a.remove_nots(debugger), self.proposition_b.remove_nots(debugger))

    def distribute_elements(self, debugger: Debugger=NoDebug()):
        return self

    def get_proper_literals(self):
        literals = []
        for p in [self.proposition_a, self.proposition_b]:
            if p.is_literal():
                literals += [p]
            else:
                raise ValueError(f"Encountered a non-literal in {str(self)} {repr(self)}: {repr(p)}")
        return literals

    def tseitin_replace(self, variable_namer: VariableNamer, debugger: Debugger=NoDebug()):
        ands = []
        prop_sides = []

        for p in [self.proposition_a, self.proposition_b]:
            if type(p) is Variable:
                prop_sides += [p]
            else:
                (p_rename, p_ands) = p.tseitin_replace(variable_namer, debugger)
                ands += p_ands
                prop_sides += [p_rename]

        self_rename = Variable(variable_namer.next())
        prop = BiimplicationProposition(
            self_rename,
            self.new_self(prop_sides[0], prop_sides[1])
        )

        ands = [prop] + ands
        return (self_rename, ands)

class AndProposition(CompoundProposition):
    def ascii_operator(self):
        return '&'

    def infix_operator(self):
        return '∧'

    def evaluate(self, state):
        return self.proposition_a.evaluate(state) and self.proposition_b.evaluate(state)

    def new_self(self, prop_a, prop_b):
        return AndProposition(prop_a, prop_b)

    def distribute_elements(self, debugger: Debugger=NoDebug()):
        dist_a = self.proposition_a.distribute_elements(debugger)   # Should be ands
        dist_b = self.proposition_b.distribute_elements(debugger)   # Should be ands

        ands_a = dist_a.get_proper_literals() if type(dist_a) is not MultiAnd else dist_a.get_sub_propositions()
        ands_b = dist_b.get_proper_literals() if type(dist_b) is not MultiAnd else dist_b.get_sub_propositions()

        ands = ands_a + ands_b

        return MultiAnd(ands)


class OrProposition(CompoundProposition):
    def ascii_operator(self):
        return '|'
    
    def infix_operator(self):
        return '∨'
    
    def evaluate(self, state):
        return self.proposition_a.evaluate(state) or self.proposition_b.evaluate(state)
    
    def is_always_same(self, debugger: Debugger=NoDebug()) -> bool:
        pi = self.proposition_a
        pj = self.proposition_b
        always_same = (
                    (type(pi) is NotProposition and type(pj) is Variable
                        and type(pi.get_sub_propositions()[0]) is Variable
                        and pi.get_sub_propositions()[0].value==pj.value
                    ) 
                    or 
                    (type(pi) is Variable and type(pj) is NotProposition
                        and type(pj.get_sub_propositions()[0]) is Variable
                        and pi.value==pj.get_sub_propositions()[0].value
                    )) 

        debugger.trace(f"Always same: {always_same} -> ({pi},{pj})")

        return always_same
        
    def new_self(self, prop_a, prop_b):
        return OrProposition(prop_a, prop_b)

    def distribute_elements(self, debugger: Debugger=NoDebug()):
        dist_a = self.proposition_a.distribute_elements(debugger)   # Should be ands
        dist_b = self.proposition_b.distribute_elements(debugger)   # Should be ands

        ands_a = dist_a.get_proper_literals() if type(dist_a) is not MultiAnd else dist_a.get_sub_propositions()
        ands_b = dist_b.get_proper_literals() if type(dist_b) is not MultiAnd else dist_b.get_sub_propositions()

        ands = []

        for and_a in ands_a:
            for and_b in ands_b:
                ands += [OrProposition(and_a, and_b)]

        return MultiAnd(ands)

    def get_ors(self) -> list[Proposition]:
        new_ors = []
        for p in [self.proposition_a, self.proposition_b]:
            if type(p) is OrProposition or type(p) is MultiOr:
                new_ors += p.get_ors()
            elif type(p) is Variable or type(p) is NotProposition:
                new_ors += [p]
            else:
                raise ValueError(f"Cannot get ors from {p} {repr(p)}")

        return new_ors

    def merge_ors(self, debugger: Debugger=NoDebug()):
        return MultiOr(self.get_ors())

class ImplicationProposition(CompoundProposition):
    def ascii_operator(self):
        return '>'
    
    def infix_operator(self):
        return '=>'
    
    def evaluate(self, state):
        pa_evaluated = self.proposition_a.evaluate(state)
        return not pa_evaluated or (pa_evaluated and self.proposition_b.evaluate(state))

    def new_self(self, prop_a, prop_b):
        return ImplicationProposition(prop_a, prop_b)

    def remove_impl(self, debugger: Debugger=NoDebug()):
        return OrProposition(
            NotProposition(self.proposition_a),
            self.proposition_b
        ).remove_impl(debugger)

class BiimplicationProposition(CompoundProposition):
    def ascii_operator(self):
        return '='
    
    def infix_operator(self):
        return '<=>'
    
    def evaluate(self, state):
        return self.proposition_a.evaluate(state) == self.proposition_b.evaluate(state)

    def remove_biimpl(self, debugger: Debugger=NoDebug()):
        return OrProposition(
            AndProposition(self.proposition_a, self.proposition_b),
            AndProposition(NotProposition(self.proposition_a), NotProposition(self.proposition_b))
        ).remove_biimpl(debugger)

    def new_self(self, prop_a, prop_b):
        return BiimplicationProposition(prop_a, prop_b)

class SingularProposition(Proposition):
    def __init__(self, proposition_a: Proposition = None):
        super().__init__()
        self.proposition_a = proposition_a

    def ascii(self, ascii_func=AsciiInflictor.ascii_normal):
        if self.proposition_a == None:
            return self.ascii_operator() + "(incomplete proposition)"
        return self.ascii_operator() + "(" + ascii_func(self.proposition_a) + ")"

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
        return type(self.proposition_a) is Variable

    def new_self(self, prop_a: Proposition):
        raise NotImplementedError()
    
    def remove_biimpl(self, debugger: Debugger=NoDebug()):
        return self.new_self(self.proposition_a.remove_biimpl(debugger))

    def remove_impl(self, debugger: Debugger=NoDebug()):
        return self.new_self(self.proposition_a.remove_impl(debugger))

    def remove_nots(self, debugger: Debugger=NoDebug()):
        return self.new_self(self.proposition_a.remove_nots(debugger))

    def distribute_elements(self, debugger: Debugger=NoDebug()):
        return self

    def get_proper_literals(self):
        if self.is_literal():
            return [self]
        else:
            raise ValueError(f"Encountered a non-literal in {str(self)} {repr(self)}: {repr(p)}")

    def merge_ors(self, debugger: Debugger=NoDebug()):
        return self

    def tseitin_replace(self, variable_namer: VariableNamer, debugger: Debugger=NoDebug()):
        ands = []
        prop_sides = []

        p = self.proposition_a
        if type(p) is Variable:
            prop_sides += [p]
        else:
            (p_rename, p_ands) = p.tseitin_replace(variable_namer, debugger)
            ands += p_ands
            prop_sides += [p_rename]

        self_rename = Variable(variable_namer.next())
        prop = BiimplicationProposition(
            self_rename,
            self.new_self(prop_sides[0])
        )

        ands = [prop] + ands
        return (self_rename, ands)

class NotProposition(SingularProposition):
    def ascii_operator(self):
        return '~'
    
    def infix_operator(self):
        return '¬'
    
    def evaluate(self, state):
        return not self.proposition_a.evaluate(state)

    def get_literals(self):
        if type(self.proposition_a) is Variable:
            return [self]
        elif type(self.proposition_a) is NotProposition:
            return self.proposition_a.proposition_a.get_literals()
        else:
            return self.proposition_a.get_literals()

    def new_self(self, prop_a):
        return NotProposition(prop_a)

    def remove_nots(self, debugger: Debugger=NoDebug()):
        if type(self.proposition_a) is Variable:
            return self
        elif type(self.proposition_a) is NotProposition:
            return self.proposition_a.proposition_a.remove_nots(debugger)
        elif type(self.proposition_a) is AndProposition:
            return OrProposition(
                NotProposition(self.proposition_a.proposition_a),
                NotProposition(self.proposition_a.proposition_b)
            ).remove_nots(debugger)
        elif type(self.proposition_a) is OrProposition:
            return AndProposition(
                NotProposition(self.proposition_a.proposition_a),
                NotProposition(self.proposition_a.proposition_b)
            ).remove_nots(debugger)
        else:
            raise NotImplementedError()