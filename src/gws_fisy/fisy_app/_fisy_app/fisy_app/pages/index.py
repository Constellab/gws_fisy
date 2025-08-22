import reflex as rx
from .layout import layout
from ..state import State

@rx.page(on_load=State.on_load, title="FISY — Guide")
def index():
    i = State.i18n
    return layout(
        rx.vstack(
            rx.heading(State.app_title, size="8"),
            rx.text(i["home.desc"]),
            spacing="3",
            align_items="start",
        )
    )
