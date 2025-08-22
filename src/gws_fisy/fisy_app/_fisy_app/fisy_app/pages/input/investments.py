import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/investissements", on_load=State.on_load, title="Saisie — Investissements")
def investments():
    i = State.i18n
    LABELS = [rx.text(i["inv.label"]), rx.text(i["inv.amount"]), rx.text(i["inv.vat"]), rx.text(i["inv.month"]), rx.text(i["inv.amort"])]
    WIDTHS = ["240px","200px","120px","160px","160px"]
    def row(inv, irow):
        return rx.table.row(
            make_cell(rx.input(value=inv.label, on_change=lambda v, irow=irow: State.update_item("investments", irow, "label", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", min=0, value=inv.amount_ht, on_change=lambda v, irow=irow: State.update_item("investments", irow, "amount_ht", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.01, min=0, value=inv.vat_rate, on_change=lambda v, irow=irow: State.update_item("investments", irow, "vat_rate", v, "float")), WIDTHS[2]),
            make_cell(rx.input(type="number", min=1, value=inv.purchase_month, on_change=lambda v, irow=irow: State.update_item("investments", irow, "purchase_month", v, "int")), WIDTHS[3]),
            make_cell(rx.input(type="number", min=1, value=inv.amort_years, on_change=lambda v, irow=irow: State.update_item("investments", irow, "amort_years", v, "int")), WIDTHS[4]),
            actions_cell("investments", irow),
        )
    return layout(rx.vstack(
        rx.heading(i["inv.title"], size="5"),
        rx.text(i["inv.desc"]),
        rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.investments, row))),
        rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_investment)),
        spacing="3", align_items="start",
    ))
