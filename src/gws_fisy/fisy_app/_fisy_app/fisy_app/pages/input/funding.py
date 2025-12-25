import reflex as rx

from ...state import State
from ..layout import header_row, layout, make_cell, page_with_fixed_title


@rx.page(route="/input/funding", on_load=State.on_load, title="Input — Funding")
def funding():
    i = State.i18n

    LABELS_CAP = [rx.text(i["fund.cap.label"]), rx.text(i["fund.cap.amount"]), rx.text(i["fund.cap.month"])]
    WIDTHS_CAP = ["45%","30%","20%"]
    def row_cap(c, irow):
        return rx.table.row(
            make_cell(rx.input(value=c.label, on_change=lambda v: State.update_item("caps", irow, "label", v, "str")), WIDTHS_CAP[0]),
            make_cell(rx.input(type="number", min=0, value=c.amount, on_change=lambda v: State.update_item("caps", irow, "amount", v, "float")), WIDTHS_CAP[1]),
            make_cell(rx.input(type="number", min=1, value=c.month, on_change=lambda v: State.update_item("caps", irow, "month", v, "int")), WIDTHS_CAP[2]),
            rx.table.cell(
                rx.button(
                    State.i18n["common.delete"],
                    color_scheme="red",
                    variant="soft",
                    on_click=lambda: State.remove_item("caps", irow),
                )
            ),
        )

    LABELS_SUB = [rx.text(i["fund.sub.label"]), rx.text(i["fund.sub.amount"]), rx.text(i["fund.sub.month"])]
    WIDTHS_SUB = ["45%","30%","20%"]
    def row_sub(s, irow):
        return rx.table.row(
            make_cell(rx.input(value=s.label, on_change=lambda v: State.update_item("subsidies", irow, "label", v, "str")), WIDTHS_SUB[0]),
            make_cell(rx.input(type="number", min=0, value=s.amount, on_change=lambda v: State.update_item("subsidies", irow, "amount", v, "float")), WIDTHS_SUB[1]),
            make_cell(rx.input(type="number", min=1, value=s.month, on_change=lambda v: State.update_item("subsidies", irow, "month", v, "int")), WIDTHS_SUB[2]),
            rx.table.cell(
                rx.button(
                    State.i18n["common.delete"],
                    color_scheme="red",
                    variant="soft",
                    on_click=lambda: State.remove_item("subsidies", irow),
                )
            ),
        )

    LABELS_LOAN = [rx.text(i["fund.loan.label"]), rx.text(i["fund.loan.principal"]), rx.text(i["fund.loan.rate"]), rx.text(i["fund.loan.months"]), rx.text(i["fund.loan.start"])]
    WIDTHS_LOAN = ["25%","18%","18%","16%","18%"]
    def row_loan(l, irow):
        return rx.table.row(
            make_cell(rx.input(value=l.label, on_change=lambda v: State.update_item("loans", irow, "label", v, "str")), WIDTHS_LOAN[0]),
            make_cell(rx.input(type="number", min=0, value=l.principal, on_change=lambda v: State.update_item("loans", irow, "principal", v, "float")), WIDTHS_LOAN[1]),
            make_cell(rx.input(type="number", step=0.1, min=0, max=100, value=l.annual_rate * 100, on_change=lambda v: State.update_item("loans", irow, "annual_rate", v, "percent")), WIDTHS_LOAN[2]),
            make_cell(rx.input(type="number", min=1, value=l.months, on_change=lambda v: State.update_item("loans", irow, "months", v, "int")), WIDTHS_LOAN[3]),
            make_cell(rx.input(type="number", min=1, value=l.start_month, on_change=lambda v: State.update_item("loans", irow, "start_month", v, "int")), WIDTHS_LOAN[4]),
            rx.table.cell(
                rx.button(
                    State.i18n["common.delete"],
                    color_scheme="red",
                    variant="soft",
                    on_click=lambda: State.remove_item("loans", irow),
                )
            ),
        )

    return layout(
        page_with_fixed_title(
            rx.vstack(
                rx.heading(i["fund.title"], size="7"),
                rx.text(i["fund.desc"]),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.heading(i["fund.section.capital"], size="4"),
                rx.table.root(
                    header_row(LABELS_CAP, WIDTHS_CAP),
                    rx.table.body(rx.foreach(State.caps, row_cap)),
                    width="100%",
                ),
                rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_capital)),
                rx.box(height="2"),
                rx.heading(i["fund.section.subsidies"], size="4"),
                rx.table.root(
                    header_row(LABELS_SUB, WIDTHS_SUB),
                    rx.table.body(rx.foreach(State.subsidies, row_sub)),
                    width="100%",
                ),
                rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_subsidy)),
                rx.box(height="2"),
                rx.heading(i["fund.section.loans"], size="4"),
                rx.table.root(
                    header_row(LABELS_LOAN, WIDTHS_LOAN),
                    rx.table.body(rx.foreach(State.loans, row_loan)),
                    width="100%",
                ),
                rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_loan)),
                spacing="3",
                align_items="start",
                width="100%",
            )
        )
    )
