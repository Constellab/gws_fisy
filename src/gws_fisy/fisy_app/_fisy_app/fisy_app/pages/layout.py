import reflex as rx
from gws_reflex_base import render_main_container
from ..state import State

def table(rows, cols) -> rx.Component:
    return rx.table.root(
        rx.table.header(rx.table.row(rx.foreach(cols, lambda c: rx.table.column_header_cell(c)))),
        rx.table.body(rx.foreach(rows, lambda r: rx.table.row(rx.foreach(cols, lambda c: rx.table.cell(rx.text(r[c])))))),
    )

def sidebar() -> rx.Component:
    t = State.i18n
    return rx.box(
        rx.vstack(
            rx.heading(State.app_title, size="6"),
            rx.text(t["nav_config"], size="2"),
            rx.link(t["nav_config_general"], href="/config"),
            rx.box(height="3"),
            rx.text(t["nav_input"], size="2"),
            rx.link(t["nav_input_overview"], href="/saisie"),
            rx.link(t["nav_activities"], href="/saisie/activites"),
            rx.link(t["nav_one_time"], href="/saisie/vente-ponctuelle"),
            rx.link(t["nav_subscriptions"], href="/saisie/abonnements"),
            rx.link(t["nav_staff"], href="/saisie/personnel"),
            rx.link(t["nav_external_charges"], href="/saisie/charges"),
            rx.link(t["nav_investments"], href="/saisie/investissements"),
            rx.link(t["nav_funding"], href="/saisie/financement"),
            rx.box(height="3"),
            rx.text(t["nav_results"], size="2"),
            rx.link(t["nav_results_dashboard"], href="/resultats/dash"),
            rx.link(t["nav_results_summary"], href="/resultats/synthese"),
            rx.link(t["nav_results_pnl"], href="/resultats/compte-resultat"),
            rx.link(t["nav_results_cashflow"], href="/resultats/cashflow"),
            rx.link(t["nav_results_plan"], href="/resultats/plan-financement"),
            rx.link(t["nav_results_balance"], href="/resultats/bilans"),
            spacing="2", align_items="start",
        ),
        min_width="240px", width="260px", flex_shrink="0",
        position="sticky", top="0", height="100%", padding_right="2",
    )

def layout(main_content: rx.Component) -> rx.Component:
    return render_main_container(
        rx.hstack(sidebar(), rx.box(main_content, width="100%", overflow_x="auto"), align="start", spacing="6")
    )

def header_row(labels, widths):
    return rx.table.header(
        rx.table.row(
            *[rx.table.column_header_cell(label, style={"minWidth": w, "width": w}) for label, w in zip(labels, widths)],
            rx.table.column_header_cell("", style={"width": "72px"}),
        )
    )

def make_cell(child, width):
    return rx.table.cell(child, style={"minWidth": width, "width": width})

def actions_cell(list_name, index):
    return rx.table.cell(rx.hstack(rx.button(State.i18n["delete"], size="1", color_scheme="red", on_click=lambda: State.remove_item(list_name, index))))
