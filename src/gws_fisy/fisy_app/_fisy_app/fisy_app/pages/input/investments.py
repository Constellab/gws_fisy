
import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/investissements", on_load=State.on_load, title="Saisie — Investissements")
def investments():
    LABELS = ["Libellé", "Montant HT", "TVA", "Mois d’achat", "Amort. (années)"]
    WIDTHS = ["260px", "160px", "120px", "160px", "180px"]

    def row(inv, i):
        return rx.table.row(
            make_cell(rx.input(value=inv.label, on_change=lambda v, i=i: State.update_item("investments", i, "label", v, "str"), placeholder="Libellé investissement"), WIDTHS[0]),
            make_cell(rx.input(type="number", value=inv.amount_ht, on_change=lambda v, i=i: State.update_item("investments", i, "amount_ht", v, "float"), placeholder="HT"), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.01, value=inv.vat_rate, on_change=lambda v, i=i: State.update_item("investments", i, "vat_rate", v, "float"), placeholder="0.2"), WIDTHS[2]),
            make_cell(rx.input(type="number", value=inv.purchase_month, on_change=lambda v, i=i: State.update_item("investments", i, "purchase_month", v, "int"), placeholder="Mois index"), WIDTHS[3]),
            make_cell(rx.input(type="number", value=inv.amort_years, on_change=lambda v, i=i: State.update_item("investments", i, "amort_years", v, "int"), placeholder="Années"), WIDTHS[4]),
            actions_cell("investments", i),
        )

    return layout(
        rx.vstack(
            rx.heading("Investissements", size="5"),
            rx.text("Saisissez vos immobilisations et leur amortissement."),
            rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.investments, row))),
            rx.hstack(rx.button("Ajouter un investissement", on_click=lambda: State.add_investment())),
            spacing="3", align_items="start",
        )
    )
