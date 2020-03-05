from typing import Optional

from .base import BaseNode


class TableRefNode(BaseNode):
    """ """
    def __init__(self, name: str, alias: Optional[str]):
        self.name = name
        self.alias = alias

    def get_text(self):
        return ("{} {}".format(self.name or "", self.alias or "")).strip()
