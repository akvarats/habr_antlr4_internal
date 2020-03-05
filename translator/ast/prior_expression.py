from .base import BaseNode


class PriorExpressionNode(BaseNode):
    """ """

    def __init__(self, expression: BaseNode):
        super().__init__()
        self.expression = expression

    def get_text(self):
        """ """
        # для PG явно указывать PRIOR не надо
        return self.expression.get_text()
