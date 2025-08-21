
from typing import List, Iterable, Dict, Tuple
from pydantic import BaseModel

class SaleRange(BaseModel):
    activity: str
    start_month: int  # >= 1
    end_month: int    # >= start_month
    q0: float         # quantity at start
    growth: float = 0.0  # total growth over the whole period (0.2 = +20%)
    mode: str = "cagr"   # "linear" or "cagr"

def _monthly_profile(n: int, q0: float, growth: float, mode: str) -> List[float]:
    if n <= 0:
        return []
    if n == 1:
        return [q0]
    qN = q0 * (1.0 + growth)
    if mode == "linear":
        slope = (qN - q0) / (n - 1)
        return [q0 + slope * t for t in range(n)]
    # CAGR default
    if q0 <= 0:
        slope = (qN - q0) / (n - 1)
        return [q0 + slope * t for t in range(n)]
    g = (qN / q0) ** (1.0 / (n - 1)) - 1.0
    return [q0 * ((1.0 + g) ** t) for t in range(n)]

def expand_sale_ranges_to_orders(
    ranges: Iterable[SaleRange], months: int, OrderCls
):
    acc: Dict[Tuple[str, int], float] = {}
    for r in ranges:
        start = max(1, int(r.start_month))
        end = min(int(r.end_month), int(months))
        if end < start:
            continue
        n = end - start + 1
        prof = _monthly_profile(n, float(r.q0), float(r.growth), r.mode)
        for t, q in enumerate(prof):
            m = start + t  # calendar month (1..months)
            acc[(r.activity, m)] = acc.get((r.activity, m), 0.0) + q
    out = [
        OrderCls(activity=a, month_index=m, quantity=round(q, 6))
        for (a, m), q in sorted(acc.items())
        if abs(q) > 1e-12
    ]
    return out
