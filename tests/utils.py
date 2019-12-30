from typing import TypeVar

from hypothesis.strategies import SearchStrategy

Domain = TypeVar('Domain')
Strategy = SearchStrategy


def identity(value: Domain) -> Domain:
    return value
