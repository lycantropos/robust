from typing import TypeVar

from hypothesis.strategies import SearchStrategy

Domain = TypeVar('Domain')
Strategy = SearchStrategy


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def identity(value: Domain) -> Domain:
    return value
