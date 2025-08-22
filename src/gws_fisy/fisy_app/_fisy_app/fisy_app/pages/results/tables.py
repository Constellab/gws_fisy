# fisy_app/pages/results/tables.py
import reflex as rx
from ..layout import layout
from ...state import State


def _table(cols, rows_values):
    """
    cols: Var[list[str]]
    rows_values: Var[list[list[str]]]  # chaque ligne est déjà ordonnée côté State
    """
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.foreach(cols, lambda c: rx.table.column_header_cell(c))
            )
        ),
        rx.table.body(
            rx.foreach(
                rows_values,
                lambda r: rx.table.row(
                    rx.foreach(r, lambda cell: rx.table.cell(cell))
                ),
            )
        ),
        style={"maxWidth": "100%", "overflowX": "auto"},
    )


@rx.page(route="/resultats/synthese", on_load=State.on_load, title="Résultats — Synthèse")
def result_synthese():
    return layout(
        rx.vstack(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(State.i18n["results.tabs.annual"], value="y"),
                    rx.tabs.trigger(State.i18n["results.tabs.monthly"], value="m"),
                ),
                rx.tabs.content(
                    rx.vstack(
                        _table(State.synthese_table_annual_cols, State.synthese_table_annual_values)
                    ),
                    value="y",
                ),
                rx.tabs.content(
                    rx.vstack(
                        _table(State.synthese_table_monthly_cols, State.synthese_table_monthly_values)
                    ),
                    value="m",
                ),
                default_value="y",
                style={"width": "100%"},
            ),
            spacing="4",
            align_items="start",
        )
    )


@rx.page(route="/resultats/compte-resultat", on_load=State.on_load, title="Résultats — Compte de résultat")
def result_pnl():
    return layout(
        rx.vstack(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(State.i18n["results.tabs.annual"], value="y"),
                    rx.tabs.trigger(State.i18n["results.tabs.monthly"], value="m"),
                ),
                rx.tabs.content(
                    rx.vstack(
                        _table(State.pnl_table_annual_cols, State.pnl_table_annual_values)
                    ),
                    value="y",
                ),
                rx.tabs.content(
                    rx.vstack(
                        _table(State.pnl_table_monthly_cols, State.pnl_table_monthly_values)
                    ),
                    value="m",
                ),
                default_value="y",
                style={"width": "100%"},
            ),
            spacing="4",
            align_items="start",
        )
    )


@rx.page(route="/resultats/cashflow", on_load=State.on_load, title="Résultats — Cashflow")
def result_cashflow():
    return layout(
        rx.vstack(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(State.i18n["results.tabs.annual"], value="y"),
                    rx.tabs.trigger(State.i18n["results.tabs.monthly"], value="m"),
                ),
                rx.tabs.content(
                    rx.vstack(
                        _table(State.cashflow_table_annual_cols, State.cashflow_table_annual_values)
                    ),
                    value="y",
                ),
                rx.tabs.content(
                    rx.vstack(
                        _table(State.cashflow_table_monthly_cols, State.cashflow_table_monthly_values)
                    ),
                    value="m",
                ),
                default_value="y",
                style={"width": "100%"},
            ),
            spacing="4",
            align_items="start",
        )
    )


@rx.page(route="/resultats/plan-financement", on_load=State.on_load, title="Résultats — Plan de financement")
def result_plan():
    # Pour l'onglet mensuel du plan, on réutilise (temporairement) les colonnes/valeurs mensuelles du cashflow,
    # sauf si tu ajoutes des vars dédiées plan_table_monthly_cols/values dans State.
    return layout(
        rx.vstack(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(State.i18n["results.tabs.annual"], value="y"),
                    rx.tabs.trigger(State.i18n["results.tabs.monthly"], value="m"),
                ),
                rx.tabs.content(
                    rx.vstack(
                        _table(State.plan_table_annual_cols, State.plan_table_annual_values)
                    ),
                    value="y",
                ),
                rx.tabs.content(
                    rx.vstack(
                        _table(State.cashflow_table_monthly_cols, State.cashflow_table_monthly_values)
                    ),
                    value="m",
                ),
                default_value="y",
                style={"width": "100%"},
            ),
            spacing="4",
            align_items="start",
        )
    )


@rx.page(route="/resultats/bilans", on_load=State.on_load, title="Résultats — Bilans")
def result_bilans():
    return layout(
        rx.vstack(
            rx.heading("Bilan — Actif", size="5"),
            _table(State.bilan_actif_table_cols, State.bilan_actif_table_values),
            rx.heading("Bilan — Passif", size="5"),
            _table(State.bilan_passif_table_cols, State.bilan_passif_table_values),
            spacing="4",
            align_items="start",
        )
    )
