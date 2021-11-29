from debugger import *

class MockTracer:
    def __init__(self, expected_calls: int):
        self.expected_calls = expected_calls
        self.called = 0
        self.received = []
    
    def call(self, receiving):
        self.called += 1
        self.received += [receiving]

    def valid_call_count(self):
        return self.called == self.expected_calls

def test_debugger_tracing():
    mocktracer = MockTracer(expected_calls=2)
    debugger = Debugger(trace_function=(lambda x : mocktracer.call(x)))
    debugger.trace("test")
    debugger.trace("test2")
    assert mocktracer.valid_call_count()
    assert mocktracer.received == ["test", "test2"]

def test_debugger_analyzing():
    mocktracer = MockTracer(expected_calls=1)
    debugger = Debugger(analyzing_functions=[(lambda x : mocktracer.call(x))])
    debugger.analyse("3")

    assert mocktracer.valid_call_count()
    assert mocktracer.received == ["3"]