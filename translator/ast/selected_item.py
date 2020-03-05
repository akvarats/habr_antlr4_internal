from typing import Optional

from .base import BaseNode


class SelectedItemNode(BaseNode):

    def __init__(self, name: str, table: Optional[str] = None, alias: Optional[str] = None):
        self.name = name
        self.table = table
        self.alias = alias

    def get_text(self):
        return "{}{} {}".format(
            "{}.".format(self.table) if self.table else "",
            self.name or "",
            self.alias or ""
        ).strip()
