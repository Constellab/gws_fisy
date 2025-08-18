import reflex as rx
from gws_reflex_base import add_unauthorized_page, get_theme, render_main_container
from gws_reflex_main import ReflexMainState

from .state import State


def _table(rows, cols) -> rx.Component:
    """Rendu table 100% réactif (pas de truthiness ni itération Python sur Vars)."""
    return rx.table.root(
        rx.table.header(
            rx.table.row(rx.foreach(cols, lambda c: rx.table.column_header_cell(c)))
        ),
        rx.table.body(
            rx.foreach(
                rows,
                lambda r: rx.table.row(
                    rx.foreach(cols, lambda c: rx.table.cell(rx.text(r[c])))
                ),
            )
        ),
    )


def _list_editor(label: str, items, render_row):
    return rx.vstack(
        rx.heading(label, size="5"),
        rx.vstack(rx.foreach(items, render_row), spacing="2"),
        spacing="3",
    )


app = rx.App(theme=get_theme())


@rx.page(on_load=ReflexMainState.on_load, title="FISY — Guide")
def index():
    return render_main_container(
        rx.vstack(
            rx.heading(State.app_title, size="8"),
            rx.text("Cette app Reflex reprend le FISY : configuration, saisie, résultats."),
            rx.link("→ Configuration", href="/config"),
            rx.link("→ Saisie (toutes les pages)", href="/saisie"),
            rx.link("→ Résultats — Synthèse", href="/resultats/synthese"),
            spacing="4",
        )
    )


@rx.page(route="/config", on_load=ReflexMainState.on_load, title="Configuration")
def config():
    return render_main_container(
        rx.vstack(
            rx.heading("Configuration générale", size="7"),

            rx.hstack(
                rx.text("Mois (horizon)"),
                rx.input(type="number", value=State.months,
                         on_change=lambda v: State.set_int("months", v)),
            ),

            rx.hstack(
                rx.text("TVA par défaut"),
                rx.input(type="number", step=0.01, value=State.tva_default,
                         on_change=lambda v: State.set_float("tva_default", v)),
            ),

            rx.hstack(
                rx.text("Taux IS (Corporate Tax)"),
                # lecture seule (souvent injecté via Constellab)
                rx.text(State.corporate_tax_rate),
            ),

            rx.hstack(
                rx.text("DSO (jours clients)"),
                rx.input(type="number", value=State.dso_days,
                         on_change=lambda v: State.set_int("dso_days", v)),
            ),

            rx.hstack(
                rx.text("DPO (jours fournisseurs)"),
                rx.input(type="number", value=State.dpo_days,
                         on_change=lambda v: State.set_int("dpo_days", v)),
            ),

            rx.hstack(
                rx.text("DIO (jours stock)"),
                rx.input(type="number", value=State.dio_days,
                         on_change=lambda v: State.set_int("dio_days", v)),
            ),

            rx.hstack(
                rx.text("Trésorerie initiale"),
                rx.input(type="number", value=State.initial_cash,
                         on_change=lambda v: State.set_float("initial_cash", v)),
            ),

            spacing="3",
        )
    )


@rx.page(route="/saisie", on_load=ReflexMainState.on_load, title="Saisie — Toutes les pages")
def saisie_all():
    return render_main_container(
        rx.vstack(
            rx.heading("Saisie — Récapitulatif", size="7"),
            rx.link("Activités", href="/saisie/activites"),
            rx.link("Commandes (ventes)", href="/saisie/commandes"),
            rx.link("Personnel", href="/saisie/personnel"),
            rx.link("Charges externes", href="/saisie/charges"),
            rx.link("Investissements", href="/saisie/investissements"),
            rx.link("Financement (apports, subventions, prêts)", href="/saisie/financement"),
            spacing="3",
        )
    )


@rx.page(route="/saisie/activites", on_load=ReflexMainState.on_load, title="Saisie — Activités")
def saisie_activites():
    def row(a, i):
        return rx.hstack(
            rx.input(
                value=a.name,
                on_change=lambda v, i=i: State.update_item("activities", i, "name", v, "str"),
            ),
            rx.input(
                type="number",
                value=a.unit_price_ht,
                on_change=lambda v, i=i: State.update_item("activities", i, "unit_price_ht", v, "float"),
            ),
            rx.input(
                type="number",
                step=0.01,
                value=a.vat_rate,
                on_change=lambda v, i=i: State.update_item("activities", i, "vat_rate", v, "float"),
            ),
            rx.input(
                type="number",
                value=a.variable_cost_per_unit_ht,
                on_change=lambda v, i=i: State.update_item("activities", i, "variable_cost_per_unit_ht", v, "float"),
            ),
            rx.input(
                type="number",
                step=0.01,
                value=a.variable_cost_rate_on_price,
                on_change=lambda v, i=i: State.update_item("activities", i, "variable_cost_rate_on_price", v, "float"),
            ),
            spacing="2",
        )

    return render_main_container(
        rx.vstack(
            _list_editor("Activités", State.activities, row),
            rx.button("Ajouter une activité", on_click=State.add_activity),
            spacing="4",
        )
    )


