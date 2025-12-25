import dataclasses
import html

import pandas as pd
import reflex as rx
from gws_fisy.scenario.scenario import Scenario
from gws_fisy.scenario.scenario_service import ScenarioService
from gws_reflex_main import ReflexMainState

from .calc.engine import compute_all
from .calc.models import (
    Activity,
    CapitalInjection,
    ChargeExterne,
    Config,
    Investment,
    Loan,
    OneTimeRange,
    Order,
    PersonnelLine,
    SubscriptionRange,
    Subsidy,
)
from .calc.sale_ranges import (
    expand_one_time_ranges_to_orders,
    expand_subscription_ranges_to_orders,
)
from .i18n import LANGS


class State(ReflexMainState):
    # ----------- Current scenario ID -----------
    current_scenario_id: str = ""

    # ----------- Base config -----------
    months: int = 60                  # 5 years horizon
    tva_default: float = 0.2
    start_year: int = 2025
    start_month: int = 1
    dso_days: int = 30
    dpo_days: int = 30
    dio_days: int = 0
    initial_cash: float = 0.0

    # Cached params from config
    _app_title: str = "Constellab Fisy"
    _corporate_tax_rate: float = 0.25
    _months_override: int = 0

    @rx.event
    async def on_load(self):
        """Load configuration parameters and scenario on page load."""
        params = await self.get_params()
        self._app_title = params.get("app_title", self.i18n.get("app.title", "Constellab Fisy"))
        self._corporate_tax_rate = float(params.get("corporate_tax_rate", 0.25))
        self._months_override = int(params.get("months", 0))

        # Load or create default scenario
        scenario_id = params.get("scenario_id")
        if scenario_id:
            await self._load_scenario(scenario_id)
        else:
            await self._create_default_scenario()

    async def _create_default_scenario(self):
        """Create a default scenario with sample data for the current user."""
        try:
            # Create scenario with default data
            scenario = ScenarioService.create_scenario(
                title="Mon scénario",
                description="Scénario par défaut",
                months=self.months,
                tva_default=self.tva_default,
                start_year=self.start_year,
                start_month=self.start_month,
                dso_days=self.dso_days,
                dpo_days=self.dpo_days,
                dio_days=self.dio_days,
                initial_cash=self.initial_cash,
                language_code=self.language_code,
                currency_code=self.currency_code,
                scale_mode=self.scale_mode,
                activities=[
                    {"name": "Service", "unit_price_ht": 1000.0, "vat_rate": 0.2, "variable_cost_per_unit_ht": 300.0}
                ],
                one_time_ranges=[
                    {"activity": "Service", "start_month": 1, "end_month": 3, "q0": 5.0, "monthly_growth": 0.0}
                ],
                subscription_ranges=[
                    {"activity": "Service", "start_month": 1, "end_month": 12, "q0": 10.0, "monthly_growth": 0.05}
                ],
                personnel=[
                    {
                        "title": "Employé 1",
                        "monthly_salary_gross": 3000.0,
                        "employer_cost_rate": 0.45,
                        "start_month": 1,
                        "end_month": 999,
                        "count": 1,
                    }
                ],
                charges=[
                    {"label": "Loyer", "monthly_amount_ht": 1200.0, "vat_rate": 0.2, "start_month": 1, "end_month": 999}
                ],
            )
            self.current_scenario_id = str(scenario.id)
            await self._load_scenario_from_model(scenario)
        except Exception:
            # Silently fail and create default scenario
            pass

    async def _load_scenario(self, scenario_id: str):
        """Load scenario from database by ID."""
        try:
            scenario = ScenarioService.get_scenario(scenario_id)
            await self._load_scenario_from_model(scenario)
        except Exception:
            # Scenario not found, create default
            await self._create_default_scenario()


    async def _load_scenario_from_model(self, scenario: Scenario):
        """Load state from scenario model."""
        self.current_scenario_id = str(scenario.id)

        # Load config (convert Peewee field types to Python types)
        self.months = int(scenario.months)
        self.tva_default = float(scenario.tva_default)
        self.start_year = int(scenario.start_year)
        self.start_month = int(scenario.start_month)
        self.dso_days = int(scenario.dso_days)
        self.dpo_days = int(scenario.dpo_days)
        self.dio_days = int(scenario.dio_days)
        self.initial_cash = float(scenario.initial_cash)

        # Load UI preferences
        self.language_code = str(scenario.language_code)
        self.currency_code = str(scenario.currency_code)
        self.scale_mode = str(scenario.scale_mode)

        # Load data lists (convert from dicts to dataclass instances)
        self.activities = [Activity(**d) for d in scenario.activities]
        self.one_time_ranges = [OneTimeRange(**d) for d in scenario.one_time_ranges]
        self.subscription_ranges = [SubscriptionRange(**d) for d in scenario.subscription_ranges]
        self.personnel = [PersonnelLine(**d) for d in scenario.personnel]
        self.charges = [ChargeExterne(**d) for d in scenario.charges]
        self.investments = [Investment(**d) for d in scenario.investments]
        self.loans = [Loan(**d) for d in scenario.loans]
        self.caps = [CapitalInjection(**d) for d in scenario.capital_injections]
        self.subsidies = [Subsidy(**d) for d in scenario.subsidies]

    async def _save_scenario(self):
        """Save current state to database."""
        if not self.current_scenario_id:
            return

        try:
            # Convert dataclass instances to dicts for JSON storage
            state_data = {
                'months': self.months,
                'tva_default': self.tva_default,
                'start_year': self.start_year,
                'start_month': self.start_month,
                'dso_days': self.dso_days,
                'dpo_days': self.dpo_days,
                'dio_days': self.dio_days,
                'initial_cash': self.initial_cash,
                'language_code': self.language_code,
                'currency_code': self.currency_code,
                'scale_mode': self.scale_mode,
                'activities': [vars(a) for a in self.activities],
                'one_time_ranges': [vars(r) for r in self.one_time_ranges],
                'subscription_ranges': [vars(r) for r in self.subscription_ranges],
                'personnel': [vars(p) for p in self.personnel],
                'charges': [vars(c) for c in self.charges],
                'investments': [vars(i) for i in self.investments],
                'loans': [vars(loan) for loan in self.loans],
                'capital_injections': [vars(c) for c in self.caps],
                'subsidies': [vars(s) for s in self.subsidies],
            }
            ScenarioService.save_state_to_scenario(self.current_scenario_id, state_data)
        except Exception:
            # Silently fail - logging would be better in production
            pass

    # ----------- i18n -----------
    language_code: str = "fr"

    @rx.var
    def language_options(self) -> list[str]:
        return sorted(LANGS.keys())

    def set_language_code(self, v: str):
        v = (v or "fr").lower()
        self.language_code = v if v in LANGS else "en"
        # Note: Cannot use async here, save will happen on next user interaction


    @rx.var
    def i18n(self) -> dict:
        return LANGS.get(self.language_code, LANGS.get("en", {}))

    # ----------- Currency & scale -----------
    currency_code: str = "EUR"        # EUR, USD, GBP, ...
    scale_mode: str = "thousands"     # units | thousands | millions (default: thousands for tables)

    def set_currency_code(self, v: str):
        self.currency_code = (v or "EUR").upper()

    def set_scale_mode(self, v: str):
        """Set scale mode, accepting both English values and translated labels."""
        v = (v or "units").lower()
        # Map translated labels back to English values
        i = self.i18n
        if v == i["config.scale.units"].lower():
            self.scale_mode = "units"
        elif v == i["config.scale.thousands"].lower():
            self.scale_mode = "thousands"
        elif v == i["config.scale.millions"].lower():
            self.scale_mode = "millions"
        elif v in ("units", "thousands", "millions"):
            self.scale_mode = v
        else:
            self.scale_mode = "units"

    @rx.var
    def currency_symbol(self) -> str:
        return {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "$", "AUD": "$", "JPY": "¥", "CNY": "¥", "XOF": "CFA"}.get(
            self.currency_code, self.currency_code
        )

    @rx.var
    def scale_div(self) -> float:
        return 1.0 if self.scale_mode == "units" else (1000.0 if self.scale_mode == "thousands" else 1_000_000.0)

    @rx.var
    def unit_suffix(self) -> str:
        """Generate unit suffix for tables based on selected currency and scale mode.

        Examples:
        - EUR + units -> "€"
        - EUR + thousands -> "k€"
        - USD + millions -> "M$"
        """
        tail = "" if self.scale_mode == "units" else ("k" if self.scale_mode == "thousands" else "M")
        return f"{self.currency_symbol}{tail}"

    @rx.var
    def synthese_y_unit_suffix(self) -> str:
        tail = "" if self.synthese_y_unit == "units" else ("k" if self.synthese_y_unit == "thousands" else "M")
        return f"{self.currency_symbol}{tail}"

    @rx.var
    def pnl_y_unit_suffix(self) -> str:
        tail = "" if self.pnl_y_unit == "units" else ("k" if self.pnl_y_unit == "thousands" else "M")
        return f"{self.currency_symbol}{tail}"

    @rx.var
    def cashflow_y_unit_suffix(self) -> str:
        tail = "" if self.cashflow_y_unit == "units" else ("k" if self.cashflow_y_unit == "thousands" else "M")
        return f"{self.currency_symbol}{tail}"

    @rx.var
    def scale_mode_label(self) -> str:
        """Returns the translated label for the current scale_mode."""
        i = self.i18n
        return i[f"config.scale.{self.scale_mode}"]

    @rx.var
    def scale_mode_options(self) -> list[str]:
        """Returns the list of translated scale mode options for the select component."""
        i = self.i18n
        return [
            i["config.scale.units"],
            i["config.scale.thousands"],
            i["config.scale.millions"]
        ]

    # ----------- Zoom (pour les graphes) -----------
    zoom_start: int = 1
    zoom_end: int = 60  # Default to full time horizon (matches default months)

    # ----------- Chart display options -----------
    # Selected series for each chart type (using internal keys that map to translation keys)
    # Internal keys: ca_ht, ebitda, rr etc.
    _synthese_default_keys: list[str] = ["ca_ht", "ebitda", "rr"]
    _pnl_default_keys: list[str] = ["revenues", "ebitda", "net_income"]
    _cashflow_default_keys: list[str] = ["operating_cf", "investing_cf", "cash_end"]
    synthese_selected_series: list[str] = []
    pnl_selected_series: list[str] = []
    cashflow_selected_series: list[str] = []

    _series_initialized: bool = False

    def _ensure_series_initialized(self):
        """Initialize selected series with translated names on first access.

        NOTE: Initialization is disabled to support "show all when none selected" behavior.
        Users can manually select series they want to display.
        """
        if not self._series_initialized:
            # Disabled: Let lists remain empty to show all series by default
            # # Map internal keys to current language column names for synthese
            # for key in self._synthese_default_keys:
            #     col_name = self.i18n.get(f"cols.{key}", "")
            #     if col_name and col_name not in self.synthese_selected_series:
            #         self.synthese_selected_series.append(col_name)

            # # Map internal keys to current language column names for PNL
            # for key in self._pnl_default_keys:
            #     col_name = self.i18n.get(f"cols.{key}", "")
            #     if col_name and col_name not in self.pnl_selected_series:
            #         self.pnl_selected_series.append(col_name)

            # # Map internal keys to current language column names for Cashflow
            # for key in self._cashflow_default_keys:
            #     col_name = self.i18n.get(f"cols.{key}", "")
            #     if col_name and col_name not in self.cashflow_selected_series:
            #         self.cashflow_selected_series.append(col_name)

            self._series_initialized = True

    # View mode: "monthly" or "yearly"
    synthese_view_mode: str = "yearly"
    pnl_view_mode: str = "yearly"
    cashflow_view_mode: str = "yearly"

    # Chart type: "line" or "bar"
    synthese_chart_type: str = "line"
    pnl_chart_type: str = "line"
    cashflow_chart_type: str = "line"

    # Y-axis units (€, k€, M€)
    synthese_y_unit: str = "thousands"  # units | thousands | millions
    pnl_y_unit: str = "thousands"
    cashflow_y_unit: str = "thousands"

    def toggle_synthese_series(self, series_key: str):
        """Toggle series selection for synthese chart."""
        if series_key in self.synthese_selected_series:
            self.synthese_selected_series.remove(series_key)
        else:
            self.synthese_selected_series.append(series_key)

    def toggle_pnl_series(self, series_key: str):
        """Toggle series selection for P&L chart."""
        if series_key in self.pnl_selected_series:
            self.pnl_selected_series.remove(series_key)
        else:
            self.pnl_selected_series.append(series_key)

    def toggle_cashflow_series(self, series_key: str):
        """Toggle series selection for cashflow chart."""
        if series_key in self.cashflow_selected_series:
            self.cashflow_selected_series.remove(series_key)
        else:
            self.cashflow_selected_series.append(series_key)

    def set_synthese_view_mode(self, mode: str):
        self.synthese_view_mode = mode

    def set_pnl_view_mode(self, mode: str):
        self.pnl_view_mode = mode

    def set_cashflow_view_mode(self, mode: str):
        self.cashflow_view_mode = mode

    def set_synthese_chart_type(self, chart_type: str):
        self.synthese_chart_type = chart_type

    def set_pnl_chart_type(self, chart_type: str):
        self.pnl_chart_type = chart_type

    def set_cashflow_chart_type(self, chart_type: str):
        self.cashflow_chart_type = chart_type

    def set_synthese_y_unit(self, v: str):
        self.synthese_y_unit = v if v in ("units", "thousands", "millions") else "thousands"

    def set_pnl_y_unit(self, v: str):
        self.pnl_y_unit = v if v in ("units", "thousands", "millions") else "thousands"

    def set_cashflow_y_unit(self, v: str):
        self.cashflow_y_unit = v if v in ("units", "thousands", "millions") else "thousands"

    # ----------- Data (avec exemples) -----------
    activities: list[Activity] = [
        Activity(name="Service", unit_price_ht=1000.0, vat_rate=0.2, variable_cost_per_unit_ht=300.0)
    ]
    one_time_ranges: list[OneTimeRange] = [
        OneTimeRange(activity="Service", start_month=1, end_month=3, q0=5.0, monthly_growth=0.0)
    ]
    subscription_ranges: list[SubscriptionRange] = [
        SubscriptionRange(activity="Service", start_month=1, end_month=12, q0=10.0, monthly_growth=0.05)
    ]
    personnel: list[PersonnelLine] = [
        PersonnelLine(
            title="Employé 1",
            monthly_salary_gross=3000.0,
            employer_cost_rate=0.45,
            start_month=1,
            end_month=999,
            count=1,  # headcount
        )
    ]
    charges: list[ChargeExterne] = [
        ChargeExterne(label="Loyer", monthly_amount_ht=1200.0, vat_rate=0.2, start_month=1, end_month=999)
    ]
    investments: list[Investment] = []
    loans: list[Loan] = []
    caps: list[CapitalInjection] = []
    subsidies: list[Subsidy] = []

    # ----------- Helpers parsing / format -----------
    def _to_int(self, v: str, default: int = 0) -> int:
        try:
            if v in ("", None):
                return default
            return int(float(v))
        except Exception:
            return default

    def _to_float(self, v: str, default: float = 0.0) -> float:
        try:
            if v in ("", None):
                return default
            return float(v)
        except Exception:
            return default

    # 2 decimals, with FR formatting if language_code == "fr"
    def _fmt2(self, x) -> str:
        try:
            val = float(x)
        except Exception:
            return str(x)
        if self.language_code == "fr":
            s = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
            return s
        return f"{val:,.2f}"

    # ----------- Generic setters (no negatives) -----------
    @rx.event(background=True)
    async def set_int(self, field: str, v: str):
        async with self:
            val = self._to_int(v, 0)
            val = max(1, val) if "month" in field or "months" in field else max(0, val)
            setattr(self, field, val)
            await self._save_scenario()

    @rx.event(background=True)
    async def set_float(self, field: str, v: str):
        async with self:
            val = self._to_float(v, 0.0)
            val = max(1.0, val) if "month" in field or "months" in field else max(0.0, val)
            setattr(self, field, val)
            await self._save_scenario()

    @rx.event(background=True)
    async def set_percent(self, field: str, v: str):
        """Set a percentage field (converts from percentage to decimal)."""
        async with self:
            val = self._to_float(v, 0.0) / 100.0
            val = max(0.0, val)
            setattr(self, field, val)
            await self._save_scenario()

    # ----------- List updates (dynamic tables) -----------
    @rx.event(background=True)
    async def update_item(self, list_name: str, index: int, field: str, v: str, kind: str = "str"):
        """Update an item in a list with validation and error handling.

        :param list_name: Name of the list attribute
        :type list_name: str
        :param index: Index of the item to update
        :type index: int
        :param field: Field name to update
        :type field: str
        :param v: New value as string
        :type v: str
        :param kind: Type conversion ('str', 'int', 'float', 'percent')
        :type kind: str
        """
        async with self:
            lst = list(getattr(self, list_name, []))
            if not (0 <= index < len(lst)):
                return

            obj = lst[index]

            try:
                # Convert and validate value
                if kind == "int":
                    newv = self._to_int(v, 0)
                    newv = max(1, newv) if ("month" in field or "months" in field) else max(0, newv)
                elif kind == "percent":
                    # Convert percentage to decimal (5% -> 0.05)
                    newv = self._to_float(v, 0.0) / 100.0
                    newv = max(0.0, newv)
                elif kind == "float":
                    newv = self._to_float(v, 0.0)
                    newv = max(1.0, newv) if ("month" in field or "months" in field) else max(0.0, newv)
                else:
                    newv = v or ""

                # Auto-increment duplicate names/titles/labels
                if field in ('name', 'title', 'label') and newv:
                    base_name = newv.strip()
                    final_name = base_name
                    counter = 1

                    # Collect all existing values except the current item
                    existing_values = set()
                    for i, item in enumerate(lst):
                        if i != index:  # Don't compare with itself
                            existing_value = getattr(item, field, None)
                            if existing_value:
                                existing_values.add(existing_value.strip().lower())

                    # Find a unique name by appending a counter
                    while final_name.lower() in existing_values:
                        counter += 1
                        final_name = f"{base_name} {counter}"

                    newv = final_name

                # Cascade activity name changes to all references
                if list_name == "activities" and field == "name":
                    old_name = obj.name
                    new_name = newv

                    # Update all one_time_ranges that reference this activity
                    updated_one_time = []
                    for ot_range in self.one_time_ranges:
                        if ot_range.activity == old_name:
                            updated_one_time.append(dataclasses.replace(ot_range, activity=new_name))
                        else:
                            updated_one_time.append(ot_range)
                    self.one_time_ranges = updated_one_time

                    # Update all subscription_ranges that reference this activity
                    updated_subscriptions = []
                    for sub_range in self.subscription_ranges:
                        if sub_range.activity == old_name:
                            updated_subscriptions.append(dataclasses.replace(sub_range, activity=new_name))
                        else:
                            updated_subscriptions.append(sub_range)
                    self.subscription_ranges = updated_subscriptions

                # Validate range constraints before updating
                if hasattr(obj, 'start_month') and hasattr(obj, 'end_month'):
                    start_val = newv if field == 'start_month' else obj.start_month
                    end_val = newv if field == 'end_month' else obj.end_month

                    if start_val > end_val:
                        # Reset to original value by forcing a re-render
                        setattr(self, list_name, lst)  # Trigger state update
                        error_msg = f"Start month ({start_val}) cannot be greater than end month ({end_val}). Change reverted."
                        return rx.window_alert(html.escape(error_msg))

                # Use dataclasses.replace instead of model_copy
                updated_obj = dataclasses.replace(obj, **{field: newv})
                lst[index] = updated_obj
                setattr(self, list_name, lst)
                await self._save_scenario()

            except (ValueError, TypeError) as e:
                # Reset to original value by forcing a re-render
                setattr(self, list_name, lst)
                error_msg = f"Invalid value for {field}: {str(e)}. Change reverted."
                return rx.window_alert(html.escape(error_msg))
            except Exception as e:
                # Reset to original value by forcing a re-render
                setattr(self, list_name, lst)
                error_msg = f"Error updating {field}: {str(e)}. Change reverted."
                return rx.window_alert(html.escape(error_msg))

    @rx.event(background=True)
    async def remove_item(self, list_name: str, index: int):
        async with self:
            lst = list(getattr(self, list_name, []))
            if not (0 <= index < len(lst)):
                return
            del lst[index]
            setattr(self, list_name, lst)
            await self._save_scenario()

    # ----------- Add actions -----------
    @rx.event(background=True)
    async def add_activity(self):
        async with self:
            # Generate unique name
            base_name = "Nouvelle activité"
            new_name = base_name
            counter = 1
            existing_names = {a.name.lower() for a in self.activities}
            while new_name.lower() in existing_names:
                counter += 1
                new_name = f"{base_name} {counter}"

            self.activities = [
                *self.activities,
                Activity(
                    name=new_name,
                    unit_price_ht=0.0,
                    vat_rate=0.2,
                    variable_cost_per_unit_ht=0.0,
                ),
            ]
            await self._save_scenario()

    @rx.event(background=True)
    async def add_one_time(self):
        async with self:
            name = self.activities[0].name if self.activities else "Service"
            self.one_time_ranges = [
                *self.one_time_ranges,
                OneTimeRange(activity=name, start_month=1, end_month=3, q0=1.0, monthly_growth=0.0),
            ]
            await self._save_scenario()

    @rx.event(background=True)
    async def add_subscription(self):
        async with self:
            name = self.activities[0].name if self.activities else "Service"
            self.subscription_ranges = [
                *self.subscription_ranges,
                SubscriptionRange(activity=name, start_month=1, end_month=12, q0=1.0, monthly_growth=0.0),
            ]
            await self._save_scenario()

    @rx.event(background=True)
    async def add_personnel(self):
        async with self:
            # Generate unique title
            base_title = "Nouveau poste"
            new_title = base_title
            counter = 1
            existing_titles = {p.title.lower() for p in self.personnel}
            while new_title.lower() in existing_titles:
                counter += 1
                new_title = f"{base_title} {counter}"

            self.personnel = [
                *self.personnel,
                PersonnelLine(
                    title=new_title,
                    monthly_salary_gross=0.0,
                    employer_cost_rate=0.45,
                    start_month=1,
                    end_month=999,
                    count=1,
                ),
            ]
            await self._save_scenario()

    @rx.event(background=True)
    async def add_charge(self):
        async with self:
            # Generate unique label
            base_label = "Nouvelle charge"
            new_label = base_label
            counter = 1
            existing_labels = {c.label.lower() for c in self.charges}
            while new_label.lower() in existing_labels:
                counter += 1
                new_label = f"{base_label} {counter}"

            self.charges = [
                *self.charges,
                ChargeExterne(
                    label=new_label,
                    monthly_amount_ht=0.0,
                    vat_rate=self.tva_default,
                    start_month=1,
                    end_month=999,
                ),
            ]
            await self._save_scenario()

    @rx.event(background=True)
    async def add_investment(self):
        async with self:
            # Generate unique label
            base_label = "Nouveau matériel"
            new_label = base_label
            counter = 1
            existing_labels = {i.label.lower() for i in self.investments}
            while new_label.lower() in existing_labels:
                counter += 1
                new_label = f"{base_label} {counter}"

            self.investments = [
                *self.investments,
                Investment(
                    label=new_label,
                    amount_ht=0.0,
                    vat_rate=self.tva_default,
                    purchase_month=1,
                    amort_years=3,
                ),
            ]
            await self._save_scenario()

    @rx.event(background=True)
    async def add_loan(self):
        async with self:
            # Generate unique label
            base_label = "Nouveau prêt"
            new_label = base_label
            counter = 1
            existing_labels = {l.label.lower() for l in self.loans}
            while new_label.lower() in existing_labels:
                counter += 1
                new_label = f"{base_label} {counter}"

            self.loans = [
                *self.loans,
                Loan(label=new_label, principal=0.0, annual_rate=0.04, months=36, start_month=1),
            ]
            await self._save_scenario()

    @rx.event(background=True)
    async def add_capital(self):
        async with self:
            # Generate unique label
            base_label = "Apport"
            new_label = base_label
            counter = 1
            existing_labels = {c.label.lower() for c in self.caps}
            while new_label.lower() in existing_labels:
                counter += 1
                new_label = f"{base_label} {counter}"

            self.caps = [*self.caps, CapitalInjection(label=new_label, amount=0.0, month=1)]
            await self._save_scenario()

    @rx.event(background=True)
    async def add_subsidy(self):
        async with self:
            # Generate unique label
            base_label = "Subvention"
            new_label = base_label
            counter = 1
            existing_labels = {s.label.lower() for s in self.subsidies}
            while new_label.lower() in existing_labels:
                counter += 1
                new_label = f"{base_label} {counter}"

            self.subsidies = [*self.subsidies, Subsidy(label=new_label, amount=0.0, month=1)]
            await self._save_scenario()


    # ----------- Constellab params -----------
    @rx.var
    def app_title(self) -> str:
        return self._app_title

    @rx.var
    def corporate_tax_rate(self) -> float:
        return self._corporate_tax_rate

    @rx.var
    def activity_options(self) -> list[str]:
        return [a.name for a in self.activities] if self.activities else []

    # ----------- Config object -----------
    def _cfg(self) -> Config:
        return Config(
            months=self._months_override if self._months_override > 0 else self.months,
            tva_default=self.tva_default,
            start_year=self.start_year,
            start_month=self.start_month,
            corporate_tax_rate=self.corporate_tax_rate,
            dso_days=self.dso_days,
            dpo_days=self.dpo_days,
            dio_days=self.dio_days,
            initial_cash=self.initial_cash,
        )

    # ----------- Orders from ranges -----------
    @rx.var
    def orders_one_time(self) -> list[Order]:
        return expand_one_time_ranges_to_orders(self.one_time_ranges, self.months, Order)

    @rx.var
    def orders_subscriptions(self) -> list[Order]:
        return expand_subscription_ranges_to_orders(self.subscription_ranges, self.months, Order)

    @rx.var
    def orders_effective(self) -> list[Order]:
        return list(self.orders_one_time) + list(self.orders_subscriptions)

    # ----------- Compute all DFs -----------
    def _translate_columns(self, df):
        """Translate dataframe column names based on current language."""
        if self.language_code == "fr":
            return df  # Already in French from engine

        # Mapping from engine output to translated names
        col_map = {
            # Synthese columns
            "Revenue HT": self.i18n.get("cols.ca_ht", "Revenue HT"),
            "Variable costs HT": self.i18n.get("cols.couts_variables_ht", "Variable costs HT"),
            "Gross margin HT": self.i18n.get("cols.marge_couts_variables_ht", "Gross margin HT"),
            "Personnel costs": self.i18n.get("cols.charges_personnel", "Personnel costs"),
            "External charges": self.i18n.get("cols.charges_externes", "External charges"),
            "EBITDA": self.i18n.get("cols.ebitda", "EBITDA"),
            "Depreciation": self.i18n.get("cols.amortissements", "Depreciation"),
            "EBIT": self.i18n.get("cols.ebit", "EBIT"),
            "Corporate tax": self.i18n.get("cols.is", "Corporate tax"),
            "Net income": self.i18n.get("cols.resultat_net", "Net income"),
            "RR": self.i18n.get("cols.rr", "RR"),
            # PNL columns
            "Revenues": self.i18n.get("cols.revenues", "Revenues"),
            "Variable costs": self.i18n.get("cols.variable_costs", "Variable costs"),
            "Gross profit": self.i18n.get("cols.gross_profit", "Gross profit"),
            "Personnel": self.i18n.get("cols.personnel", "Personnel"),
            "Tax": self.i18n.get("cols.tax", "Tax"),
            # Cashflow columns
            "Operating CF": self.i18n.get("cols.operating_cf", "Operating CF"),
            "Investing CF": self.i18n.get("cols.investing_cf", "Investing CF"),
            "Financing CF": self.i18n.get("cols.financing_cf", "Financing CF"),
            "Cash end": self.i18n.get("cols.cash_end", "Cash end"),
            # Plan financement columns
            "Year": self.i18n.get("cols.year", "Year"),
            "Capital+Subsidies": self.i18n.get("cols.capital_subsidies", "Capital+Subsidies"),
            "Capex": self.i18n.get("cols.capex", "Capex"),
            "Cash variation": self.i18n.get("cols.cash_variation", "Cash variation"),
            # Bilans columns
            "Cash": self.i18n.get("cols.cash", "Cash"),
            "Net fixed assets": self.i18n.get("cols.net_fixed_assets", "Net fixed assets"),
            "Equity (approx)": self.i18n.get("cols.equity", "Equity (approx)"),
            "Liabilities (placeholder)": self.i18n.get("cols.liabilities", "Liabilities (placeholder)"),
        }
        return df.rename(columns=col_map)

    def _dfs(self):
        raw_dfs = compute_all(
            self._cfg(),
            self.activities,
            self.orders_one_time,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
            subs_orders=self.orders_subscriptions,
        )

        # Translate column names based on current language
        if "synthese" in raw_dfs:
            raw_dfs["synthese"] = self._translate_columns(raw_dfs["synthese"])
        if "pnl" in raw_dfs:
            raw_dfs["pnl"] = self._translate_columns(raw_dfs["pnl"])
        if "cashflow" in raw_dfs:
            raw_dfs["cashflow"] = self._translate_columns(raw_dfs["cashflow"])

        return raw_dfs

    # ----------- Scaling for tables -----------
    def _scaled_df_for_table(self, df, index_label: str = "Month", exclude_cols=None):
        exclude_cols = set(exclude_cols or [])
        df = df.reset_index()
        # Remove level_0 column if it exists
        if "level_0" in df.columns:
            df = df.drop(columns=["level_0"])
        if "index" in df.columns:
            # Translate index label
            translated_label = self.i18n.get(f"cols.{index_label.lower()}", index_label)
            df = df.rename(columns={"index": translated_label})
            index_label = translated_label
        div = float(self.scale_div)
        # Get translated Month and Year for comparison
        month_label = self.i18n.get("cols.month", "Month")
        year_label = self.i18n.get("cols.year", "Year")
        for c in df.columns:
            if c in (month_label, year_label):
                continue
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c] / div
        # Suffix with unit
        new_cols = []
        for c in df.columns:
            if c in (month_label, year_label) or c in exclude_cols:
                new_cols.append(c)
            else:
                new_cols.append(f"{c} ({self.unit_suffix})")
        df.columns = new_cols
        # Format numbers
        for c in df.columns:
            if c in (month_label, year_label):
                continue
            try:
                if pd.api.types.is_numeric_dtype(df[c]):
                    df[c] = df[c].map(self._fmt2)
            except Exception:
                pass
        return df

    # ----------- Scaling for charts -----------
    def _get_chart_y_divisor(self, chart_type: str) -> float:
        """Get the divisor for a specific chart type based on its y-axis unit."""
        if chart_type == "synthese":
            unit = self.synthese_y_unit
        elif chart_type == "pnl":
            unit = self.pnl_y_unit
        elif chart_type == "cashflow":
            unit = self.cashflow_y_unit
        else:
            unit = "thousands"

        return 1.0 if unit == "units" else (1000.0 if unit == "thousands" else 1_000_000.0)

    def _scaled_df_for_chart(self, df, chart_type: str = "synthese"):
        df = df.copy()
        # Ensure we have an "index" column
        if "index" not in df.columns:
            df = df.reset_index()
            # Remove level_0 column if it exists
            if "level_0" in df.columns:
                df = df.drop(columns=["level_0"])
            # If reset_index didn't create an "index" column, rename the first column
            if "index" not in df.columns and len(df.columns) > 0:
                df = df.rename(columns={df.columns[0]: "index"})

        div = self._get_chart_y_divisor(chart_type)
        for c in df.columns:
            if c == "index":
                continue
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c] / div
        return df

    # ----------- Monthly -> Annual -----------
    def _monthly_to_annual(self, df):
        df = df.copy().reset_index()
        # Remove level_0 column if it exists
        if "level_0" in df.columns:
            df = df.drop(columns=["level_0"])
        if "index" not in df.columns:
            return df
        months = df["index"].astype(int)
        years = self.start_year + (self.start_month - 1 + (months - 1)) // 12
        # Use internal column name temporarily for grouping
        df["_year_temp"] = years
        num_cols = [c for c in df.columns if c not in ("index", "_year_temp")]
        out = df.groupby("_year_temp", as_index=False)[num_cols].sum(numeric_only=True)
        # Rename "_year_temp" to "index" for consistency with chart code
        out = out.rename(columns={"_year_temp": "index"})
        return out

    # ----------- Helper to expose table cols+values (ordered) -----------
    def _cols_vals(self, df, index_label: str, exclude_cols=None):
        df2 = self._scaled_df_for_table(df, index_label=index_label, exclude_cols=exclude_cols)
        cols = list(df2.columns)
        values = [[str(row[c]) for c in cols] for _, row in df2.iterrows()]
        return cols, values

    # ========== SYNTHÈSE ==========
    @rx.var
    def synthese_table_annual_cols(self) -> list[str]:
        return self._cols_vals(self._monthly_to_annual(self._dfs()["synthese"]), "Year", ["Year"])[0]

    @rx.var
    def synthese_table_annual_values(self) -> list[list[str]]:
        return self._cols_vals(self._monthly_to_annual(self._dfs()["synthese"]), "Year", ["Year"])[1]

    @rx.var
    def synthese_table_monthly_cols(self) -> list[str]:
        return self._cols_vals(self._dfs()["synthese"], "Month")[0]

    @rx.var
    def synthese_table_monthly_values(self) -> list[list[str]]:
        return self._cols_vals(self._dfs()["synthese"], "Month")[1]

    # ========== P&L ==========
    @rx.var
    def pnl_table_annual_cols(self) -> list[str]:
        return self._cols_vals(self._monthly_to_annual(self._dfs()["pnl"]), "Year", ["Year"])[0]

    @rx.var
    def pnl_table_annual_values(self) -> list[list[str]]:
        return self._cols_vals(self._monthly_to_annual(self._dfs()["pnl"]), "Year", ["Year"])[1]

    @rx.var
    def pnl_table_monthly_cols(self) -> list[str]:
        return self._cols_vals(self._dfs()["pnl"], "Month")[0]

    @rx.var
    def pnl_table_monthly_values(self) -> list[list[str]]:
        return self._cols_vals(self._dfs()["pnl"], "Month")[1]

    # ========== CASHFLOW ==========
    @rx.var
    def cashflow_table_annual_cols(self) -> list[str]:
        return self._cols_vals(self._monthly_to_annual(self._dfs()["cashflow"]), "Year", ["Year"])[0]

    @rx.var
    def cashflow_table_annual_values(self) -> list[list[str]]:
        return self._cols_vals(self._monthly_to_annual(self._dfs()["cashflow"]), "Year", ["Year"])[1]

    @rx.var
    def cashflow_table_monthly_cols(self) -> list[str]:
        return self._cols_vals(self._dfs()["cashflow"], "Month")[0]

    @rx.var
    def cashflow_table_monthly_values(self) -> list[list[str]]:
        return self._cols_vals(self._dfs()["cashflow"], "Month")[1]

    # ========== PLAN DE FINANCEMENT (annuel) ==========
    @rx.var
    def plan_table_annual_cols(self) -> list[str]:
        return self._cols_vals(self._dfs()["plan_financement"], "Year", ["Year"])[0]

    @rx.var
    def plan_table_annual_values(self) -> list[list[str]]:
        return self._cols_vals(self._dfs()["plan_financement"], "Year", ["Year"])[1]

    # ========== BILANS (mensuel) ==========
    @rx.var
    def bilan_actif_table_cols(self) -> list[str]:
        return self._cols_vals(self._dfs()["bilans"]["actif"], "Month")[0]

    @rx.var
    def bilan_actif_table_values(self) -> list[list[str]]:
        return self._cols_vals(self._dfs()["bilans"]["actif"], "Month")[1]

    @rx.var
    def bilan_passif_table_cols(self) -> list[str]:
        return self._cols_vals(self._dfs()["bilans"]["passif"], "Month")[0]

    @rx.var
    def bilan_passif_table_values(self) -> list[list[str]]:
        return self._cols_vals(self._dfs()["bilans"]["passif"], "Month")[1]

    # ----------- Charts palette & quantities by activity -----------
    @rx.var
    def chart_palette(self) -> list[str]:
        """Extended color palette with 30 distinct colors for chart series."""
        return [
            # Primary colors (original palette)
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
            # Extended palette for more variables
            "#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24", "#6c5ce7",
            "#a29bfe", "#fd79a8", "#fdcb6e", "#00b894", "#0984e3",
            "#e17055", "#74b9ff", "#a29bfe", "#fab1a0", "#ff7675",
            "#55efc4", "#81ecec", "#ffeaa7", "#dfe6e9", "#636e72",
            "#e84393", "#00cec9", "#00b894", "#fdcb6e", "#fd79a8",
            "#6c5ce7", "#ffeaa7", "#74b9ff", "#a29bfe", "#dfe6e9"
        ]

    @rx.var
    def one_time_qty_chart_rows(self) -> list[dict]:
        qty_by_act = self._dfs()["qty_by_activity_one_time"]
        acts = {r.activity for r in self.one_time_ranges}
        idx = pd.Index(range(1, self.months + 1), name="index")
        data = pd.DataFrame(index=idx)
        for a in acts:
            s = qty_by_act.get(a)
            if s is None:
                s = pd.Series(0.0, index=idx)
            data[a] = s
        return data.reset_index().to_dict(orient="records")

    @rx.var
    def subscription_qty_chart_rows(self) -> list[dict]:
        qty_by_act = self._dfs()["qty_by_activity_subscription"]
        acts = {r.activity for r in self.subscription_ranges}
        idx = pd.Index(range(1, self.months + 1), name="index")
        data = pd.DataFrame(index=idx)
        for a in acts:
            s = qty_by_act.get(a)
            if s is None:
                s = pd.Series(0.0, index=idx)
            data[a] = s
        return data.reset_index().to_dict(orient="records")

    def _series_defs_from_acts(self, acts: list[str]) -> list[dict]:
        pal = self.chart_palette
        return [{"key": a, "color": pal[i % len(pal)], "unit": ""} for i, a in enumerate(acts or [])]

    @rx.var
    def one_time_qty_series_defs(self) -> list[dict]:
        return self._series_defs_from_acts([r.activity for r in self.one_time_ranges])

    @rx.var
    def subscription_qty_series_defs(self) -> list[dict]:
        return self._series_defs_from_acts([r.activity for r in self.subscription_ranges])

    # ----------- Financial charts data -----------
    @rx.var
    def synthese_chart_rows(self) -> list[dict]:
        """Chart data for summary/synthese with zoom and view mode applied."""
        df = self._dfs()["synthese"]

        # Apply yearly aggregation if needed
        if self.synthese_view_mode == "yearly":
            df = self._monthly_to_annual(df)

        # Scale the data
        df = self._scaled_df_for_chart(df, "synthese")

        # Apply zoom filter based on view mode
        if self.synthese_view_mode == "yearly":
            # For yearly view, index represents years, not months
            # Don't filter by zoom since zoom is for months
            pass
        else:
            # For monthly view, apply zoom normally
            df = df[(df["index"] >= self.zoom_start) & (df["index"] <= self.zoom_end)]

        # Filter by selected series
        if self.synthese_selected_series:
            cols_to_keep = ["index"] + [c for c in df.columns if c in self.synthese_selected_series]
            df = df[cols_to_keep]

        return df.to_dict(orient="records")

    @rx.var
    def synthese_series_defs(self) -> list[dict]:
        """Series definitions for synthese chart."""
        cols = [c for c in self._dfs()["synthese"].columns if c != "index"]
        pal = self.chart_palette
        all_defs = [{"key": col, "color": pal[i % len(pal)], "unit": ""} for i, col in enumerate(cols)]

        # Filter by selected series
        if self.synthese_selected_series:
            return [d for d in all_defs if d["key"] in self.synthese_selected_series]
        return all_defs

    @rx.var
    def pnl_chart_rows(self) -> list[dict]:
        """Chart data for P&L with zoom and view mode applied."""
        df = self._dfs()["pnl"]

        # Apply yearly aggregation if needed
        if self.pnl_view_mode == "yearly":
            df = self._monthly_to_annual(df)

        # Scale the data
        df = self._scaled_df_for_chart(df, "pnl")

        # Apply zoom filter based on view mode
        if self.pnl_view_mode == "yearly":
            # For yearly view, index represents years, not months
            # Don't filter by zoom since zoom is for months
            pass
        else:
            # For monthly view, apply zoom normally
            df = df[(df["index"] >= self.zoom_start) & (df["index"] <= self.zoom_end)]

        # Filter by selected series
        if self.pnl_selected_series:
            cols_to_keep = ["index"] + [c for c in df.columns if c in self.pnl_selected_series]
            df = df[cols_to_keep]

        return df.to_dict(orient="records")

    @rx.var
    def pnl_series_defs(self) -> list[dict]:
        """Series definitions for P&L chart."""
        cols = [c for c in self._dfs()["pnl"].columns if c != "index"]
        pal = self.chart_palette
        all_defs = [{"key": col, "color": pal[i % len(pal)], "unit": ""} for i, col in enumerate(cols)]

        # Filter by selected series
        if self.pnl_selected_series:
            return [d for d in all_defs if d["key"] in self.pnl_selected_series]
        return all_defs

    @rx.var
    def cashflow_chart_rows(self) -> list[dict]:
        """Chart data for cashflow with zoom and view mode applied."""
        df = self._dfs()["cashflow"]

        # Apply yearly aggregation if needed
        if self.cashflow_view_mode == "yearly":
            df = self._monthly_to_annual(df)

        # Scale the data
        df = self._scaled_df_for_chart(df, "cashflow")

        # Apply zoom filter based on view mode
        if self.cashflow_view_mode == "yearly":
            # For yearly view, index represents years, not months
            # Don't filter by zoom since zoom is for months
            pass
        else:
            # For monthly view, apply zoom normally
            df = df[(df["index"] >= self.zoom_start) & (df["index"] <= self.zoom_end)]

        # Filter by selected series
        if self.cashflow_selected_series:
            cols_to_keep = ["index"] + [c for c in df.columns if c in self.cashflow_selected_series]
            df = df[cols_to_keep]

        return df.to_dict(orient="records")

    @rx.var
    def cashflow_series_defs(self) -> list[dict]:
        """Series definitions for cashflow chart."""
        cols = [c for c in self._dfs()["cashflow"].columns if c != "index"]
        pal = self.chart_palette
        all_defs = [{"key": col, "color": pal[i % len(pal)], "unit": ""} for i, col in enumerate(cols)]

        # Filter by selected series
        if self.cashflow_selected_series:
            return [d for d in all_defs if d["key"] in self.cashflow_selected_series]
        return all_defs

    @rx.var
    def synthese_all_series(self) -> list[dict]:
        """All available series for synthese (for selection UI)."""
        self._ensure_series_initialized()
        cols = [c for c in self._dfs()["synthese"].columns if c != "index"]
        pal = self.chart_palette
        return [{"key": col, "color": pal[i % len(pal)]} for i, col in enumerate(cols)]

    @rx.var
    def pnl_all_series(self) -> list[dict]:
        """All available series for P&L (for selection UI)."""
        self._ensure_series_initialized()
        cols = [c for c in self._dfs()["pnl"].columns if c != "index"]
        pal = self.chart_palette
        return [{"key": col, "color": pal[i % len(pal)]} for i, col in enumerate(cols)]

    @rx.var
    def cashflow_all_series(self) -> list[dict]:
        """All available series for cashflow (for selection UI)."""
        self._ensure_series_initialized()
        cols = [c for c in self._dfs()["cashflow"].columns if c != "index"]
        pal = self.chart_palette
        return [{"key": col, "color": pal[i % len(pal)]} for i, col in enumerate(cols)]

    # ----------- Zoom helpers -----------
    def _clamp_zoom(self):
        s = max(1, min(self.zoom_start, self.months))
        e = max(1, min(self.zoom_end, self.months))
        if e < s:
            s, e = e, s
        self.zoom_start, self.zoom_end = s, e

    def zoom_set_start(self, v: str):
        try:
            self.zoom_start = int(float(v)) if v not in ("", None) else 1
        except Exception:
            self.zoom_start = 1
        self._clamp_zoom()

    def zoom_set_end(self, v: str):
        try:
            self.zoom_end = int(float(v)) if v not in ("", None) else self.months
        except Exception:
            self.zoom_end = self.months
        self._clamp_zoom()

    def zoom_all(self):
        self.zoom_start, self.zoom_end = 1, self.months
        self._clamp_zoom()

    def zoom_3m(self):
        self.zoom_end = self.months
        self.zoom_start = max(1, self.months - 3 + 1)
        self._clamp_zoom()

    def zoom_6m(self):
        self.zoom_end = self.months
        self.zoom_start = max(1, self.months - 6 + 1)
        self._clamp_zoom()

    def zoom_12m(self):
        self.zoom_end = self.months
        self.zoom_start = max(1, self.months - 12 + 1)
        self._clamp_zoom()
