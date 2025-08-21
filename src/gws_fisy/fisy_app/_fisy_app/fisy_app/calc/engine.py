from __future__ import annotations
from typing import List, Dict, Any
import math
import pandas as pd

from .models import (
    Config, Activity, Order, PersonnelLine, ChargeExterne,
    Investment, Loan, CapitalInjection, Subsidy,
)

def _zero_series(n: int) -> pd.Series:
    return pd.Series([0.0] * n, index=range(1, n + 1))

def _activity_map(activities: List[Activity]) -> Dict[str, Activity]:
    return {a.name: a for a in activities}

def _amort_schedule_annuity(principal: float, annual_rate: float, months: int):
    r = annual_rate / 12.0
    if months <= 0:
        return 0.0, [], [], []
    if r == 0:
        pmt = principal / months
    else:
        pmt = principal * (r / (1 - (1 + r) ** (-months)))
    bal = principal
    interests, principals, balances = [], [], []
    for _ in range(months):
        it = bal * r
        pr = pmt - it
        bal = max(0.0, bal - pr)
        interests.append(it)
        principals.append(pr)
        balances.append(bal)
    return pmt, interests, principals, balances

def _shift_month(idx: int, shift_days: int) -> int:
    if shift_days <= 0:
        return idx
    return idx + int((shift_days + 29) // 30)

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
    subs_orders: List[Order] | None = None,
) -> Dict[str, Any]:
    n = int(cfg.months)
    idx = range(1, n + 1)
    act_map = _activity_map(activities)

    revenue_ht = _zero_series(n)
    revenue_vat = _zero_series(n)
    var_costs_ht = _zero_series(n)

    def add_order(o: Order):
        if 1 <= o.month_index <= n and o.activity in act_map:
            a = act_map[o.activity]
            price_ht = float(a.unit_price_ht)
            vat_rate = float(a.vat_rate if a.vat_rate is not None else cfg.tva_default)
            rev = o.quantity * price_ht
            revenue_ht[o.month_index] += rev
            revenue_vat[o.month_index] += rev * vat_rate
            vc = o.quantity * float(a.variable_cost_per_unit_ht) + rev * float(a.variable_cost_rate_on_price)
            var_costs_ht[o.month_index] += vc

    for o in orders:
        add_order(o)

    mrr = _zero_series(n)
    if subs_orders:
        for o in subs_orders:
            if 1 <= o.month_index <= n and o.activity in act_map:
                a = act_map[o.activity]
                mrr[o.month_index] += o.quantity * float(a.unit_price_ht)

    staff_cost = _zero_series(n)
    for p in personnel:
        start = max(1, int(p.start_month))
        end = min(int(p.end_month), n)
        if end < start:
            continue
        monthly = float(p.monthly_salary_gross) * (1.0 + float(p.employer_cost_rate))
        staff_cost[start:end+1] += monthly

    ext_ht = _zero_series(n)
    ext_vat = _zero_series(n)
    for c in charges:
        start = max(1, int(c.start_month)); end = min(int(c.end_month), n)
        if end < start: continue
        amt = float(c.monthly_amount_ht)
        vat_rate = float(c.vat_rate if c.vat_rate is not None else cfg.tva_default)
        ext_ht[start:end+1] += amt
        ext_vat[start:end+1] += amt * vat_rate

    depreciation = _zero_series(n)
    invest_ht = _zero_series(n)
    invest_vat = _zero_series(n)
    for inv in investments:
        m = int(inv.purchase_month)
        if 1 <= m <= n:
            amt_ht = float(inv.amount_ht)
            invest_ht[m] += amt_ht
            invest_vat[m] += amt_ht * float(inv.vat_rate if inv.vat_rate is not None else cfg.tva_default)
            months_amort = max(1, int(inv.amort_years) * 12)
            end = min(n, m + months_amort - 1)
            depreciation[m:end+1] += amt_ht / months_amort

    loan_interest = _zero_series(n)
    loan_principal_out = _zero_series(n)
    loan_disb_in = _zero_series(n)
    for ln in loans:
        start = int(ln.start_month)
        principal = float(ln.principal); months = int(ln.months); r = float(ln.annual_rate)
        if principal <= 0 or months <= 0: continue
        pmt, interests, principals, _ = _amort_schedule_annuity(principal, r, months)
        if 1 <= start <= n: loan_disb_in[start] += principal
        for i, (it, pr) in enumerate(zip(interests, principals), start=0):
            m = start + i
            if 1 <= m <= n:
                loan_interest[m] += it
                loan_principal_out[m] += pr

    # cash movements
    def lag(series, days):
        out = _zero_series(n)
        for m in idx:
            mm = _shift_month(m, days)
            if 1 <= mm <= n:
                out[mm] += series[m]
        return out

    var_vat = var_costs_ht * float(cfg.tva_default)
    cash_in_customers = lag(revenue_ht + revenue_vat, cfg.dso_days)
    cash_out_suppliers = lag((var_costs_ht + var_vat) + (ext_ht + ext_vat), cfg.dpo_days)
    cash_out_capex = invest_ht + invest_vat
    cash_out_staff = staff_cost
    cash_in_loans = loan_disb_in
    cash_out_loans = loan_principal_out + loan_interest

    cash_in_caps = _zero_series(n)
    for c in caps:
        if 1 <= int(c.month) <= n:
            cash_in_caps[int(c.month)] += float(c.amount)
    cash_in_subs = _zero_series(n)
    for s in subsidies:
        if 1 <= int(s.month) <= n:
            cash_in_subs[int(s.month)] += float(s.amount)

    net_vat = revenue_vat - (ext_vat + invest_vat + var_vat)
    vat_settlement = _zero_series(n)
    for m in idx:
        if m+1 <= n:
            vat_settlement[m+1] += net_vat[m]

    gross_margin = revenue_ht - var_costs_ht
    ebit = gross_margin - ext_ht - staff_cost - depreciation
    ebt = ebit - loan_interest
    corporate_tax = ebt.apply(lambda x: x * cfg.corporate_tax_rate if x > 0 else 0.0)
    net_income = ebt - corporate_tax

    pnl = pd.DataFrame({
        "Chiffre d'affaires HT": revenue_ht,
        "Coûts variables HT": var_costs_ht,
        "Marge brute": gross_margin,
        "Charges externes HT": ext_ht,
        "Masse salariale": staff_cost,
        "Amortissements": depreciation,
        "EBIT": ebit,
        "Intérêts": loan_interest,
        "EBT": ebt,
        "IS": corporate_tax,
        "Résultat net": net_income,
    })

    cash_in = cash_in_customers + cash_in_loans + cash_in_caps + cash_in_subs
    cash_out = cash_out_suppliers + cash_out_capex + cash_out_staff + cash_out_loans + vat_settlement
    net_cash_flow = cash_in - cash_out

    cash_start = _zero_series(n); cash_end = _zero_series(n)
    cash_start[1] = float(cfg.initial_cash)
    cash_end[1] = cash_start[1] + net_cash_flow[1]
    for m in range(2, n+1):
        cash_start[m] = cash_end[m-1]
        cash_end[m] = cash_start[m] + net_cash_flow[m]

    cashflow = pd.DataFrame({
        "Cash début": cash_start,
        "Encaissements": cash_in,
        "Décaissements": cash_out,
        "Flux net": net_cash_flow,
        "Cash fin": cash_end,
    })

    synthese = pd.DataFrame({
        "CA HT": revenue_ht,
        "MRR": mrr,
        "Marge brute": gross_margin,
        "EBIT": ebit,
        "Résultat net": net_income,
        "Cash fin": cash_end,
    })

    def month_to_year(m: int) -> int:
        return cfg.start_year + ((m - 1 + (cfg.start_month - 1)) // 12)

    inv_ttc = invest_ht + invest_vat
    plan_df = pd.DataFrame({
        "Encaissements": cash_in,
        "Décaissements": cash_out,
        "Investissements": inv_ttc,
        "Emprunts reçus": cash_in_loans,
        "Remb. emprunts": loan_principal_out + loan_interest,
    })
    plan_df["Année"] = [month_to_year(m) for m in plan_df.index]
    plan_agg = plan_df.groupby("Année").sum(numeric_only=True)
    plan_agg["Var. Trésorerie"] = plan_agg["Encaissements"] - plan_agg["Décaissements"]

    cum_invest_ht = invest_ht.cumsum()
    cum_depr = depreciation.cumsum()
    fixed_assets_net = cum_invest_ht - cum_depr
    fixed_assets_net[fixed_assets_net < 0] = 0.0
    equity = net_income.cumsum()

    actif = pd.DataFrame({"Immobilisations nettes": fixed_assets_net, "Trésorerie": cash_end})
    actif["Total actif"] = actif.sum(axis=1)
    passif = pd.DataFrame({"Capitaux propres (cumul RN)": equity, "Dettes financières": _zero_series(n)})
    passif["Total passif"] = passif.sum(axis=1)

    return {
        "synthese": synthese,
        "pnl": pnl,
        "cashflow": cashflow,
        "plan_financement": plan_agg[["Encaissements", "Décaissements", "Investissements", "Emprunts reçus", "Remb. emprunts", "Var. Trésorerie"]],
        "bilans": {"actif": actif, "passif": passif},
    }
