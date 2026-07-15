import ast
import builtins

from models import FileInfo, FunctionInfo


class FunctionVisitor(ast.NodeVisitor):

    def __init__(self):

        self.calls = set()
        self.variables = set()
        self.locals = set()

    def visit_Call(self, node):

        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)

        elif isinstance(node.func, ast.Attribute):
            self.calls.add(node.func.attr)

        self.generic_visit(node)

    def visit_Name(self, node):

        self.variables.add(node.id)

        self.generic_visit(node)

    def visit_Assign(self, node):

        for target in node.targets:

            if isinstance(target, ast.Name):
                self.locals.add(target.id)

            elif isinstance(target, (ast.Tuple, ast.List)):

                for element in target.elts:

                    if isinstance(element, ast.Name):
                        self.locals.add(element.id)

        self.generic_visit(node)

    def visit_FunctionDef(self, node):

        for arg in node.args.args:
            self.locals.add(arg.arg)

        self.generic_visit(node)

    def visit_For(self, node):

        if isinstance(node.target, ast.Name):
            self.locals.add(node.target.id)

        self.generic_visit(node)


def parse_file(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)

    lines = source.splitlines()

    info = FileInfo(filename=filepath)

    # ------------------------------------------
    # Imports do arquivo
    # ------------------------------------------

    imported_names = set()

    for node in tree.body:

        if isinstance(node, ast.Import):

            for alias in node.names:

                imported_names.add(alias.asname or alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):

            for alias in node.names:

                imported_names.add(alias.asname or alias.name)

    info.imports = sorted(imported_names)

    # ------------------------------------------

    builtin_names = set(dir(builtins))

    local_functions = {
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }

    for node in tree.body:

        if isinstance(node, ast.FunctionDef):

            visitor = FunctionVisitor()
            visitor.visit(node)

            calls = sorted(
                c
                for c in visitor.calls
                if c in local_functions
            )

            variables = sorted(visitor.variables)

            locals_ = sorted(visitor.locals)

            dependencies = sorted(
                v
                for v in variables
                if (
                    v not in locals_
                    and v not in local_functions
                    and v not in imported_names
                    and v not in builtin_names
                )
            )

            code = "\n".join(
                lines[node.lineno - 1:node.end_lineno]
            )

            function = FunctionInfo(
                name=node.name,
                lineno=node.lineno,
                end_lineno=node.end_lineno,
                nlines=node.end_lineno - node.lineno + 1,
                source=code,
                calls=calls,
                variables=variables,
                local_variables=locals_,
                dependencies=dependencies
            )

            info.functions.append(function)

    info.functions.sort(key=lambda f: f.name)

    return info