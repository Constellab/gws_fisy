
import reflex as rx
from .layout import layout
from ..state import State


@rx.page(on_load=State.on_load, title="FISY — Guide")
def index():
    return layout(
        rx.vstack(
            rx.heading("Bienvenue 👋", size="8"),
            rx.text(
                "Utilisez le menu latéral pour naviguer. Les tableaux de bord proposent des graphiques et le zoom par période."),
            spacing="4",))
