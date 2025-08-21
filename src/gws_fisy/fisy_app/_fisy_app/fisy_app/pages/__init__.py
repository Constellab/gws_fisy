
import reflex as rx
from gws_reflex_base import get_theme

app = rx.App(theme=get_theme())

from . import home, config  # noqa: F401
from .input import overview, activities, one_time, subscriptions, staff, external_charges, investments, funding  # noqa: F401
from .results import dashboard, summary, income_statement, cashflow, funding_plan, balance_sheets  # noqa: F401
