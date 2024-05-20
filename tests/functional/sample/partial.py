# Copyright 2020-2024 Lynn Root
"""Sample module-level docs"""
import typing

from typing import overload


class Foo:
    """Foo class"""

    def __init__(self):
        """init method of Foo class"""
        self.foo = None

    def __str__(self):
        """a documented magic method."""
        pass

    def __repr__(self):
        pass

    def _semiprivate_documented(self):
        """a documented semipriate method"""
        pass

    def _semiprivate_undocumented(self):
        pass

    def __private(self):
        pass

    def method_foo(self):
        pass

    def get(self):
        pass

    async def get(self):
        pass

    @property
    def a_prop(self):
        pass

    @a_prop.setter
    def a_prop(self, x):
        pass

    @a_prop.deleter
    def a_prop(self):
        """A documented del property decorator"""

    @typing.overload
    def module_overload(a: None) -> None: ...

    @typing.overload
    def module_overload(a: int) -> int: ...

    def module_overload(a):
        """overloaded method implementation"""
        pass

    @overload
    def simple_overload(a: None) -> None: ...

    @overload
    def simple_overload(a: int) -> int: ...

    def simple_overload(a):
        """overloaded method implementation"""
        pass


def documented_top_level_func():
    """A documented top level function"""

    def documented_inner_func():
        """A documented inner function"""
        pass


def undocumented_top_level_func():
    def undocumented_inner_func():
        pass


class Bar:
    def method_bar(self):
        class InnerBar:
            pass


class _SemiprivateClass:
    pass


class __PrivateClass:
    pass
