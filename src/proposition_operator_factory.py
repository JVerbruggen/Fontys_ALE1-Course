from proposition_operator import *

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

    def __class_getitem__(cls, type):
        return OperatorFactory.operator_storage[type]