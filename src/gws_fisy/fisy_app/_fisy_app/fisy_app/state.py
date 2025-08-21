
from typing import List
import reflex as rx
from gws_reflex_main import ReflexMainState

from .calc.models import (
    Config,
    Activity,
    Order,
    PersonnelLine,
    ChargeExterne,
    Investment,
    Loan,
    CapitalInjection,
    Subsidy,
)
from .calc.engine import compute_all
from .calc.sale_ranges import SaleRange, expand_sale_ranges_to_orders


class State(ReflexMainState):
    # --------- Global parameters ----------
    months: int = 36
    tva_default: float = 0.2
    start_year: int = 2025
    start_month: int = 1
    dso_days: int = 30
    dpo_days: int = 30
    dio_days: int = 0
    initial_cash: float = 0.0

    # Zoom (for charts / results)
    zoom_start: int = 1
    zoom_end:   int = 12

    # --------- User data ----------
    activities: List[Activity] = [
        Activity(name="Service", unit_price_ht=1000.0, vat_rate=0.2, variable_cost_per_unit_ht=300.0)
    ]
    orders: List[Order] = [Order(activity="Service", month_index=1, quantity=1.0)]
    sale_ranges: List[SaleRange] = [
        SaleRange(activity="Service", start_month=1, end_month=6, q0=10.0, growth=0.2, mode="cagr")
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

    # --------- Parse helpers ----------
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

    # --------- Zoom setters & presets ----------
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

    # --------- Update / Remove items ----------
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

    # --------- Add item actions ----------
    def add_activity(self):
        self.activities = [
            *self.activities,
            Activity(name="Nouvelle activité", unit_price_ht=0.0, vat_rate=0.2, variable_cost_per_unit_ht=0.0),
        ]

    def add_order(self):
        activity_name = self.activities[0].name if self.activities else "Service"
        self.orders = [*self.orders, Order(activity=activity_name, month_index=1, quantity=1.0)]

    def add_sale_range(self):
        activity_name = self.activities[0].name if self.activities else "Service"
        self.sale_ranges = [
            *self.sale_ranges,
            SaleRange(activity=activity_name, start_month=1, end_month=3, q0=1.0, growth=0.0, mode="linear"),
        ]

    def add_personnel(self):
        self.personnel = [
            *self.personnel,
            PersonnelLine(title="Nouveau poste", monthly_salary_gross=0.0, employer_cost_rate=0.45, start_month=1),
        ]

    def add_charge(self):
        self.charges = [
            *self.charges,
            ChargeExterne(label="Nouvelle charge", monthly_amount_ht=0.0, vat_rate=0.2, start_month=1),
        ]

    def add_investment(self):
        self.investments = [
            *self.investments,
            Investment(label="Nouveau matériel", amount_ht=0.0, vat_rate=0.2, purchase_month=1, amort_years=3),
        ]

    def add_loan(self):
        self.loans = [
            *self.loans,
            Loan(label="Nouveau prêt", principal=0.0, annual_rate=0.04, months=36, start_month=1),
        ]

    def add_capital(self):
        self.caps = [*self.caps, CapitalInjection(label="Apport", amount=0.0, month=1)]

    def add_subsidy(self):
        self.subsidies = [*self.subsidies, Subsidy(label="Subvention", amount=0.0, month=1)]

    # --------- Constellab params / labels ----------
    @rx.var
    def app_title(self) -> str:
        return self.get_param("app_title", "FISY — App")

    @rx.var
    def corporate_tax_rate(self) -> float:
        return float(self.get_param("corporate_tax_rate", 0.25))

    @rx.var
    def activity_options(self) -> list[str]:
        return [a.name for a in self.activities] if self.activities else []

    # --------- Internal config ----------
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

    # --------- Effective orders = manual + ranges ----------
    @rx.var
    def orders_effective(self) -> List[Order]:
        auto_orders = expand_sale_ranges_to_orders(self.sale_ranges, self.months, Order)
        return list(self.orders) + list(auto_orders)

    # --------- Compute helpers ----------
    def _dfs(self):
        return compute_all(
            self._cfg(), self.activities, self.orders_effective, self.personnel,
            self.charges, self.investments, self.loans, self.caps, self.subsidies
        )

    @rx.var
    def synthese_rows(self) -> List[dict]:
        return self._dfs()["synthese"].reset_index().to_dict(orient="records")

    @rx.var
    def pnl_rows(self) -> List[dict]:
        return self._dfs()["pnl"].reset_index().to_dict(orient="records")

    @rx.var
    def cashflow_rows(self) -> List[dict]:
        return self._dfs()["cashflow"].reset_index().to_dict(orient="records")

    @rx.var
    def plan_rows(self) -> List[dict]:
        return self._dfs()["plan_financement"].reset_index().rename(columns={"index": "Année"}).to_dict(orient="records")

    @rx.var
    def bilan_actif_rows(self) -> List[dict]:
        return self._dfs()["bilans"]["actif"].reset_index().to_dict(orient="records")

    @rx.var
    def bilan_passif_rows(self) -> List[dict]:
        return self._dfs()["bilans"]["passif"].reset_index().to_dict(orient="records")

    # --------- Columns ----------
    @rx.var
    def synthese_cols(self) -> list[str]:
        return list(self._dfs()["synthese"].reset_index().columns)

    @rx.var
    def pnl_cols(self) -> list[str]:
        return list(self._dfs()["pnl"].reset_index().columns)

    @rx.var
    def cashflow_cols(self) -> list[str]:
        return list(self._dfs()["cashflow"].reset_index().columns)

    @rx.var
    def plan_cols(self) -> list[str]:
        return list(self._dfs()["plan_financement"].reset_index().rename(columns={"index": "Année"}).columns)

    @rx.var
    def bilan_actif_cols(self) -> list[str]:
        return list(self._dfs()["bilans"]["actif"].reset_index().columns)

    @rx.var
    def bilan_passif_cols(self) -> list[str]:
        return list(self._dfs()["bilans"]["passif"].reset_index().columns)

    # --------- Chart data (respect zoom) ----------
    def _slice_rows(self, df):
        s, e = self.zoom_start, self.zoom_end
        s = max(1, min(s, len(df)))
        e = max(1, min(e, len(df)))
        if e < s:
            s, e = e, s
        return df.reset_index(drop=True).iloc[s-1:e].to_dict(orient="records")

    @rx.var
    def pnl_chart_rows(self) -> List[dict]:
        return self._slice_rows(self._dfs()["pnl"].reset_index())

    @rx.var
    def cashflow_chart_rows(self) -> List[dict]:
        return self._slice_rows(self._dfs()["cashflow"].reset_index())

    @rx.var
    def synthese_chart_rows(self) -> List[dict]:
        return self._slice_rows(self._dfs()["synthese"].reset_index())

    def _series_from_cols(self, cols):
        return [c for c in cols[1:5]] if len(cols) > 1 else []

    @rx.var
    def pnl_series(self) -> list[str]:
        return self._series_from_cols(self.pnl_cols)

    @rx.var
    def cashflow_series(self) -> list[str]:
        return self._series_from_cols(self.cashflow_cols)

    @rx.var
    def synthese_series(self) -> list[str]:
        return self._series_from_cols(self.synthese_cols)
