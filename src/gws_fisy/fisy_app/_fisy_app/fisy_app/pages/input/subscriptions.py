import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/abonnements", on_load=State.on_load, title="Saisie — Abonnement (Ventes récurrentes)")
def subscriptions():
    t = State.i18n
    LABELS = [t["sub_col_activity"], t["sub_col_start"], t["sub_col_end"], t["sub_col_q0"], t["sub_col_growth"]]
    WIDTHS = ["220px","140px","140px","160px","200px"]

    def row(r, i):
        return rx.table.row(
            make_cell(rx.select(items=State.activity_options, value=r.activity, on_change=lambda v, i=i: State.update_item("subscription_ranges", i, "activity", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", value=r.start_month, on_change=lambda v, i=i: State.update_item("subscription_ranges", i, "start_month", v, "int")), WIDTHS[1]),
            make_cell(rx.input(type="number", value=r.end_month, on_change=lambda v, i=i: State.update_item("subscription_ranges", i, "end_month", v, "int")), WIDTHS[2]),
            make_cell(rx.input(type="number", value=r.q0, on_change=lambda v, i=i: State.update_item("subscription_ranges", i, "q0", v, "float")), WIDTHS[3]),
            make_cell(rx.input(type="number", step=0.01, value=r.monthly_growth, on_change=lambda v, i=i: State.update_item("subscription_ranges", i, "monthly_growth", v, "float")), WIDTHS[4]),
            actions_cell("subscription_ranges", i),
        )

    return layout(
        rx.vstack(
            rx.heading(t["sub_title"], size="5"),
            rx.text(t["sub_desc"]),
            rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.subscription_ranges, row))),
            rx.hstack(rx.button(t["sub_add"], on_click=State.add_subscription)),
            spacing="3", align_items="start",
        )
    )
