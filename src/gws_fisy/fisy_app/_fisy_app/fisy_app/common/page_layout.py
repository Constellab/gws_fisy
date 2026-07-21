"""Shared page layout with a collapsible left sidebar.

Modeled on gws_care's care_app/common/page_layout.py, scoped down to what
gws_fisy actually has: a single top-level nav item ("Projects") and no
roles/notifications/i18n state to gate content with.
"""

import reflex as rx
from gws_reflex_main import menu_item_component

_SIDEBAR_FULL = "300px"
_SIDEBAR_FOLDED = "60px"


class SidebarFoldState(rx.State):
    is_folded: bool = False

    def toggle(self) -> None:
        self.is_folded = not self.is_folded

    def fold(self) -> None:
        self.is_folded = True

    def unfold(self) -> None:
        self.is_folded = False

    @rx.var
    def current_path(self) -> str:
        return self.router.url.path


def _folded_item(icon_name: str, label: str, href: str) -> rx.Component:
    """Icon + small permanent label, used when the sidebar is folded."""
    is_active = SidebarFoldState.current_path == href
    return rx.tooltip(
        rx.link(
            rx.vstack(
                rx.icon(
                    icon_name,
                    size=18,
                    color=rx.cond(is_active, "var(--accent-9)", "var(--gray-11)"),
                ),
                rx.text(
                    label,
                    color=rx.cond(is_active, "var(--accent-9)", "var(--gray-9)"),
                    text_align="center",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                    max_width="100%",
                    style={"font-size": "0.6rem", "line-height": "1.1"},
                ),
                spacing="0",
                align="center",
                width="100%",
                padding_y="0.4rem",
                padding_x="0.15rem",
                border_radius="var(--radius-2)",
                background=rx.cond(is_active, "var(--accent-3)", "transparent"),
                _hover={"background": rx.cond(is_active, "var(--accent-4)", "var(--gray-3)")},
            ),
            href=href,
            width="100%",
            text_decoration="none",
        ),
        content=label,
        side="right",
    )


def _nav_item(icon_name: str, label: str, href: str) -> rx.Component:
    """Full or folded nav item depending on sidebar state."""
    full = menu_item_component(icon_name, label, href)
    return rx.cond(SidebarFoldState.is_folded, _folded_item(icon_name, label, href), full)


def _sidebar_content() -> rx.Component:
    return rx.box(
        # ── Header: branding + fold/unfold toggle ─────────────────────────────
        rx.cond(
            SidebarFoldState.is_folded,
            rx.vstack(
                rx.center(
                    rx.icon("banknote", size=24, color="var(--accent-9)"),
                    width="100%",
                    padding_top="0.9em",
                ),
                rx.center(
                    rx.icon_button(
                        rx.icon("chevron-right", size=18),
                        on_click=SidebarFoldState.toggle,
                        variant="solid",
                        size="2",
                        color_scheme="blue",
                        cursor="pointer",
                    ),
                    width="100%",
                    padding_bottom="0.6em",
                ),
                spacing="2",
                width="100%",
            ),
            rx.hstack(
                rx.icon("banknote", size=28, color="var(--accent-9)"),
                rx.vstack(
                    rx.heading("Fisy", size="4", line_height="1em"),
                    rx.text("By Constellab", size="1", color="var(--gray-9)", line_height="1em"),
                    spacing="1",
                    flex="1",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=SidebarFoldState.toggle,
                    variant="ghost",
                    size="2",
                    color_scheme="gray",
                    cursor="pointer",
                ),
                spacing="2",
                align="center",
                padding="0.85em 0.75em 0.85em 1em",
                width="100%",
            ),
        ),
        # ── Nav ────────────────────────────────────────────────────────────────
        rx.vstack(
            _nav_item("layout-grid", "Projects", "/projects"),
            width="100%",
            spacing="1",
            align_items="start",
            padding_x=rx.cond(SidebarFoldState.is_folded, "0.35rem", "1rem"),
            overflow_y="auto",
            flex="1",
            min_height="0",
        ),
        position="relative",
        width="100%",
        height="100%",
        display="flex",
        flex_direction="column",
        align_items="start",
        overflow="hidden",
    )


def page_layout(*children: rx.Component, **kwargs) -> rx.Component:
    """Wrap content in the standard collapsible sidebar layout."""
    sidebar_width = rx.cond(SidebarFoldState.is_folded, _SIDEBAR_FOLDED, _SIDEBAR_FULL)

    vstack_props = {
        "width": "100%",
        "spacing": "4",
        "padding": "1.5rem",
        "min_width": "0",
        "overflow_x": "hidden",
        "flex_shrink": "0",
    }
    vstack_props.update(kwargs)

    return rx.box(
        rx.box(
            _sidebar_content(),
            position="fixed",
            left="0",
            top="0",
            height="100vh",
            width=sidebar_width,
            background="white",
            border_right="1px solid var(--gray-4)",
            z_index="10",
            overflow="hidden",
            style={"transition": "width 0.22s ease"},
        ),
        rx.box(
            rx.vstack(*children, **vstack_props),
            margin_left=sidebar_width,
            height="100vh",
            overflow_y="auto",
            style={"transition": "margin-left 0.22s ease"},
        ),
        width="100%",
        position="relative",
    )
