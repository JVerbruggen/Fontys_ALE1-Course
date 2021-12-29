class Debugger:
    def __init__(self, trace_function=None, analyzing_functions=[]):
        self.trace_function = trace_function
        self.analyzing_functions = analyzing_functions

    def analyse(self, instance):
        for func in self.analyzing_functions:
            func(instance)

    def trace(self, msg):
        if self.trace_function is not None:
            self.trace_function(msg)

class NoDebug(Debugger):
    def __init__(self):
        pass

    def analyse(self, instance):
        pass

    def trace(self, msg):
        pass