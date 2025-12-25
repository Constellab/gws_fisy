import reflex as rx

from ...state import State
from ..layout import header_row, layout, make_cell, page_with_fixed_title


def qty_chart(data, series_defs):
    return rx.recharts.responsive_container(
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.x_axis(data_key="index"),
            rx.recharts.y_axis(),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.foreach(series_defs, lambda s: rx.recharts.line(data_key=s["key"], type_="monotone", stroke_width=2, stroke=s["color"], dot={"fill": s["color"], "r": 3})),
            data=data,
        ),
        width="100%", height=360
    )

@rx.page(route="/input/one-time-sales", on_load=State.on_load, title="Input — One-time sales")
def one_time():
    i = State.i18n
    LABELS = [rx.text(i["one_time.activity"]), rx.text(i["one_time.start"]), rx.text(i["one_time.end"]), rx.text(i["one_time.q0"]), rx.text(i["one_time.growth"])]
    WIDTHS = ["25%","16%","16%","18%","20%"]
    def row(r, irow):
        return rx.table.row(
            make_cell(rx.select(items=State.activity_options, value=r.activity, on_change=lambda v: State.update_item("one_time_ranges", irow, "activity", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", min=1, value=r.start_month, on_change=lambda v: State.update_item("one_time_ranges", irow, "start_month", v, "int")), WIDTHS[1]),
            make_cell(rx.input(type="number", min=1, value=r.end_month, on_change=lambda v: State.update_item("one_time_ranges", irow, "end_month", v, "int")), WIDTHS[2]),
            make_cell(rx.input(type="number", min=0, value=r.q0, on_change=lambda v: State.update_item("one_time_ranges", irow, "q0", v, "float")), WIDTHS[3]),
            make_cell(rx.input(type="number", step=0.1, min=-100, max=1000, value=r.monthly_growth * 100, on_change=lambda v: State.update_item("one_time_ranges", irow, "monthly_growth", v, "percent")), WIDTHS[4]),
            rx.table.cell(
                rx.button(
                    State.i18n["common.delete"],
                    color_scheme="red",
                    variant="soft",
                    on_click=lambda: State.remove_item("one_time_ranges", irow),
                )
            ),
        )
    return layout(
        page_with_fixed_title(
            rx.vstack(
                rx.heading(i["one_time.title"], size="7"),
                rx.text(i["one_time.desc"]),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(i["sales.tabs.input"], value="input"),
                        rx.tabs.trigger(i["sales.tabs.evolution"], value="evo"),
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            rx.table.root(
                                header_row(LABELS, WIDTHS),
                                rx.table.body(rx.foreach(State.one_time_ranges, row)),
                                width="100%",
                            ),
                            rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_one_time)),
                            spacing="3", align_items="start", width="100%",
                        ),
                        value="input",
                    ),
                    rx.tabs.content(
                        rx.vstack(qty_chart(State.one_time_qty_chart_rows, State.one_time_qty_series_defs)),
                        value="evo",
                    ),
                    default_value="input",
                    orientation="horizontal",
                    style={"width":"100%"}
                ),
                spacing="3",
                align_items="start",
                width="100%",
            )
        )
    )
