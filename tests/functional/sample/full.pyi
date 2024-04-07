# Copyright 2024 Lynn Root
"""Sample stub with docs"""
import typing

from typing import overload


class Foo:
    """Foo class"""

    def __init__(self) -> None:
        """init method of Foo class"""

    def __str__(self) -> None:
        """a magic method."""

    def _semiprivate(self) -> None:
        """a semipriate method"""

    def __private(self) -> None:
        """a private method"""

    def method_foo(self) -> None:
        """this method does foo"""

    def get(self) -> None:
        """this method gets something"""

    async def get(self) -> None:
        """this async method gets something"""

    @property
    def prop(self) -> None:
        """this method has a get property decorator"""

    @prop.setter
    def prop(self) -> None:
        """this method has a set property decorator"""

    @prop.deleter
    def prop(self) -> None:
        """this method as a del property decorator"""

    @typing.overload
    def module_overload(a: None) -> None:
        """overloaded method"""

    @typing.overload
    def module_overload(a: int) -> int:
        """overloaded method"""

    def module_overload(a: str) -> str:
        """overloaded method implementation"""

    @overload
    def simple_overload(a: None) -> None:
        """overloaded method"""

    @overload
    def simple_overload(a: int) -> int:
        """overloaded method"""

    def simple_overload(a: str) -> str:
        """overloaded method implementation"""

def top_level_func() -> None:
    """A top level function"""

    def inner_func() -> None:
        """A inner function"""

class Bar:
    """Bar class"""

    def method_bar(self) -> None:
        """a method that does bar"""

        class InnerBar:
            """an inner class"""

class _SemiprivateClass:
    """a semiprivate class"""

class __PrivateClass:
    """a private class"""

# Coverage % for InitDocs should be the same as ClassDocs
class InitDocs:
    def __init__(self) -> None:
        """A docstring for init"""

# Coverage % for ClassDocs should be the same as InitDocs
class ClassDocs:
    """A docstring for a class"""

    def __init__(self) -> None:
        pass
