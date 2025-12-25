import reflex as rx

from ...state import State
from ..layout import layout, page_with_fixed_title
from .summary import bar_chart, cashflow_chart_options, line_chart, zoom_controls


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


@rx.page(route="/results/cashflow", on_load=State.on_load, title="Results — Cashflow")
def cashflow():
    return layout(
        page_with_fixed_title(
            rx.heading(State.i18n["results.cf"], " (", State.cashflow_y_unit_suffix, ")", size="7"),
            rx.vstack(
                zoom_controls(),
                rx.box(height="2"),
                cashflow_chart_options(),
                rx.box(height="2"),
                rx.cond(
                    State.cashflow_chart_type == "line",
                    line_chart(State.cashflow_chart_rows, "index", State.cashflow_series_defs, State.cashflow_y_unit_suffix),
                    bar_chart(State.cashflow_chart_rows, "index", State.cashflow_series_defs, State.cashflow_y_unit_suffix),
                ),
                rx.box(height="3"),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(State.i18n["results.tabs.annual"], value="y"),
                        rx.tabs.trigger(State.i18n["results.tabs.monthly"], value="m"),
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            _table(State.cashflow_table_annual_cols, State.cashflow_table_annual_values)
                        ),
                        value="y",
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            _table(State.cashflow_table_monthly_cols, State.cashflow_table_monthly_values)
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
