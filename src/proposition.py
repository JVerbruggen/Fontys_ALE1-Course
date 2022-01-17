from debugger import *
from ascii_inflictor import *

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

    def cnf_inner(self, debugger: Debugger=NoDebug()) -> 'Proposition':
        raise NotImplementedError()

    # def cnf(self, debugger: Debugger=NoDebug()) -> 'Proposition':
    #     debugger.trace("start with: " + self.ascii_complex())
    #     debugger.analyse(self)

    #     res = self.cnf_inner(debugger=debugger)
    #     debugger.trace("before contradiction removal: " + res.ascii_complex())
    #     debugger.analyse(res)

    #     res = res.remove_contradictions()

    #     debugger.trace("after contradiction removal: " + res.ascii_complex())
    #     debugger.analyse(res)

    #     return res

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

    def is_always_true_or_false(self, debugger: Debugger=NoDebug()) -> bool:
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

    def cnf_inner(self,debugger=NoDebug()):
        return Variable(self.value)

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

    # def cnf(self,debugger=NoDebug()):
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
    
    def cnf_inner(self,debugger=NoDebug()):
        props = self.get_sub_propositions()
        props = [p.cnf_inner(debugger) for p in props]
        return MultiAnd(props)

    def cnf_notation(self):
        raise NotImplementedError()

    def remove_contradictions(self, debugger: Debugger=NoDebug()):
        return MultiAnd([p for p in self.propositions if p.is_always_true_or_false() == False])
    
    def absorb(self, other: 'MultiAnd'):
        return MultiAnd(self.propositions + other.propositions)

    def cnf_notation(self):
        return "[ " + " , ".join([prop.cnf_notation() for prop in self.propositions]) + " ]"
    
    def new_self(self, props: list[Proposition]):
        return MultiAnd(props)

    def distribute_elements(self, debugger: Debugger=NoDebug()):
        ands = []
        for p in self.propositions:
            ands += [p.distribute_elements(debugger)]

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
    
    def cnf_inner(self,debugger=NoDebug()):
        props = self.get_sub_propositions()
        props = [p.cnf_inner(debugger) for p in props]
        return MultiOr(props)

        # props = self.get_sub_propositions()
        # if len(props) != 2:
        #     raise NotImplementedError()

        # return OrProposition(props[0], prop[1]).cnf_inner(debugger)

    def is_always_true_or_false(self, debugger: Debugger=NoDebug()) -> bool:
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

    def distribute_elements(self, debugger: Debugger=NoDebug()):
        raise NotImplementedError("MultiOr doesnt support distribution")

        # if len(self.propositions) < 2:
        #     raise ValueError("This MultiOr has less than 2 propositions")

        # ands = []
        # for i,prop in enumerate(self.propositions):
        #     ands_here = prop.distribute_elements(debugger).get_proper_literals()
        #     if i == 0:
        #         ands += ands_here
        #         continue

        #     ands_new = []
        #     for a in ands:
        #         for b in ands_here:
        #             ands_new += [OrProposition(a, b)]
            
        #     ands = ands_new

        # return MultiAnd(ands)

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

