# Copyright 2020-2024 Lynn Root
"""AST traversal for finding docstrings."""
from __future__ import annotations

import ast
import os

from typing import Union

import attr

from interrogate.config import InterrogateConfig


DocumentableFunc = Union[ast.AsyncFunctionDef, ast.FunctionDef]
DocumentableFuncOrClass = Union[DocumentableFunc, ast.ClassDef]
DocumentableNode = Union[DocumentableFuncOrClass, ast.Module]


@attr.s(eq=False)
class CovNode:
    """Coverage of an AST Node.

    :param str name: Name of node (module, class, method or function
        names).
    :param str path: Pseudo-import path to node (i.e. ``sample.py:
        MyClass.my_method``).
    :param int level: Level of recursiveness/indentation
    :param int lineno: Line number of class, method, or function.
    :param bool covered: Has a docstring
    :param str node_type: type of node (e.g "module", "class", or
        "function").
    :param bool is_nested_func: if the node itself is a nested function
        or method.
    :param bool is_nested_cls: if the node itself is a nested class.
    :param CovNode _parent: parent node of current CovNode, if any.
    """

    name: str = attr.ib()
    path: str = attr.ib()
    level: int = attr.ib()
    lineno: int | None = attr.ib()
    covered: bool = attr.ib()
    node_type: str = attr.ib()
    is_nested_func: bool = attr.ib()
    is_nested_cls: bool = attr.ib()
    parent: CovNode | None = attr.ib()


