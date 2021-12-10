from proposition import *
from proposition_operator_factory import OperatorFactory
from debugger import *

class CNFStrategy:
    def get_result(self) -> Proposition:
        raise NotImplementedError()

class CompoundPropositionStrategy(CNFStrategy):
    def set_propositions(self, a: Proposition, b: Proposition):
        self.proposition_a = a
        self.proposition_b = b

class SingularPropositionStrategy(CNFStrategy):
    def set_propositions(self, a: Proposition):
        self.proposition = a

class AndStrategy(CompoundPropositionStrategy):
    def __init__(self, debugger):
        self.debugger = debugger

    def get_result(self):
        if self.proposition_a == None or self.proposition_b == None:
            raise ValueError("Propositions in strategies not defined")

        pa_items = self.proposition_a.cnf(self.debugger).get_literals()
        pb_items = self.proposition_b.cnf(self.debugger).get_literals()
        res = ExtendedProposition(OperatorFactory.get_operator('&'), pa_items + pb_items)
        if self.debugger is not None: 
            self.debugger.trace(res.ascii())
            self.debugger.analyse(res)
        return res

class OrStrategy(CompoundPropositionStrategy):
    def __init__(self, debugger):
        self.debugger = debugger

    def get_result(self):
        # Something here is wrong
        and_props = []

        prop_a = self.proposition_a.cnf(self.debugger)
        prop_b = self.proposition_b.cnf(self.debugger)

        # all_literals = True
        # subs = prop_a.get_sub_propositions() + prop_b.get_sub_propositions()
        # for sub in subs:
        #     all_literals = sub.is_literal()
        #     if all_literals == False:
        #         break

        p_items = prop_a.get_literals()
        q_items = prop_b.get_literals()

        if self.debugger is not None:
            self.debugger.analyse(self)
            self.debugger.trace("OR1: " + str(prop_a.ascii()))
            self.debugger.trace("OR2: " + str(prop_b.ascii()))
            self.debugger.trace("LIT: " + str([x.ascii() for x in p_items + q_items]))
            self.debugger.trace("OR2: " + str(prop_b.ascii()))


        for p_item in p_items:
            for q_item in q_items:
                and_props += [CompoundProposition(OperatorFactory.get_operator('|'), p_item, q_item)]

        if len(and_props) == 1:
            return and_props[0]

        res = ExtendedProposition(OperatorFactory.get_operator('&'), and_props)
        if self.debugger is not None: 
            self.debugger.trace(res.ascii())
            self.debugger.analyse(res)
        return res
    
class ImplicationStrategy(CompoundPropositionStrategy):
    def __init__(self, debugger):
        self.debugger = debugger

    def get_result(self):
        res = CompoundProposition(OperatorFactory.get_operator('|'), 
            SingularProposition(OperatorFactory.get_operator('~'), self.proposition_a).cnf(self.debugger), 
            self.proposition_b.cnf(self.debugger)
            )
        # res_cnf = res.cnf(debugger)
        if self.debugger is not None: 
            self.debugger.trace(res.ascii())
            self.debugger.analyse(res)
            # debugger.trace(res_cnf.ascii())
            # debugger.analyse(res_cnf)
        return res
        # return res_cnf

class BiimplicationStrategy(CompoundPropositionStrategy):
    def __init__(self, debugger):
        self.debugger = debugger

    def get_result(self):
        res = CompoundProposition(OperatorFactory.get_operator('&'),
            CompoundProposition(OperatorFactory.get_operator('|'), SingularProposition(OperatorFactory.get_operator('~'), self.proposition_a), self.proposition_b),
            CompoundProposition(OperatorFactory.get_operator('|'), self.proposition_a, SingularProposition(OperatorFactory.get_operator('~'), self.proposition_b))
        )
        # res_cnf = res.cnf(debugger)
        if self.debugger is not None: 
            self.debugger.trace(res.ascii())
            self.debugger.analyse(res)
            # debugger.trace(res_cnf.ascii())
            # debugger.analyse(res_cnf)
        return res

class NotStrategy(SingularPropositionStrategy()):
    def __init__(self, debugger):
        self.debugger = debugger

    def get_result(self):
        raise NotImplementedError()
    
