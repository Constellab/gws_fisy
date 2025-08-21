import reflex as rx
from ..layout import layout, table
from ...state import State

@rx.page(route="/resultats/plan-financement", on_load=State.on_load, title="Résultats — Plan de financement")
def funding_plan():
    t = State.i18n
    return layout(
        rx.vstack(
            rx.heading(t["res_plan_title"], size="7"),
            rx.text(t["res_plan_desc"]),
            rx.box(height="2"),
            table(State.plan_rows, State.plan_cols),
            spacing="4",
        )
    )
