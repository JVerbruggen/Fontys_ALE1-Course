from proposition_factory import *
from proposition import *

def test_propositions():
    assert PropositionFactory.exists('&') == True
    assert PropositionFactory.exists('|') == True
    assert PropositionFactory.exists('>') == True
    assert PropositionFactory.exists('=') == True
    assert PropositionFactory.exists('~') == True
    assert PropositionFactory.exists('#') == False
    assert PropositionFactory.exists('$') == False
    assert PropositionFactory.exists('%') == False
    assert PropositionFactory.exists('a') == False
    assert PropositionFactory.exists('b') == False

def test_get_proposition():
    assert type(PropositionFactory.get_proposition('&')) is AndProposition
    assert type(PropositionFactory.get_proposition('|')) is OrProposition
    assert type(PropositionFactory.get_proposition('=')) is BiimplicationProposition
    assert type(PropositionFactory.get_proposition('>')) is ImplicationProposition
    assert type(PropositionFactory.get_proposition('~')) is NotProposition

    assert type(PropositionFactory.get_proposition('&')) is not CompoundProposition
    assert type(PropositionFactory.get_proposition('|')) is not CompoundProposition
    assert type(PropositionFactory.get_proposition('=')) is not CompoundProposition
    assert type(PropositionFactory.get_proposition('>')) is not CompoundProposition

