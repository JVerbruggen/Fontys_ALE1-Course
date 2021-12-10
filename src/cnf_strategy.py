from proposition import *
from proposition_operator_factory import *
from debugger import *

class CNFStrategy:
    def get_result(self) -> Proposition:
        raise NotImplementedError()

class AndStrategy(CNFStrategy):
    def __init__(self, proposition_a, proposition_b, debugger=None):
        self.proposition_a = proposition_a
        self.proposition_b = proposition_b
        self.debugger = debugger

    def get_result(self):
        pa_items = self.proposition_a.cnf(debugger).get_literals()
        pb_items = self.proposition_b.cnf(debugger).get_literals()
        res = ExtendedProposition(OperatorFactory[AndOperator], pa_items + pb_items)
        if debugger is not None: 
            debugger.trace(res.ascii())
            debugger.analyse(res)
        return res
    
