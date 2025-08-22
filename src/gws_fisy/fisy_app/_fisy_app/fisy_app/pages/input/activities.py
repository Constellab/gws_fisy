import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/activites", on_load=State.on_load, title="Saisie — Activités")
def activities():
    i = State.i18n
    LABELS = [rx.text(i["activities.name"]), rx.text(i["activities.unit_price_ht"]), rx.text(i["activities.vat_rate"]), rx.text(i["activities.var_cost_unit"]), rx.text(i["activities.var_cost_rate"])]
    WIDTHS = ["220px","160px","120px","220px","200px"]
    def row(a, irow):
        return rx.table.row(
            make_cell(rx.input(value=a.name, on_change=lambda v, irow=irow: State.update_item("activities", irow, "name", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", min=0, value=a.unit_price_ht, on_change=lambda v, irow=irow: State.update_item("activities", irow, "unit_price_ht", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.01, min=0, value=a.vat_rate, on_change=lambda v, irow=irow: State.update_item("activities", irow, "vat_rate", v, "float")), WIDTHS[2]),
            make_cell(rx.input(type="number", min=0, value=a.variable_cost_per_unit_ht, on_change=lambda v, irow=irow: State.update_item("activities", irow, "variable_cost_per_unit_ht", v, "float")), WIDTHS[3]),
            make_cell(rx.input(type="number", step=0.01, min=0, value=a.variable_cost_rate_on_price, on_change=lambda v, irow=irow: State.update_item("activities", irow, "variable_cost_rate_on_price", v, "float")), WIDTHS[4]),
            actions_cell("activities", irow),
        )
    return layout(rx.vstack(
        rx.heading(i["activities.title"], size="5"),
        rx.text(i["activities.desc"]),
        rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.activities, row))),
        rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_activity)),
        spacing="3", align_items="start",
    ))
