# Copyright 2020 Lynn Root
# intentionally no docstrings here


class ChildFoo(object):
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


class ChildBar(object):
    def method_bar(self):
        class InnerBar(object):
            pass

        return InnerBar


class _ChildBaz(object):
    pass


class __ChildBla(object):
    pass
