import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

def qty_chart(data, series_defs):
    return rx.recharts.responsive_container(
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.x_axis(data_key="index"),
            rx.recharts.y_axis(),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.foreach(series_defs, lambda s: rx.recharts.line(data_key=s["key"], type_="monotone", stroke_width=2, stroke=s["color"])),
            data=data,
        ),
        width="100%", height=360
    )

@rx.page(route="/saisie/abonnements", on_load=State.on_load, title="Saisie — Abonnements")
def subscriptions():
    i = State.i18n
    LABELS = [rx.text(i["subs.activity"]), rx.text(i["subs.start"]), rx.text(i["subs.end"]), rx.text(i["subs.q0"]), rx.text(i["subs.growth"])]
    WIDTHS = ["220px","140px","140px","160px","200px"]
    def row(r, irow):
        return rx.table.row(
            make_cell(rx.select(items=State.activity_options, value=r.activity, on_change=lambda v, irow=irow: State.update_item("subscription_ranges", irow, "activity", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", min=1, value=r.start_month, on_change=lambda v, irow=irow: State.update_item("subscription_ranges", irow, "start_month", v, "int")), WIDTHS[1]),
            make_cell(rx.input(type="number", min=1, value=r.end_month, on_change=lambda v, irow=irow: State.update_item("subscription_ranges", irow, "end_month", v, "int")), WIDTHS[2]),
            make_cell(rx.input(type="number", min=0, value=r.q0, on_change=lambda v, irow=irow: State.update_item("subscription_ranges", irow, "q0", v, "float")), WIDTHS[3]),
            make_cell(rx.input(type="number", step=0.01, min=0, value=r.monthly_growth, on_change=lambda v, irow=irow: State.update_item("subscription_ranges", irow, "monthly_growth", v, "float")), WIDTHS[4]),
            actions_cell("subscription_ranges", irow),
        )
    return layout(rx.vstack(
        rx.heading(i["subs.title"], size="5"),
        rx.text(i["subs.desc"]),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger(i["sales.tabs.input"], value="input"),
                rx.tabs.trigger(i["sales.tabs.evolution"], value="evo"),
            ),
            rx.tabs.content(
                rx.vstack(
                    rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.subscription_ranges, row))),
                    rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_subscription)),
                    spacing="3", align_items="start",
                ),
                value="input",
            ),
            rx.tabs.content(
                rx.vstack(qty_chart(State.subscription_qty_chart_rows, State.subscription_qty_series_defs)),
                value="evo",
            ),
            default_value="input",
            orientation="horizontal",
            style={"width":"100%"}
        ),
        spacing="3", align_items="start",
    ))
