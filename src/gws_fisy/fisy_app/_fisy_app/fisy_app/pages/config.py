import reflex as rx

from ..state import State
from .layout import layout, page_with_fixed_title


@rx.page(route="/config", on_load=State.on_load, title="Configuration")
def config():
    i = State.i18n
    left_col = rx.vstack(
        rx.vstack(
            rx.text(i["config.language"]),
            rx.select(items=State.language_options, value=State.language_code, on_change=State.set_language_code),
            spacing="1", align_items="start",
        ),
        rx.vstack(
            rx.text(i["config.currency"]),
            rx.select(items=["EUR","USD","GBP","CHF","CAD","AUD","JPY","CNY","XOF"], value=State.currency_code, on_change=State.set_currency_code),
            rx.hstack(rx.text(i["config.symbol"]), rx.text(State.currency_symbol)),
            spacing="1", align_items="start",
        ),
        rx.vstack(
            rx.text(i["config.scale"]),
            rx.select(
                items=State.scale_mode_options,
                value=State.scale_mode_label,
                on_change=State.set_scale_mode
            ),
            rx.hstack(rx.text(i["config.unit_shown"]), rx.text(State.unit_suffix)),
            spacing="1", align_items="start",
        ),
        rx.vstack(
            rx.text(i["config.months"]),
            rx.input(type="number", min=1, value=State.months, on_change=lambda v: State.set_int("months", v)),
            spacing="1", align_items="start",
        ),
        rx.vstack(
            rx.text(i["config.vat_default"]),
            rx.input(type="number", step=0.1, min=0, max=100, value=State.tva_default * 100, on_change=lambda v: State.set_percent("tva_default", v)),
            spacing="1", align_items="start",
        ),
        spacing="3", align_items="start", style={"flex":"1 1 0%","minWidth":"320px"},
    )
    right_col = rx.vstack(
        rx.vstack(
            rx.text(i["config.cit"]),
            rx.input(type="number", step=0.1, min=0, max=100, value=State.corporate_tax_rate * 100, on_change=lambda v: State.set_percent("corporate_tax_rate", v)),
            spacing="1", align_items="start",
        ),
        rx.vstack(rx.text(i["config.dso"]), rx.input(type="number", min=0, value=State.dso_days, on_change=lambda v: State.set_int("dso_days", v)), spacing="1", align_items="start"),
        rx.vstack(rx.text(i["config.dpo"]), rx.input(type="number", min=0, value=State.dpo_days, on_change=lambda v: State.set_int("dpo_days", v)), spacing="1", align_items="start"),
        rx.vstack(rx.text(i["config.dio"]), rx.input(type="number", min=0, value=State.dio_days, on_change=lambda v: State.set_int("dio_days", v)), spacing="1", align_items="start"),
        rx.vstack(rx.text(i["config.initial_cash"]), rx.input(type="number", min=0, value=State.initial_cash, on_change=lambda v: State.set_float("initial_cash", v)), spacing="1", align_items="start"),
        spacing="3", align_items="start", style={"flex":"1 1 0%","minWidth":"320px"},
    )
    return layout(
        page_with_fixed_title(
            rx.vstack(
                rx.heading(i["config.title"], size="7"),
                rx.text(i["config.desc"]),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(left_col, right_col, spacing="6", align="start", width="100%"),
                spacing="4",
                align_items="start",
                width="100%",
            )
        )
    )
