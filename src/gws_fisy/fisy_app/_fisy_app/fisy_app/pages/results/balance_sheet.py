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


@rx.page(route="/results/balance-sheets", on_load=State.on_load, title="Results — Balance sheets")
def balance_sheets():
    return layout(
        page_with_fixed_title(
            rx.heading(State.i18n["results.balance_sheets"], " (", State.unit_suffix, ")", size="7"),
            rx.vstack(
                rx.heading(State.i18n["results.balance.assets"], size="5"),
                _table(State.bilan_actif_table_cols, State.bilan_actif_table_values),
                rx.heading(State.i18n["results.balance.liabilities"], size="5"),
                _table(State.bilan_passif_table_cols, State.bilan_passif_table_values),
                spacing="4",
                align_items="start",
                width="100%",
            )
        )
    )
