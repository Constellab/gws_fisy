import reflex as rx
from ..layout import layout, table
from ...state import State


@rx.page(route="/resultats/cashflow", on_load=State.on_load, title="Résultats — Cashflow")
def cashflow():
    t = State.i18n
    return layout(
        rx.vstack(
            rx.heading(t["res_cf_title"], size="7"),
            rx.text(t["res_cf_desc"]),
            rx.box(height="2"),
            table(State.cashflow_rows, State.cashflow_cols),
            spacing="4",
        )
    )
