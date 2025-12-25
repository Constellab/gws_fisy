from typing import Dict, List

import pandas as pd

from .models import (
    Activity,
    CapitalInjection,
    ChargeExterne,
    Config,
    Investment,
    Loan,
    Order,
    PersonnelLine,
    Subsidy,
)


def _idx_months(cfg: Config) -> pd.Index:
    return pd.Index(range(1, cfg.months + 1), name="index")

def _activities_map(activities: List[Activity]) -> Dict[str, Activity]:
    return {a.name: a for a in (activities or [])}

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
    subs_orders: List[Order] = None,
):
    idx = _idx_months(cfg)
    act_map = _activities_map(activities)

    # ----- Revenues & variable costs -----
    rev = pd.Series(0.0, index=idx)
    var_cost = pd.Series(0.0, index=idx)
    vat_sales = pd.Series(0.0, index=idx)
    qty_by_act = {}
    qty_by_act_one_time = {}
    qty_by_act_subscription = {}

    # Process one-time orders
    if orders:
        for o in orders:
            a = act_map.get(o.activity)
            if a is None:
                continue
            m = int(o.month_index)
            if m not in idx:
                continue
            q = float(o.quantity)
            p = float(a.unit_price_ht)
            rev[m] += q * p
            var_cost[m] += q * (float(a.variable_cost_per_unit_ht) + float(a.variable_cost_rate_on_price) * p)
            vat_sales[m] += q * p * float(a.vat_rate)
            qty_by_act.setdefault(a.name, pd.Series(0.0, index=idx))
            qty_by_act[a.name][m] += q
            qty_by_act_one_time.setdefault(a.name, pd.Series(0.0, index=idx))
            qty_by_act_one_time[a.name][m] += q

    # Process subscription orders
    if subs_orders:
        for o in subs_orders:
            a = act_map.get(o.activity)
            if a is None:
                continue
            m = int(o.month_index)
            if m not in idx:
                continue
            q = float(o.quantity)
            p = float(a.unit_price_ht)
            rev[m] += q * p
            var_cost[m] += q * (float(a.variable_cost_per_unit_ht) + float(a.variable_cost_rate_on_price) * p)
            vat_sales[m] += q * p * float(a.vat_rate)
            qty_by_act.setdefault(a.name, pd.Series(0.0, index=idx))
            qty_by_act[a.name][m] += q
            qty_by_act_subscription.setdefault(a.name, pd.Series(0.0, index=idx))
            qty_by_act_subscription[a.name][m] += q

    # ----- Personnel -----
    pers = pd.Series(0.0, index=idx)
    for p in personnel or []:
        sm = max(1, int(p.start_month))
        em = min(cfg.months, int(p.end_month))
        if em < sm:
            sm, em = em, sm
        monthly = float(p.monthly_salary_gross) * (1.0 + float(p.employer_cost_rate)) * max(1, int(p.count or 1))
        pers.loc[sm:em] += monthly

    # ----- External charges -----
    chg = pd.Series(0.0, index=idx)
    vat_purchases = pd.Series(0.0, index=idx)
    for c in charges or []:
        sm = max(1, int(c.start_month))
        em = min(cfg.months, int(c.end_month))
        if em < sm:
            sm, em = em, sm
        chg.loc[sm:em] += float(c.monthly_amount_ht)
        vat_purchases.loc[sm:em] += float(c.monthly_amount_ht) * float(c.vat_rate)

    # ----- Investments & depreciation -----
    dep = pd.Series(0.0, index=idx)
    capex = pd.Series(0.0, index=idx)
    for inv in investments or []:
        pm = max(1, min(cfg.months, int(inv.purchase_month)))
        capex[pm] += float(inv.amount_ht)
        months = max(1, int(inv.amort_years) * 12)
        monthly_dep = float(inv.amount_ht) / months
        dep.loc[pm:cfg.months] += monthly_dep
        vat_purchases[pm] += float(inv.amount_ht) * float(inv.vat_rate)

    # ----- Simple financing flows -----
    fin_in = pd.Series(0.0, index=idx)
    for cap in caps or []:
        m = max(1, min(cfg.months, int(cap.month)))
        fin_in[m] += float(cap.amount)
    for sub in subsidies or []:
        m = max(1, min(cfg.months, int(sub.month)))
        fin_in[m] += float(sub.amount)

    # ----- P&L -----
    ebitda = rev - var_cost - pers - chg
    ebit = ebitda - dep
    tax = (ebit.clip(lower=0.0)) * float(cfg.corporate_tax_rate)
    net = ebit - tax

    # ----- Cashflow (simplifié) -----
    op_cf = ebitda - tax
    inv_cf = -capex
    fin_cf = fin_in
    cash = pd.Series(0.0, index=idx)
    cash.iloc[0] = float(cfg.initial_cash) + op_cf.iloc[0] + inv_cf.iloc[0] + fin_cf.iloc[0]
    for i in range(1, len(idx)):
        cash.iloc[i] = cash.iloc[i-1] + op_cf.iloc[i] + inv_cf.iloc[i] + fin_cf.iloc[i]

    # ----- RR (Recurring Revenue) -----
    rr = pd.Series(0.0, index=idx)
    if subs_orders:
        for o in subs_orders:
            a = act_map.get(o.activity)
            if a is None: continue
            m = int(o.month_index)
            if m in idx:
                q = float(o.quantity)
                rr[m] += q * float(a.unit_price_ht)

    # ----- DataFrames -----
    synthese = pd.DataFrame({
        "Revenue HT": rev,
        "Variable costs HT": var_cost,
        "Gross margin HT": rev - var_cost,
        "Personnel costs": pers,
        "External charges": chg,
        "EBITDA": ebitda,
        "Depreciation": dep,
        "EBIT": ebit,
        "Corporate tax": tax,
        "Net income": net,
        "RR": rr
    })

    pnl = pd.DataFrame({
        "Revenues": rev,
        "Variable costs": var_cost,
        "Gross profit": rev - var_cost,
        "Personnel": pers,
        "External charges": chg,
        "EBITDA": ebitda,
        "Depreciation": dep,
        "EBIT": ebit,
        "Tax": tax,
        "Net income": net
    })

    cashflow = pd.DataFrame({
        "Operating CF": op_cf,
        "Investing CF": inv_cf,
        "Financing CF": fin_cf,
        "Cash end": cash
    })

    # Funding plan (annual)
    years = []
    for m in idx:
        year = cfg.start_year + (cfg.start_month - 1 + (m - 1)) // 12
        years.append(year)
    df_plan = pd.DataFrame({
        "Year": years,
        "Capital+Subsidies": fin_in,
        "Capex": capex,
        "Tax": tax,
        "Cash variation": op_cf + inv_cf + fin_cf
    })
    plan_financement = df_plan.groupby("Year", as_index=True).sum(numeric_only=True)

    # Simplified balance sheets
    actif = pd.DataFrame({
        "Cash": cash,
        "Net fixed assets": (capex.cumsum() - dep.cumsum()).clip(lower=0.0)
    })
    passif = pd.DataFrame({
        "Equity (approx)": (net).cumsum() + float(cfg.initial_cash) + (fin_in).cumsum(),
        "Liabilities (placeholder)": pd.Series(0.0, index=idx)
    })

    return {
        "synthese": synthese,
        "pnl": pnl,
        "cashflow": cashflow,
        "plan_financement": plan_financement,
        "bilans": {"actif": actif, "passif": passif},
        "qty_by_activity": qty_by_act,
        "qty_by_activity_one_time": qty_by_act_one_time,
        "qty_by_activity_subscription": qty_by_act_subscription
    }
