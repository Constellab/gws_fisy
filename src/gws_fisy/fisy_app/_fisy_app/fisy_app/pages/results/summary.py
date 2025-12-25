import reflex as rx

from ...state import State
from ..layout import layout, page_with_fixed_title


def zoom_controls():
    i = State.i18n
    return rx.vstack(
        rx.text(i.get("zoom.caption", "Time range :"), weight="bold", size="2"),
        rx.hstack(
            rx.vstack(
                rx.text(i["zoom.start"]),
                rx.input(type="number", value=State.zoom_start, on_change=State.zoom_set_start),
                align_items="start",
                spacing="1",
                width="220px",
            ),
            rx.vstack(
                rx.text(i["zoom.end"]),
                rx.input(type="number", value=State.zoom_end, on_change=State.zoom_set_end),
                align_items="start",
                spacing="1",
                width="220px",
            ),
            width="100%",
            align="center",
        ),
        spacing="2",
        align_items="start",
        width="100%",
    )


def synthese_chart_options():
    """Display chart options for synthese chart."""
    i = State.i18n

    return rx.vstack(
        # Series selection
        rx.vstack(
            rx.text(i["chart.variables"], weight="bold", size="2"),
            rx.box(
                rx.flex(
                    rx.foreach(
                        State.synthese_all_series,
                        lambda s: rx.badge(
                            rx.checkbox(
                                s["key"],
                                checked=State.synthese_selected_series.contains(s["key"]),
                                on_change=lambda _: State.toggle_synthese_series(s["key"]),
                            ),
                            color_scheme=rx.cond(
                                State.synthese_selected_series.contains(s["key"]),
                                "blue",
                                "gray"
                            ),
                            variant="soft",
                        ),
                    ),
                    spacing="2",
                    wrap="wrap",
                ),
                max_width="800px",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        # View mode and chart type
        rx.hstack(
            rx.card(
                rx.vstack(
                    rx.text(i["chart.period"], weight="bold", size="2"),
                    rx.radio_group.root(
                        rx.flex(
                            rx.radio_group.item(i["chart.period.yearly"], value="yearly"),
                            rx.radio_group.item(i["chart.period.monthly"], value="monthly"),
                            spacing="3",
                        ),
                        value=State.synthese_view_mode,
                        on_change=State.set_synthese_view_mode,
                    ),
                    spacing="2",
                    align_items="start",
                ),
                variant="surface",
            ),
            rx.card(
                rx.vstack(
                    rx.text(i["chart.type"], weight="bold", size="2"),
                    rx.radio_group.root(
                        rx.flex(
                            rx.radio_group.item(i["chart.type.line"], value="line"),
                            rx.radio_group.item(i["chart.type.bar"], value="bar"),
                            spacing="3",
                        ),
                        value=State.synthese_chart_type,
                        on_change=State.set_synthese_chart_type,
                    ),
                    spacing="2",
                    align_items="start",
                ),
                variant="surface",
            ),
            spacing="4",
        ),
        spacing="4",
        width="100%",
        padding_y="2",
    )


def pnl_chart_options():
    """Display chart options for P&L chart."""
    i = State.i18n

    return rx.vstack(
        # Series selection
        rx.vstack(
            rx.text(i["chart.variables"], weight="bold", size="2"),
            rx.box(
                rx.flex(
                    rx.foreach(
                        State.pnl_all_series,
                        lambda s: rx.badge(
                            rx.checkbox(
                                s["key"],
                                checked=State.pnl_selected_series.contains(s["key"]),
                                on_change=lambda _: State.toggle_pnl_series(s["key"]),
                            ),
                            color_scheme=rx.cond(
                                State.pnl_selected_series.contains(s["key"]),
                                "blue",
                                "gray"
                            ),
                            variant="soft",
                        ),
                    ),
                    spacing="2",
                    wrap="wrap",
                ),
                max_width="800px",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        # View mode and chart type
        rx.hstack(
            rx.card(
                rx.vstack(
                    rx.text(i["chart.period"], weight="bold", size="2"),
                    rx.radio_group.root(
                        rx.flex(
                            rx.radio_group.item(i["chart.period.yearly"], value="yearly"),
                            rx.radio_group.item(i["chart.period.monthly"], value="monthly"),
                            spacing="3",
                        ),
                        value=State.pnl_view_mode,
                        on_change=State.set_pnl_view_mode,
                    ),
                    spacing="2",
                    align_items="start",
                ),
                variant="surface",
            ),
            rx.card(
                rx.vstack(
                    rx.text(i["chart.type"], weight="bold", size="2"),
                    rx.radio_group.root(
                        rx.flex(
                            rx.radio_group.item(i["chart.type.line"], value="line"),
                            rx.radio_group.item(i["chart.type.bar"], value="bar"),
                            spacing="3",
                        ),
                        value=State.pnl_chart_type,
                        on_change=State.set_pnl_chart_type,
                    ),
                    spacing="2",
                    align_items="start",
                ),
                variant="surface",
            ),
            spacing="4",
        ),
        spacing="4",
        width="100%",
        padding_y="2",
    )


def cashflow_chart_options():
    """Display chart options for cashflow chart."""
    i = State.i18n

    return rx.vstack(
        # Series selection
        rx.vstack(
            rx.text(i["chart.variables"], weight="bold", size="2"),
            rx.box(
                rx.flex(
                    rx.foreach(
                        State.cashflow_all_series,
                        lambda s: rx.badge(
                            rx.checkbox(
                                s["key"],
                                checked=State.cashflow_selected_series.contains(s["key"]),
                                on_change=lambda _: State.toggle_cashflow_series(s["key"]),
                            ),
                            color_scheme=rx.cond(
                                State.cashflow_selected_series.contains(s["key"]),
                                "blue",
                                "gray"
                            ),
                            variant="soft",
                        ),
                    ),
                    spacing="2",
                    wrap="wrap",
                ),
                max_width="800px",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        # View mode and chart type
        rx.hstack(
            rx.card(
                rx.vstack(
                    rx.text(i["chart.period"], weight="bold", size="2"),
                    rx.radio_group.root(
                        rx.flex(
                            rx.radio_group.item(i["chart.period.yearly"], value="yearly"),
                            rx.radio_group.item(i["chart.period.monthly"], value="monthly"),
                            spacing="3",
                        ),
                        value=State.cashflow_view_mode,
                        on_change=State.set_cashflow_view_mode,
                    ),
                    spacing="2",
                    align_items="start",
                ),
                variant="surface",
            ),
            rx.card(
                rx.vstack(
                    rx.text(i["chart.type"], weight="bold", size="2"),
                    rx.radio_group.root(
                        rx.flex(
                            rx.radio_group.item(i["chart.type.line"], value="line"),
                            rx.radio_group.item(i["chart.type.bar"], value="bar"),
                            spacing="3",
                        ),
                        value=State.cashflow_chart_type,
                        on_change=State.set_cashflow_chart_type,
                    ),
                    spacing="2",
                    align_items="start",
                ),
                variant="surface",
            ),
            spacing="4",
        ),
        spacing="4",
        width="100%",
        padding_y="2",
    )


def line_chart(data, x_key, series_defs, unit=""):
    return rx.recharts.responsive_container(
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.x_axis(data_key=x_key),
            rx.recharts.y_axis(unit=unit),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.foreach(
                series_defs,
                lambda s: rx.recharts.line(
                    data_key=s["key"],
                    type_="monotone",
                    stroke_width=2,
                    stroke=s["color"],
                    dot={"fill": s["color"], "r": 3},
                    unit=s["unit"],
                ),
            ),
            rx.recharts.brush(data_key=x_key, height=22),
            data=data,
        ),
        width="100%",
        height=360,
    )


def bar_chart(data, x_key, series_defs, unit=""):
    return rx.recharts.responsive_container(
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.x_axis(data_key=x_key),
            rx.recharts.y_axis(unit=unit),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.foreach(
                series_defs,
                lambda s: rx.recharts.bar(
                    data_key=s["key"],
                    fill=s["color"],
                    unit=s["unit"],
                ),
            ),
            data=data,
        ),
        width="100%",
        height=360,
    )


def _table(cols, rows_values):
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.foreach(cols, lambda c: rx.table.column_header_cell(c))
            )
        ),
        rx.table.body(
            rx.foreach(
                rows_values,
                lambda r: rx.table.row(
                    rx.foreach(r, lambda cell: rx.table.cell(cell))
                ),
            )
        ),
        style={"maxWidth": "100%", "overflowX": "auto"},
    )


@rx.page(route="/results/summary", on_load=State.on_load, title="Results — Summary")
def summary():
    return layout(
        page_with_fixed_title(
            rx.heading(State.i18n["results.syn"], " (", State.synthese_y_unit_suffix, ")", size="7"),
            rx.vstack(
                zoom_controls(),
                rx.box(height="2"),
                synthese_chart_options(),
                rx.box(height="2"),
                rx.cond(
                    State.synthese_chart_type == "line",
                    line_chart(State.synthese_chart_rows, "index", State.synthese_series_defs, State.synthese_y_unit_suffix),
                    bar_chart(State.synthese_chart_rows, "index", State.synthese_series_defs, State.synthese_y_unit_suffix),
                ),
                rx.box(height="3"),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(State.i18n["results.tabs.annual"], value="y"),
                        rx.tabs.trigger(State.i18n["results.tabs.monthly"], value="m"),
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            _table(State.synthese_table_annual_cols, State.synthese_table_annual_values)
                        ),
                        value="y",
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            _table(State.synthese_table_monthly_cols, State.synthese_table_monthly_values)
                        ),
                        value="m",
                    ),
                    default_value="y",
                    style={"width": "100%"},
                ),
                spacing="4",
                align_items="start",
                width="100%",
            )
        )
    )
