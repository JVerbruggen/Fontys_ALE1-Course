from proposition_operator import *
from proposition_operator_factory import *
from debugger import *

class Proposition:
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

    def output(self, state: dict) -> bool:
        raise NotImplementedError()

    def cnf(self, debugger=None) -> 'Proposition':
        raise NotImplementedError()

    def concat_sub_propositions(self, other: 'Proposition') -> list['Proposition']:
        return self.get_literals() + other.get_literals()

    def get_operator(self):
        raise NotImplementedError()

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

    def output(self, state: dict):
        if self.value in state.keys():
            return state[self.value]
        return False

    def cnf(self,debugger=None):
        return Variable(self.value)

    def __str__(self):
        return self.value

    def get_operator(self):
        raise NotImplementedError()

    def is_literal(self):
        return True

class ExtendedProposition(Proposition):
    def __init__(self, operator: CompoundOperator, propositions: list[Proposition]):
        super().__init__()
        self.operator = operator
        self.propositions = propositions

    def get_rational_equivalent(self, to_process=None):
        if to_process is None:
            to_process = self.propositions

        take = to_process[0]

        if len(to_process) == 2:
            return CompoundProposition(self.operator, take, to_process[1])
        elif len(to_process) < 2:
            raise ValueError()

        to_process = to_process[1:]

        return CompoundProposition(self.operator, take, self.get_rational_equivalent(to_process))
    
    def ascii(self):
        closing_brackets = 1

        operator_ascii = self.operator.ascii()
        ascii_string = operator_ascii + "(" + self.propositions[0].ascii() + ","
        for i in range(1,len(self.propositions)-1):
            prop = self.propositions[i]

            ascii_string += operator_ascii + "(" + prop.ascii() + ","

            closing_brackets += 1
        
        ascii_string += self.propositions[-1].ascii()

        ascii_string += ''.join(')' for _ in range(closing_brackets))

        return ascii_string

        # return self.operator.ascii() + "(" + ",".join([prop.ascii() for prop in self.propositions]) + ")"
    
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

    def get_literals(self):
        return self.propositions[:]

    def get_sub_propositions(self):
        return self.propositions[:]

    def cnf(self,debugger=None):
        if debugger is not None: debugger.analyse(self)
        return self.get_rational_equivalent().cnf(debugger)
        # raise Exception("CNF not available for extended proposition")

    def __str__(self):
        return self.ascii()
    
    def get_operator(self):
        return self.operator
    
    def is_literal(self):
        return False

class CompoundProposition(Proposition):
    def __init__(self, operator: CompoundOperator, proposition_a: Proposition = None, proposition_b: Proposition = None):
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

    def get_literals(self):
        return [self.proposition_a, self.proposition_b]

    def output(self, state):
        return self.operator.evaluate(self.proposition_a.output(state), self.proposition_b.output(state))

    def get_sub_propositions(self):
        return [self.proposition_a, self.proposition_b]

    def cnf(self,debugger=None):
        # Very not OOP, but if delegated to operator we would have circular import?
        operator_type = type(self.operator)
        if operator_type is AndOperator:
            pa_items = self.proposition_a.cnf(debugger).get_literals()
            pb_items = self.proposition_b.cnf(debugger).get_literals()
            res = ExtendedProposition(OperatorFactory[AndOperator], pa_items + pb_items)
            if debugger is not None: 
                debugger.trace(res.ascii())
                debugger.analyse(res)
            return res
        elif operator_type is OrOperator:
            # Something here is wrong
            and_props = []

            prop_a = self.proposition_a.cnf(debugger)
            prop_b = self.proposition_b.cnf(debugger)

            # all_literals = True
            # subs = prop_a.get_sub_propositions() + prop_b.get_sub_propositions()
            # for sub in subs:
            #     all_literals = sub.is_literal()
            #     if all_literals == False:
            #         break

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
                    and_props += [CompoundProposition(OperatorFactory[OrOperator], p_item, q_item)]

            if len(and_props) == 1:
                return and_props[0]

            res = ExtendedProposition(OperatorFactory[AndOperator], and_props)
            if debugger is not None: 
                debugger.trace(res.ascii())
                debugger.analyse(res)
            return res
        elif operator_type is ImplicationOperator:
            res = CompoundProposition(OperatorFactory[OrOperator], 
                SingularProposition(OperatorFactory[NotOperator], self.proposition_a).cnf(debugger), 
                self.proposition_b.cnf(debugger)
                )
            # res_cnf = res.cnf(debugger)
            if debugger is not None: 
                debugger.trace(res.ascii())
                debugger.analyse(res)
                # debugger.trace(res_cnf.ascii())
                # debugger.analyse(res_cnf)
            return res
            # return res_cnf
        elif operator_type is BiimplicationOperator:
            # res = CompoundProposition(OperatorFactory[OrOperator], 
            #     CompoundProposition(OperatorFactory[AndOperator], self.proposition_a.cnf(debugger), self.proposition_b.cnf(debugger)), 
            #     CompoundProposition(OperatorFactory[AndOperator], 
            #         SingularProposition(OperatorFactory[NotOperator], self.proposition_a).cnf(debugger), 
            #         SingularProposition(OperatorFactory[NotOperator], self.proposition_b).cnf(debugger)).cnf(debugger)
            # )
            res = CompoundProposition(OperatorFactory[AndOperator],
                CompoundProposition(OperatorFactory[OrOperator], SingularProposition(OperatorFactory[NotOperator], self.proposition_a), self.proposition_b),
                CompoundProposition(OperatorFactory[OrOperator], self.proposition_a, SingularProposition(OperatorFactory[NotOperator], self.proposition_b))
            )
            # res_cnf = res.cnf(debugger)
            if debugger is not None: 
                debugger.trace(res.ascii())
                debugger.analyse(res)
                # debugger.trace(res_cnf.ascii())
                # debugger.analyse(res_cnf)
            return res
            # return res_cnf
        raise Exception("Unsupported operator")

    def __str__(self):
        return self.operator.ascii() + "(" + str(self.proposition_a) + "," + str(self.proposition_b) + ")"
    
    def get_operator(self):
        return self.operator

    def is_literal(self):
        return False