@rx.page(route="/saisie/commandes", on_load=ReflexMainState.on_load, title="Saisie — Commandes")
def saisie_commandes():
    def row(c, i):
        return rx.hstack(
            rx.select(
                items=State.activity_options,            # <- high-level Select requires `items`
                value=c.activity,                        # controlled value
                on_change=lambda v, i=i: State.update_item("orders", i, "activity", v, "str"),
            ),
            rx.input(
                type="number",
                value=c.month_index,
                on_change=lambda v, i=i: State.update_item("orders", i, "month_index", v, "int"),
            ),
            rx.input(
                type="number",
                value=c.quantity,
                on_change=lambda v, i=i: State.update_item("orders", i, "quantity", v, "float"),
            ),
            spacing="2",
        )

    return render_main_container(
        rx.vstack(
            _list_editor("Commandes", State.orders, row),
            rx.button("Ajouter une commande", on_click=State.add_order),
            spacing="4",
        )
    )


@rx.page(route="/saisie/personnel", on_load=ReflexMainState.on_load, title="Saisie — Personnel")
def saisie_personnel():
    def row(p, i):
        return rx.hstack(
            rx.input(
                value=p.title,
                on_change=lambda v, i=i: State.update_item("personnel", i, "title", v, "str"),
            ),
            rx.input(
                type="number",
                value=p.monthly_salary_gross,
                on_change=lambda v, i=i: State.update_item("personnel", i, "monthly_salary_gross", v, "float"),
            ),
            rx.input(
                type="number",
                step=0.01,
                value=p.employer_cost_rate,
                on_change=lambda v, i=i: State.update_item("personnel", i, "employer_cost_rate", v, "float"),
            ),
            rx.input(
                type="number",
                value=p.start_month,
                on_change=lambda v, i=i: State.update_item("personnel", i, "start_month", v, "int"),
            ),
            rx.input(
                type="number",
                value=p.end_month,
                on_change=lambda v, i=i: State.update_item("personnel", i, "end_month", v, "int"),
            ),
            spacing="2",
        )

    return render_main_container(
        rx.vstack(
            _list_editor("Personnel", State.personnel, row),
            rx.button("Ajouter un poste", on_click=State.add_personnel),
            spacing="4",
        )
    )


@rx.page(route="/saisie/charges", on_load=ReflexMainState.on_load, title="Saisie — Charges externes")
def saisie_charges():
    def row(c, i):
        return rx.hstack(
            rx.input(
                value=c.label,
                on_change=lambda v, i=i: State.update_item("charges", i, "label", v, "str"),
            ),
            rx.input(
                type="number",
                value=c.monthly_amount_ht,
                on_change=lambda v, i=i: State.update_item("charges", i, "monthly_amount_ht", v, "float"),
            ),
            rx.input(
                type="number",
                step=0.01,
                value=c.vat_rate,
                on_change=lambda v, i=i: State.update_item("charges", i, "vat_rate", v, "float"),
            ),
            rx.input(
                type="number",
                value=c.start_month,
                on_change=lambda v, i=i: State.update_item("charges", i, "start_month", v, "int"),
            ),
            rx.input(
                type="number",
                value=c.end_month,
                on_change=lambda v, i=i: State.update_item("charges", i, "end_month", v, "int"),
            ),
            spacing="2",
        )

    return render_main_container(
        rx.vstack(
            _list_editor("Charges externes", State.charges, row),
            rx.button("Ajouter une charge", on_click=State.add_charge),
            spacing="4",
        )
    )


@rx.page(route="/saisie/investissements", on_load=ReflexMainState.on_load, title="Saisie — Investissements")
def saisie_invest():
    def row(inv, i):
        return rx.hstack(
            rx.input(
                value=inv.label,
                on_change=lambda v, i=i: State.update_item("investments", i, "label", v, "str"),
            ),
            rx.input(
                type="number",
                value=inv.amount_ht,
                on_change=lambda v, i=i: State.update_item("investments", i, "amount_ht", v, "float"),
            ),
            rx.input(
                type="number",
                step=0.01,
                value=inv.vat_rate,
                on_change=lambda v, i=i: State.update_item("investments", i, "vat_rate", v, "float"),
            ),
            rx.input(
                type="number",
                value=inv.purchase_month,
                on_change=lambda v, i=i: State.update_item("investments", i, "purchase_month", v, "int"),
            ),
            rx.input(
                type="number",
                value=inv.amort_years,
                on_change=lambda v, i=i: State.update_item("investments", i, "amort_years", v, "int"),
            ),
            spacing="2",
        )

    return render_main_container(
        rx.vstack(
            _list_editor("Investissements", State.investments, row),
            rx.button("Ajouter un investissement", on_click=State.add_investment),
            spacing="4",
        )
    )


