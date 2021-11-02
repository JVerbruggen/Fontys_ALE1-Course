from proposition import *
from proposition_export import *
import os

prop = CompoundProposition(Operator.BIIMPL,
        CompoundProposition(Operator.IMPL,
            Variable('A'),
            Variable('B')
        ),
        CompoundProposition(Operator.OR,
            SingularProposition(Operator.NOT,
                Variable('A')
            ),
            Variable('C')
        )
    )

generator = GraphVizGenerator(prop)

def test_graphvizgenerator():
    string_contents = generator.generate()
    GraphVizGenerator.save_output(string_contents, "export/graph.dot")
    
    with open("export/graph.dot") as file:
        assert file.read() == string_contents

    assert os.path.isfile("export/graph.dot.png")
