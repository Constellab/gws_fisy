from typing import List, Type
from .models import OneTimeRange, SubscriptionRange, Order

def expand_one_time_ranges_to_orders(ranges: List[OneTimeRange], horizon: int, OrderCls: Type[Order]) -> List[Order]:
    orders: List[Order] = []
    for r in ranges or []:
        m0 = max(1, int(r.start_month))
        m1 = min(horizon, int(r.end_month))
        if m1 < m0:
            m0, m1 = m1, m0
        for m in range(m0, m1 + 1):
            k = m - m0
            q = float(r.q0) * ((1.0 + float(r.monthly_growth)) ** k)
            orders.append(OrderCls(activity=r.activity, month_index=m, quantity=q))
    return orders

def expand_subscription_ranges_to_orders(ranges: List[SubscriptionRange], horizon: int, OrderCls: Type[Order]) -> List[Order]:
    orders: List[Order] = []
    for r in ranges or []:
        m0 = max(1, int(r.start_month))
        m1 = min(horizon, int(r.end_month))
        if m1 < m0:
            m0, m1 = m1, m0
        for m in range(m0, m1 + 1):
            k = m - m0
            q = float(r.q0) * ((1.0 + float(r.monthly_growth)) ** k)
            orders.append(OrderCls(activity=r.activity, month_index=m, quantity=q))
    return orders
