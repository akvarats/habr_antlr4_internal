from .base import BaseNode


class RelationalExpressionNode(BaseNode):
    """ left op right """
    def __init__(self, left: BaseNode, op: str, right: BaseNode):
        self.left = left
        self.op = op
        self.right = right

    def get_text(self):
        return "{} {} {}".format(
            self.left.get_text(), self.op, self.right.get_text()
        )