class SingularProposition(Proposition):
    def __init__(self, operator: SingularOperator, proposition_a: Proposition = None):
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

    def get_sub_propositions(self):
        return [self.proposition_a]

    def get_literals(self):
        if type(self.operator) is NotOperator:
            if type(self.proposition_a) is Variable:
                return [self]
            elif type(self.proposition_a) is SingularProposition:
                return [self.proposition_a.proposition_a.get_literals()]
        raise Exception("Literals not supported in this case")

    def output(self, state):
        return self.operator.evaluate(self.proposition_a.output(state))

    def cnf(self,debugger=None):
        # Very not OOP, but if delegated to operator we would have circular import?
        operator_type = type(self.operator)
        if operator_type is NotOperator:
            pa_type = type(self.proposition_a)
            if pa_type is Variable:
                return self
            elif pa_type is SingularProposition:
                pa_operator_type = type(self.proposition_a.get_operator())
                if pa_operator_type is NotOperator:
                    return self.proposition_a.proposition_a.cnf(debugger)
                raise Exception("Unsupported operator")
            elif pa_type is CompoundProposition:
                pa_operator_type = type(self.proposition_a.get_operator())
                if pa_operator_type is AndOperator:
                    pa = self.proposition_a.proposition_a
                    pb = self.proposition_a.proposition_b
                    res = CompoundProposition(OperatorFactory[OrOperator],
                        SingularProposition(OperatorFactory[NotOperator], pa),
                        SingularProposition(OperatorFactory[NotOperator], pb)
                        )
                    res_cnf = res.cnf(debugger)
                    if debugger is not None: 
                        debugger.trace(res.ascii())
                        debugger.analyse(res)
                        debugger.trace(res_cnf.ascii())
                        debugger.analyse(res_cnf)
                    return res_cnf
                elif pa_operator_type is OrOperator:
                    pa = self.proposition_a.proposition_a
                    pb = self.proposition_a.proposition_b
                    res = CompoundProposition(OperatorFactory[AndOperator],
                        SingularProposition(OperatorFactory[NotOperator], pa),
                        SingularProposition(OperatorFactory[NotOperator], pb)
                        )
                    res_cnf = res.cnf(debugger)
                    if debugger is not None: 
                        debugger.trace(res.ascii())
                        debugger.analyse(res)
                        debugger.trace(res_cnf.ascii())
                        debugger.analyse(res_cnf)
                    return res_cnf
                raise Exception("Unsupported operator")
            raise Exception("Unsupported operator")    
        raise Exception("Unrecognized singular operator in cnf conversion")

    def __str__(self):
        return self.operator.ascii() + "(" + str(self.proposition_a) + ")"
    
    def get_operator(self):
        return self.operator

    def is_literal(self):
        return self.proposition_a.is_literal() # ~(A) is also a literal

class PropositionFactory:
    def generate_proposition(operator: Operator) -> Proposition:
        if operator.is_compound():
            return CompoundProposition(operator)
        else:
            return SingularProposition(operator)