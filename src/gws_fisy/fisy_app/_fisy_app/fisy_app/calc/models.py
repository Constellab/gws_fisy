from typing import Optional
from pydantic import BaseModel, Field

class Config(BaseModel):
    months: int = 36
    tva_default: float = 0.2
    start_year: int = 2025
    start_month: int = 1
    corporate_tax_rate: float = 0.25
    dso_days: int = 30
    dpo_days: int = 30
    dio_days: int = 0
    initial_cash: float = 0.0

class Activity(BaseModel):
    name: str
    unit_price_ht: float = 0.0
    vat_rate: float = 0.2
    variable_cost_per_unit_ht: float = 0.0
    variable_cost_rate_on_price: float = 0.0

class Order(BaseModel):
    activity: str
    month_index: int
    quantity: float

class PersonnelLine(BaseModel):
    title: str
    monthly_salary_gross: float = 0.0
    employer_cost_rate: float = 0.45
    start_month: int = 1
    end_month: int = 999

class ChargeExterne(BaseModel):
    label: str
    monthly_amount_ht: float = 0.0
    vat_rate: float = 0.2
    start_month: int = 1
    end_month: int = 999

class Investment(BaseModel):
    label: str
    amount_ht: float = 0.0
    vat_rate: float = 0.2
    purchase_month: int = 1
    amort_years: int = 3

class Loan(BaseModel):
    label: str
    principal: float = 0.0
    annual_rate: float = 0.04
    months: int = 36
    start_month: int = 1

class CapitalInjection(BaseModel):
    label: str
    amount: float = 0.0
    month: int = 1

class Subsidy(BaseModel):
    label: str
    amount: float = 0.0
    month: int = 1
