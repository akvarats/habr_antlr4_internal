from antlr4.tree.Tree import ParseTree

from parser.PlSqlParser import PlSqlParser
from .visitor import Visitor

from .ast.hie_query import HierarchicalQueryNode
from .ast.token import TokenNode
from .ast.table_ref import TableRefNode
from .ast.selected_item import SelectedItemNode
from .ast.dot_id import DotIdNode
from .ast.relational_expression import RelationalExpressionNode
from .ast.prior_expression import PriorExpressionNode


class Translator(object):
    """
    Транслятор нод (ORA -> PG)
    """
    def __init__(self):
        self.visitor = Visitor(translator=self)

    def translate(self, tree: ParseTree):
        return self.visit(tree)

    def visit(self, ctx: ParseTree):
        return self.visitor.visit(ctx)

    def translate_hierarchical_query(self, ctx: PlSqlParser.Query_blockContext):
        """ """
        result = HierarchicalQueryNode()

        # обрабатываем selected элементы
        if ctx.selected_list().select_list_elements():
            # указано явное перечисление полей
            for selected_element in ctx.selected_list().select_list_elements():
                result.selected_elements.append(self.visit(selected_element))
        else:
            # SELECT * FROM
            result.selected_elements.append(TokenNode("*"))

        # обрабатываем выражение FROM

        for table_ref_ctx in ctx.from_clause().table_ref_list().table_ref():
            result.table_refs.append(self.visit(table_ref_ctx))

        # стартовая часть иерархического запроса
        start_part_ctx = ctx.hierarchical_query_clause().start_part() if ctx.hierarchical_query_clause() else None
        result.start_part = self.visit(start_part_ctx.condition()) if start_part_ctx else None

        # рекурсивная часть иерархического запроса
        hie_condition_ctx = ctx.hierarchical_query_clause().condition() if ctx.hierarchical_query_clause() else None
        result.hie_condition = self.visit(hie_condition_ctx) if hie_condition_ctx else None

        return result

    def translate_selected_list_elements(self, ctx: PlSqlParser.Select_list_elementsContext):
        """ Конвертация правила select_list_elements """
        if ctx.ASTERISK() is not None:
            return SelectedItemNode(name="*", table=self.visit(ctx.table_view_name()))

        alias = None
        if ctx.column_alias():
            alias = self.visit(
                ctx=ctx.column_alias().identifier() if ctx.column_alias().identifier() else \
                    ctx.column_alias().quoted_string()
            ).get_text()

        table = None
        name = None
        name_node = self.visit(ctx.expression())

        if isinstance(name_node, DotIdNode):
            table, name = name_node.left, name_node.right
        else:
            name = name_node.get_text()

        return SelectedItemNode(table=table, name=name, alias=alias)

    def translate_dot_id(self, ctx: PlSqlParser.General_element_partContext):
        """ """
        return DotIdNode(
            left=ctx.id_expression()[0].getText(),
            right=ctx.id_expression()[1].getText()
        )

    def translate_table_ref_aux(self, ctx: PlSqlParser.Table_ref_auxContext):
        """ """
        return TableRefNode(
            name=ctx.table_ref_aux_internal().getText(),
            alias=ctx.table_alias().getText() if ctx.table_alias() else None
        )

    def translate_relational_expression(self, ctx: PlSqlParser.Relational_expressionContext):
        """ """
        return RelationalExpressionNode(
            left=self.visit(ctx.relational_expression()[0]),
            op=ctx.relational_operator().getText(),
            right=self.visit(ctx.relational_expression()[1])
        )

    def translate_prior_expression(self, ctx: PlSqlParser.Unary_expressionContext):
        return PriorExpressionNode(self.visit(ctx.unary_expression()))
