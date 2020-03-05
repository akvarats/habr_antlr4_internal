import copy

from .base import BaseNode
from .relational_expression import RelationalExpressionNode
from .prior_expression import PriorExpressionNode
from .dot_id import DotIdNode


class HierarchicalQueryNode(BaseNode):
    """ Нода, соответствующая иерархическому запросу """

    def __init__(self):
        super().__init__()
        self.selected_elements = []
        self.where_condition = None  # WHERE условие
        self.order_by = None
        self.hie_condition = None
        self.start_part = None
        self.table_refs = []

    def get_text(self):
        """ """
        result = (
            "WITH RECURSIVE tmp AS (\n"
            "  ({starter})\n"
            "UNION\n"
            "  ({recursive})\n"
            ")\n"
            "{final}".format(
                starter=self._starter_part_text(),
                recursive=self._recursive_part_text(),
                final=self._final_part_text(),
            )
        )
        return result

    def _starter_part_text(self):
        selected = ", ".join((element.get_text() for element in self.selected_elements))
        table = ", ".join((table_ref.get_text() for table_ref in self.table_refs))
        condition = "WHERE {}".format(self.start_part.get_text()) if self.start_part else ""

        return "SELECT {}, 1 as level FROM {} {}".format(
            selected, table, condition
        ).strip()

    def _recursive_part_text(self):
        """ """

        # если у основной таблицы нет алиаса, то придумываем свой алиас и проставляем его у полей и таблицы
        primary_table_ref = self.table_refs[0] if self.table_refs else None
        recursive_table_alias = primary_table_ref.alias if primary_table_ref and primary_table_ref.alias else "m"

        x_selected = copy.deepcopy(self.selected_elements)
        for element in x_selected:
            element.table = recursive_table_alias

        x_table_refs = self.table_refs
        if primary_table_ref and recursive_table_alias != primary_table_ref.alias:
            x_table_refs = copy.deepcopy(x_table_refs)
            x_table_refs[0].alias = recursive_table_alias

        selected = ", ".join((e.get_text() for e in x_selected))
        table = ", ".join((tf.get_text() for tf in x_table_refs))

        # формируем условие JOIN внутри рекурсивной части
        if not isinstance(self.hie_condition, RelationalExpressionNode):
            raise NotImplementedError("Unknown hie condition type")

        prior_expr, expr = self._split_hie_condition(self.hie_condition)

        join_expr_left = self._replace_table_alias(prior_expr.expression, "tmp")
        join_expr_right = self._replace_table_alias(expr, recursive_table_alias)

        condition = "{} {} {}".format(
            join_expr_left.get_text(),
            self.hie_condition.op,
            join_expr_right.get_text()
        )

        return "SELECT {}, tmp.level + 1 as level FROM {} JOIN tmp ON {}".format(
            selected, table, condition
        ).strip()

    def _final_part_text(self):
        """ """

        # у selected_elements убираем префиксы таблиц (выбираться будет всё из таблицы tmp)
        x_selected = copy.deepcopy(self.selected_elements)
        for element in x_selected:
            element.table = None

        selected = ", ".join((element.get_text() for element in x_selected))
        order_by = " ORDER BY {}".format(self.order_by.get_text()) if self.order_by else ""

        return "SELECT {} FROM tmp {}".format(
            selected, order_by
        ).strip()

    def _split_hie_condition(self, condition: RelationalExpressionNode):
        """ Возвращает кортеж (prior_expression, expression) """
        if isinstance(self.hie_condition.right, PriorExpressionNode):
            prior_expr, expr = self.hie_condition.right, self.hie_condition.left
        else:
            prior_expr, expr = self.hie_condition.left, self.hie_condition.right

        return prior_expr, expr

    def _replace_table_alias(self, node: DotIdNode, table_alias: str):
        """ Заменяет в node алиас таблицы на table_alias """
        if node.left == table_alias:
            return node

        result = copy.deepcopy(node)
        result.left = table_alias

        return result
