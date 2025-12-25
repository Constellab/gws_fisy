"""
Financial scenario model.

Stores all financial planning data for a user including configuration,
activities, personnel, charges, investments, loans, and funding.
"""

from gws_core import JSONField
from peewee import CharField, FloatField, IntegerField

from ..core.model_with_user import ModelWithUser
from .scenario_dto import ScenarioDTO


class Scenario(ModelWithUser):
    """
    Financial scenario model.

    A scenario contains all the financial planning data including:
    - Basic configuration (months, tax rates, dates)
    - Activities and pricing
    - One-time and subscription sales ranges
    - Personnel costs
    - External charges
    - Investments and loans
    - Capital injections and subsidies
    """

    # Basic info
    title = CharField(max_length=255, null=False)
    description = CharField(max_length=1000, null=True)

    # Base configuration
    months = IntegerField(default=60, null=False)
    tva_default = FloatField(default=0.2, null=False)
    start_year = IntegerField(default=2025, null=False)
    start_month = IntegerField(default=1, null=False)
    dso_days = IntegerField(default=30, null=False)
    dpo_days = IntegerField(default=30, null=False)
    dio_days = IntegerField(default=0, null=False)
    initial_cash = FloatField(default=0.0, null=False)

    # UI preferences
    language_code = CharField(max_length=10, default="fr", null=False)
    currency_code = CharField(max_length=10, default="EUR", null=False)
    scale_mode = CharField(max_length=20, default="units", null=False)

    # Data stored as JSON
    activities = JSONField(default=list, null=False)
    one_time_ranges = JSONField(default=list, null=False)
    subscription_ranges = JSONField(default=list, null=False)
    personnel = JSONField(default=list, null=False)
    charges = JSONField(default=list, null=False)
    investments = JSONField(default=list, null=False)
    loans = JSONField(default=list, null=False)
    capital_injections = JSONField(default=list, null=False)
    subsidies = JSONField(default=list, null=False)

    def to_dto(self) -> ScenarioDTO:
        """Convert model to DTO."""
        return ScenarioDTO(
            id=str(self.id),
            created_at=self.created_at,  # type: ignore
            last_modified_at=self.last_modified_at,  # type: ignore
            created_by=self.created_by.to_dto(),
            last_modified_by=self.last_modified_by.to_dto(),
            title=str(self.title),
            description=str(self.description) if self.description else None,
            months=int(self.months),  # type: ignore
            tva_default=float(self.tva_default),  # type: ignore
            start_year=int(self.start_year),  # type: ignore
            start_month=int(self.start_month),  # type: ignore
            dso_days=int(self.dso_days),  # type: ignore
            dpo_days=int(self.dpo_days),  # type: ignore
            dio_days=int(self.dio_days),  # type: ignore
            initial_cash=float(self.initial_cash),  # type: ignore
            language_code=str(self.language_code),
            currency_code=str(self.currency_code),
            scale_mode=str(self.scale_mode),
            activities=list(self.activities),
            one_time_ranges=list(self.one_time_ranges),
            subscription_ranges=list(self.subscription_ranges),
            personnel=list(self.personnel),
            charges=list(self.charges),
            investments=list(self.investments),
            loans=list(self.loans),
            capital_injections=list(self.capital_injections),
            subsidies=list(self.subsidies),
        )

    class Meta:
        table_name = "gws_fisy_scenarios"
        is_table = True
