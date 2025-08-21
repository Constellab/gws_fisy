
import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/commandes", on_load=State.on_load, title="Saisie — Commandes")
def orders():
    LABELS = ["Activité", "Mois (index)", "Quantité"]
    WIDTHS = ["220px", "160px", "160px"]

    def row(c, i):
        return rx.table.row(
            make_cell(rx.select(items=State.activity_options, value=c.activity, on_change=lambda v, i=i: State.update_item("orders", i, "activity", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", value=c.month_index, on_change=lambda v, i=i: State.update_item("orders", i, "month_index", v, "int"), placeholder=">=1"), WIDTHS[1]),
            make_cell(rx.input(type="number", value=c.quantity, on_change=lambda v, i=i: State.update_item("orders", i, "quantity", v, "float"), placeholder="Qté"), WIDTHS[2]),
            actions_cell("orders", i),
        )

    return layout(
        rx.vstack(
            rx.heading("Commandes (ventes)", size="5"),
            rx.text("Planifiez des ventes ponctuelles par activité et mois."),
            rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.orders, row))),
            rx.hstack(rx.button("Ajouter une commande", on_click=lambda: State.add_order())),
            spacing="3", align_items="start",
        )
    )
