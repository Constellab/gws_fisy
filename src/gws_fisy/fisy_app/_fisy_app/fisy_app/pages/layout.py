import reflex as rx
from gws_reflex_base import get_theme, render_main_container
from ..state import State

app = rx.App(theme=get_theme())

def sidebar():
    i = State.i18n
    return rx.vstack(
        rx.link(i["nav.config"], href="/config"),
        rx.spacer(),
        rx.text(i["nav.input"], weight="bold"),
        rx.link(i["nav.activities"], href="/saisie/activites"),
        rx.link(i["nav.one_time"], href="/saisie/vente-ponctuelle"),
        rx.link(i["nav.subscriptions"], href="/saisie/abonnements"),
        rx.link(i["nav.staff"], href="/saisie/personnel"),
        rx.link(i["nav.charges"], href="/saisie/charges"),
        rx.link(i["nav.investments"], href="/saisie/investissements"),
        rx.link(i["nav.funding"], href="/saisie/financement"),
        rx.spacer(),
        rx.text(i["nav.results"], weight="bold"),
        rx.link(i["nav.results.dashboard"], href="/resultats/dash"),
        rx.link(i["nav.results.summary"], href="/resultats/synthese"),
        rx.link(i["nav.results.pnl"], href="/resultats/compte-resultat"),
        rx.link(i["nav.results.cashflow"], href="/resultats/cashflow"),
        rx.link(i["nav.results.plan"], href="/resultats/plan-financement"),
        rx.link(i["nav.results.balance"], href="/resultats/bilans"),
        width="240px",
        align_items="start",
        spacing="2",
        padding="12px",
        style={"position": "sticky", "top": "0"}
    )

def layout(content: rx.Component) -> rx.Component:
    return render_main_container(
        rx.hstack(
            sidebar(),
            rx.box(content, flex="1", padding_left="16px"),
            align="start",
            spacing="4",
            width="100%",
        )
    )

def header_row(labels, widths):
    return rx.table.header(
        rx.table.row(*[rx.table.column_header_cell(l, style={"width": w}) for l, w in zip(labels, widths)])
    )

def make_cell(comp: rx.Component, width: str):
    return rx.table.cell(rx.box(comp, style={"width": width}))

def actions_cell(list_name: str, irow):
    return rx.table.cell(
        rx.hstack(
            rx.button(State.i18n["common.delete"], color_scheme="red", variant="soft",
                      on_click=lambda i=irow: State.remove_item(list_name, i)),
            spacing="2"
        )
    )
