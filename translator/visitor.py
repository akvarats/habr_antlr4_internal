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

    # def visitQuery_block(self, ctx:PlSqlParser.Query_blockContext):
    #     return self.translator.translate_query_block(ctx)

