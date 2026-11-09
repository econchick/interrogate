# Copyright 2020-2024 Lynn Root
"""Sample module-level docs"""


class Foo:
    """Foo class"""

    def do_it(self):
        """Do the thing!"""
        pass

    async def do_it_async(self):
        """Do the thing asynchronously!"""
        pass


class SpecialFoo(Foo):
    def do_it(self):
        pass

    async def do_it_async(self):
        pass


class ExtraSpecialFoo(SpecialFoo):
    def do_it(self):
        pass


class Undocumented:
    def do_it(self):
        pass
