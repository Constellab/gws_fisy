
import reflex as rx
from ..layout import layout, table
from ...state import State

@rx.page(route="/resultats/plan-financement", on_load=State.on_load, title="Résultats — Plan de financement")
def funding_plan():
    return layout(
        rx.vstack(
            rx.heading("Plan de financement (annuel)", size="7"),
            rx.text("Vision annuelle des ressources et emplois, consolidée par année."),
            rx.box(height="2"),
            table(State.plan_rows, State.plan_cols),
            spacing="4",
        )
    )
