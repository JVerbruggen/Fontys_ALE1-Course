from proposition import *

class PropositionAnalysis:
    def get_variables(prop: Proposition):
        variables = []
        queue = [prop]
        
        while len(queue) > 0:
            prop = queue[0]
            queue = queue[1:]

            if type(prop) is CompoundProposition:
                queue += [prop.proposition_a, prop.proposition_b]
            elif type(prop) is SingularProposition:
                queue += [prop.proposition_a]
            elif type(prop) is Variable:
                if prop.value not in variables:
                    variables += [prop.value]
        
        return variables
