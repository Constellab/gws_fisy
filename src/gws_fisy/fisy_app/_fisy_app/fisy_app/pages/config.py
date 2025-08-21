
import reflex as rx
from .layout import layout
from ..state import State

@rx.page(route="/config", on_load=State.on_load, title="Configuration")
def config():
    return layout(
        rx.vstack(
            rx.heading("Configuration générale", size="7"),
            rx.text("Renseignez les paramètres globaux. Les valeurs numériques acceptent les décimales avec un point (ex. 0.2 pour 20%)."),
            rx.box(height="3"),
            rx.vstack(rx.text("Mois (horizon)"),
                      rx.input(type="number", value=State.months, on_change=lambda v: State.set_int("months", v), placeholder="Ex. 36"),
                      spacing="1", align_items="start"),
            rx.vstack(rx.text("TVA par défaut"),
                      rx.input(type="number", step=0.01, value=State.tva_default, on_change=lambda v: State.set_float("tva_default", v), placeholder="Ex. 0.2"),
                      spacing="1", align_items="start"),
            rx.vstack(rx.text("Taux IS (Corporate Tax)"), rx.text(State.corporate_tax_rate), spacing="1", align_items="start"),
            rx.vstack(rx.text("DSO (jours clients)"),
                      rx.input(type="number", value=State.dso_days, on_change=lambda v: State.set_int("dso_days", v), placeholder="Ex. 30"),
                      spacing="1", align_items="start"),
            rx.vstack(rx.text("DPO (jours fournisseurs)"),
                      rx.input(type="number", value=State.dpo_days, on_change=lambda v: State.set_int("dpo_days", v), placeholder="Ex. 30"),
                      spacing="1", align_items="start"),
            rx.vstack(rx.text("DIO (jours stock)"),
                      rx.input(type="number", value=State.dio_days, on_change=lambda v: State.set_int("dio_days", v), placeholder="Ex. 0 si pas de stock"),
                      spacing="1", align_items="start"),
            rx.vstack(rx.text("Trésorerie initiale"),
                      rx.input(type="number", value=State.initial_cash, on_change=lambda v: State.set_float("initial_cash", v), placeholder="Ex. 10000"),
                      spacing="1", align_items="start"),
            spacing="3", align_items="start",
        )
    )
