"""
Data Transfer Objects for Scenario.
"""

from datetime import datetime
from typing import Any

from gws_core import BaseModelDTO, UserDTO


class ScenarioDTO(BaseModelDTO):
    """DTO for Scenario model."""

    id: str
    created_at: datetime
    last_modified_at: datetime
    created_by: UserDTO
    last_modified_by: UserDTO

    title: str
    description: str | None = None

    # Base configuration
    months: int = 60
    tva_default: float = 0.2
    start_year: int = 2025
    start_month: int = 1
    dso_days: int = 30
    dpo_days: int = 30
    dio_days: int = 0
    initial_cash: float = 0.0

    # UI preferences
    language_code: str = "fr"
    currency_code: str = "EUR"
    scale_mode: str = "units"

    # Data as lists of dicts
    activities: list[dict[str, Any]] = []
    one_time_ranges: list[dict[str, Any]] = []
    subscription_ranges: list[dict[str, Any]] = []
    personnel: list[dict[str, Any]] = []
    charges: list[dict[str, Any]] = []
    investments: list[dict[str, Any]] = []
    loans: list[dict[str, Any]] = []
    capital_injections: list[dict[str, Any]] = []
    subsidies: list[dict[str, Any]] = []
