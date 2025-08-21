
import reflex as rx
from ..layout import layout
from ...state import State

@rx.page(route="/saisie", on_load=State.on_load, title="Saisie — Toutes les pages")
def overview():
    return layout(
        rx.vstack(
            rx.heading("Saisie — Récapitulatif", size="7"),
            rx.text("Saisissez vos données dans les tableaux dynamiques : Activités, Ventes par plages, Commandes, Personnel, Charges, Investissements, Financement."),
            spacing="3",
        )
    )
