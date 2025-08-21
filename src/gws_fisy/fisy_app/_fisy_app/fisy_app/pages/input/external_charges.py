
import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/charges", on_load=State.on_load, title="Saisie — Charges externes")
def external_charges():
    LABELS = ["Libellé", "Montant mensuel HT", "TVA", "Début (mois)", "Fin (mois)"]
    WIDTHS = ["240px", "180px", "120px", "140px", "140px"]

    def row(c, i):
        return rx.table.row(
            make_cell(rx.input(value=c.label, on_change=lambda v, i=i: State.update_item("charges", i, "label", v, "str"), placeholder="Libellé"), WIDTHS[0]),
            make_cell(rx.input(type="number", value=c.monthly_amount_ht, on_change=lambda v, i=i: State.update_item("charges", i, "monthly_amount_ht", v, "float"), placeholder="HT/mois"), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.01, value=c.vat_rate, on_change=lambda v, i=i: State.update_item("charges", i, "vat_rate", v, "float"), placeholder="0.2"), WIDTHS[2]),
            make_cell(rx.input(type="number", value=c.start_month, on_change=lambda v, i=i: State.update_item("charges", i, "start_month", v, "int"), placeholder="Début"), WIDTHS[3]),
            make_cell(rx.input(type="number", value=c.end_month, on_change=lambda v, i=i: State.update_item("charges", i, "end_month", v, "int"), placeholder="Fin ou 999"), WIDTHS[4]),
            actions_cell("charges", i),
        )

    return layout(
        rx.vstack(
            rx.heading("Charges externes", size="5"),
            rx.text("Déclarez vos charges récurrentes avec TVA et période."),
            rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.charges, row))),
            rx.hstack(rx.button("Ajouter une charge", on_click=State.add_charge)),
            spacing="3", align_items="start",
        )
    )
