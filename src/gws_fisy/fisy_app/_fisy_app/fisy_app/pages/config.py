import reflex as rx
from .layout import layout
from ..state import State


@rx.page(route="/config", on_load=State.on_load, title="Configuration")
def config():
    return layout(
        rx.vstack(
            rx.heading("Configuration générale", size="7"),
            rx.text("Paramètres globaux du modèle."),
            rx.box(height="3"),

            # --- Currency ---
            rx.vstack(
                rx.text("Monnaie"),
                rx.select(
                    items=["EUR", "USD", "GBP", "CHF", "CAD", "AUD", "JPY"],
                    value=State.currency_code,
                    on_change=State.set_currency_code,
                ),
                # ❌ no lambda here — just compose texts
                rx.hstack(rx.text("Symbole : "), rx.text(State.currency_symbol)),
                spacing="1",
                align_items="start",
            ),

            # --- Scale ---
            rx.vstack(
                rx.text("Affichage des montants"),
                rx.select(
                    items=["units", "thousands", "millions"],
                    value=State.scale_mode,
                    on_change=State.set_scale_mode,
                ),
                # ❌ no lambda here either
                rx.hstack(rx.text("Unité affichée : "), rx.text(State.unit_suffix)),
                spacing="1",
                align_items="start",
            ),

            rx.box(height="3"),

            # --- Existing fields ---
            rx.vstack(
                rx.text("Mois (horizon)"),
                rx.input(
                    type="number", value=State.months,
                    on_change=lambda v: State.set_int("months", v)
                ),
                spacing="1", align_items="start"
            ),

            rx.vstack(
                rx.text("TVA par défaut"),
                rx.input(
                    type="number", step=0.01, value=State.tva_default,
                    on_change=lambda v: State.set_float("tva_default", v)
                ),
                spacing="1", align_items="start"
            ),

            rx.vstack(
                rx.text("Taux IS (Corporate Tax)"),
                rx.text(State.corporate_tax_rate),
                spacing="1", align_items="start"
            ),

            rx.vstack(
                rx.text("DSO (jours clients)"),
                rx.input(
                    type="number", value=State.dso_days,
                    on_change=lambda v: State.set_int("dso_days", v)
                ),
                spacing="1", align_items="start"
            ),

            rx.vstack(
                rx.text("DPO (jours fournisseurs)"),
                rx.input(
                    type="number", value=State.dpo_days,
                    on_change=lambda v: State.set_int("dpo_days", v)
                ),
                spacing="1", align_items="start"
            ),

            rx.vstack(
                rx.text("DIO (jours stock)"),
                rx.input(
                    type="number", value=State.dio_days,
                    on_change=lambda v: State.set_int("dio_days", v)
                ),
                spacing="1", align_items="start"
            ),

            rx.vstack(
                rx.text("Trésorerie initiale"),
                rx.input(
                    type="number", value=State.initial_cash,
                    on_change=lambda v: State.set_float("initial_cash", v)
                ),
                spacing="1", align_items="start"
            ),

            spacing="3", align_items="start",
        )
    )
