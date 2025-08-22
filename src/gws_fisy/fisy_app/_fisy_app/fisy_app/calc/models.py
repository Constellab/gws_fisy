from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    months: int
    tva_default: float
    start_year: int
    start_month: int
    corporate_tax_rate: float
    dso_days: int
    dpo_days: int
    dio_days: int
    initial_cash: float

@dataclass
class Activity:
    name: str
    unit_price_ht: float
    vat_rate: float
    variable_cost_per_unit_ht: float = 0.0
    variable_cost_rate_on_price: float = 0.0

@dataclass
class Order:
    activity: str
    month_index: int
    quantity: float

@dataclass
class OneTimeRange:
    activity: str
    start_month: int
    end_month: int
    q0: float
    monthly_growth: float

@dataclass
class SubscriptionRange:
    activity: str
    start_month: int
    end_month: int
    q0: float
    monthly_growth: float

@dataclass
class PersonnelLine:
    title: str
    monthly_salary_gross: float
    employer_cost_rate: float
    start_month: int
    end_month: int = 999
    count: int = 1

@dataclass
class ChargeExterne:
    label: str
    monthly_amount_ht: float
    vat_rate: float
    start_month: int
    end_month: int = 999

@dataclass
class Investment:
    label: str
    amount_ht: float
    vat_rate: float
    purchase_month: int
    amort_years: int

@dataclass
class Loan:
    label: str
    principal: float
    annual_rate: float
    months: int
    start_month: int

@dataclass
class CapitalInjection:
    label: str
    amount: float
    month: int

@dataclass
class Subsidy:
    label: str
    amount: float
    month: int
