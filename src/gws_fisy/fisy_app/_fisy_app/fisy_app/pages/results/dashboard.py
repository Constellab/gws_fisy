
import reflex as rx
from ..layout import layout
from ...state import State

def zoom_controls():
    return rx.hstack(
        rx.vstack(
            rx.text("Zoom — Début (mois)"),
            rx.input(type="number", value=State.zoom_start, on_change=State.zoom_set_start),
            align_items="start",
            spacing="1",
            width="180px",
        ),
        rx.vstack(
            rx.text("Zoom — Fin (mois)"),
            rx.input(type="number", value=State.zoom_end, on_change=State.zoom_set_end),
            align_items="start",
            spacing="1",
            width="180px",
        ),
        rx.spacer(),
        rx.hstack(
            rx.button("3M",  size="2", on_click=State.zoom_3m),
            rx.button("6M",  size="2", on_click=State.zoom_6m),
            rx.button("12M", size="2", on_click=State.zoom_12m),
            rx.button("Tout", size="2", variant="soft", on_click=State.zoom_all),
            spacing="2",
        ),
        width="100%",
        align="center",
    )

def line_chart(data, x_key, series_keys):
    return rx.recharts.responsive_container(
        rx.recharts.line_chart(
            data=data,
            children=[
                rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                rx.recharts.x_axis(data_key=x_key),
                rx.recharts.y_axis(),
                rx.recharts.tooltip(),
                rx.recharts.legend(),
                rx.foreach(series_keys, lambda k: rx.recharts.line(data_key=k, type_="monotone", stroke_width=2)),
                rx.recharts.brush(data_key=x_key, height=22),
            ],
        ),
        width="100%",
        height=360,
    )

@rx.page(route="/resultats/dash", on_load=State.on_load, title="Résultats — Tableaux de bord")
def dashboard():
    return layout(
        rx.vstack(
            rx.heading("Tableaux de bord — Résultats", size="7"),
            rx.text("Visualisez vos résultats via des graphiques interactifs. Utilisez les contrôles de zoom pour vous concentrer sur une période."),
            rx.box(height="2"),
            zoom_controls(),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Synthèse", value="syn"),
                    rx.tabs.trigger("Compte de résultat", value="pnl"),
                    rx.tabs.trigger("Cashflow", value="cf"),
                    value="syn",
                ),
                rx.tabs.content(
                    value="syn",
                    children=rx.vstack(
                        rx.heading("Synthèse — Graphique", size="4"),
                        line_chart(State.synthese_chart_rows, "index", State.synthese_series),
                        spacing="3",
                    ),
                ),
                rx.tabs.content(
                    value="pnl",
                    children=rx.vstack(
                        rx.heading("Compte de résultat — Graphique", size="4"),
                        line_chart(State.pnl_chart_rows, "index", State.pnl_series),
                        spacing="3",
                    ),
                ),
                rx.tabs.content(
                    value="cf",
                    children=rx.vstack(
                        rx.heading("Cashflow — Graphique", size="4"),
                        line_chart(State.cashflow_chart_rows, "index", State.cashflow_series),
                        spacing="3",
                    ),
                ),
                orientation="horizontal",
                style={"width": "100%"},
            ),
            spacing="4",
            align_items="start",
        )
    )
