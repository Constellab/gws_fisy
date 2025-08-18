import numpy as np
import pandas as pd
from typing import Dict, Any, List

from .models import (
    Config, Activity, Order, PersonnelLine, ChargeExterne, Investment,
    Loan, CapitalInjection, Subsidy
)

def _series(months: int, val: float = 0.0) -> pd.Series:
    return pd.Series(float(val), index=pd.RangeIndex(1, months + 1), dtype="float64")

def _annuity_payment(P: float, r_month: float, n: int) -> float:
    if n <= 0:
        return 0.0
    if r_month == 0:
        return P / n
    return P * r_month / (1 - (1 + r_month) ** (-n))

def compute_all(
    cfg: Config,
    activities: List[Activity],
    orders: List[Order],
    personnel: List[PersonnelLine],
    charges: List[ChargeExterne],
    investments: List[Investment],
    loans: List[Loan],
    caps: List[CapitalInjection],
    subsidies: List[Subsidy],
) -> Dict[str, Any]:
    m = cfg.months
    idx = pd.RangeIndex(1, m + 1)
    zero = _series(m, 0.0)

    price_map = {a.name: a.unit_price_ht for a in activities}
    vat_map = {a.name: a.vat_rate for a in activities}
    var_cost_unit = {a.name: a.variable_cost_per_unit_ht for a in activities}
    var_cost_rate = {a.name: a.variable_cost_rate_on_price for a in activities}

    revenue_ht = zero.copy()
    vat_collected = zero.copy()
    variable_costs_ht = zero.copy()
    for o in orders:
        if 1 <= o.month_index <= m and o.activity in price_map:
            p = price_map[o.activity]; q = o.quantity
            revenue_ht.iloc[o.month_index - 1] += p * q
            vat_collected.iloc[o.month_index - 1] += p * q * vat_map.get(o.activity, cfg.tva_default)
            rate = var_cost_rate.get(o.activity, 0.0)
            if rate and rate > 0:
                variable_costs_ht.iloc[o.month_index - 1] += p * q * rate
            else:
                variable_costs_ht.iloc[o.month_index - 1] += var_cost_unit.get(o.activity, 0.0) * q

    personnel_costs = zero.copy()
    for p in personnel:
        start = max(1, p.start_month); end = min(m, p.end_month)
        monthly = p.monthly_salary_gross * (1 + p.employer_cost_rate)
        if start <= end:
            personnel_costs.iloc[start - 1:end] += monthly

    ext_charges_ht = zero.copy()
    vat_deductible = zero.copy()
    for c in charges:
        start = max(1, c.start_month); end = min(m, c.end_month)
        if start <= end:
            ext_charges_ht.iloc[start - 1:end] += c.monthly_amount_ht
            vat_deductible.iloc[start - 1:end] += c.monthly_amount_ht * c.vat_rate

    amort = zero.copy()
    inv_cash_ttc = zero.copy()
    fixed_gross = zero.copy()
    for inv in investments:
        pm = min(max(1, inv.purchase_month), m)
        fixed_gross.iloc[pm - 1:] += inv.amount_ht
        inv_cash_ttc.iloc[pm - 1] += inv.amount_ht * (1 + inv.vat_rate)
        vat_deductible.iloc[pm - 1] += inv.amount_ht * inv.vat_rate
        months_amort = max(1, inv.amort_years * 12)
        monthly_dep = inv.amount_ht / months_amort
        end = min(m, pm - 1 + months_amort)
        amort.iloc[pm - 1:end] += monthly_dep

    loan_inflow = zero.copy()
    loan_payment = zero.copy()
    loan_interest = zero.copy()
    loan_outstanding = zero.copy()
    for loan in loans:
        sm = min(max(1, loan.start_month), m)
        n = min(loan.months, m - sm + 1)
        r = loan.annual_rate / 12.0
        A = _annuity_payment(loan.principal, r, n)
        if n <= 0:
            continue
        loan_inflow.iloc[sm - 1] += loan.principal
        outstanding = loan.principal
        for k in range(n):
            t = sm - 1 + k
            if t >= m: break
            interest = outstanding * r
            principal = max(0.0, A - interest)
            outstanding = max(0.0, outstanding - principal)
            loan_payment.iloc[t] += A
            loan_interest.iloc[t] += interest
            loan_outstanding.iloc[t] += outstanding

    cap_inflow = zero.copy()
    for c in caps:
        mo = min(max(1, c.month), m)
        cap_inflow.iloc[mo - 1] += c.amount
    subsidy_inflow = zero.copy()
    for s in subsidies:
        mo = min(max(1, s.month), m)
        subsidy_inflow.iloc[mo - 1] += s.amount

    ebitda = revenue_ht - variable_costs_ht - personnel_costs - ext_charges_ht
    ebit = ebitda - amort
    ebt = ebit - loan_interest
    taxes_is = ebt.clip(lower=0) * cfg.corporate_tax_rate

    net_vat = vat_collected - vat_deductible
    vat_balance = zero.copy()
    vat_cash = zero.copy()
    bal = 0.0
    for t in range(m):
        bal += net_vat.iloc[t]
        pay = max(0.0, bal)
        if t + 1 < m:
            vat_cash.iloc[t + 1] += pay
        else:
            vat_cash.iloc[t] += pay
        bal -= pay
        vat_balance.iloc[t] = bal

    def shift_series(ht, months_shift):
        shifted = zero.copy()
        for i in range(1, m + 1):
            j = i + months_shift
            if 1 <= j <= m:
                shifted.iloc[j - 1] += ht.iloc[i - 1]
        return shifted

    dso_m = max(0, int(round(cfg.dso_days / 30.0)))
    dpo_m = max(0, int(round(cfg.dpo_days / 30.0)))

    cash_in_sales = shift_series(revenue_ht + vat_collected, dso_m)
    purchases_ht = variable_costs_ht + ext_charges_ht
    cash_out_suppliers = shift_series(purchases_ht, dpo_m)

    cash_out_personnel = personnel_costs.copy()
    cash_out_invest = inv_cash_ttc.copy()
    cash_out_tax = taxes_is.copy()

    cash_inflows = cash_in_sales + cap_inflow + subsidy_inflow + loan_inflow
    cash_outflows = cash_out_suppliers + cash_out_personnel + loan_payment + cash_out_invest + cash_out_tax + vat_cash
    cash_variation = cash_inflows - cash_outflows
    cash = cash_variation.cumsum() + cfg.initial_cash

    pnl = pd.DataFrame({
        "CA (HT)": revenue_ht,
        "Variab. (HT)": -variable_costs_ht,
        "Perso": -personnel_costs,
        "Charges externes (HT)": -ext_charges_ht,
        "EBITDA": ebitda,
        "Amortissements": -amort,
        "EBIT": ebit,
        "Intérêts": -loan_interest,
        "EBT": ebt,
        "Impôt (IS)": -taxes_is,
        "Résultat net": ebt - taxes_is,
    }, index=idx)

    cashflow = pd.DataFrame({
        "Encaissements ventes (TTC, décalées)": cash_in_sales,
        "Apports en capital": cap_inflow,
        "Subventions": subsidy_inflow,
        "Décaissements fournisseurs (HT)": -cash_out_suppliers,
        "Personnel": -cash_out_personnel,
        "Remboursements prêts (annuités)": -loan_payment,
        "Investissements (TTC)": -cash_out_invest,
        "Impôts": -cash_out_tax,
        "TVA (paiement net)": -vat_cash,
        "Variation de trésorerie": cash_variation,
        "Trésorerie": cash,
    }, index=idx)

    by_year = lambda s: s.groupby(((s.index - 1) // 12) + 1).sum()
    plan_fin = pd.DataFrame({
        "Ressources": by_year(cash_in_sales + cap_inflow + subsidy_inflow + loan_inflow),
        "Emplois": by_year(cash_out_suppliers + cash_out_personnel + loan_payment + cash_out_invest + cash_out_tax + vat_cash),
    })

    depcum = (pnl["Amortissements"] * -1).cumsum()
    fixed_net = fixed_gross.cumsum() - depcum
    ca_ttc = revenue_ht + vat_collected
    receivables = (ca_ttc.cumsum() - cash_in_sales.cumsum()).clip(lower=0)
    payables = (purchases_ht.cumsum() - cash_out_suppliers.cumsum()).clip(lower=0)
    retained = (pnl["Résultat net"]).cumsum()
    equity = cap_inflow.cumsum() + retained

    assets = pd.DataFrame({
        "Immobilisations nettes": fixed_net,
        "Créances clients (TTC)": receivables,
        "Trésorerie": cash,
    }, index=idx)
    liabilities = pd.DataFrame({
        "Capitaux propres": equity,
        "Dettes financières": loan_outstanding,
        "Dettes fournisseurs (HT)": payables,
        "TVA nette à payer (+) / crédit (-)": vat_balance,
    }, index=idx)

    bilans = {"actif": assets, "passif": liabilities}

    synthese = pd.DataFrame({
        "CA cumulé (HT)": revenue_ht.cumsum(),
        "EBITDA cumulé": ebitda.cumsum(),
        "Résultat net cumulé": (pnl["Résultat net"]).cumsum(),
        "Trésorerie": cash,
    }, index=idx)

    return {"pnl": pnl, "cashflow": cashflow, "plan_financement": plan_fin, "bilans": bilans, "synthese": synthese}
