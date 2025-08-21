import reflex as rx
from gws_reflex_base import get_theme

app = rx.App(theme=get_theme())

from . import home, config  # noqa
from .input import overview, activities, one_time, subscriptions, staff, external_charges, investments, funding  # noqa
from .results import dashboard, summary, income_statement, cashflow, funding_plan, balance_sheets  # noqa
