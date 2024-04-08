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
        """a magic method."""
        pass

    def _semiprivate(self):
        """a semipriate method"""
        pass

    def __private(self):
        """a private method"""
        pass

    def method_foo(self):
        """this method does foo"""
        pass

    def get(self):
        """this method gets something"""
        pass

    async def get(self):
        """this async method gets something"""
        pass

    @property
    def prop(self):
        """this method has a get property decorator"""
        pass

    @prop.setter
    def prop(self):
        """this method has a set property decorator"""
        pass

    @prop.deleter
    def prop(self):
        """this method as a del property decorator"""
        pass

    @typing.overload
    def module_overload(a: None) -> None:
        """overloaded method"""
        ...

    @typing.overload
    def module_overload(a: int) -> int:
        """overloaded method"""
        ...

    def module_overload(a):
        """overloaded method implementation"""
        pass

    @overload
    def simple_overload(a: None) -> None:
        """overloaded method"""
        ...

    @overload
    def simple_overload(a: int) -> int:
        """overloaded method"""
        ...

    def simple_overload(a):
        """overloaded method implementation"""
        pass


def top_level_func():
    """A top level function"""

    def inner_func():
        """A inner function"""
        pass


class Bar:
    """Bar class"""

    def method_bar(self):
        """a method that does bar"""

        class InnerBar:
            """an inner class"""

            pass


class _SemiprivateClass:
    """a semiprivate class"""

    pass


class __PrivateClass:
    """a private class"""

    pass


# Coverage % for InitDocs should be the same as ClassDocs
class InitDocs:
    def __init__(self):
        """A docstring for init"""
        pass


# Coverage % for ClassDocs should be the same as InitDocs
class ClassDocs:
    """A docstring for a class"""

    def __init__(self):
        pass
