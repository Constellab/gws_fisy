
import reflex as rx
from .layout import layout
from ..state import State


@rx.page(on_load=State.on_load, title="FISY — Guide")
def index():
    return layout(
        rx.vstack(
            rx.heading("Bienvenue 👋", size="8"),
            rx.text(
                "Utilisez le menu pour saisir vos hypothèses. Les Abonnements alimentent aussi la métrique MRR dans la synthèse."),
            spacing="4",))
