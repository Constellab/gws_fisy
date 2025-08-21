import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/investissements", on_load=State.on_load, title="Saisie — Investissements")
def investments():
    t = State.i18n
    LABELS = [t["inv_col_label"], t["inv_col_amount"], t["inv_col_vat"], t["inv_col_month"], t["inv_col_years"]]
    WIDTHS = ["240px","200px","120px","160px","180px"]

    def row(inv, i):
        return rx.table.row(
            make_cell(rx.input(value=inv.label, on_change=lambda v, i=i: State.update_item("investments", i, "label", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", value=inv.amount_ht, on_change=lambda v, i=i: State.update_item("investments", i, "amount_ht", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.01, value=inv.vat_rate, on_change=lambda v, i=i: State.update_item("investments", i, "vat_rate", v, "float")), WIDTHS[2]),
            make_cell(rx.input(type="number", value=inv.purchase_month, on_change=lambda v, i=i: State.update_item("investments", i, "purchase_month", v, "int")), WIDTHS[3]),
            make_cell(rx.input(type="number", value=inv.amort_years, on_change=lambda v, i=i: State.update_item("investments", i, "amort_years", v, "int")), WIDTHS[4]),
            actions_cell("investments", i),
        )

    return layout(
        rx.vstack(
            rx.heading(t["inv_title"], size="5"),
            rx.text(t["inv_desc"]),
            rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.investments, row))),
            rx.hstack(rx.button(t["inv_add"], on_click=State.add_investment)),
            spacing="3", align_items="start",
        )
    )