@rx.page(route="/saisie/financement", on_load=ReflexMainState.on_load, title="Saisie — Financement")
def saisie_financement():
    def row_cap(c, i):
        return rx.hstack(
            rx.input(
                value=c.label,
                on_change=lambda v, i=i: State.update_item("caps", i, "label", v, "str"),
            ),
            rx.input(
                type="number",
                value=c.amount,
                on_change=lambda v, i=i: State.update_item("caps", i, "amount", v, "float"),
            ),
            rx.input(
                type="number",
                value=c.month,
                on_change=lambda v, i=i: State.update_item("caps", i, "month", v, "int"),
            ),
            spacing="2",
        )

    def row_sub(s, i):
        return rx.hstack(
            rx.input(
                value=s.label,
                on_change=lambda v, i=i: State.update_item("subsidies", i, "label", v, "str"),
            ),
            rx.input(
                type="number",
                value=s.amount,
                on_change=lambda v, i=i: State.update_item("subsidies", i, "amount", v, "float"),
            ),
            rx.input(
                type="number",
                value=s.month,
                on_change=lambda v, i=i: State.update_item("subsidies", i, "month", v, "int"),
            ),
            spacing="2",
        )

    def row_loan(l, i):
        return rx.hstack(
            rx.input(
                value=l.label,
                on_change=lambda v, i=i: State.update_item("loans", i, "label", v, "str"),
            ),
            rx.input(
                type="number",
                value=l.principal,
                on_change=lambda v, i=i: State.update_item("loans", i, "principal", v, "float"),
            ),
            rx.input(
                type="number",
                step=0.001,
                value=l.annual_rate,
                on_change=lambda v, i=i: State.update_item("loans", i, "annual_rate", v, "float"),
            ),
            rx.input(
                type="number",
                value=l.months,
                on_change=lambda v, i=i: State.update_item("loans", i, "months", v, "int"),
            ),
            rx.input(
                type="number",
                value=l.start_month,
                on_change=lambda v, i=i: State.update_item("loans", i, "start_month", v, "int"),
            ),
            spacing="2",
        )

    return render_main_container(
        rx.vstack(
            _list_editor("Apports en capital", State.caps, row_cap),
            rx.button("Ajouter un apport", on_click=State.add_capital),
            rx.box(height="1"),
            _list_editor("Subventions", State.subsidies, row_sub),
            rx.button("Ajouter une subvention", on_click=State.add_subsidy),
            rx.box(height="1"),
            _list_editor("Prêts", State.loans, row_loan),
            rx.button("Ajouter un prêt", on_click=State.add_loan),
            spacing="4",
        )
    )


@rx.page(route="/resultats/synthese", on_load=ReflexMainState.on_load, title="Résultats — Synthèse")
def result_synthese():
    return render_main_container(
        rx.vstack(
            rx.heading("Synthèse", size="7"),
            _table(State.synthese_rows, State.synthese_cols),
            spacing="4",
        )
    )


@rx.page(route="/resultats/compte-resultat", on_load=ReflexMainState.on_load, title="Résultats — Compte de résultat")
def result_pnl():
    return render_main_container(
        rx.vstack(
            rx.heading("Compte de résultat (mensuel)", size="7"),
            _table(State.pnl_rows, State.pnl_cols),
            spacing="4",
        )
    )


@rx.page(route="/resultats/cashflow", on_load=ReflexMainState.on_load, title="Résultats — Cashflow")
def result_cashflow():
    return render_main_container(
        rx.vstack(
            rx.heading("Tableau de trésorerie (mensuel)", size="7"),
            _table(State.cashflow_rows, State.cashflow_cols),
            spacing="4",
        )
    )


@rx.page(route="/resultats/plan-financement", on_load=ReflexMainState.on_load, title="Résultats — Plan de financement")
def result_plan():
    return render_main_container(
        rx.vstack(
            rx.heading("Plan de financement (annuel)", size="7"),
            _table(State.plan_rows, State.plan_cols),
            spacing="4",
        )
    )


@rx.page(route="/resultats/bilans", on_load=ReflexMainState.on_load, title="Résultats — Bilans")
def result_bilans():
    return render_main_container(
        rx.vstack(
            rx.heading("Bilan — Actif", size="7"),
            _table(State.bilan_actif_rows, State.bilan_actif_cols),
            rx.heading("Bilan — Passif", size="7"),
            _table(State.bilan_passif_rows, State.bilan_passif_cols),
            spacing="4",
        )
    )


# Add the unauthorized page to the app.
# This page will be displayed if the user is not authenticated
add_unauthorized_page(app)
