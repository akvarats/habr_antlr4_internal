from antlr4.tree.Tree import ParseTree

from parser.PlSqlParser import PlSqlParser
from .visitor import Visitor


class Translator(object):

    def __init__(self):
        self.visitor = Visitor(translator=self)

    def translate(self, tree: ParseTree):
        return self.visit(tree)

    def visit(self, ctx: ParseTree):
        return self.visitor.visit(ctx)

    def translate_query_block(self, ctx:PlSqlParser.Query_blockContext):
        pass