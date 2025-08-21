
import reflex as rx
from ..layout import layout, header_row, make_cell, actions_cell
from ...state import State

@rx.page(route="/saisie/personnel", on_load=State.on_load, title="Saisie — Personnel")
def staff():
    LABELS = ["Intitulé", "Salaire brut mensuel", "Taux charges employeur", "Début (mois)", "Fin (mois)"]
    WIDTHS = ["220px", "180px", "180px", "140px", "140px"]

    def row(p, i):
        return rx.table.row(
            make_cell(rx.input(value=p.title, on_change=lambda v, i=i: State.update_item("personnel", i, "title", v, "str"), placeholder="Poste"), WIDTHS[0]),
            make_cell(rx.input(type="number", value=p.monthly_salary_gross, on_change=lambda v, i=i: State.update_item("personnel", i, "monthly_salary_gross", v, "float"), placeholder="€ brut"), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.01, value=p.employer_cost_rate, on_change=lambda v, i=i: State.update_item("personnel", i, "employer_cost_rate", v, "float"), placeholder="0.45"), WIDTHS[2]),
            make_cell(rx.input(type="number", value=p.start_month, on_change=lambda v, i=i: State.update_item("personnel", i, "start_month", v, "int"), placeholder="Début"), WIDTHS[3]),
            make_cell(rx.input(type="number", value=p.end_month, on_change=lambda v, i=i: State.update_item("personnel", i, "end_month", v, "int"), placeholder="Fin ou 999"), WIDTHS[4]),
            actions_cell("personnel", i),
        )

    return layout(
        rx.vstack(
            rx.heading("Personnel", size="5"),
            rx.text("Renseignez vos postes, salaires et périodes d’activité."),
            rx.table.root(header_row(LABELS, WIDTHS), rx.table.body(rx.foreach(State.personnel, row))),
            rx.hstack(rx.button("Ajouter un poste", on_click=lambda: State.add_personnel())),
            spacing="3", align_items="start",
        )
    )
