
import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/financement", on_load=State.on_load, title="Saisie — Financement")
def funding():
    CAP_LABELS = ["Libellé", "Montant", "Mois"]
    CAP_WIDTHS = ["260px", "160px", "160px"]
    SUB_LABELS = ["Libellé", "Montant", "Mois"]
    SUB_WIDTHS = ["260px", "160px", "160px"]
    LOAN_LABELS = ["Libellé", "Capital", "Taux annuel", "Durée (mois)", "Départ (mois)"]
    LOAN_WIDTHS = ["220px", "160px", "160px", "140px", "160px"]

    def row_cap(c, i):
        return rx.table.row(
            make_cell(rx.input(value=c.label, on_change=lambda v, i=i: State.update_item("caps", i, "label", v, "str"), placeholder="Libellé apport"), CAP_WIDTHS[0]),
            make_cell(rx.input(type="number", value=c.amount, on_change=lambda v, i=i: State.update_item("caps", i, "amount", v, "float"), placeholder="Montant"), CAP_WIDTHS[1]),
            make_cell(rx.input(type="number", value=c.month, on_change=lambda v, i=i: State.update_item("caps", i, "month", v, "int"), placeholder="Mois"), CAP_WIDTHS[2]),
            actions_cell("caps", i),
        )

    def row_sub(s, i):
        return rx.table.row(
            make_cell(rx.input(value=s.label, on_change=lambda v, i=i: State.update_item("subsidies", i, "label", v, "str"), placeholder="Libellé subvention"), SUB_WIDTHS[0]),
            make_cell(rx.input(type="number", value=s.amount, on_change=lambda v, i=i: State.update_item("subsidies", i, "amount", v, "float"), placeholder="Montant"), SUB_WIDTHS[1]),
            make_cell(rx.input(type="number", value=s.month, on_change=lambda v, i=i: State.update_item("subsidies", i, "month", v, "int"), placeholder="Mois"), SUB_WIDTHS[2]),
            actions_cell("subsidies", i),
        )

    def row_loan(l, i):
        return rx.table.row(
            make_cell(rx.input(value=l.label, on_change=lambda v, i=i: State.update_item("loans", i, "label", v, "str"), placeholder="Libellé prêt"), LOAN_WIDTHS[0]),
            make_cell(rx.input(type="number", value=l.principal, on_change=lambda v, i=i: State.update_item("loans", i, "principal", v, "float"), placeholder="Capital"), LOAN_WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.001, value=l.annual_rate, on_change=lambda v, i=i: State.update_item("loans", i, "annual_rate", v, "float"), placeholder="0.04"), LOAN_WIDTHS[2]),
            make_cell(rx.input(type="number", value=l.months, on_change=lambda v, i=i: State.update_item("loans", i, "months", v, "int"), placeholder="Mois"), LOAN_WIDTHS[3]),
            make_cell(rx.input(type="number", value=l.start_month, on_change=lambda v, i=i: State.update_item("loans", i, "start_month", v, "int"), placeholder="Départ"), LOAN_WIDTHS[4]),
            actions_cell("loans", i),
        )

    return layout(
        rx.vstack(
            rx.heading("Financement — Mode d’emploi", size="5"),
            rx.text("Ajoutez/supprimez des lignes et éditez directement dans les cellules. Pour les prêts, indiquez capital, taux annuel, durée et mois de départ."),
            rx.box(height="2"),
            rx.heading("Apports en capital", size="4"),
            rx.table.root(header_row(CAP_LABELS, CAP_WIDTHS), rx.table.body(rx.foreach(State.caps, row_cap))),
            rx.hstack(rx.button("Ajouter un apport", on_click=State.add_capital)),
            rx.box(height="3"),
            rx.heading("Subventions", size="4"),
            rx.table.root(header_row(SUB_LABELS, SUB_WIDTHS), rx.table.body(rx.foreach(State.subsidies, row_sub))),
            rx.hstack(rx.button("Ajouter une subvention", on_click=State.add_subsidy)),
            rx.box(height="3"),
            rx.heading("Prêts", size="4"),
            rx.table.root(header_row(LOAN_LABELS, LOAN_WIDTHS), rx.table.body(rx.foreach(State.loans, row_loan))),
            rx.hstack(rx.button("Ajouter un prêt", on_click=State.add_loan)),
            spacing="3", align_items="start",
        )
    )
