import reflex as rx
from gws_reflex_main import main_component, register_gws_reflex_app

from .projects.projects_component import projects_page

app = register_gws_reflex_app()


@rx.page(route="/projects")
def projects() -> rx.Component:
    """Projects list page."""
    return projects_page()


@rx.page(route="/")
def index() -> rx.Component:
    """Entry point — redirects to the projects list once the app state is initialized."""
    # Wrap in main_component so the main state runs its auth init (the gws_code -> JWT
    # exchange) before we navigate. A bare on_mount redirect fires before init settles,
    # so the destination page loads with no authenticated user ("User not authenticated").
    return main_component(
        rx.box(on_mount=rx.redirect("/projects")),
    )
