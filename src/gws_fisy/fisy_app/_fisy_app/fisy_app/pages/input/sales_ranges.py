
import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/ventes-plages", on_load=State.on_load, title="Saisie — Ventes par plages")
def sales_ranges():
    LABELS = ["Activité", "Début (mois)", "Fin (mois)", "q0 (début)", "Croissance période", "Mode"]
    WIDTHS = ["220px", "140px", "140px", "160px", "200px", "140px"]

    def row(r, i):
        return rx.table.row(
            make_cell(rx.select(items=State.activity_options, value=r.activity, on_change=lambda v, i=i: State.update_item("sale_ranges", i, "activity", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", value=r.start_month, on_change=lambda v, i=i: State.update_item("sale_ranges", i, "start_month", v, "int"), placeholder=">=1"), WIDTHS[1]),
            make_cell(rx.input(type="number", value=r.end_month, on_change=lambda v, i=i: State.update_item("sale_ranges", i, "end_month", v, "int"), placeholder=">= début"), WIDTHS[2]),
            make_cell(rx.input(type="number", value=r.q0, on_change=lambda v, i=i: State.update_item("sale_ranges", i, "q0", v, "float"), placeholder="Qté début"), WIDTHS[3]),
            make_cell(rx.input(type="number", step=0.01, value=r.growth, on_change=lambda v, i=i: State.update_item("sale_ranges", i, "growth", v, "float"), placeholder="ex. 0.2"), WIDTHS[4]),
            make_cell(rx.select(items=["cagr", "linear"], value=r.mode, on_change=lambda v, i=i: State.update_item("sale_ranges", i, "mode", v, "str")), WIDTHS[5]),
            actions_cell("sale_ranges", i),
        )

    return layout(
        rx.vstack(
            rx.heading("Ventes par plages (début/fin + croissance)", size="5"),
            rx.text("Saisissez des plages de ventes par activité : mois de début/fin, quantité initiale, croissance totale (ex. 0.2 = +20%) et mode (CAGR ou linéaire)."),
            rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.sale_ranges, row))),
            rx.hstack(rx.button("Ajouter une plage", on_click=lambda: State.add_sale_range())),
            spacing="3", align_items="start",
        )
    )
