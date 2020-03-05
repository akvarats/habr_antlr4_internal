from .ast.common import CommonNode
from .ast.token import TokenNode

from parser.PlSqlParser import PlSqlParser
from parser.PlSqlParserVisitor import PlSqlParserVisitor


class Visitor(PlSqlParserVisitor):
    """ """
    def __init__(self, translator):
        self.translator = translator

    def aggregateResult(self, aggregate, nextResult):
        """ """
        if nextResult is None:
            return aggregate

        if aggregate is None:
            return nextResult

        if isinstance(aggregate, CommonNode):
            aggregate.add_child(nextResult)
            return aggregate

        result = CommonNode()
        result.add_child(aggregate)
        result.add_child(nextResult)

        return result

    def visitChildren(self, node):
        result = super().visitChildren(node)
        if result is None:
            result = TokenNode(node.getText())
        return result

    def visitTerminal(self, node):
        text = node.getText()
        return TokenNode(text) if text != "<EOF>" else None

    def visitQuery_block(self, ctx: PlSqlParser.Query_blockContext):
        if ctx.hierarchical_query_clause() is not None:
            # это иерархический запрос
            return self.translator.translate_hierarchical_query(ctx)

        # реализуем поведение визитора по умолчанию
        return super().visitQuery_block(ctx)

    def visitSelect_list_elements(self, ctx: PlSqlParser.Select_list_elementsContext):
        return self.translator.translate_selected_list_elements(ctx)

    def visitGeneral_element_part(self, ctx: PlSqlParser.General_element_partContext):

        if ctx.char_set_name() is None and ctx.link_name() is None and ctx.function_argument() is None:
            if len(ctx.id_expression()) == 2:
                # очень похоже на идентификаторы типа t.field
                return self.translator.translate_dot_id(ctx)

        return super().visitGeneral_element_part(ctx)

    def visitTable_ref_aux(self, ctx: PlSqlParser.Table_ref_auxContext):
        return self.translator.translate_table_ref_aux(ctx)

    def visitRelational_expression(self, ctx: PlSqlParser.Relational_expressionContext):
        """ Rule: relational_expression """
        if ctx.relational_expression() and ctx.relational_operator():
            return self.translator.translate_relational_expression(ctx)
        return super().visitRelational_expression(ctx)

    def visitUnary_expression(self, ctx: PlSqlParser.Unary_expressionContext):
        return self.translator.translate_prior_expression(ctx) if ctx.PRIOR() else \
            super().visitUnary_expression(ctx)



