"""Projects page — placeholder.

Full project list/create functionality belongs to FISY-001 (not yet
implemented). This page exists only so the sidebar's "Projects" link has a
route to point to and highlight.
"""

import reflex as rx
from gws_reflex_main import main_component

from ..common.page_layout import page_layout


def projects_page() -> rx.Component:
    """Projects list page (placeholder)."""
    return main_component(
        page_layout(
            rx.heading("Projects", size="6"),
        )
    )
