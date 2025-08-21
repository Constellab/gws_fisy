import reflex as rx
from ..layout import layout
from ...state import State

@rx.page(route="/saisie", on_load=State.on_load, title="Saisie — Toutes les pages")
def overview():
    t = State.i18n
    return layout(
        rx.vstack(
            rx.heading(t["nav_input_overview"], size="7"),
            rx.text(""),
            spacing="3",
        )
    )
