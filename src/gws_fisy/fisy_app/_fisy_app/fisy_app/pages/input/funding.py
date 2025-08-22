import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/financement", on_load=State.on_load, title="Saisie — Financement")
def funding():
    i = State.i18n

    LABELS_CAP = [rx.text(i["fund.cap.label"]), rx.text(i["fund.cap.amount"]), rx.text(i["fund.cap.month"])]
    WIDTHS_CAP = ["240px","200px","160px"]
    def row_cap(c, irow):
        return rx.table.row(
            make_cell(rx.input(value=c.label, on_change=lambda v, irow=irow: State.update_item("caps", irow, "label", v, "str")), WIDTHS_CAP[0]),
            make_cell(rx.input(type="number", min=0, value=c.amount, on_change=lambda v, irow=irow: State.update_item("caps", irow, "amount", v, "float")), WIDTHS_CAP[1]),
            make_cell(rx.input(type="number", min=1, value=c.month, on_change=lambda v, irow=irow: State.update_item("caps", irow, "month", v, "int")), WIDTHS_CAP[2]),
            actions_cell("caps", irow),
        )

    LABELS_SUB = [rx.text(i["fund.sub.label"]), rx.text(i["fund.sub.amount"]), rx.text(i["fund.sub.month"])]
    WIDTHS_SUB = ["240px","200px","160px"]
    def row_sub(s, irow):
        return rx.table.row(
            make_cell(rx.input(value=s.label, on_change=lambda v, irow=irow: State.update_item("subsidies", irow, "label", v, "str")), WIDTHS_SUB[0]),
            make_cell(rx.input(type="number", min=0, value=s.amount, on_change=lambda v, irow=irow: State.update_item("subsidies", irow, "amount", v, "float")), WIDTHS_SUB[1]),
            make_cell(rx.input(type="number", min=1, value=s.month, on_change=lambda v, irow=irow: State.update_item("subsidies", irow, "month", v, "int")), WIDTHS_SUB[2]),
            actions_cell("subsidies", irow),
        )

    LABELS_LOAN = [rx.text(i["fund.loan.label"]), rx.text(i["fund.loan.principal"]), rx.text(i["fund.loan.rate"]), rx.text(i["fund.loan.months"]), rx.text(i["fund.loan.start"])]
    WIDTHS_LOAN = ["220px","160px","160px","140px","160px"]
    def row_loan(l, irow):
        return rx.table.row(
            make_cell(rx.input(value=l.label, on_change=lambda v, irow=irow: State.update_item("loans", irow, "label", v, "str")), WIDTHS_LOAN[0]),
            make_cell(rx.input(type="number", min=0, value=l.principal, on_change=lambda v, irow=irow: State.update_item("loans", irow, "principal", v, "float")), WIDTHS_LOAN[1]),
            make_cell(rx.input(type="number", step=0.001, min=0, value=l.annual_rate, on_change=lambda v, irow=irow: State.update_item("loans", irow, "annual_rate", v, "float")), WIDTHS_LOAN[2]),
            make_cell(rx.input(type="number", min=1, value=l.months, on_change=lambda v, irow=irow: State.update_item("loans", irow, "months", v, "int")), WIDTHS_LOAN[3]),
            make_cell(rx.input(type="number", min=1, value=l.start_month, on_change=lambda v, irow=irow: State.update_item("loans", irow, "start_month", v, "int")), WIDTHS_LOAN[4]),
            actions_cell("loans", irow),
        )

    return layout(rx.vstack(
        rx.heading(i["fund.title"], size="5"),
        rx.text(i["fund.desc"]),
        rx.heading("Apports", size="4"),
        rx.table.root(header_row(LABELS_CAP, WIDTHS_CAP), rx.table.body(rx.foreach(State.caps, row_cap))),
        rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_capital)),
        rx.box(height="2"),
        rx.heading("Subventions", size="4"),
        rx.table.root(header_row(LABELS_SUB, WIDTHS_SUB), rx.table.body(rx.foreach(State.subsidies, row_sub))),
        rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_subsidy)),
        rx.box(height="2"),
        rx.heading("Prêts", size="4"),
        rx.table.root(header_row(LABELS_LOAN, WIDTHS_LOAN), rx.table.body(rx.foreach(State.loans, row_loan))),
        rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_loan)),
        spacing="3", align_items="start",
    ))
