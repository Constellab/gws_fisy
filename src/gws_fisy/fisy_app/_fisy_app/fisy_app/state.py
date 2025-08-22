from typing import List
import reflex as rx
from gws_reflex_main import ReflexMainState
from .i18n import LANGS
from .calc.models import (
    Config, Activity, Order, PersonnelLine, ChargeExterne, Investment,
    Loan, CapitalInjection, Subsidy, OneTimeRange, SubscriptionRange
)
from .calc.engine import compute_all
from .calc.sale_ranges import (
    expand_one_time_ranges_to_orders, expand_subscription_ranges_to_orders
)

class State(ReflexMainState):
    # Horizon par défaut: 5 ans (60 mois)
    months: int = 60
    tva_default: float = 0.2
    start_year: int = 2025
    start_month: int = 1
    dso_days: int = 30
    dpo_days: int = 30
    dio_days: int = 0
    initial_cash: float = 0.0

    # i18n
    language_code: str = "fr"
    @rx.var
    def language_options(self) -> list[str]:
        return sorted(list(LANGS.keys()))
    def set_language_code(self, v: str):
        v = (v or "fr").lower()
        self.language_code = v if v in LANGS else "en"
    @rx.var
    def i18n(self) -> dict:
        return LANGS.get(self.language_code, LANGS.get("en", {}))

    # Monnaie & échelle
    currency_code: str = "EUR"
    scale_mode: str = "units"
    def set_currency_code(self, v: str): self.currency_code = (v or "EUR").upper()
    def set_scale_mode(self, v: str):
        v = (v or "units").lower()
        self.scale_mode = v if v in ("units","thousands","millions") else "units"
    @rx.var
    def currency_symbol(self) -> str:
        return {"EUR":"€","USD":"$","GBP":"£","CHF":"CHF","CAD":"$","AUD":"$","JPY":"¥"}.get(self.currency_code, self.currency_code)
    @rx.var
    def scale_div(self) -> float:
        return 1.0 if self.scale_mode=="units" else (1000.0 if self.scale_mode=="thousands" else 1_000_000.0)
    @rx.var
    def unit_suffix(self) -> str:
        tail = "" if self.scale_mode=="units" else ("k" if self.scale_mode=="thousands" else "M")
        return f"{self.currency_symbol}{tail}"

    # Zoom
    zoom_start: int = 1
    zoom_end: int = 12

    # Données
    activities: List[Activity] = [Activity(name="Service", unit_price_ht=1000.0, vat_rate=0.2, variable_cost_per_unit_ht=300.0)]
    one_time_ranges: List[OneTimeRange] = [OneTimeRange(activity="Service", start_month=1, end_month=3, q0=5.0, monthly_growth=0.0)]
    subscription_ranges: List[SubscriptionRange] = [SubscriptionRange(activity="Service", start_month=1, end_month=12, q0=10.0, monthly_growth=0.05)]
    personnel: List[PersonnelLine] = [PersonnelLine(title="Employé 1", monthly_salary_gross=3000.0, employer_cost_rate=0.45, start_month=1, end_month=999, count=1)]
    charges: List[ChargeExterne] = [ChargeExterne(label="Loyer", monthly_amount_ht=1200.0, vat_rate=0.2, start_month=1, end_month=999)]
    investments: List[Investment] = []
    loans: List[Loan] = []
    caps: List[CapitalInjection] = []
    subsidies: List[Subsidy] = []

    # Parsing helpers
    def _to_int(self, v: str, default: int = 0) -> int:
        try:
            if v in ("",None): return default
            return int(float(v))
        except Exception:
            return default
    def _to_float(self, v: str, default: float = 0.0) -> float:
        try:
            if v in ("",None): return default
            return float(v)
        except Exception:
            return default

    # Format 2 décimales (localisé)
    def _fmt2(self, x) -> str:
        try: val = float(x)
        except Exception: return str(x)
        if self.language_code == "fr":
            s = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ")
            return s
        return f"{val:,.2f}"

    # Setters anti-négatifs
    def set_int(self, field: str, v: str):
        val = self._to_int(v, 0)
        if "month" in field or "months" in field: val = max(1, val)
        else: val = max(0, val)
        setattr(self, field, val)
    def set_float(self, field: str, v: str):
        val = self._to_float(v, 0.0)
        if "month" in field or "months" in field: val = max(1.0, val)
        else: val = max(0.0, val)
        setattr(self, field, val)

    # MAJ listes dynamiques
    def update_item(self, list_name: str, index: int, field: str, v: str, kind: str="str"):
        lst = list(getattr(self, list_name, []))
        if not (0 <= index < len(lst)): return
        obj = lst[index]
        if kind == "int":
            newv = self._to_int(v, 0)
            newv = max(1, newv) if ("month" in field or "months" in field) else max(0, newv)
        elif kind == "float":
            newv = self._to_float(v, 0.0)
            newv = max(1.0, newv) if ("month" in field or "months" in field) else max(0.0, newv)
        else:
            newv = v or ""
        lst[index] = obj.model_copy(update={field: newv})
        setattr(self, list_name, lst)

    def remove_item(self, list_name: str, index: int):
        lst = list(getattr(self, list_name, []))
        if not (0 <= index < len(lst)): return
        del lst[index]
        setattr(self, list_name, lst)

    # Actions d'ajout
    def add_activity(self):
        self.activities = [*self.activities, Activity(name="Nouvelle activité", unit_price_ht=0.0, vat_rate=0.2, variable_cost_per_unit_ht=0.0)]
    def add_one_time(self):
        name = self.activities[0].name if self.activities else "Service"
        self.one_time_ranges = [*self.one_time_ranges, OneTimeRange(activity=name, start_month=1, end_month=3, q0=1.0, monthly_growth=0.0)]
    def add_subscription(self):
        name = self.activities[0].name if self.activities else "Service"
        self.subscription_ranges = [*self.subscription_ranges, SubscriptionRange(activity=name, start_month=1, end_month=12, q0=1.0, monthly_growth=0.0)]
    def add_personnel(self):
        self.personnel = [*self.personnel, PersonnelLine(title="Nouveau poste", monthly_salary_gross=0.0, employer_cost_rate=0.45, start_month=1, end_month=999, count=1)]
    def add_charge(self):
        self.charges = [*self.charges, ChargeExterne(label="Nouvelle charge", monthly_amount_ht=0.0, vat_rate=self.tva_default, start_month=1, end_month=999)]
    def add_investment(self):
        self.investments = [*self.investments, Investment(label="Nouveau matériel", amount_ht=0.0, vat_rate=self.tva_default, purchase_month=1, amort_years=3)]
    def add_loan(self):
        self.loans = [*self.loans, Loan(label="Nouveau prêt", principal=0.0, annual_rate=0.04, months=36, start_month=1)]
    def add_capital(self):
        self.caps = [*self.caps, CapitalInjection(label="Apport", amount=0.0, month=1)]
    def add_subsidy(self):
        self.subsidies = [*self.subsidies, Subsidy(label="Subvention", amount=0.0, month=1)]

    # Paramètres Constellab
    @rx.var
    def app_title(self) -> str:
        return self.get_param("app_title", self.i18n.get("app.title", "FISY — App"))
    @rx.var
    def corporate_tax_rate(self) -> float:
        return float(self.get_param("corporate_tax_rate", 0.25))

    @rx.var
    def activity_options(self) -> list[str]:
        return [a.name for a in self.activities] if self.activities else []

    # Config
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

    # Orders
    @rx.var
    def orders_one_time(self) -> List[Order]:
        return expand_one_time_ranges_to_orders(self.one_time_ranges, self.months, Order)
    @rx.var
    def orders_subscriptions(self) -> List[Order]:
        return expand_subscription_ranges_to_orders(self.subscription_ranges, self.months, Order)
    @rx.var
    def orders_effective(self) -> List[Order]:
        return list(self.orders_one_time) + list(self.orders_subscriptions)

    # Compute
    def _dfs(self):
        return compute_all(
            self._cfg(),
            self.activities,
            self.orders_effective,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
            subs_orders=self.orders_subscriptions
        )

    # Mise à l'échelle (tables)
    def _scaled_df_for_table(self, df, index_label: str = "Mois", exclude_cols=None):
        import pandas as pd
        exclude_cols = set(exclude_cols or [])
        df = df.reset_index()
        if "index" in df.columns:
            df = df.rename(columns={"index": index_label})
        div = float(self.scale_div)
        for c in df.columns:
            if c in ("Mois","Année"):
                continue
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c] / div
        new_cols = []
        for c in df.columns:
            if c in ("Mois","Année") or c in exclude_cols:
                new_cols.append(c)
            else:
                new_cols.append(f"{c} ({self.unit_suffix})")
        df.columns = new_cols
        for c in df.columns:
            if c in ("Mois","Année"): continue
            try:
                if pd.api.types.is_numeric_dtype(df[c]):
                    df[c] = df[c].map(self._fmt2)
            except Exception:
                pass
        return df

    # Mise à l'échelle (charts)
    def _scaled_df_for_chart(self, df):
        import pandas as pd
        df = df.reset_index()
        div = float(self.scale_div)
        for c in df.columns:
            if c == "index": continue
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c] / div
        return df

    # Mensuel -> Annuel
    def _monthly_to_annual(self, df):
        import pandas as pd
        df = df.copy().reset_index()
        if "index" not in df.columns:
            return df
        months = df["index"].astype(int)
        years = self.start_year + (self.start_month - 1 + (months - 1)) // 12
        df["Année"] = years
        num_cols = [c for c in df.columns if c not in ("index","Année")]
        out = df.groupby("Année", as_index=True)[num_cols].sum(numeric_only=True)
        return out

    # Tables (mensuel/annuel)
    @rx.var
    def synthese_rows_monthly(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["synthese"], index_label="Mois").to_dict(orient="records")
    @rx.var
    def pnl_rows_monthly(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["pnl"], index_label="Mois").to_dict(orient="records")
    @rx.var
    def cashflow_rows_monthly(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["cashflow"], index_label="Mois").to_dict(orient="records")
    @rx.var
    def plan_rows_annual(self) -> List[dict]:
        return self._scaled_df_for_table(self._dfs()["plan_financement"], index_label="Année", exclude_cols=["Année"]).to_dict(orient="records")

    @rx.var
    def synthese_rows_annual(self) -> List[dict]:
        return self._scaled_df_for_table(self._monthly_to_annual(self._dfs()["synthese"]), index_label="Année", exclude_cols=["Année"]).to_dict(orient="records")
    @rx.var
    def pnl_rows_annual(self) -> List[dict]:
        return self._scaled_df_for_table(self._monthly_to_annual(self._dfs()["pnl"]), index_label="Année", exclude_cols=["Année"]).to_dict(orient="records")
    @rx.var
    def cashflow_rows_annual(self) -> List[dict]:
        return self._scaled_df_for_table(self._monthly_to_annual(self._dfs()["cashflow"]), index_label="Année", exclude_cols=["Année"]).to_dict(orient="records")
    @rx.var
    def plan_rows_monthly(self) -> List[dict]:
        # Vue mensuelle simplifiée (placeholder)
        import pandas as pd
        out = pd.DataFrame({"Mois": list(range(1, self.months+1))})
        out["Apports+Subventions"] = 0.0
        out["Capex"] = 0.0
        out["Taxe"] = 0.0
        out["Variation Trésorerie"] = 0.0
        return self._scaled_df_for_table(out.set_index(pd.Index(range(1, self.months+1))), index_label="Mois").to_dict(orient="records")

    @rx.var
    def synthese_cols_monthly(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["synthese"], index_label="Mois").columns)
    @rx.var
    def pnl_cols_monthly(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["pnl"], index_label="Mois").columns)
    @rx.var
    def cashflow_cols_monthly(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["cashflow"], index_label="Mois").columns)
    @rx.var
    def plan_cols_annual(self) -> list[str]:
        return list(self._scaled_df_for_table(self._dfs()["plan_financement"], index_label="Année", exclude_cols=["Année"]).columns)
    @rx.var
    def synthese_cols_annual(self) -> list[str]:
        return list(self._scaled_df_for_table(self._monthly_to_annual(self._dfs()["synthese"]), index_label="Année", exclude_cols=["Année"]).columns)
    @rx.var
    def pnl_cols_annual(self) -> list[str]:
        return list(self._scaled_df_for_table(self._monthly_to_annual(self._dfs()["pnl"]), index_label="Année", exclude_cols=["Année"]).columns)
    @rx.var
    def cashflow_cols_annual(self) -> list[str]:
        return list(self._scaled_df_for_table(self._monthly_to_annual(self._dfs()["cashflow"]), index_label="Année", exclude_cols=["Année"]).columns)

    # Palette charts
    @rx.var
    def chart_palette(self) -> list[str]:
        return ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]

    # Quantités vendues (par activité)
    @rx.var
    def one_time_qty_chart_rows(self) -> List[dict]:
        import pandas as pd
        qty_by_act = self._dfs()["qty_by_activity"]
        acts = set([r.activity for r in self.one_time_ranges])
        idx = pd.Index(range(1, self.months+1), name="index")
        data = pd.DataFrame(index=idx)
        for a in acts:
            s = qty_by_act.get(a)
            if s is None: s = pd.Series(0.0, index=idx)
            data[a] = s
        return data.reset_index().to_dict(orient="records")

    @rx.var
    def subscription_qty_chart_rows(self) -> List[dict]:
        import pandas as pd
        qty_by_act = self._dfs()["qty_by_activity"]
        acts = set([r.activity for r in self.subscription_ranges])
        idx = pd.Index(range(1, self.months+1), name="index")
        data = pd.DataFrame(index=idx)
        for a in acts:
            s = qty_by_act.get(a)
            if s is None: s = pd.Series(0.0, index=idx)
            data[a] = s
        return data.reset_index().to_dict(orient="records")

    def _series_defs_from_acts(self, acts: List[str]) -> list[dict]:
        pal = self.chart_palette
        return [{"key": a, "color": pal[i % len(pal)], "unit": ""} for i, a in enumerate(acts or [])]

    @rx.var
    def one_time_qty_series_defs(self) -> list[dict]:
        return self._series_defs_from_acts([r.activity for r in self.one_time_ranges])
    @rx.var
    def subscription_qty_series_defs(self) -> list[dict]:
        return self._series_defs_from_acts([r.activity for r in self.subscription_ranges])

    # Zoom helpers
    def _clamp_zoom(self):
        s = max(1, min(self.zoom_start, self.months))
        e = max(1, min(self.zoom_end, self.months))
        if e < s: s, e = e, s
        self.zoom_start, self.zoom_end = s, e
    def zoom_set_start(self, v: str):
        try: self.zoom_start = int(float(v)) if v not in ("",None) else 1
        except Exception: self.zoom_start = 1
        self._clamp_zoom()
    def zoom_set_end(self, v: str):
        try: self.zoom_end = int(float(v)) if v not in ("",None) else self.months
        except Exception: self.zoom_end = self.months
        self._clamp_zoom()
    def zoom_all(self):
        self.zoom_start, self.zoom_end = 1, self.months; self._clamp_zoom()
    def zoom_3m(self):
        self.zoom_end = self.months; self.zoom_start = max(1, self.months-3+1); self._clamp_zoom()
    def zoom_6m(self):
        self.zoom_end = self.months; self.zoom_start = max(1, self.months-6+1); self._clamp_zoom()
    def zoom_12m(self):
        self.zoom_end = self.months; self.zoom_start = max(1, self.months-12+1); self._clamp_zoom()
