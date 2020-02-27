from .base import BaseNode


class TokenNode(BaseNode):
    """ """
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def get_text(self):
        return self.text or ""
