import reflex as rx
from ..layout import layout, table
from ...state import State

@rx.page(route="/resultats/synthese", on_load=State.on_load, title="Résultats — Synthèse")
def summary():
    t = State.i18n
    return layout(
        rx.vstack(
            rx.heading(t["res_summary_title"], size="7"),
            rx.text(t["res_summary_desc"]),
            rx.box(height="2"),
            table(State.synthese_rows, State.synthese_cols),
            spacing="4",
        )
    )
