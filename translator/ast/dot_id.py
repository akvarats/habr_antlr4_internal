from .base import BaseNode


class DotIdNode(BaseNode):
    """ """

    def __init__(self, left: str, right: str):
        self.left = left
        self.right = right

    def get_text(self):
        return "{}.{}".format(self.left, self.right)
