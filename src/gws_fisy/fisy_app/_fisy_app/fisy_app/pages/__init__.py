
import reflex as rx
from gws_reflex_base import get_theme

app = rx.App(theme=get_theme())

from . import home, config  # noqa: F401
from .input import overview, activities, orders, staff, external_charges, investments, funding, sales_ranges  # noqa: F401
from .results import dashboard, summary, income_statement, cashflow, funding_plan, balance_sheets  # noqa: F401
