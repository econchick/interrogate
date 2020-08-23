# Copyright 2020 Lynn Root
"""Sample module-level docs"""


class Foo(object):
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


def top_level_func():
    """A top level function"""

    def inner_func():
        """A inner function"""
        pass


class Bar(object):
    """Bar class"""

    def method_bar(self):
        """a method that does bar"""

        class InnerBar(object):
            """an inner class"""

            pass


class _SemiprivateClass(object):
    """a semiprivate class"""

    pass


class __PrivateClass(object):
    """a private class"""

    pass
