from proposition import *

class GraphVizGenerator():
    def __init__(self, proposition: Proposition):
        self.proposition = proposition

    def generate(self):
        stack = [(self.proposition, None)]

        nodes_str = "  node [ fontname = \"Arial\" ]\n"

        node_nr_incr = 1
        while len(stack) > 0:
            (prop, parent) = stack[0]
            stack = stack[1:]

            nodename = "node" + str(node_nr_incr)
            node_nr_incr+=1

            if parent is not None:
                nodes_str += "  " + parent + " -- " + nodename + "\n"

            if type(prop) == CompoundProposition:
                operator = prop.operator.ascii()
                stack = [(prop.proposition_b, nodename)] + stack
                stack = [(prop.proposition_a, nodename)] + stack

                nodes_str += "  " + nodename + " [ label = \"" + operator + "\" ]\n"
            elif type(prop) == SingularProposition:
                operator = prop.operator.ascii()
                stack = [(prop.proposition_a, nodename)] + stack

                nodes_str += "  " + nodename + " [ label = \"" + operator + "\" ]\n"
            elif type(prop) == Variable:
                nodes_str += "  " + nodename + " [ label = \"" + prop.value + "\" ]\n"
            else:
                nodes_str += "  " + nodename + " [ UNKOWN ]\n"

        return "graph logic {\n" + nodes_str + "}"