class CoverageVisitor(ast.NodeVisitor):
    """NodeVisitor for a Python file to find docstrings.

    :param str filename: filename to parse coverage.
    :param config.InterrogateConfig config: configuration.
    """

    def __init__(self, filename: str, config: InterrogateConfig):
        self.filename = filename
        self.config = config
        self.stack: list[CovNode] = []
        self.nodes: list[CovNode] = []

    @staticmethod
    def _has_doc(node: DocumentableNode) -> bool:
        """Return if node has docstrings."""
        return (
            ast.get_docstring(node) is not None
            and ast.get_docstring(node).strip() != ""  # type: ignore
        )

    def _visit_helper(self, node: DocumentableNode) -> None:
        """Recursively visit AST node for docstrings."""
        if not hasattr(node, "name"):
            node_name = os.path.basename(self.filename)
        else:
            node_name = node.name

        parent = None
        path = node_name

        if self.stack:
            parent = self.stack[-1]
            parent_path = parent.path
            if parent_path.endswith(".py"):
                path = parent_path + ":" + node_name
            else:
                path = parent_path + "." + node_name

        lineno = None
        if hasattr(node, "lineno"):
            lineno = node.lineno

        node_type = type(node).__name__
        cov_node = CovNode(
            name=node_name,
            path=path,
            covered=self._has_doc(node),
            level=len(self.stack),
            node_type=node_type,
            lineno=lineno,
            is_nested_func=self._is_nested_func(parent, node_type),
            is_nested_cls=self._is_nested_cls(parent, node_type),
            parent=parent,
        )
        self.stack.append(cov_node)
        self.nodes.append(cov_node)

        self.generic_visit(node)

        self.stack.pop()

    def _is_nested_func(self, parent: CovNode | None, node_type: str) -> bool:
        """Is node a nested func/method of another func/method."""
        if parent is None:
            return False
        # is it a nested function?
        if parent.node_type == "FunctionDef" and node_type == "FunctionDef":
            return True
        return False

    def _is_nested_cls(self, parent: CovNode | None, node_type: str) -> bool:
        """Is node a nested func/method of another func/method."""
        if parent is None:
            return False
        # is it a nested class?
        if (
            parent.node_type in ("ClassDef", "FunctionDef")
            and node_type == "ClassDef"
        ):
            return True
        return False

    def _is_private(self, node: DocumentableFuncOrClass) -> bool:
        """Is node private (i.e. __MyClass, __my_func)."""
        if node.name.endswith("__"):
            return False
        if not node.name.startswith("__"):
            return False
        return True

    def _is_semiprivate(self, node: DocumentableFuncOrClass) -> bool:
        """Is node semiprivate (i.e. _MyClass, _my_func)."""
        if node.name.endswith("__"):
            return False
        if node.name.startswith("__"):
            return False
        if not node.name.startswith("_"):
            return False
        return True

    def _is_ignored_common(self, node: DocumentableFuncOrClass) -> bool:
        """Commonly-shared ignore checkers."""
        is_private = self._is_private(node)
        is_semiprivate = self._is_semiprivate(node)

        if self.config.ignore_private and is_private:
            return True
        if self.config.ignore_semiprivate and is_semiprivate:
            return True

        if self.config.ignore_regex:
            for regexp in self.config.ignore_regex:
                regex_result = regexp.match(node.name)
                if regex_result:
                    return True
        return False

    def _has_property_decorators(self, node: DocumentableFuncOrClass) -> bool:
        """Detect if node has property get/setter/deleter decorators."""
        if not hasattr(node, "decorator_list"):
            return False

        for dec in node.decorator_list:
            if hasattr(dec, "id"):
                if dec.id == "property":
                    return True
            if hasattr(dec, "attr"):
                if dec.attr == "setter":
                    return True
                if dec.attr == "deleter":
                    return True
        return False

    def _has_setters(self, node: DocumentableFuncOrClass) -> bool:
        """Detect if node has property get/setter decorators."""
        if not hasattr(node, "decorator_list"):
            return False

        for dec in node.decorator_list:
            if hasattr(dec, "attr"):
                if dec.attr == "setter":
                    return True
        return False

    def _has_overload_decorator(self, node: DocumentableFuncOrClass) -> bool:
        """Detect if node has a typing.overload decorator."""
        if not hasattr(node, "decorator_list"):
            return False

        for dec in node.decorator_list:
            if (
                hasattr(dec, "attr")
                and hasattr(dec, "value")
                and hasattr(dec.value, "id")
                and dec.value.id == "typing"
                and dec.attr == "overload"
            ):
                # @typing.overload decorator
                return True
            if hasattr(dec, "id") and dec.id == "overload":
                # @overload decorator
                return True
        return False

    def _is_func_ignored(self, node: DocumentableFuncOrClass) -> bool:
        """Should the AST visitor ignore this func/method node."""
        is_init = node.name == "__init__"
        is_magic = all(
            [
                node.name.startswith("__"),
                node.name.endswith("__"),
                node.name != "__init__",
            ]
        )
        has_property_decorators = self._has_property_decorators(node)
        has_setters = self._has_setters(node)
        has_overload = self._has_overload_decorator(node)

        if self.config.ignore_init_method and is_init:
            return True
        if self.config.ignore_magic and is_magic:
            return True
        if self.config.ignore_property_decorators and has_property_decorators:
            return True
        if self.config.ignore_property_setters and has_setters:
            return True
        if self.config.ignore_overloaded_functions and has_overload:
            return True

        return self._is_ignored_common(node)

    def _is_class_ignored(self, node: DocumentableFuncOrClass) -> bool:
        """Should the AST visitor ignore this class node."""
        return self._is_ignored_common(node)

    def visit_Module(self, node: DocumentableNode) -> None:
        """Visit module for docstrings.

        :param ast.Module node: a module AST node.
        """
        self._visit_helper(node)

    def visit_ClassDef(self, node: DocumentableFuncOrClass) -> None:
        """Visit class for docstrings.

        :param ast.ClassDef node: a class AST node.
        """
        if self._is_class_ignored(node):
            return
        self._visit_helper(node)

    def visit_FunctionDef(self, node: DocumentableFuncOrClass) -> None:
        """Visit function or method for docstrings.

        :param ast.FunctionDef node: a function/method AST node.
        """
        if self._is_func_ignored(node):
            return
        self._visit_helper(node)

    def visit_AsyncFunctionDef(self, node: DocumentableFuncOrClass) -> None:
        """Visit async function or method for docstrings.

        :param ast.AsyncFunctionDef node: a async function/method AST node.
        """
        if self._is_func_ignored(node):
            return
        self._visit_helper(node)
