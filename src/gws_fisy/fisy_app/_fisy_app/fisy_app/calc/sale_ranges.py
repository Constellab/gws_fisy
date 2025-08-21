
from typing import List, Iterable, Dict, Tuple
from pydantic import BaseModel

class OneTimeRange(BaseModel):
    activity: str
    start_month: int
    end_month: int
    q0: float                      # starting quantity in start_month
    monthly_growth: float = 0.0    # per-month growth rate (e.g., 0.05 = +5%/mo)

class SubscriptionRange(BaseModel):
    activity: str
    start_month: int
    end_month: int
    q0: float                      # active subscriptions at start_month
    monthly_growth: float = 0.0    # per-month growth on active subs

def _profile_cagr(n: int, q0: float, g: float) -> List[float]:
    if n <= 0:
        return []
    return [q0 * ((1.0 + g) ** t) for t in range(n)]

def expand_one_time_ranges_to_orders(ranges: Iterable[OneTimeRange], months: int, OrderCls):
    acc: Dict[Tuple[str, int], float] = {}
    for r in ranges:
        start = max(1, int(r.start_month))
        end = min(int(r.end_month), int(months))
        if end < start:
            continue
        prof = _profile_cagr(end - start + 1, float(r.q0), float(r.monthly_growth))
        for t, q in enumerate(prof):
            m = start + t
            acc[(r.activity, m)] = acc.get((r.activity, m), 0.0) + q
    return [
        OrderCls(activity=a, month_index=m, quantity=round(q, 6))
        for (a, m), q in sorted(acc.items())
        if abs(q) > 1e-12
    ]

def expand_subscription_ranges_to_orders(ranges: Iterable[SubscriptionRange], months: int, OrderCls):
    acc: Dict[Tuple[str, int], float] = {}
    for r in ranges:
        start = max(1, int(r.start_month))
        end = min(int(r.end_month), int(months))
        if end < start:
            continue
        prof = _profile_cagr(end - start + 1, float(r.q0), float(r.monthly_growth))
        for t, q in enumerate(prof):
            m = start + t
            acc[(r.activity, m)] = acc.get((r.activity, m), 0.0) + q
    return [
        OrderCls(activity=a, month_index=m, quantity=round(q, 6))
        for (a, m), q in sorted(acc.items())
        if abs(q) > 1e-12
    ]
