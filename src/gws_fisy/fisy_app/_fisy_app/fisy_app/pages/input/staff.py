import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/personnel", on_load=State.on_load, title="Saisie — Personnel")
def staff():
    t = State.i18n
    LABELS = [t["staff_col_title"], t["staff_col_salary"], t["staff_col_rate"], t["staff_col_start"], t["staff_col_end"]]
    WIDTHS = ["220px","180px","160px","140px","140px"]

    def row(p, i):
        return rx.table.row(
            make_cell(rx.input(value=p.title, on_change=lambda v, i=i: State.update_item("personnel", i, "title", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", value=p.monthly_salary_gross, on_change=lambda v, i=i: State.update_item("personnel", i, "monthly_salary_gross", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.01, value=p.employer_cost_rate, on_change=lambda v, i=i: State.update_item("personnel", i, "employer_cost_rate", v, "float")), WIDTHS[2]),
            make_cell(rx.input(type="number", value=p.start_month, on_change=lambda v, i=i: State.update_item("personnel", i, "start_month", v, "int")), WIDTHS[3]),
            make_cell(rx.input(type="number", value=p.end_month, on_change=lambda v, i=i: State.update_item("personnel", i, "end_month", v, "int")), WIDTHS[4]),
            actions_cell("personnel", i),
        )

    return layout(
        rx.vstack(
            rx.heading(t["staff_title"], size="5"),
            rx.text(t["staff_desc"]),
            rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.personnel, row))),
            rx.hstack(rx.button(t["staff_add"], on_click=State.add_personnel)),
            spacing="3", align_items="start",
        )
    )
