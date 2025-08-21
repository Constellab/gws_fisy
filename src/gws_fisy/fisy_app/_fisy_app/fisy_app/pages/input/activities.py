
import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/activites", on_load=State.on_load, title="Saisie — Activités")
def activities():
    LABELS = ["Nom activité", "Prix unitaire HT", "TVA", "Coût var. unitaire HT", "Taux coût var./prix"]
    WIDTHS = ["220px", "160px", "120px", "220px", "200px"]

    def row(a, i):
        return rx.table.row(
            make_cell(rx.input(value=a.name, on_change=lambda v, i=i: State.update_item("activities", i, "name", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", value=a.unit_price_ht, on_change=lambda v, i=i: State.update_item("activities", i, "unit_price_ht", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.01, value=a.vat_rate, on_change=lambda v, i=i: State.update_item("activities", i, "vat_rate", v, "float")), WIDTHS[2]),
            make_cell(rx.input(type="number", value=a.variable_cost_per_unit_ht, on_change=lambda v, i=i: State.update_item("activities", i, "variable_cost_per_unit_ht", v, "float")), WIDTHS[3]),
            make_cell(rx.input(type="number", step=0.01, value=a.variable_cost_rate_on_price, on_change=lambda v, i=i: State.update_item("activities", i, "variable_cost_rate_on_price", v, "float")), WIDTHS[4]),
            actions_cell("activities", i),
        )

    return layout(
        rx.vstack(
            rx.heading("Activités", size="5"),
            rx.text("Paramétrez le prix unitaire HT, la TVA et les coûts variables."),
            rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.activities, row))),
            rx.hstack(rx.button("Ajouter une activité", on_click=State.add_activity)),
            spacing="3", align_items="start",
        )
    )
