import reflex as rx
from ..layout import layout, table
from ...state import State


@rx.page(route="/resultats/bilans", on_load=State.on_load, title="Résultats — Bilans")
def balance_sheets():
    t = State.i18n
    return layout(
        rx.vstack(
            rx.heading(t["res_bs_title"], size="7"),
            rx.text(t["res_bs_desc"]),
            rx.box(height="2"),
            rx.heading(t["res_bs_assets"], size="6"),
            table(State.bilan_actif_rows, State.bilan_actif_cols),
            rx.heading(t["res_bs_liab"], size="6"),
            table(State.bilan_passif_rows, State.bilan_passif_cols),
            spacing="4",
        )
    )
