from proposition import *

class PropositionFactory:
    known_operators = {'&': AndProposition, '|': OrProposition, '>': ImplicationProposition, '=': BiimplicationProposition, '~': NotProposition}

    def exists(char: str) -> bool:
        return char in PropositionFactory.known_operators.keys()
    
    def get_proposition(char: str) -> Proposition:
        if PropositionFactory.exists(char) == False: 
            return None
        return PropositionFactory.known_operators[char]()