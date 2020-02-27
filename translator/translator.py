from antlr4.tree.Tree import ParseTree

from .visitor import Visitor


class Translator(object):

    def __init__(self):
        self.visitor = Visitor()

    def translate(self, tree: ParseTree):
        self.visit(tree)

    def visit(self, ctx: ParseTree):
        return self.visitor.visit(ctx)
