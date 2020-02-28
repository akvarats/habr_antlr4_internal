from .base import BaseNode


class PriorExpressionNode(BaseNode):
    """ """

    def __init__(self):
        super().__init__()
        self.expression = None

    def get_text(self):
        return self.expression.x