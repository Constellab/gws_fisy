import reflex as rx
from ..layout import layout, table
from ...state import State


@rx.page(route="/resultats/compte-resultat", on_load=State.on_load, title="Résultats — Compte de résultat")
def income_statement():
    t = State.i18n
    return layout(
        rx.vstack(
            rx.heading(t["res_pnl_title"], size="7"),
            rx.text(t["res_pnl_desc"]),
            rx.box(height="2"),
            table(State.pnl_rows, State.pnl_cols),
            spacing="4",
        )
    )
