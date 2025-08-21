import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/financement", on_load=State.on_load, title="Saisie — Financement")
def funding():
    t = State.i18n

    # Capital injections
    LABELS_CAP = [t["cap_col_label"], t["cap_col_amount"], t["cap_col_month"]]
    WIDTHS_CAP = ["240px","160px","140px"]

    def row_cap(c, i):
        return rx.table.row(
            make_cell(rx.input(value=c.label, on_change=lambda v, i=i: State.update_item("caps", i, "label", v, "str")), WIDTHS_CAP[0]),
            make_cell(rx.input(type="number", value=c.amount, on_change=lambda v, i=i: State.update_item("caps", i, "amount", v, "float")), WIDTHS_CAP[1]),
            make_cell(rx.input(type="number", value=c.month, on_change=lambda v, i=i: State.update_item("caps", i, "month", v, "int")), WIDTHS_CAP[2]),
            actions_cell("caps", i),
        )

    # Subsidies
    LABELS_SUB = [t["subv_col_label"], t["subv_col_amount"], t["subv_col_month"]]
    WIDTHS_SUB = ["240px","160px","140px"]

    def row_sub(s, i):
        return rx.table.row(
            make_cell(rx.input(value=s.label, on_change=lambda v, i=i: State.update_item("subsidies", i, "label", v, "str")), WIDTHS_SUB[0]),
            make_cell(rx.input(type="number", value=s.amount, on_change=lambda v, i=i: State.update_item("subsidies", i, "amount", v, "float")), WIDTHS_SUB[1]),
            make_cell(rx.input(type="number", value=s.month, on_change=lambda v, i=i: State.update_item("subsidies", i, "month", v, "int")), WIDTHS_SUB[2]),
            actions_cell("subsidies", i),
        )

    # Loans
    LABELS_LOAN = [t["loan_col_label"], t["loan_col_principal"], t["loan_col_rate"], t["loan_col_months"], t["loan_col_start"]]
    WIDTHS_LOAN = ["240px","160px","140px","140px","140px"]

    def row_loan(l, i):
        return rx.table.row(
            make_cell(rx.input(value=l.label, on_change=lambda v, i=i: State.update_item("loans", i, "label", v, "str")), WIDTHS_LOAN[0]),
            make_cell(rx.input(type="number", value=l.principal, on_change=lambda v, i=i: State.update_item("loans", i, "principal", v, "float")), WIDTHS_LOAN[1]),
            make_cell(rx.input(type="number", step=0.001, value=l.annual_rate, on_change=lambda v, i=i: State.update_item("loans", i, "annual_rate", v, "float")), WIDTHS_LOAN[2]),
            make_cell(rx.input(type="number", value=l.months, on_change=lambda v, i=i: State.update_item("loans", i, "months", v, "int")), WIDTHS_LOAN[3]),
            make_cell(rx.input(type="number", value=l.start_month, on_change=lambda v, i=i: State.update_item("loans", i, "start_month", v, "int")), WIDTHS_LOAN[4]),
            actions_cell("loans", i),
        )

    return layout(
        rx.vstack(
            rx.heading(t["fund_title"], size="5"),
            rx.text(t["fund_desc"]),
            rx.heading("Capital", size="4"),
            rx.table.root(
                header_row(LABELS_CAP, WIDTHS_CAP),
                rx.table.body(rx.foreach(State.caps, row_cap)),
            ),
            rx.hstack(rx.button(t["cap_add"], on_click=State.add_capital)),
            rx.box(height="3"),

            rx.heading("Subsidies", size="4"),
            rx.table.root(
                header_row(LABELS_SUB, WIDTHS_SUB),
                rx.table.body(rx.foreach(State.subsidies, row_sub)),
            ),
            rx.hstack(rx.button(t["subv_add"], on_click=State.add_subsidy)),
            rx.box(height="3"),

            rx.heading("Loans", size="4"),
            rx.table.root(
                header_row(LABELS_LOAN, WIDTHS_LOAN),
                rx.table.body(rx.foreach(State.loans, row_loan)),
            ),
            rx.hstack(rx.button(t["loan_add"], on_click=State.add_loan)),

            spacing="3", align_items="start",
        )
    )
