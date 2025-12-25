import reflex as rx

from ...state import State
from ..layout import header_row, layout, make_cell, page_with_fixed_title


@rx.page(route="/input/activities", on_load=State.on_load, title="Input — Activities")
def activities():
    i = State.i18n
    LABELS = [rx.text(i["activities.name"]), rx.text(i["activities.unit_price_ht"]), rx.text(i["activities.vat_rate"]), rx.text(i["activities.var_cost_unit"]), rx.text(i["activities.var_cost_rate"])]
    WIDTHS = ["25%","15%","12%","25%","18%"]
    def row(a, irow):
        return rx.table.row(
            make_cell(rx.input(value=a.name, on_change=lambda v: State.update_item("activities", irow, "name", v, "str")), WIDTHS[0]),
            make_cell(rx.input(type="number", min=0, value=a.unit_price_ht, on_change=lambda v: State.update_item("activities", irow, "unit_price_ht", v, "float")), WIDTHS[1]),
            make_cell(rx.input(type="number", step=0.1, min=0, max=100, value=a.vat_rate * 100, on_change=lambda v: State.update_item("activities", irow, "vat_rate", v, "percent")), WIDTHS[2]),
            make_cell(rx.input(type="number", min=0, value=a.variable_cost_per_unit_ht, on_change=lambda v: State.update_item("activities", irow, "variable_cost_per_unit_ht", v, "float")), WIDTHS[3]),
            make_cell(rx.input(type="number", step=0.1, min=0, max=100, value=a.variable_cost_rate_on_price * 100, on_change=lambda v: State.update_item("activities", irow, "variable_cost_rate_on_price", v, "percent")), WIDTHS[4]),
            rx.table.cell(
                rx.button(
                    State.i18n["common.delete"],
                    color_scheme="red",
                    variant="soft",
                    on_click=lambda: State.remove_item("activities", irow),
                )
            ),
        )
    return layout(
        page_with_fixed_title(
            rx.vstack(
                rx.heading(i["activities.title"], size="7"),
                rx.text(i["activities.desc"]),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.table.root(
                    header_row(LABELS, WIDTHS),
                    rx.table.body(rx.foreach(State.activities, row)),
                    width="100%",
                ),
                rx.hstack(rx.button(State.i18n["common.add"], on_click=State.add_activity)),
                spacing="3",
                align_items="start",
                width="100%",
            )
        )
    )
