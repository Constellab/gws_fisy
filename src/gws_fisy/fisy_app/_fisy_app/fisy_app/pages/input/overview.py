
import reflex as rx
from ..layout import layout
from ...state import State

@rx.page(route="/saisie", on_load=State.on_load, title="Saisie — Toutes les pages")
def overview():
    return layout(
        rx.vstack(
            rx.heading("Saisie — Récapitulatif", size="7"),
            rx.text("Saisissez vos activités, ventes ponctuelles, abonnements, RH, charges, investissements, financement."),
            spacing="3",
        )
    )
