import reflex as rx

from ...state import State
from ..layout import header_row, layout, make_cell, page_with_fixed_title


@rx.page(route="/input/external-charges", on_load=State.on_load, title="Input — External charges")
def external_charges():
    i = State.i18n
    LABELS = [rx.text(i["charges.label"]), rx.text(i["charges.amount"]), rx.text(i["charges.vat"]), rx.text(i["charges.start"]), rx.text(i["charges.end"])]
    WIDTHS = ["28%","22%","14%","16%","16%"]
    def row(c, irow):
        return rx.table.row(
            make_cell(rx.input(value=c.label, on_change=lambda v: State.update_item("charges", irow, "label", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", min=0, value=c.monthly_amount_ht, on_change=lambda v: State.update_item("charges", irow, "monthly_amount_ht", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.1, min=0, max=100, value=c.vat_rate * 100, on_change=lambda v: State.update_item("charges", irow, "vat_rate", v, "percent")), WIDTHS[2]),
            make_cell(rx.input(type="number", min=1, value=c.start_month, on_change=lambda v: State.update_item("charges", irow, "start_month", v, "int")), WIDTHS[3]),
            make_cell(rx.input(type="number", min=1, value=c.end_month, on_change=lambda v: State.update_item("charges", irow, "end_month", v, "int")), WIDTHS[4]),
            rx.table.cell(
                rx.button(
                    State.i18n["common.delete"],
                    color_scheme="red",
                    variant="soft",
                    on_click=lambda: State.remove_item("charges", irow),
                )
            ),
        )
    return layout(
        page_with_fixed_title(
            rx.vstack(
                rx.heading(i["charges.title"], size="7"),
                rx.text(i["charges.desc"]),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.table.root(
                    header_row(LABELS, WIDTHS),
                    rx.table.body(rx.foreach(State.charges, row)),
                    width="100%",
                ),
                rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_charge)),
                spacing="3",
                align_items="start",
                width="100%",
            )
        )
    )