class AndProposition(CompoundProposition):
    def ascii_operator(self):
        return '&'

    def infix_operator(self):
        return '∧'

    def evaluate(self, state):
        return self.proposition_a.evaluate(state) and self.proposition_b.evaluate(state)
    
    def cnf_inner(self,debugger=NoDebug()):
        if self.proposition_a == None or self.proposition_b == None:
            raise ValueError("Propositions in strategies not defined")

        pa = self.proposition_a.cnf_inner(debugger)
        pb = self.proposition_b.cnf_inner(debugger)

        and_props = list()
        for prop in [pa, pb]:                   # merge child ands into itself
            if type(prop) is AndProposition:
                and_props += [prop.proposition_a, prop.proposition_b]
            elif type(prop) is MultiAnd:
                and_props += prop.propositions
            else:
                and_props += [prop]


        return MultiAnd(and_props)
        # pa_items = self.proposition_a.cnf_inner(debugger).get_literals()
        # pb_items = self.proposition_b.cnf_inner(debugger).get_literals()
        # res = MultiAnd(pa_items + pb_items)
        # if debugger is not None: 
        #     debugger.trace(res.ascii_complex())
        #     debugger.analyse(res)
        # return res

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
    
    def cnf_inner(self,debugger=NoDebug()):
        and_props = []

        prop_a = self.proposition_a.cnf_inner(debugger)
        prop_b = self.proposition_b.cnf_inner(debugger)

        if type(prop_a) is not AndProposition and type(prop_a) is not MultiAnd and prop_a.is_literal() == False:
            raise ValueError(f"Expected AndProposition, MultiAnd or literal at prop_a 'or' CNF but got: {type(prop_a)} ({prop_a})")
        if type(prop_b) is not AndProposition and type(prop_b) is not MultiAnd and prop_b.is_literal() == False:
            raise ValueError(f"Expected AndProposition, MultiAnd or literal at prop_b 'or' CNF but got: {type(prop_b)} ({prop_b})")

        p_items = prop_a.get_literals()
        q_items = prop_b.get_literals()

        if debugger is not None:
            debugger.analyse(self)
            debugger.trace("OR1: " + str(prop_a.ascii_complex()))
            debugger.trace("OR2: " + str(prop_b.ascii_complex()))
            # debugger.trace("LIT: " + str([x.ascii_complex() for x in p_items + q_items]))


        for p_item in p_items:
            for q_item in q_items:
                adding = []

                for item in [p_item, q_item]:
                    if item.is_literal():
                        adding += [item]
                    elif type(item) is OrProposition or type(item) is MultiOr:
                        adding += item.get_sub_propositions()
                

                and_props += [MultiOr(adding)]

        # if len(and_props) == 1:
        #     return and_props[0]

        res = MultiAnd(and_props)
        # Dont CNF this, only CNF its children
        if debugger is not None: 
            debugger.trace(res.ascii_complex())
            debugger.analyse(res)
        return res
    
    def is_always_true_or_false(self, debugger: Debugger=NoDebug()) -> bool:
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
    
    def cnf_inner(self,debugger=NoDebug()):
        res = OrProposition(NotProposition(self.proposition_a), 
            self.proposition_b
            )
        res_cnf = res.cnf_inner(debugger)
        if debugger is not None: 
            debugger.trace(res.ascii_complex())
            debugger.analyse(res)
            debugger.trace(res_cnf.ascii_complex())
            debugger.analyse(res_cnf)
        # return res
        return res_cnf

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

    def cnf_inner(self,debugger=NoDebug()):
        reformat = OrProposition(
            AndProposition(
                self.proposition_a,
                self.proposition_b
            ),
            AndProposition(
                NotProposition(self.proposition_a),
                NotProposition(self.proposition_b)
            )
        )
        res = reformat.cnf_inner(debugger)
        if debugger is not None: 
            debugger.trace(res.ascii_complex())
            debugger.analyse(res)
        return res

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

class NotProposition(SingularProposition):
    def ascii_operator(self):
        return '~'
    
    def infix_operator(self):
        return '¬'
    
    def evaluate(self, state):
        return not self.proposition_a.evaluate(state)
    
    def cnf_inner(self,debugger=NoDebug()):
        # Very not OOP, but if delegated to operator we would have circular import?
        pa_type = type(self.proposition_a)
        if pa_type is Variable:
            return self
        elif issubclass(pa_type, SingularProposition):
            return self.proposition_a.proposition_a.cnf_inner(debugger)
        elif issubclass(pa_type, CompoundProposition):
            if pa_type is AndProposition:
                pa = self.proposition_a.proposition_a
                pb = self.proposition_a.proposition_b
                res = OrProposition(
                    NotProposition(pa),
                    NotProposition(pb)
                    )
                res_cnf = res.cnf_inner(debugger)
                debugger.trace("in NOT (and): " + res.ascii_complex())
                debugger.analyse(res)
                debugger.trace("in NOT after (and): " + res_cnf.ascii_complex())
                debugger.analyse(res_cnf)
                return res_cnf
            elif pa_type is OrProposition:
                pa = self.proposition_a.proposition_a
                pb = self.proposition_a.proposition_b
                res = AndProposition(
                    NotProposition(pa),
                    NotProposition(pb)
                    )
                res_cnf = res.cnf_inner(debugger)
                debugger.trace("in NOT (or): " + res.ascii_complex())
                debugger.analyse(res)
                debugger.trace("in NOT after (or): " + res_cnf.ascii_complex())
                debugger.analyse(res_cnf)
                return res_cnf
            else:
                return NotProposition(self.proposition_a.cnf_inner(debugger)).cnf_inner(debugger)
            raise Exception("Unsupported operator")
        elif issubclass(pa_type, ExtendedProposition): 
            old_props = self.proposition_a.get_sub_propositions()
            props = [NotProposition(p) for p in old_props]
            res = MultiAnd(props) if pa_type == MultiOr else MultiOr(props)
            res_cnf = res.cnf()

            if debugger is not None: 
                debugger.trace("in NOT (extended): " + res.ascii_complex())
                debugger.analyse(res)
                debugger.trace("in NOT after (extended): " + res_cnf.ascii_complex())
                debugger.analyse(res_cnf)
            
            return res_cnf
        raise Exception("Unsupported operator")     

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