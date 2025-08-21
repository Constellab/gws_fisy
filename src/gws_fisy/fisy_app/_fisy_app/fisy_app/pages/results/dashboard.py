import reflex as rx
from ..layout import layout
from ...state import State


def zoom_controls():
    i = State.i18n
    return rx.hstack(
        rx.vstack(
            rx.text(i["zoom.start"]),
            rx.input(type="number", value=State.zoom_start, on_change=State.zoom_set_start),
            align_items="start",
            spacing="1",
            width="220px",
        ),
        rx.vstack(
            rx.text(i["zoom.end"]),
            rx.input(type="number", value=State.zoom_end, on_change=State.zoom_set_end),
            align_items="start",
            spacing="1",
            width="220px",
        ),
        rx.spacer(),
        rx.hstack(
            rx.button("3M", size="2", on_click=State.zoom_3m),
            rx.button("6M", size="2", on_click=State.zoom_6m),
            rx.button("12M", size="2", on_click=State.zoom_12m),
            rx.button("Tout", size="2", variant="soft", on_click=State.zoom_all),
            spacing="2",
        ),
        width="100%",
        align="center",
    )


def line_chart(data, x_key, series_defs):
    # series_defs = [{ "key": str, "color": str, "unit": str }, ...]
    return rx.recharts.responsive_container(
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.x_axis(data_key=x_key),
            # 👉 Affiche l’unité sur l’axe Y (utilisée aussi par la Tooltip/Legend)
            rx.recharts.y_axis(unit=State.unit_suffix),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.foreach(
                series_defs,
                lambda s: rx.recharts.line(
                    data_key=s["key"],
                    type_="monotone",
                    stroke_width=2,
                    stroke=s["color"],
                    unit=s["unit"],
                ),
            ),
            rx.recharts.brush(data_key=x_key, height=22),
            data=data,
        ),
        width="100%",
        height=360,
    )


@rx.page(route="/resultats/dash", on_load=State.on_load, title="Résultats — Tableaux de bord")
def dashboard():
    i = State.i18n
    return layout(
        rx.vstack(
            # 👉 Titre principal avec l’unité
            rx.heading(i["results.dashboard"], " (", State.unit_suffix, ")", size="7"),
            rx.text(i["results.dashboard.desc"]),
            rx.box(height="2"),
            zoom_controls(),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(i["results.syn"], value="syn"),
                    rx.tabs.trigger(i["results.pnl"], value="pnl"),
                    rx.tabs.trigger(i["results.cf"], value="cf"),
                ),

                # --- Synthèse ---
                rx.tabs.content(
                    rx.vstack(
                        rx.heading(i["results.syn"], " (", State.unit_suffix, ")", size="4"),
                        line_chart(State.synthese_chart_rows, "index", State.synthese_series_defs),
                        spacing="3",
                    ),
                    value="syn",
                ),

                # --- P&L ---
                rx.tabs.content(
                    rx.vstack(
                        rx.heading(i["results.pnl"], " (", State.unit_suffix, ")", size="4"),
                        line_chart(State.pnl_chart_rows, "index", State.pnl_series_defs),
                        spacing="3",
                    ),
                    value="pnl",
                ),

                # --- Cashflow ---
                rx.tabs.content(
                    rx.vstack(
                        rx.heading(i["results.cf"], " (", State.unit_suffix, ")", size="4"),
                        line_chart(State.cashflow_chart_rows, "index", State.cashflow_series_defs),
                        spacing="3",
                    ),
                    value="cf",
                ),

                default_value="syn",
                orientation="horizontal",
                style={"width": "100%"},
            ),
            spacing="4",
            align_items="start",
        )
    )
