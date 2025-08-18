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


class State(ReflexMainState):
    # --------- paramètres généraux ----------
    months: int = 36
    tva_default: float = 0.2
    start_year: int = 2025
    start_month: int = 1
    dso_days: int = 30
    dpo_days: int = 30
    dio_days: int = 0
    initial_cash: float = 0.0

    # --------- données de saisie ----------
    activities: List[Activity] = [
        Activity(
            name="Service",
            unit_price_ht=1000.0,
            vat_rate=0.2,
            variable_cost_per_unit_ht=300.0,
        )
    ]
    orders: List[Order] = [Order(activity="Service", month_index=1, quantity=1.0)]
    personnel: List[PersonnelLine] = [
        PersonnelLine(
            title="Employé 1",
            monthly_salary_gross=3000.0,
            employer_cost_rate=0.45,
            start_month=1,
        )
    ]
    charges: List[ChargeExterne] = [
        ChargeExterne(label="Loyer", monthly_amount_ht=1200.0, vat_rate=0.2, start_month=1)
    ]
    investments: List[Investment] = []
    loans: List[Loan] = []
    caps: List[CapitalInjection] = []
    subsidies: List[Subsidy] = []

    # --------- helpers parsing pour <input> (Reflex 0.8.x envoie des strings) ----------
    def _to_int(self, v: str, default: int = 0) -> int:
        try:
            return int(float(v)) if v not in ("", None) else default
        except Exception:
            return default

    def _to_float(self, v: str, default: float = 0.0) -> float:
        try:
            return float(v) if v not in ("", None) else default
        except Exception:
            return default

    def set_int(self, field: str, v: str):
        """Setter générique pour champs int à partir d'une string d'input."""
        setattr(self, field, self._to_int(v))

    def set_float(self, field: str, v: str):
        """Setter générique pour champs float à partir d'une string d'input."""
        setattr(self, field, self._to_float(v))

    def update_item(self, list_name: str, index: int, field: str, v: str, kind: str = "str"):
        """MAJ d'un élément d'une liste de modèles (Pydantic) avec parsing côté serveur."""
        lst = list(getattr(self, list_name, []))
        if not (0 <= index < len(lst)):
            return
        obj = lst[index]
        try:
            if kind == "int":
                newv = self._to_int(v)
            elif kind == "float":
                newv = self._to_float(v)
            else:
                newv = v or ""
        except Exception:
            newv = 0 if kind == "int" else (0.0 if kind == "float" else "")
        lst[index] = obj.model_copy(update={field: newv})
        setattr(self, list_name, lst)

    # --------- wrappers spécifiques utilisés par pages.py ----------
    def set_months(self, v: str): self.set_int("months", v)
    def set_tva_default(self, v: str): self.set_float("tva_default", v)
    def set_dso_days(self, v: str): self.set_int("dso_days", v)
    def set_dpo_days(self, v: str): self.set_int("dpo_days", v)
    def set_dio_days(self, v: str): self.set_int("dio_days", v)
    def set_initial_cash(self, v: str): self.set_float("initial_cash", v)

    # --------- actions d'ajout (réassignation pour déclencher la MAJ) ----------
    def add_activity(self):
        self.activities = [
            *self.activities,
            Activity(
                name="Nouvelle activité",
                unit_price_ht=0.0,
                vat_rate=0.2,
                variable_cost_per_unit_ht=0.0,
            ),
        ]

    def add_order(self):
        name = self.activities[0].name if self.activities else "Service"
        self.orders = [*self.orders, Order(activity=name, month_index=1, quantity=1.0)]

    def add_personnel(self):
        self.personnel = [
            *self.personnel,
            PersonnelLine(
                title="Nouveau poste",
                monthly_salary_gross=0.0,
                employer_cost_rate=0.45,
                start_month=1,
            ),
        ]

    def add_charge(self):
        self.charges = [
            *self.charges,
            ChargeExterne(
                label="Nouvelle charge",
                monthly_amount_ht=0.0,
                vat_rate=0.2,
                start_month=1,
            ),
        ]

    def add_investment(self):
        self.investments = [
            *self.investments,
            Investment(
                label="Nouveau matériel",
                amount_ht=0.0,
                vat_rate=0.2,
                purchase_month=1,
                amort_years=3,
            ),
        ]

    def add_loan(self):
        self.loans = [
            *self.loans,
            Loan(
                label="Nouveau prêt",
                principal=0.0,
                annual_rate=0.04,
                months=36,
                start_month=1,
            ),
        ]

    def add_capital(self):
        self.caps = [*self.caps, CapitalInjection(label="Apport", amount=0.0, month=1)]

    def add_subsidy(self):
        self.subsidies = [*self.subsidies, Subsidy(label="Subvention", amount=0.0, month=1)]

    # --------- paramètres Constellab ----------
    @rx.var
    def app_title(self) -> str:
        return self.get_param("app_title", "FISY — App")

    @rx.var
    def corporate_tax_rate(self) -> float:
        return float(self.get_param("corporate_tax_rate", 0.25))

    # options de sélection (évite d'itérer un Var côté Python)
    @rx.var
    def activity_options(self) -> list[str]:
        return [a.name for a in self.activities] if self.activities else []

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

    # --------- vues calculées (rows) ----------
    @rx.var
    def synthese_rows(self) -> List[dict]:
        res = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )
        return res["synthese"].reset_index().to_dict(orient="records")

    @rx.var
    def pnl_rows(self) -> List[dict]:
        res = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )
        return res["pnl"].reset_index().to_dict(orient="records")

    @rx.var
    def cashflow_rows(self) -> List[dict]:
        res = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )
        return res["cashflow"].reset_index().to_dict(orient="records")

    @rx.var
    def plan_rows(self) -> List[dict]:
        res = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )
        return (
            res["plan_financement"]
            .reset_index()
            .rename(columns={"index": "Année"})
            .to_dict(orient="records")
        )

    @rx.var
    def bilan_actif_rows(self) -> List[dict]:
        res = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )
        return res["bilans"]["actif"].reset_index().to_dict(orient="records")

    @rx.var
    def bilan_passif_rows(self) -> List[dict]:
        res = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )
        return res["bilans"]["passif"].reset_index().to_dict(orient="records")

    # --------- listes de colonnes (pour rendu table réactif) ----------
    @rx.var
    def synthese_cols(self) -> list[str]:
        df = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )["synthese"].reset_index()
        return list(df.columns)

    @rx.var
    def pnl_cols(self) -> list[str]:
        df = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )["pnl"].reset_index()
        return list(df.columns)

    @rx.var
    def cashflow_cols(self) -> list[str]:
        df = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )["cashflow"].reset_index()
        return list(df.columns)

    @rx.var
    def plan_cols(self) -> list[str]:
        df = (
            compute_all(
                self._cfg(),
                self.activities,
                self.orders,
                self.personnel,
                self.charges,
                self.investments,
                self.loans,
                self.caps,
                self.subsidies,
            )["plan_financement"]
            .reset_index()
            .rename(columns={"index": "Année"})
        )
        return list(df.columns)

    @rx.var
    def bilan_actif_cols(self) -> list[str]:
        df = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )["bilans"]["actif"].reset_index()
        return list(df.columns)

    @rx.var
    def bilan_passif_cols(self) -> list[str]:
        df = compute_all(
            self._cfg(),
            self.activities,
            self.orders,
            self.personnel,
            self.charges,
            self.investments,
            self.loans,
            self.caps,
            self.subsidies,
        )["bilans"]["passif"].reset_index()
        return list(df.columns)
