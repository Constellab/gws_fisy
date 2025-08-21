
import reflex as rx
from ..layout import layout, table
from ...state import State

@rx.page(route="/resultats/synthese", on_load=State.on_load, title="Résultats — Synthèse")
def summary():
    return layout(
        rx.vstack(
            rx.heading("Synthèse", size="7"),
            rx.text("Vue d’ensemble des indicateurs clés calculés à partir de vos saisies."),
            rx.box(height="2"),
            table(State.synthese_rows, State.synthese_cols),
            spacing="4",
        )
    )
