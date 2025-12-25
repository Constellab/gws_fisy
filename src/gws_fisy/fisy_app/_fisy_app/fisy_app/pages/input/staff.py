import reflex as rx

from ...state import State
from ..layout import header_row, layout, make_cell, page_with_fixed_title


@rx.page(route="/input/staff", on_load=State.on_load, title="Input — Staff")
def staff():
    i = State.i18n
    LABELS = [rx.text(i["staff.role"]), rx.text(i["staff.gross"]), rx.text(i["staff.rate"]), rx.text(i["staff.count"]), rx.text(i["staff.start"]), rx.text(i["staff.end"])]
    WIDTHS = ["23%","16%","16%","16%","12%","12%"]
    def row(p, irow):
        return rx.table.row(
            make_cell(rx.input(value=p.title, on_change=lambda v: State.update_item("personnel", irow, "title", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", min=0, value=p.monthly_salary_gross, on_change=lambda v: State.update_item("personnel", irow, "monthly_salary_gross", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.1, min=0, max=100, value=p.employer_cost_rate * 100, on_change=lambda v: State.update_item("personnel", irow, "employer_cost_rate", v, "percent")), WIDTHS[2]),
            make_cell(rx.input(type="number", min=1, value=p.count, on_change=lambda v: State.update_item("personnel", irow, "count", v, "int")), WIDTHS[3]),
            make_cell(rx.input(type="number", min=1, value=p.start_month, on_change=lambda v: State.update_item("personnel", irow, "start_month", v, "int")), WIDTHS[4]),
            make_cell(rx.input(type="number", min=1, value=p.end_month, on_change=lambda v: State.update_item("personnel", irow, "end_month", v, "int")), WIDTHS[5]),
            rx.table.cell(
                rx.button(
                    State.i18n["common.delete"],
                    color_scheme="red",
                    variant="soft",
                    on_click=lambda: State.remove_item("personnel", irow),
                )
            ),
        )
    return layout(
        page_with_fixed_title(
            rx.vstack(
                rx.heading(i["staff.title"], size="7"),
                rx.text(i["staff.desc"]),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.table.root(
                    header_row(LABELS, WIDTHS),
                    rx.table.body(rx.foreach(State.personnel, row)),
                    width="100%",
                ),
                rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_personnel)),
                spacing="3",
                align_items="start",
                width="100%",
            )
        )
    )
