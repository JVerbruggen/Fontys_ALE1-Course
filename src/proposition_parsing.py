from proposition import *
from proposition_factory import *

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
        self.expecting = "a"                            # Expect a single proposition as a result
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
                is_operator = PropositionFactory.exists(char)                    # Check if char is operator
                if is_operator:
                    proposition = PropositionFactory.get_proposition(char)
                    self.process_proposition(proposition, exp)
                    self.proposition_stack += [proposition]

                    if issubclass(type(proposition), CompoundProposition):                        # Expect two propositions to be next
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

class PropositionCNFFormatParser:
    def __init__(self, cnf_format_string: str):
        self.error = False
        self.proposition_stack = []
        self.cnf_props = []
        self.expecting = "[e]"
        self.characters = [c for c in cnf_format_string]
        self.var_dict = dict()

    def get_var(self, var_name: str) -> Variable:
        if var_name in self.var_dict:
            return self.var_dict[var_name]
        elif var_name.upper() in self.var_dict:
            return NotProposition(self.var_dict[var_name.upper()])
        else:
            var = Variable(var_name.upper())
            self.var_dict[var_name.upper()] = var
            if var_name.isupper():
                return var
            else:
                return NotProposition(var)

    def raise_error(self, error: str):
        self.error = True
        raise ValueError(error)

    def process_prop_stack(self):
        if len(self.proposition_stack) == 1:
            self.cnf_props += self.proposition_stack
        elif len(self.proposition_stack) > 1:
            self.cnf_props += [MultiOr(self.proposition_stack)]

        self.proposition_stack = []

    def read(self) -> Proposition:
        for c in self.characters:
            if c == ' ':
                continue
            elif self.expecting[0] == '[':
                if c == "[":
                    self.expecting = self.expecting[1:]
                    continue
                else:
                    self.raise_error(f"Expected [ but got '{c}'")
            elif self.expecting[0] == ']':
                if c == ",":
                    self.expecting = "e]"
                elif c == "]":
                    self.expecting = self.expecting[1:]
                else:
                    self.raise_error(f"Expected ] but got '{c}'")

                self.process_prop_stack()

                continue
            elif self.expecting[0] == "e":
                if c.isalpha():
                    self.proposition_stack += [self.get_var(c)]
                elif c == "," or c == "]":
                    self.process_prop_stack()
                    continue
                else:
                    self.raise_error(f"Expected e but got '{c}'")
            else:
                self.raise_error(f"Unknown expected value {self.expecting[0]}")
                break
    
        return MultiAnd(self.cnf_props)

            