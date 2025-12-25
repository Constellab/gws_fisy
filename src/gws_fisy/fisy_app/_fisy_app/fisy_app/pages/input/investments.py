import reflex as rx

from ...state import State
from ..layout import header_row, layout, make_cell, page_with_fixed_title


@rx.page(route="/input/investments", on_load=State.on_load, title="Input — Investments")
def investments():
    i = State.i18n
    LABELS = [rx.text(i["inv.label"]), rx.text(i["inv.amount"]), rx.text(i["inv.vat"]), rx.text(i["inv.month"]), rx.text(i["inv.amort"])]
    WIDTHS = ["28%","22%","14%","18%","18%"]
    def row(inv, irow):
        return rx.table.row(
            make_cell(rx.input(value=inv.label, on_change=lambda v: State.update_item("investments", irow, "label", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", min=0, value=inv.amount_ht, on_change=lambda v: State.update_item("investments", irow, "amount_ht", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.1, min=0, max=100, value=inv.vat_rate * 100, on_change=lambda v: State.update_item("investments", irow, "vat_rate", v, "percent")), WIDTHS[2]),
            make_cell(rx.input(type="number", min=1, value=inv.purchase_month, on_change=lambda v: State.update_item("investments", irow, "purchase_month", v, "int")), WIDTHS[3]),
            make_cell(rx.input(type="number", min=1, value=inv.amort_years, on_change=lambda v: State.update_item("investments", irow, "amort_years", v, "int")), WIDTHS[4]),
            rx.table.cell(
                rx.button(
                    State.i18n["common.delete"],
                    color_scheme="red",
                    variant="soft",
                    on_click=lambda: State.remove_item("investments", irow),
                )
            ),
        )
    return layout(
        page_with_fixed_title(
            rx.vstack(
                rx.heading(i["inv.title"], size="7"),
                rx.text(i["inv.desc"]),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.table.root(
                    header_row(LABELS, WIDTHS),
                    rx.table.body(rx.foreach(State.investments, row)),
                    width="100%",
                ),
                rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_investment)),
                spacing="3",
                align_items="start",
                width="100%",
            )
        )
    )
