# Copyright 2020-2024 Lynn Root
# intentionally no docstrings here


class ChildFoo:
    def __init__(self):
        self.foo = None

    def __str__(self):
        pass

    def _ignore_me(self):
        pass

    def __ignore_me_too(self):
        pass

    def method_foo(self):
        pass


def a_child_func():
    pass


class ChildBar:
    def method_bar(self):
        class InnerBar:
            pass

        return InnerBar


class _ChildBaz:
    pass


class __ChildBla:
    pass
