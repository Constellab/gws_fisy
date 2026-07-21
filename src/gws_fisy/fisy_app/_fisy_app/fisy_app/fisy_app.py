import reflex as rx
from gws_reflex_main import register_gws_reflex_app

from .projects.projects_component import projects_page

app = register_gws_reflex_app()


@rx.page(route="/projects")
def projects() -> rx.Component:
    """Projects list page."""
    return projects_page()


@rx.page(route="/")
def index() -> rx.Component:
    """Entry point — redirects to the projects list."""
    return rx.box(on_mount=rx.redirect("/projects"))
