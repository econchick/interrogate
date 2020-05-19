# Copyright 2020 Lynn Root
"""AST traversal for finding docstrings."""

import ast
import os

import attr


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
    :param CovNode _parent: parent node of current CovNode, if any.
    """

    name = attr.ib()
    path = attr.ib()
    level = attr.ib()
    lineno = attr.ib()
    covered = attr.ib()
    node_type = attr.ib()
    is_nested_func = attr.ib()
    _parent = attr.ib()


class CoverageVisitor(ast.NodeVisitor):
    """NodeVisitor for a Python file to find docstrings.

    :param str filename: filename to parse coverage.
    :param config.InterrogateConfig config: configuration.
    """

    def __init__(self, filename, config):
        self.filename = filename
        self.stack = []
        self.nodes = []
        self.config = config

    @staticmethod
    def _has_doc(node):
        """Return if node has docstrings."""
        return (
            ast.get_docstring(node) is not None
            and ast.get_docstring(node).strip() != ""
        )

    def _visit_helper(self, node):
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
            parent=parent,
            is_nested_func=self._is_nested(parent, node_type),
        )
        self.stack.append(cov_node)
        self.nodes.append(cov_node)

        self.generic_visit(node)

        self.stack.pop()

    def _is_nested(self, parent, node_type):
        """Is node a nested func/method of another func/method."""
        if parent is None:
            return False
        # is it a nested function?
        if parent.node_type == "FunctionDef" and node_type == "FunctionDef":
            return True
        return False

    def _is_private(self, node):
        """Is node private (i.e. __MyClass, __my_func)."""
        if node.name.endswith("__"):
            return False
        if not node.name.startswith("__"):
            return False
        return True

    def _is_semiprivate(self, node):
        """Is node semiprivate (i.e. _MyClass, _my_func)."""
        if node.name.endswith("__"):
            return False
        if node.name.startswith("__"):
            return False
        if not node.name.startswith("_"):
            return False
        return True

    def _is_ignored_common(self, node):
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

    def _is_func_ignored(self, node):
        """Should the AST visitor ignore this func/method node."""
        is_init = node.name == "__init__"
        is_magic = all(
            [
                node.name.startswith("__"),
                node.name.endswith("__"),
                node.name != "__init__",
            ]
        )

        if self.config.ignore_init_method and is_init:
            return True
        if self.config.ignore_magic and is_magic:
            return True
        return self._is_ignored_common(node)

    def _is_class_ignored(self, node):
        """Should the AST visitor ignore this class node."""
        return self._is_ignored_common(node)

    def visit_Module(self, node):
        """Visit module for docstrings.

        :param ast.Module node: a module AST node.
        """
        self._visit_helper(node)

    def visit_ClassDef(self, node):
        """Visit class for docstrings.

        :param ast.ClassDef node: a class AST node.
        """
        if self._is_class_ignored(node):
            return
        self._visit_helper(node)

    def visit_FunctionDef(self, node):
        """Visit function or method for docstrings.

        :param ast.FunctionDef node: a function/method AST node.
        """
        if self._is_func_ignored(node):
            return
        self._visit_helper(node)

    def visit_AsyncFunctionDef(self, node):
        """Visit async function or method for docstrings.

        :param ast.AsyncFunctionDef node: a async function/method AST node.
        """
        if self._is_func_ignored(node):
            return
        self._visit_helper(node)
