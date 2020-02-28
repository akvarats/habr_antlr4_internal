from antlr4.tree.Tree import ParseTree

from parser.PlSqlParser import PlSqlParser
from .visitor import Visitor

from .ast.hie_query import HierarchicalQueryNode
from .ast.token import TokenNode


class Translator(object):

    def __init__(self):
        self.visitor = Visitor(translator=self)

    def translate(self, tree: ParseTree):
        return self.visit(tree)

    def visit(self, ctx: ParseTree):
        return self.visitor.visit(ctx)

    def translate_hierarchical_query(self, ctx:PlSqlParser.Query_blockContext):
        """"""
        result = HierarchicalQueryNode()

        # обрабатываем selected элементы
        if ctx.selected_list().select_list_elements():
            # указано явное перечисление полей
            for selected_element in ctx.selected_list().select_list_elements():
                result.selected_elements.append(self.visit(selected_element))
        else:
            # SELECT * FROM
            result.selected_elements.append(TokenNode("*"))

        return result
        # if ctx.selected_list().select_list_elements():
        #
        # else:

        # обрабатываем список selected_elements
        # for selected_element in ctx.selected_list():
        #     pass

