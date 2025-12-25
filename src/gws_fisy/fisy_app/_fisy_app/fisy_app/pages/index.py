import reflex as rx

from ..state import State
from .layout import layout


def feature_card(icon: str, title: rx.Var, description: rx.Var, color: str = "blue"):
    """Create a feature card with icon, title and description.

    :param icon: The Lucide icon name
    :type icon: str
    :param title: The feature title
    :type title: rx.Var
    :param description: The feature description
    :type description: rx.Var
    :param color: The accent color for the icon
    :type color: str
    :return: A feature card component
    :rtype: rx.Component
    """
    return rx.box(
        rx.vstack(
            rx.icon(icon, size=40, color=f"var(--{color}-9)", stroke_width=1.5),
            rx.heading(title, size="5", weight="bold"),
            rx.text(
                description,
                size="3",
                color="var(--gray-11)",
                line_height="1.7",
            ),
            align_items="start",
            spacing="3",
        ),
        padding="2rem",
        border_radius="12px",
        border="1px solid var(--gray-6)",
        background="var(--gray-2)",
        _hover={
            "border_color": f"var(--{color}-7)",
            "background": "var(--gray-1)",
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.05)",
        },
        transition="all 0.2s ease",
    )


def benefit_card(icon: str, title: rx.Var, description: rx.Var, color: str = "accent"):
    """Create a benefit card for the 'Why Choose Fisy' section.

    :param icon: The Lucide icon name
    :type icon: str
    :param title: The benefit title
    :type title: rx.Var
    :param description: The benefit description
    :type description: rx.Var
    :param color: The accent color
    :type color: str
    :return: A benefit card component
    :rtype: rx.Component
    """
    return rx.hstack(
        rx.box(
            rx.icon(icon, size=24, color=f"var(--{color}-11)"),
            padding="0.75rem",
            border_radius="8px",
            background=f"var(--{color}-3)",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.heading(title, size="4", weight="bold"),
            rx.text(description, size="2", color="var(--gray-11)", line_height="1.6"),
            align_items="start",
            spacing="1",
        ),
        align="start",
        spacing="4",
        padding="1.5rem",
        border_radius="10px",
        background="var(--gray-1)",
        border="1px solid var(--gray-5)",
    )


@rx.page(route="/", on_load=State.on_load, title="Constellab Fisy")
def index():
    i = State.i18n
    return layout(
        rx.vstack(
            # Hero Section
            rx.vstack(
                rx.hstack(
                    rx.icon("banknote", size=48, color="var(--accent-9)", stroke_width=1.5),
                    rx.heading(State.app_title, size="9", weight="bold"),
                    spacing="4",
                    align="center",
                ),
                rx.heading(
                    i["home.title"],
                    size="7",
                    weight="medium",
                    text_align="center",
                    max_width="800px",
                ),
                rx.text(
                    i["home.subtitle"],
                    size="4",
                    color="var(--gray-11)",
                    text_align="center",
                    max_width="700px",
                    line_height="1.7",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            rx.icon("line-chart", size=18),
                            i["home.get_started"],
                            size="3",
                            variant="solid",
                        ),
                        href="/resultats/synthese",
                    ),
                    rx.link(
                        rx.button(
                            rx.icon("settings", size=18),
                            i["home.view_config"],
                            size="3",
                            variant="outline",
                        ),
                        href="/config",
                    ),
                    spacing="3",
                ),
                spacing="5",
                align_items="center",
                padding_y="3rem",
            ),

            # Features Section
            rx.vstack(
                rx.heading(
                    i["home.features_title"],
                    size="7",
                    weight="bold",
                    text_align="center",
                ),
                rx.grid(
                    feature_card(
                        "lightbulb",
                        i["home.feature1.title"],
                        i["home.feature1.desc"],
                        "blue",
                    ),
                    feature_card(
                        "wallet",
                        i["home.feature2.title"],
                        i["home.feature2.desc"],
                        "green",
                    ),
                    feature_card(
                        "refresh-cw",
                        i["home.feature3.title"],
                        i["home.feature3.desc"],
                        "purple",
                    ),
                    feature_card(
                        "file-text",
                        i["home.feature4.title"],
                        i["home.feature4.desc"],
                        "orange",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                spacing="5",
                padding_y="3rem",
                width="100%",
            ),

            # Why Choose Section
            rx.vstack(
                rx.heading(
                    i["home.why.title"],
                    size="7",
                    weight="bold",
                    text_align="center",
                ),
                rx.grid(
                    benefit_card(
                        "zap",
                        i["home.why1.title"],
                        i["home.why1.desc"],
                        "amber",
                    ),
                    benefit_card(
                        "activity",
                        i["home.why2.title"],
                        i["home.why2.desc"],
                        "blue",
                    ),
                    benefit_card(
                        "shield-check",
                        i["home.why3.title"],
                        i["home.why3.desc"],
                        "green",
                    ),
                    benefit_card(
                        "layers",
                        i["home.why4.title"],
                        i["home.why4.desc"],
                        "purple",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                spacing="5",
                padding_y="3rem",
                width="100%",
            ),

            # Footer note
            rx.divider(),
            rx.vstack(
                rx.text(
                    "💡 ",
                    i["home.desc"],
                    size="2",
                    color="var(--gray-11)",
                    text_align="center",
                ),
                rx.text(
                    "Based on Fisy by Rémi BERTHIER - ",
                    rx.link("fisy.fr", href="https://fisy.fr", target="_blank", color="var(--accent-11)"),
                    size="1",
                    color="var(--gray-10)",
                    text_align="center",
                ),
                spacing="2",
                padding_y="2rem",
            ),

            spacing="6",
            align_items="center",
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding="2rem",
        )
    )
