import reflex as rx
from .layout import layout
from ..state import State


@rx.page(on_load=State.on_load, title="FISY — Guide")
def index():
    t = State.i18n
    return layout(
        rx.vstack(
            rx.heading(t["home_title"], size="8"),
            rx.text(t["home_subtitle"]),
            spacing="4",
        )
    )
