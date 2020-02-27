import abc


class BaseNode(metaclass=abc.ABCMeta):

    def __init__(self):
        self.children = []

    def add_child(self, child):
        if child is not None:
            self.children.append(child)

    def get_text(self):
        """ """
        # TOKENS_NO_SPACE = (".", "|")
        # tokens = []

        # prev = current = None
        # for child in self.children:
        #     prev = current if current is not None else prev
        #         current = child.get_text()
        #         need_space = (prev is not None)
        #
        #         if prev in ("")

        # return "".join(tokens)
        return " ".join([child.get_text() for child in self.children])
