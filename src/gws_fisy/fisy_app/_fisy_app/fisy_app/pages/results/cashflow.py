
import reflex as rx
from ..layout import layout, table
from ...state import State

@rx.page(route="/resultats/cashflow", on_load=State.on_load, title="Résultats — Cashflow")
def cashflow():
    return layout(
        rx.vstack(
            rx.heading("Tableau de trésorerie (mensuel)", size="7"),
            rx.text("Entrées et sorties de cash (TTC avec règlement TVA net décalé)."),
            rx.box(height="2"),
            table(State.cashflow_rows, State.cashflow_cols),
            spacing="4",
        )
    )
