
import reflex as rx
from ..layout import layout, table
from ...state import State

@rx.page(route="/resultats/compte-resultat", on_load=State.on_load, title="Résultats — Compte de résultat")
def income_statement():
    return layout(
        rx.vstack(
            rx.heading("Compte de résultat (mensuel)", size="7"),
            rx.text("Produits et charges mensuels."),
            rx.box(height="2"),
            table(State.pnl_rows, State.pnl_cols),
            spacing="4",
        )
    )
