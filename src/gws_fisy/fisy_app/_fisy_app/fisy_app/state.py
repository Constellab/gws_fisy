from typing import List, Dict
import json
from pathlib import Path
import reflex as rx
from gws_reflex_main import ReflexMainState

from .calc.models import (
    Config, Activity, Order, PersonnelLine, ChargeExterne,
    Investment, Loan, CapitalInjection, Subsidy,
)
from .calc.engine import compute_all
from .calc.sale_ranges import (
    OneTimeRange, SubscriptionRange,
    expand_one_time_ranges_to_orders, expand_subscription_ranges_to_orders,
)

# Load translations from JSON (extensible)
_I18N_PATH = Path(__file__).parent / "i18n" / "translations.json"
try:
    _I18N_ALL: Dict[str, Dict[str, str]] = json.loads(_I18N_PATH.read_text(encoding="utf-8"))
except Exception:
    _I18N_ALL = {"en": {"app_title": "FISY — App"}, "fr": {"app_title": "FISY — App"}}


class State(ReflexMainState):
    # Global params
    months: int = 36
    tva_default: float = 0.2
    start_year: int = 2025
    start_month: int = 1
    dso_days: int = 30
    dpo_days: int = 30
    dio_days: int = 0
    initial_cash: float = 0.0

    # Language / Currency / Scale
    language_code: str = "fr"       # "fr", "en", ...
    currency_code: str = "EUR"      # "EUR","USD","GBP","CHF","CAD","AUD","JPY"
    scale_mode: str = "units"       # "units" | "thousands" | "millions"

    def set_language_code(self, v: str):
        self.language_code = (v or "en").lower()

    def set_currency_code(self, v: str):
        self.currency_code = (v or "EUR").upper()

    def set_scale_mode(self, v: str):
        v = (v or "units").lower()
        if v not in ("units", "thousands", "millions"):
            v = "units"
        self.scale_mode = v

    @rx.var
    def i18n(self) -> Dict[str, str]:
        lang = (self.language_code or "en").lower()
        base = _I18N_ALL.get("en", {})
        loc = _I18N_ALL.get(lang, {})
        # Merge with fallback to English
        merged = dict(base)
        merged.update(loc)
        return merged

    @rx.var
    def app_title(self) -> str:
        return self.i18n.get("app_title", "FISY — App")

    @rx.var
    def currency_symbol(self) -> str:
        mapping = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "$", "AUD": "$", "JPY": "¥"}
        return mapping.get(self.currency_code, self.currency_code)

    @rx.var
    def scale_div(self) -> float:
        return 1.0 if self.scale_mode == "units" else (1000.0 if self.scale_mode == "thousands" else 1_000_000.0)

    @rx.var
    def unit_suffix(self) -> str:
        tail = "" if self.scale_mode == "units" else ("k" if self.scale_mode == "thousands" else "M")
        return f"{self.currency_symbol}{tail}"

    # Zoom for charts
    zoom_start: int = 1
    zoom_end: int = 12

    # User data
    activities: List[Activity] = [
        Activity(name="Service", unit_price_ht=1000.0, vat_rate=0.2, variable_cost_per_unit_ht=300.0)
    ]
    one_time_ranges: List[OneTimeRange] = [
        OneTimeRange(activity="Service", start_month=1, end_month=3, q0=5.0, monthly_growth=0.0)
    ]
    subscription_ranges: List[SubscriptionRange] = [
        SubscriptionRange(activity="Service", start_month=1, end_month=12, q0=10.0, monthly_growth=0.05)
    ]
    personnel: List[PersonnelLine] = [
        PersonnelLine(title="Employé 1", monthly_salary_gross=3000.0, employer_cost_rate=0.45, start_month=1)
    ]
    charges: List[ChargeExterne] = [
        ChargeExterne(label="Loyer", monthly_amount_ht=1200.0, vat_rate=0.2, start_month=1)
    ]
    investments: List[Investment] = []
    loans: List[Loan] = []
    caps: List[CapitalInjection] = []
    subsidies: List[Subsidy] = []

    # Helpers
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

    def set_int(self, field: str, v: str):
        setattr(self, field, self._to_int(v))

    def set_float(self, field: str, v: str):
        setattr(self, field, self._to_float(v))

    def update_item(self, list_name: str, index: int, field: str, v: str, kind: str = "str"):
        lst = list(getattr(self, list_name, []))
        if not (0 <= index < len(lst)):
            return
        obj = lst[index]
        if kind == "int":
            newv = self._to_int(v)
        elif kind == "float":
            newv = self._to_float(v)
        else:
            newv = v or ""
        lst[index] = obj.model_copy(update={field: newv})
        setattr(self, list_name, lst)

    def remove_item(self, list_name: str, index: int):
        lst = list(getattr(self, list_name, []))
        if not (0 <= index < len(lst)):
            return
        del lst[index]
        setattr(self, list_name, lst)

    # Adders
    def add_activity(self):
        self.activities = [
            *self.activities,
            Activity(name="New activity", unit_price_ht=0.0, vat_rate=0.2, variable_cost_per_unit_ht=0.0)]

    def add_one_time(self):
        name = self.activities[0].name if self.activities else "Service"
        self.one_time_ranges = [
            *self.one_time_ranges,
            OneTimeRange(activity=name, start_month=1, end_month=3, q0=1.0, monthly_growth=0.0)]

    def add_subscription(self):
        name = self.activities[0].name if self.activities else "Service"
        self.subscription_ranges = [
            *self.subscription_ranges,
            SubscriptionRange(activity=name, start_month=1, end_month=12, q0=1.0, monthly_growth=0.0)]

    def add_personnel(self):
        self.personnel = [
            *self.personnel,
            PersonnelLine(
                title="New position", monthly_salary_gross=0.0, employer_cost_rate=0.45, start_month=1, end_month=999)]

    def add_charge(self):
        self.charges = [
            *self.charges,
            ChargeExterne(
                label="New charge", monthly_amount_ht=0.0, vat_rate=self.tva_default, start_month=1, end_month=999)]

    def add_investment(self):
        self.investments = [
            *self.investments,
            Investment(
                label="New asset", amount_ht=0.0, vat_rate=self.tva_default, purchase_month=1, amort_years=3)]

    def add_loan(self):
        self.loans = [*self.loans, Loan(label="New loan", principal=0.0, annual_rate=0.04, months=36, start_month=1)]

    def add_capital(self):
        self.caps = [*self.caps, CapitalInjection(label="Capital", amount=0.0, month=1)]

    def add_subsidy(self):
        self.subsidies = [*self.subsidies, Subsidy(label="Subsidy", amount=0.0, month=1)]

    # Derived
    @rx.var
    def activity_options(self) -> list[str]:
        return [a.name for a in self.activities] if self.activities else []

    @rx.var
    def corporate_tax_rate(self) -> float:
        return float(self.get_param("corporate_tax_rate", 0.25))

    def _cfg(self) -> Config:
        return Config(
            months=int(self.get_param("months", self.months)),
            tva_default=self.tva_default,
            start_year=self.start_year,
            start_month=self.start_month,
            corporate_tax_rate=self.corporate_tax_rate,
            dso_days=self.dso_days,
            dpo_days=self.dpo_days,
            dio_days=self.dio_days,
            initial_cash=self.initial_cash,
        )

    @rx.var
    def orders_one_time(self) -> List[Order]:
        return expand_one_time_ranges_to_orders(self.one_time_ranges, self.months, Order)

    @rx.var
    def orders_subscriptions(self) -> List[Order]:
        return expand_subscription_ranges_to_orders(self.subscription_ranges, self.months, Order)

    @rx.var
    def orders_effective(self) -> List[Order]:
        return list(self.orders_one_time) + list(self.orders_subscriptions)

    def _dfs(self):
        return compute_all(
            self._cfg(), self.activities, self.orders_effective, self.personnel,
            self.charges, self.investments, self.loans, self.caps, self.subsidies,
            subs_orders=self.orders_subscriptions,
        )

    # Scaling helpers
    def _scaled_df_for_table(self, df):
        import pandas as pd
        df = df.reset_index()
        if "index" in df.columns:
            df = df.rename(columns={"index": "Mois"})
        div = float(self.scale_div)

        # 1) scale numeric columns
        for c in df.columns:
            if c == "Mois":
                continue
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c] / div

        # 2) add unit suffix to headers
        new_cols = []
        for c in df.columns:
            if c == "Mois":
                new_cols.append(c)
            else:
                new_cols.append(f"{c} ({self.unit_suffix})")
        df.columns = new_cols

        # 3) format numeric values to 2 decimals (localized)
        for c in df.columns:
            if c == "Mois":
                continue
            # si la série est numérique (après scaling), on la formate en string 2 décimales
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c].map(self._fmt2)

        return df

    def _scaled_df_for_chart(self, df):
        import pandas as pd
        df = df.reset_index()
        div = float(self.scale_div)
        for c in df.columns:
            if c != "index" and pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c] / div
        return df

    def _series_from_cols_scaled(self, cols):
        return [c for c in cols if c != "index"]

    # Tables (rows/cols)
    @rx.var
    def synthese_rows(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["synthese"]).to_dict(orient="records")

    @rx.var
    def pnl_rows(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["pnl"]).to_dict(orient="records")

    @rx.var
    def cashflow_rows(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["cashflow"]).to_dict(orient="records")

    @rx.var
    def plan_rows(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["plan_financement"]).to_dict(orient="records")

    @rx.var
    def bilan_actif_rows(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["bilans"]["actif"]).to_dict(orient="records")

    @rx.var
    def bilan_passif_rows(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["bilans"]["passif"]).to_dict(orient="records")

    @rx.var
    def synthese_cols(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["synthese"]).columns)

    @rx.var
    def pnl_cols(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["pnl"]).columns)

    @rx.var
    def cashflow_cols(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["cashflow"]).columns)

    @rx.var
    def plan_cols(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["plan_financement"]).columns)

    @rx.var
    def bilan_actif_cols(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["bilans"]["actif"]).columns)

    @rx.var
    def bilan_passif_cols(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["bilans"]["passif"]).columns)

    # Charts (scaled)
    def _chart_cols(self, key: str) -> list[str]:
        if key == "pnl":
            cols = list(self._scaled_df_for_chart(self._dfs()["pnl"]).columns)
        elif key == "cashflow":
            cols = list(self._scaled_df_for_chart(self._dfs()["cashflow"]).columns)
        else:
            cols = list(self._scaled_df_for_chart(self._dfs()["synthese"]).columns)
        return cols

    @rx.var
    def pnl_chart_rows(self) -> List[dict]:
        return self._scaled_df_for_chart(self._dfs()["pnl"]).to_dict(orient="records")

    @rx.var
    def cashflow_chart_rows(self) -> List[dict]:
        return self._scaled_df_for_chart(self._dfs()["cashflow"]).to_dict(orient="records")

    @rx.var
    def synthese_chart_rows(self) -> List[dict]:
        return self._scaled_df_for_chart(self._dfs()["synthese"]).to_dict(orient="records")

    @rx.var
    def pnl_series(self) -> list[str]:
        return self._series_from_cols_scaled(self._chart_cols("pnl"))

    @rx.var
    def cashflow_series(self) -> list[str]:
        return self._series_from_cols_scaled(self._chart_cols("cashflow"))

    @rx.var
    def synthese_series(self) -> list[str]:
        return self._series_from_cols_scaled(self._chart_cols("syn"))

    # Palette & series defs
    @rx.var
    def chart_palette(self) -> list[str]:
        return ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

    def _series_defs(self, keys: list[str]) -> list[dict]:
        pal = self.chart_palette
        n = len(pal) if pal else 1
        return [{"key": k, "color": pal[i % n], "unit": self.unit_suffix} for i, k in enumerate(keys or [])]

    @rx.var
    def synthese_series_defs(self) -> list[dict]:
        return self._series_defs(self.synthese_series)

    @rx.var
    def pnl_series_defs(self) -> list[dict]:
        return self._series_defs(self.pnl_series)

    @rx.var
    def cashflow_series_defs(self) -> list[dict]:
        return self._series_defs(self.cashflow_series)

    # Zoom controls
    def _clamp_zoom(self):
        s = max(1, min(self.zoom_start, self.months))
        e = max(1, min(self.zoom_end, self.months))
        if e < s:
            s, e = e, s
        self.zoom_start, self.zoom_end = s, e

    def zoom_set_start(self, v: str):
        self.zoom_start = int(float(v)) if v not in ("", None) else 1
        self._clamp_zoom()

    def zoom_set_end(self, v: str):
        self.zoom_end = int(float(v)) if v not in ("", None) else self.months
        self._clamp_zoom()

    def zoom_all(self):
        self.zoom_start, self.zoom_end = 1, self.months
        self._clamp_zoom()

    def zoom_3m(self): self.zoom_end = self.months; self.zoom_start = max(1, self.months-3+1); self._clamp_zoom()
    def zoom_6m(self): self.zoom_end = self.months; self.zoom_start = max(1, self.months-6+1); self._clamp_zoom()
    def zoom_12m(self): self.zoom_end = self.months; self.zoom_start = max(1, self.months-12+1); self._clamp_zoom()

    def _fmt2(self, x) -> str:
        """Format a number with 2 decimals, localized."""
        try:
            val = float(x)
        except Exception:
            return str(x)
        if self.language_code == "fr":
            # 12 345,67
            s = f"{val:,.2f}"           # '12,345.67'
            s = s.replace(",", "X")     # '12X345.67'
            s = s.replace(".", ",")     # '12X345,67'
            s = s.replace("X", " ")     # '12 345,67'
            return s
        else:
            # 12,345.67 (EN/other)
            return f"{val:,.2f}"
