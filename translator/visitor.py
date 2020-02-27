from parser.PlSqlParser import PlSqlParser
from parser.PlSqlParserVisitor import PlSqlParserVisitor


class Visitor(PlSqlParserVisitor):
    """ """

    def visitQuery_block(self, ctx:PlSqlParser.Query_blockContext):
        return None
