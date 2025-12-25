import reflex as rx

from ...state import State
from ..layout import layout, page_with_fixed_title


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


@rx.page(route="/results/funding-plan", on_load=State.on_load, title="Results — Funding plan")
def funding_plan():
    return layout(
        page_with_fixed_title(
            rx.heading(State.i18n["results.funding_plan"], " (", State.unit_suffix, ")", size="7"),
            rx.vstack(
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(State.i18n["results.tabs.annual"], value="y"),
                        rx.tabs.trigger(State.i18n["results.tabs.monthly"], value="m"),
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            _table(State.plan_table_annual_cols, State.plan_table_annual_values)
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
