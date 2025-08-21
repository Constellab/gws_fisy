
import reflex as rx
from gws_reflex_base import render_main_container
from ..state import State

def table(rows, cols) -> rx.Component:
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

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(State.app_title, size="6"),
            rx.text("Navigation", size="2"),
            rx.box(height="6"),
            rx.text("Configuration", size="2"),
            rx.link("Configuration générale", href="/config"),
            rx.box(height="3"),
            rx.text("Saisie", size="2"),
            rx.link("Vue d’ensemble", href="/saisie"),
            rx.link("Activités", href="/saisie/activites"),
            rx.link("Vente ponctuelle", href="/saisie/vente-ponctuelle"),
            rx.link("Abonnement (Ventes récurrentes)", href="/saisie/abonnements"),
            rx.link("Personnel", href="/saisie/personnel"),
            rx.link("Charges externes", href="/saisie/charges"),
            rx.link("Investissements", href="/saisie/investissements"),
            rx.link("Financement", href="/saisie/financement"),
            rx.box(height="3"),
            rx.text("Résultats", size="2"),
            rx.link("Tableaux de bord (charts)", href="/resultats/dash"),
            rx.link("Synthèse (table)", href="/resultats/synthese"),
            rx.link("Compte de résultat (table)", href="/resultats/compte-resultat"),
            rx.link("Cashflow (table)", href="/resultats/cashflow"),
            rx.link("Plan de financement (table)", href="/resultats/plan-financement"),
            rx.link("Bilans (tables)", href="/resultats/bilans"),
            spacing="2",
            align_items="start",
        ),
        min_width="240px",
        width="260px",
        flex_shrink="0",
        position="sticky",
        top="0",
        height="100%",
        padding_right="2",
    )

def layout(main_content: rx.Component) -> rx.Component:
    return render_main_container(
        rx.hstack(
            sidebar(),
            rx.box(main_content, width="100%", overflow_x="auto"),
            align="start",
            spacing="6",
        )
    )

def header_row(labels, widths):
    return rx.table.header(
        rx.table.row(
            *[rx.table.column_header_cell(label, style={"minWidth": w, "width": w}) for label, w in zip(labels, widths)],
            rx.table.column_header_cell("", style={"width": "72px"})
        )
    )

def make_cell(child, width):
    return rx.table.cell(child, style={"minWidth": width, "width": width})

def actions_cell(list_name, index):
    return rx.table.cell(
        rx.hstack(
            rx.button("Delete", size="1", color_scheme="red", on_click=lambda: State.remove_item(list_name, index)),
        )
    )
