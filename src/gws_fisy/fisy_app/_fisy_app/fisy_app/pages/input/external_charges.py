import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/charges", on_load=State.on_load, title="Saisie — Charges externes")
def external_charges():
    i = State.i18n
    LABELS = [rx.text(i["charges.label"]), rx.text(i["charges.amount"]), rx.text(i["charges.vat"]), rx.text(i["charges.start"]), rx.text(i["charges.end"])]
    WIDTHS = ["240px","200px","120px","140px","140px"]
    def row(c, irow):
        return rx.table.row(
            make_cell(rx.input(value=c.label, on_change=lambda v, irow=irow: State.update_item("charges", irow, "label", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", min=0, value=c.monthly_amount_ht, on_change=lambda v, irow=irow: State.update_item("charges", irow, "monthly_amount_ht", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.01, min=0, value=c.vat_rate, on_change=lambda v, irow=irow: State.update_item("charges", irow, "vat_rate", v, "float")), WIDTHS[2]),
            make_cell(rx.input(type="number", min=1, value=c.start_month, on_change=lambda v, irow=irow: State.update_item("charges", irow, "start_month", v, "int")), WIDTHS[3]),
            make_cell(rx.input(type="number", min=1, value=c.end_month, on_change=lambda v, irow=irow: State.update_item("charges", irow, "end_month", v, "int")), WIDTHS[4]),
            actions_cell("charges", irow),
        )
    return layout(rx.vstack(
        rx.heading(i["charges.title"], size="5"),
        rx.text(i["charges.desc"]),
        rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.charges, row))),
        rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_charge)),
        spacing="3", align_items="start",
    ))
