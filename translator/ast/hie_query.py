from .base import BaseNode


class HierarchicalQueryNode(BaseNode):
    """ Нода, соответствующая иерархическому запросу """

    def __init__(self):
        super().__init__()
        self.selected_elements = []
        self.where_condition = None  # WHERE условие
        self.hie_condition = None
        self.start_part = None
