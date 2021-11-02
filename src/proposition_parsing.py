from proposition import *

class PropositionParser:
    def set_childproposition(parent_proposition: Proposition, location, child_proposition: Proposition):
        if location == "a":
            parent_proposition.proposition_a = child_proposition
        elif location == "b":
            parent_proposition.proposition_b = child_proposition
            
    def __init__(self, ascii_string):
        self.error = None
        self.final_proposition = None
        self.cursor = -1
        self.proposition_stack = []
        self.expecting = "a"                            # Expect a single proposition as a whole
        self.characters = [c for c in ascii_string]
        self.lenc = len(self.characters)
        self.used = False                               # Can only be read once
    
    # ----------------------------------------------------------------
    # Incoming proposition is set as 'final' proposition (highest position)
    #   or is set as parent from proposition that is last on the stack
    # ----------------------------------------------------------------
    def process_proposition(self, proposition, exp):
        parent_proposition = self.proposition_stack[-1] if len(self.proposition_stack) > 0 else None
        if parent_proposition is None:
            self.final_proposition = proposition
        else:
            PropositionParser.set_childproposition(parent_proposition, exp, proposition)

    # ----------------------------------------------------------------
    # Removes first char from expected chars as cursor moves
    # ----------------------------------------------------------------
    def expecting_iteration(self):
        self.expecting = self.expecting[1:]

    # ----------------------------------------------------------------
    # Reads ascii string that is given in the constructor argument
    # ----------------------------------------------------------------
    def read(self) -> Proposition:
        if self.used:
            print("Error: Parser already read")
            return None
        self.used = True

        while self.cursor < self.lenc-1:
            self.cursor += 1

            char = self.characters[self.cursor] # Pick character on cursor for reading
            if char == " ":                     # Ignore all spaces
                continue

            exp = self.expecting[0]             # Check expected value: 'a' and 'b' are propositions, '(' and ',' are checked but basically ignored, ')' pops proposition stack
            if exp in ['a', 'b']:
                char_operator = Operator.get_operator(char)                     # Check if char is operator
                if char_operator != None:
                    proposition = Operator.generate_proposition(char_operator)
                    self.process_proposition(proposition, exp)
                    self.proposition_stack += [proposition]

                    if type(proposition) is CompoundProposition:                        # Expect two propositions to be next
                        self.expecting = "(a,b)" + self.expecting[1:]
                    else:                                                               # or expect one
                        self.expecting = "(a)" + self.expecting[1:]

                    continue
                if char.isalpha():                                              # Check if char is variable
                    proposition = Variable(char)
                    self.process_proposition(proposition, exp)

                    self.expecting_iteration()
                    continue
                                                                                # Else string is invalid
                self.error = "Invalid character at position " + self.cursor + ": '" + char + "'" 
                break
            elif exp == "(" and char == "(":
                self.expecting_iteration()
                continue
            elif exp == "," and char == ",":
                self.expecting_iteration()
                continue
            elif exp == ")" and char == ")":
                self.proposition_stack.pop()
                self.expecting_iteration()
                continue
            else:
                break
        
        if self.error != None:
            print(self.error)
            return None

        return self.final_proposition


            