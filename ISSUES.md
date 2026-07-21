# gws_fisy — Issues Backlog

> Source of truth for product scope and issue backlog. Read and updated by
> gws-issue-define, gws-issue-spec, gws-issue-implement, gws-issue-sync,
> gws-issue-refactor.

## Context
- **What it does:** A Reflex web app where a founder inputs business assumptions (revenue, payroll, opex, capex, financing) and gets an auto-generated multi-year financial forecast — P&L, balance sheet, cash flow, funding plan, French tax computations, and break-even/ratio analysis — with progressively richer sophistication across three tiers: STARTER (no finance background needed), ESSENTIEL (full config-driven 5-year forecasting engine with French statutory taxes), and INNOVATION (adds R&D tax-incentive modeling: JEI status, CIR/CII/CICE tax credits).
- **Who it's for:** French startup founders across a sophistication spectrum — pre-seed founders with no finance background (STARTER), early-stage founders/accountants needing a bankable forecast (ESSENTIEL), and deep-tech/R&D founders or their tax consultants needing R&D tax-credit modeling (INNOVATION).
- **Repository:** bricks/gws_fisy/ (Constellab brick, Reflex web app) — GitHub: https://github.com/Constellab/gws_fisy
- **Reference prefix:** FISY (issue refs are `FISY-NNN`)
- **Non-goals / out of scope (for this pass):**
  - Configurable/versioned tax law — current French statutory rates/thresholds are hardcoded for v1; no support for multiple simultaneous tax years or historical rate changes.
  - Spreadsheet-style hard caps (max activities, max named financing sources, etc.) — deliberately rejected; the app allows unlimited entries where the source spreadsheets capped them for column-count reasons only.
  - PDF/formatted business-plan document export — v1 export is CSV/Excel data export only.
  - Tier-downgrade (ESSENTIEL/INNOVATION → STARTER) — only upgrade is in scope.
- **Key design decisions locked in during definition:**
  - Tier (STARTER/ESSENTIEL/INNOVATION) is chosen per project at creation and is upgradeable later with data carried over (not a fixed, non-upgradeable choice; not a single always-full model).
  - No caps on activities, financing sources, etc. — unlimited by default.
  - Forecast granularity is monthly throughout the full 5-year horizon for every tier (not the source spreadsheets' degressive monthly→quarterly→semestrial schedule).
  - Investment amortization duration is always user-set per line (defaulting to 5 years), even for STARTER-tier projects — one consistent data model across tiers.
- **Source material:** derived from `bricks/gws_fisy/specs/FISY-STARTER.xls`, `FISY-ESSENTIEL.xlsx`, `FISY-INNOVATION.xlsx` (the original French FISY spreadsheet tool by Remi BERTHIER, fisy.fr)

## Domains

### D1. Assumptions & Configuration
Company setup, per-activity revenue/cost model, payment terms, default cost templates, payroll rates, VAT rates, loan terms, and tier/mode selection (STARTER/ESSENTIEL/INNOVATION).

**Features**
- F1.1 Project setup & tier selection — create a project with a start date and initial tier
- F1.2 Activity/business-line management — add/edit/remove revenue-generating activities, unlimited
- F1.3 Per-activity revenue model config — unit price, delivery lag, payment terms, price escalation
- F1.4 Per-activity cost model config — unit variable cost, delivery/payment lag
- F1.5 Recurring revenue contract config (INNOVATION) — monthly recurring amount + contract duration
- F1.6 Default overhead cost category templates — pre-populated, editable external-charge lines
- F1.7 Payroll burden configuration — burden rate(s), SMIC reference
- F1.8 VAT rate configuration — per-activity and generic rates
- F1.9 Financing sources & terms configuration — capital, debt, subsidies, current accounts, advances
- F1.10 Tier upgrade — carry data forward when upgrading a project to a higher tier

### D2. Revenue & Order Management
Order volume forecasting, multi-activity/business-line support, cash-vs-accrual revenue timing, recurring revenue (INNOVATION), price escalation.

**Features**
- F2.1 Order volume forecasting per activity
- F2.2 Revenue/cost calculation from orders × unit price/cost
- F2.3 Cash-vs-accrual revenue split using payment-timing config
- F2.4 Recurring revenue calculation (INNOVATION)
- F2.5 Fixed-vs-recurring revenue reporting (INNOVATION)

### D3. Personnel & Payroll Planning
Headcount/salary planning, ETP calculation, payroll burden, R&D time-allocation tagging (INNOVATION).

**Features**
- F3.1 Headcount & salary planning per role
- F3.2 ETP (FTE) calculation
- F3.3 Payroll burden calculation
- F3.4 R&D time-allocation tagging (INNOVATION)
- F3.5 Activity time-allocation (INNOVATION)

### D4. Operating Costs & Investments
External charges, capex/depreciation, leasing (crédit-bail), subcontracting with R&D-eligibility tagging (INNOVATION).

**Features**
- F4.1 External charges management
- F4.2 CapEx/investment tracking with per-line depreciation
- F4.3 Leasing (crédit-bail) handling
- F4.4 In-kind capital contributions (apports en nature)
- F4.5 Subcontracting tracking with R&D-eligibility tagging (INNOVATION)
- F4.6 Per-activity/R&D-usage allocation for capex & subcontracting (INNOVATION)

### D5. Financing & Cash Flow
Funding plan (equity, debt, subsidies, current accounts, incubator advances) and monthly treasury/cash-flow statement.

**Features**
- F5.1 Basic debt repayment & net debt tracking
- F5.2 Detailed loan amortization schedule
- F5.3 Sources-and-uses funding plan
- F5.4 Monthly cash-flow statement (core lines)
- F5.5 Extended cash-flow lines (VAT, R&D credits, subcontracting, de-minimis)

### D6. Tax & Compliance Engine
VAT, corporate income tax (IS), statutory payroll/business taxes, R&D tax credits (JEI/CIR/CII/CICE) (INNOVATION).

**Features**
- F6.1 VAT (TVA) engine
- F6.2 Corporate income tax (IS) computation
- F6.3 Statutory payroll/business taxes (taxe d'apprentissage, formation continue, effort de construction, C3S, CFE, CVAE)
- F6.4 JEI eligibility & exemption engine (INNOVATION)
- F6.5 CIR/CII/CICE R&D tax-credit computation (INNOVATION)
- F6.6 EU de-minimis state-aid ceiling tracking (INNOVATION)

### D7. Financial Statements & Reporting
P&L, balance sheet, working capital (BFR), synthesis dashboard, break-even/ratios.

**Features**
- F7.1 Break-even & ratios dashboard (base level)
- F7.2 Full P&L statement
- F7.3 Balance sheet
- F7.4 Working capital requirement (BFR)
- F7.5 Break-even split with/without state aid (INNOVATION)
- F7.6 Per-activity profitability & funding-need analytics (INNOVATION)
- F7.7 Forecast charts (results, treasury/BFR)

### D8. Actuals Tracking & Export
Forecast-vs-actual "Pilotage" tracking, business-plan export.

**Features**
- F8.1 Actuals entry
- F8.2 Forecast-vs-actual variance tracking
- F8.3 Custom KPI tracking
- F8.4 Business-plan export (CSV/Excel)

### D9. App Shell & Navigation
Cross-cutting UI infrastructure — branding, top-level navigation, and the shared page shell every page wraps in. Not a forecasting business domain; added when the left-sidebar request surfaced scope no existing domain covered.

**Features**
- F9.1 Left sidebar app shell — fixed left sidebar (branding, top-level nav links, fold/unfold) plus a shared page-layout wrapper every page uses, modeled on gws_care's `page_layout()`/`SidebarFoldState` pattern

## Issues

<!-- Status: Backlog | Ongoing | Doing | Done. Type: feature | bug | chore.
     Priority: P0 (compulsory/prerequisite) | P1 (Pareto 20%, high-impact) | P2 (deferred).
     Reference: FISY-NNN, unique and never reused across the whole file.
     GitHub links use the issue number once gws-issue-sync has pushed it. -->

### Backlog

- [ ] **FISY-001** `[D1]` Create forecast project with tier selection
  - Type: feature
  - Priority: P0
  - Description: User creates a new project, sets a start date, and selects an initial tier (STARTER/ESSENTIEL/INNOVATION), which determines which config fields/screens are shown downstream.
  - Acceptance criteria: Given the new-project form, when the user submits a start date and tier, then the project is created and every later screen shows only the fields relevant to that tier.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/1
  - Spec:
    - Interfaces:
      - New Reflex app `fisy_app` scaffolded via `gws reflex generate fisy_app` inside `bricks/gws_fisy/src/gws_fisy/` (per the standard `generate_fisy_app_app.py` + `_fisy_app/` layout).
      - Page `/projects` — `ProjectListState(rx.State)`: `@rx.var projects: List[ProjectDTO]` populated by `load_projects` (`on_load`), calling `ProjectService.list_projects_of_user(user)`. Renders a list of project cards (name, tier badge, start date) and a "New Project" button.
      - `ProjectFormDialogState(rx.State)`: public fields `name: str = ""`, `start_date: str = ""`, `tier: str = FisyTier.STARTER.value`; explicit setters `set_name`, `set_start_date`, `set_tier`; `@rx.event async def create_project(self)` calling `ProjectService.create_project(CreateProjectDTO(...))` inside `main_state.authenticate_user()`, then closing the dialog and appending the new `ProjectDTO` to `ProjectListState.projects` (callback pattern, matching gws_project's `ProjectFormDialogState`).
      - Page `/projects/[project_id]` — `ProjectWorkspaceState(rx.State)`: loads `project: ProjectDTO` from the route param via `ProjectService.get_by_id_and_check(project_id, user)`. Renders an `rx.tabs` shell with one tab per domain (Config, Activities, Revenue, Personnel, Costs & Investments, Financing, Cash Flow, Synthesis — Tax and Actuals/Export tabs added once their P2 issues land). This issue implements only the **Config** tab (read display of start date + tier); other tabs render an empty placeholder until their own issue is built.
      - Shared module `core/fisy_tier.py`: `class FisyTier(str, Enum): STARTER = "STARTER"; ESSENTIEL = "ESSENTIEL"; INNOVATION = "INNOVATION"` — reused by every later tier-gated feature.
    - Data model:
      - New brick DB infrastructure (created once here, reused by every subsequent issue): `core/fisy_db_manager.py:FisyDbManager(LazyAbstractDbManager)`; brick-local `core/model_with_user.py:ModelWithUser(Model)` with `created_by`/`last_modified_by` FKs to a brick-local `User` model kept in sync via a `user_sync_service.py`, mirroring gws_project/gws_care exactly.
      - `project/project.py:Project(ModelWithUser)`: `name: CharField(max_length=255)`, `start_date: DateField`, `tier: CharField(max_length=20)` (stores a `FisyTier` value). Table auto-created at startup from the model (no explicit migration needed for a new table).
      - `project/project_dto.py`: `ProjectDTO(BaseModel)` (id, name, start_date, tier, created_at); `CreateProjectDTO(BaseModel)` (name, start_date, tier).
      - `project/project_service.py:ProjectService`: `create_project(dto, user) -> Project`, `get_by_id_and_check(id, user) -> Project`, `list_projects_of_user(user) -> List[Project]`. All three scope to `Project.created_by == user` (see Data visibility below).
    - Flow: User opens `/projects` → projects load scoped to the current user → clicks "New Project" → fills name/start date/tier (tier defaults to STARTER) → submits → `ProjectFormDialogState.create_project` → row saved → dialog closes, list updates → user clicks into the project → lands on `/projects/[project_id]`, Config tab showing the saved start date and tier.
    - Edge cases:
      - Empty/whitespace-only `name` → `raise ReflexAppException("Project name is required")`.
      - Missing/unparseable `start_date` → `raise ReflexAppException("A valid start date is required")`.
      - `tier` outside the 3 valid values (shouldn't happen via the UI select, but the service validates defensively) → `raise ReflexAppException("Invalid tier")`.
      - Navigating to `/projects/[project_id]` for a project that doesn't exist, or exists but belongs to another user → `get_by_id_and_check` raises (via `BaseHTTPException`), surfaced as an error toast; user is not shown any data about a project they don't own.
      - No uniqueness constraint on `name` — duplicate project names for the same user are allowed (not a stated requirement to prevent this).
    - Non-functional: standard `authenticate_user()` gate on all state mutations, per every Reflex app in this repo. Data-visibility model: **Project (and everything created inside it by later issues) is private to its creator for v1** — every service method scopes to `created_by == current_user`. Sharing a project with other users was explicitly named as a later capability, not part of this issue — **flagging it as a new candidate feature for gws-issue-define to scope separately** (a "Share project with other users" issue), not designed here.
    - Out of scope: editing an existing project's name/start date after creation (not stated in the acceptance criteria — flagging as a possible gap to raise with gws-issue-define if editing turns out to be needed before FISY-013's tier-upgrade issue). Tier upgrade itself is FISY-013, not this issue. Project sharing/multi-user visibility (see above).

- [ ] **FISY-002** `[D1]` Manage revenue-generating activities
  - Type: feature
  - Priority: P0
  - Description: Add, edit, remove, and rename activities (business lines) within a project. No cap on count.
  - Acceptance criteria: A user can add any number of activities to a project, and each subsequent revenue/cost/tax configuration screen exposes per-activity fields for every activity that exists.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/2
  - Spec:
    - Interfaces:
      - Activities tab of `/projects/[project_id]` — `ActivityListState(rx.State)`: `@rx.var activities: List[ActivityDTO]`, loaded alongside the project. Renders an editable, ordered list (name + drag-or-up/down reorder + delete icon-button) and an "Add activity" inline input/button.
      - `ActivityFormDialogState(rx.State)` (or an inline-editable row, whichever the eventual UI pass prefers — both call the same service methods): `create_activity(project_id, name)`, `update_activity(activity_id, name)`, `delete_activity(activity_id)`.
    - Data model:
      - `activity/activity.py:Activity(ModelWithUser)`: `project = ForeignKeyField(Project, on_delete="CASCADE", backref="activities")`, `name: CharField(max_length=255)`, `sort_order: IntegerField(default=0)` (drives display order; new activities append at `max(sort_order) + 1`).
      - `activity/activity_dto.py`: `ActivityDTO` (id, project_id, name, sort_order); `CreateActivityDTO` (project_id, name); `UpdateActivityDTO` (name) and/or `(sort_order)` for reordering.
      - `activity/activity_service.py:ActivityService`: `create_activity(dto, user) -> Activity`, `update_activity(id, dto, user) -> Activity`, `delete_activity(id, user) -> None`, `reorder_activities(project_id, ordered_ids, user) -> List[Activity]`, `list_activities_of_project(project_id, user) -> List[Activity]`. Every method first loads the parent `Project` via `ProjectService.get_by_id_and_check` to enforce the same creator-only visibility as FISY-001, since an activity has no visibility of its own.
    - Flow: User opens a project's Activities tab → existing activities list loads → adds a new activity by name → appears at the end of the list → can rename any activity inline → can reorder (updates `sort_order` for affected rows) → can delete, which cascades (via `on_delete="CASCADE"`) to any per-activity child records created by later issues (revenue config, cost config, order forecasts, etc. — none exist yet at this issue's scope).
    - Edge cases:
      - Empty/whitespace-only activity name → `raise ReflexAppException("Activity name is required")`.
      - Deleting an activity that already has downstream data (once FISY-003/014/etc. exist) → cascades and removes that data too; no separate confirmation is designed here since no such data exists yet at this issue's scope — **flagging for the later issues that add per-activity children: confirm whether delete should warn the user before cascading once there's real data at stake.**
      - Deleting the last remaining activity → allowed; a project with zero activities is a valid, if not yet useful, state (later domains simply show no per-activity rows to configure).
      - Reordering with a stale/partial id list (e.g. a concurrent delete from another tab) → `reorder_activities` ignores ids no longer present rather than erroring.
      - No cap on the number of activities per project (per the earlier "no artificial caps" decision).
    - Non-functional: none beyond FISY-001's auth/visibility model, which this issue inherits.
    - Out of scope: any per-activity revenue/cost/order configuration (FISY-003, FISY-014, etc.) — this issue only manages the activity as a named, ordered entity.

- [ ] **FISY-003** `[D1]` Basic per-activity revenue & cost inputs
  - Type: feature
  - Priority: P1
  - Description: For each activity, enter a unit price and a unit variable cost — the flat, no-timing model used at STARTER tier.
  - Acceptance criteria: Entering a unit price and unit cost per activity is sufficient to drive STARTER-tier revenue/cost calculations (F2.2), with no other configuration required.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/3
  - Spec:
    - Interfaces: Extends the Activities tab row/dialog from FISY-002 with two numeric fields per activity: "Unit price (€ HT)" and "Unit variable cost (€ HT)". `ActivityFormDialogState` gains `unit_price: str`, `unit_variable_cost: str` (+ setters), included in the existing `create_activity`/`update_activity` calls. `ActivityDTO`/`UpdateActivityDTO` extended with `unit_price: Optional[Decimal]`, `unit_variable_cost: Optional[Decimal]`.
    - Data model: Both values are a single constant per activity for the whole forecast (per the source spreadsheet — only order volume varies over time at STARTER tier; price/cost escalation over time is FISY-004/005). Add `unit_price: DecimalField(max_digits=12, decimal_places=2, null=True)` and `unit_variable_cost: DecimalField(max_digits=12, decimal_places=2, null=True)` columns to the existing `Activity` model via an additive `@brick_migration` step (`sql_migrator.add_column_if_not_exists`), since `Activity` already exists from FISY-002.
    - Flow: User edits an activity (from the FISY-002 list) and also sets unit price/cost → saved via the existing `ActivityService.update_activity`.
    - Edge cases: Negative unit price or cost → `raise ReflexAppException("Unit price/cost cannot be negative")`. Left blank (null) → allowed; that activity contributes zero revenue/cost until filled in (FISY-015 treats null as 0).
    - Non-functional: none beyond FISY-001's inherited auth/visibility model.
    - Out of scope: time-varying price/cost or payment timing (FISY-004/FISY-005, P2); order-volume entry (FISY-014); the actual revenue/cost calculation from these inputs (FISY-015).

- [ ] **FISY-004** `[D1]` Advanced revenue timing config
  - Type: feature
  - Priority: P2
  - Description: Extend per-activity revenue config with delivery lag, deposit/milestone/final payment-split percentages, and year-over-year price escalation.
  - Acceptance criteria: Given a project above STARTER tier, a user can set delivery lag and payment-split percentages per activity, and these values change the cash-vs-accrual timing computed in F2.3.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/4

- [ ] **FISY-005** `[D1]` Advanced cost timing config
  - Type: feature
  - Priority: P2
  - Description: Extend per-activity cost config with delivery/payment lag, mirroring FISY-004 for variable costs.
  - Acceptance criteria: Given a project above STARTER tier, a user can set delivery/payment lag per activity for variable costs, changing the cash timing of cost outflows.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/5

- [ ] **FISY-006** `[D1]` Recurring revenue contract config
  - Type: feature
  - Priority: P2
  - Description: Per activity, mark it as recurring and configure a monthly recurring amount plus contract duration (INNOVATION tier).
  - Acceptance criteria: Given an INNOVATION-tier activity, a user can flag it recurring and set a monthly amount and duration, which then drives the recurring revenue calculation (F2.4).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/6

- [ ] **FISY-007** `[D1]` Default overhead cost category templates
  - Type: feature
  - Priority: P1
  - Description: A pre-populated, editable list of standard external-charge categories (e.g. marketing, sales, premises, legal/accounting, IT, insurance), each with a fixed annual amount and a variable % of revenue or per-headcount.
  - Acceptance criteria: A new project starts with the standard category list pre-filled with sensible defaults, and the user can edit or delete any line.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/7
  - Spec:
    - Interfaces: Tagged `[D1]` in the backlog (shared config), but its natural UI home is the project workspace's "Costs & Investments" tab, alongside FISY-024 which extends the same list. `OverheadChargeListState(rx.State)`: `@rx.var overhead_charges: List[OverheadChargeDTO]`. Renders an editable table — name, fixed annual amount, variable basis (select: "% of revenue" / "amount per employee"), and a variable coefficient field whose label/unit switches with the basis — with a delete icon per row. No "add new line" control in this issue (see Out of scope).
    - Data model:
      - `overhead_charge/overhead_charge.py:OverheadCharge(ModelWithUser)`: `project = ForeignKeyField(Project, on_delete="CASCADE", backref="overhead_charges")`, `name: CharField(max_length=255)`, `fixed_annual_amount: DecimalField(max_digits=12, decimal_places=2, default=0)`, `variable_coefficient: DecimalField(max_digits=12, decimal_places=4, default=0)`, `variable_basis: CharField(max_length=20)` (new `FisyVariableBasis(str, Enum)`: `REVENUE` / `HEADCOUNT`), `is_custom: BooleanField(default=False)`, `sort_order: IntegerField`. **Note the field's meaning depends on `variable_basis`** (matches the source spreadsheet's two distinct modes): when `REVENUE`, `variable_coefficient` is a fraction of monthly revenue (e.g. `0.03` = 3% of CA); when `HEADCOUNT`, it's a flat currency amount per employee (e.g. `500` = €500/employee), not a percentage. FISY-024 is where this coefficient is actually applied.
      - `overhead_charge/overhead_charge_dto.py`: `OverheadChargeDTO`; `UpdateOverheadChargeDTO` (name, fixed_annual_amount, variable_coefficient, variable_basis).
      - `overhead_charge/overhead_charge_service.py:OverheadChargeService`: `seed_defaults(project, user) -> List[OverheadCharge]` (`is_custom=False` rows; exact category names and default fixed/variable figures mirror the "Charges externes" sheet in `bricks/gws_fisy/specs/FISY-STARTER.xls`, copied verbatim at implementation time rather than re-specified here), `update_overhead_charge(id, dto, user) -> OverheadCharge`, `delete_overhead_charge(id, user) -> None`, `list_overhead_charges_of_project(project_id, user) -> List[OverheadCharge]`.
    - Flow: Creating a project (FISY-001) now also calls `seed_defaults` as part of the same creation flow, pre-filling the standard category list. User opens the Costs & Investments tab, sees the pre-filled list, and edits any line's amount/rate/basis inline or deletes it entirely.
    - Edge cases: Negative fixed amount or variable rate → rejected (`ReflexAppException`). Deleting every default line → allowed, leaves an empty list. `variable_basis` must be one of the two enum values.
    - Non-functional: none beyond the inherited auth/visibility model.
    - Out of scope: adding new custom charge lines and computing the actual monthly expense amount from this config (both are FISY-024); any per-activity or time-varying override of these categories.

- [ ] **FISY-008** `[D1]` Basic payroll burden rate
  - Type: feature
  - Priority: P1
  - Description: A single configurable payroll burden percentage applied to gross salaries.
  - Acceptance criteria: A user can set one overall payroll burden rate that scales every gross salary in the payroll burden calculation (F3.3).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/8
  - Spec:
    - Interfaces: Shown in the project workspace's Config tab, alongside FISY-001's start date/tier — a new "Payroll burden rate (%)" field. Reuses `ProjectWorkspaceState` (or a `ProjectConfigState` if the Config tab grows its own state): `set_payroll_burden_rate(rate)` → `ProjectService.update_payroll_burden_rate(project_id, rate, user)`.
    - Data model: Single project-wide rate, not per-role/per-activity (matches STARTER's flat "Taux de charges"). Add `payroll_burden_rate: DecimalField(max_digits=6, decimal_places=4, default=Decimal("0.45"))` column to the existing `Project` model via an additive migration (default 45%, mirroring STARTER's hardcoded constant, but user-editable from creation onward).
    - Flow: A new project is created with `payroll_burden_rate` pre-filled at 45%. User opens Config and changes it to any other value; the new rate applies to all payroll burden calculations (FISY-021) from that point on (no historical/per-period rate — a single current value, matching STARTER).
    - Edge cases: Value outside `[0, 1]` (0%–100%) → `raise ReflexAppException("Payroll burden rate must be between 0% and 100%")`.
    - Non-functional: none beyond the inherited auth/visibility model.
    - Out of scope: split employer/employee rates, SMIC reference wage, JEI-adjusted rates (FISY-009, P2); the actual payroll cost computation using this rate (FISY-021).

- [ ] **FISY-009** `[D1]` Detailed payroll burden config
  - Type: feature
  - Priority: P2
  - Description: Split employer vs. employee charge rates, a SMIC reference wage, and (INNOVATION) JEI-adjusted payroll rates.
  - Acceptance criteria: Given a project above STARTER tier, employer and employee charge rates can be set independently and feed both F3.3 and the JEI engine (F6.4).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/9

- [ ] **FISY-010** `[D1]` VAT rate configuration
  - Type: feature
  - Priority: P2
  - Description: Per-activity VAT rate plus a generic rate for investments/external charges.
  - Acceptance criteria: Setting a VAT rate per activity or generically changes the VAT computed by the VAT engine (F6.1).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/10

- [ ] **FISY-011** `[D1]` Basic financing sources config
  - Type: feature
  - Priority: P1
  - Description: Three financing lines — capital, debt, subsidies — entered as flat values across the 5-year horizon.
  - Acceptance criteria: A user can enter capital/debt/subsidy amounts per period, feeding the STARTER-level cash flow (F5.4) and break-even/ratios dashboard (F7.1).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/11
  - Spec:
    - Interfaces: Financing tab of `/projects/[project_id]`. `FinancingConfigState(rx.State)`: `@rx.var monthly_capital: List[Decimal]`, `monthly_debt: List[Decimal]`, `monthly_subsidy: List[Decimal]` (each length 60, 0-filled for unset months), displayed as a 3-row × 60-month editable grid (grouped by year for readability). `set_financing_amount(financing_type: str, month_index: int, value: str)` → `FinancingService.set_amount(project_id, financing_type, month_index, value, user)`. "Flat" here means no rate/duration/timing terms attached to these three fixed types (contrast with FISY-012's named sources + loan terms) — entry is still monthly, per the app's monthly-throughout-all-tiers decision.
    - Data model: `financing/financing_entry.py:FinancingEntry(ModelWithUser)`: `project = ForeignKeyField(Project, on_delete="CASCADE", backref="financing_entries")`, `financing_type: CharField(max_length=20)` (new `FisyFinancingType(str, Enum)`: `CAPITAL` / `DEBT` / `SUBSIDY`), `month_index: SmallIntegerField()` (0–59), `amount: DecimalField(max_digits=12, decimal_places=2, default=0)`. Unique constraint on `(project, financing_type, month_index)`. Storage is sparse — only non-zero entries need a row; the service 0-fills the other months on read.
      - `financing/financing_entry_dto.py`: `FinancingEntryDTO`; `SetFinancingAmountDTO` (financing_type, month_index, amount).
      - `financing/financing_service.py:FinancingService`: `set_amount(project_id, financing_type, month_index, amount, user) -> FinancingEntry`, `list_monthly_series(project_id, user) -> Dict[FisyFinancingType, List[Decimal]]` (returns all 3 types as 60-length 0-filled arrays).
    - Flow: User opens the Financing tab → sees a 60-month grid per financing type (initially all zero) → enters an amount in any month (e.g. a capital injection in month 1) → `set_amount` upserts the corresponding row.
    - Edge cases: Negative amount → `raise ReflexAppException("Financing amount cannot be negative")` (repayment/outflow is tracked separately by FISY-030, not as a negative value here). Non-numeric input → standard form validation. `month_index` outside `[0, 59]` → rejected defensively (shouldn't be reachable via the UI grid).
    - Non-functional: none beyond the inherited auth/visibility model.
    - Out of scope: loan interest rate, amortization duration, short/medium-long-term split, and any named source beyond these 3 fixed types (all FISY-012, P2); debt repayment tracking (FISY-030); consumption of these series in the cash-flow statement (FISY-033) and break-even dashboard (FISY-041).

- [ ] **FISY-012** `[D1]` Advanced financing terms config
  - Type: feature
  - Priority: P2
  - Description: Loan interest rate, amortization duration, short-term/medium-long-term split, plus named current accounts, repayable advances, and (INNOVATION) incubator advances — unlimited count of named sources.
  - Acceptance criteria: Given a project above STARTER tier, a user can configure loan terms and add any number of named financing sources beyond the three basic types.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/12

- [ ] **FISY-013** `[D1]` Tier upgrade
  - Type: feature
  - Priority: P2
  - Description: Upgrade an existing project from STARTER→ESSENTIEL or ESSENTIEL→INNOVATION, carrying over existing data and unlocking the new tier's fields.
  - Acceptance criteria: Given a STARTER project with existing data, when the user upgrades it to ESSENTIEL, then all existing inputs are preserved and the new ESSENTIEL-only fields appear (empty, ready to fill in).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/13

- [ ] **FISY-014** `[D2]` Order volume forecasting per activity
  - Type: feature
  - Priority: P1
  - Description: Monthly unit-order input per activity across the full 5-year (60-month) horizon.
  - Acceptance criteria: For each activity, the user can enter a forecasted order quantity for each of the 60 months.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/14
  - Spec:
    - Interfaces: Revenue tab of `/projects/[project_id]`. `OrderVolumeState(rx.State)`: `@rx.var order_volumes_by_activity: Dict[str, List[int]]` (activity id → 60-length list, 0-filled). Editable grid: rows = activities (from FISY-002), columns = 60 months. `set_order_volume(activity_id: str, month_index: int, quantity: str)` → `OrderVolumeService.set_quantity(...)`.
    - Data model: Same monthly-time-series-row shape as FISY-011's `FinancingEntry`. `revenue/order_volume.py:OrderVolume(ModelWithUser)`: `activity = ForeignKeyField(Activity, on_delete="CASCADE", backref="order_volumes")`, `month_index: SmallIntegerField()` (0–59), `quantity: IntegerField(default=0)`. Unique constraint on `(activity, month_index)`; sparse storage, 0-filled on read.
      - `revenue/order_volume_dto.py`: `OrderVolumeDTO`; `SetOrderVolumeDTO` (activity_id, month_index, quantity).
      - `revenue/order_volume_service.py:OrderVolumeService`: `set_quantity(activity_id, month_index, quantity, user) -> OrderVolume` (validates ownership by walking activity → project → creator, same as FISY-002), `list_monthly_series_of_project(project_id, user) -> Dict[str, List[int]]` (keyed by activity id).
    - Flow: User opens the Revenue tab → sees one row per existing activity, 60 zero-filled month columns → enters quantities per month per activity.
    - Edge cases: Negative quantity → `raise ReflexAppException("Order quantity cannot be negative")`. Non-integer input → standard form validation. Deleting an activity (FISY-002) cascades and removes its order volumes (`on_delete="CASCADE"`). A project with no activities yet shows an empty grid, not an error.
    - Non-functional: none beyond the inherited auth/visibility model.
    - Out of scope: computing revenue/cost from these quantities (FISY-015); recurring-revenue orders (FISY-017).

- [ ] **FISY-015** `[D2]` Basic revenue & cost calculation
  - Type: feature
  - Priority: P1
  - Description: Compute monthly revenue and variable cost as orders × unit price/cost (FISY-003), with no cash/accrual distinction — matching STARTER's model.
  - Acceptance criteria: Given order volumes and unit price/cost, monthly revenue and variable-cost figures are computed automatically with no further input.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/15
  - Spec:
    - Interfaces: A read-only computed summary directly below FISY-014's order-volume grid on the Revenue tab — per-activity monthly revenue and cost rows plus a total row, spanning the same 60 months. Backed by `@rx.var monthly_revenue_by_activity: Dict[str, List[Decimal]]` / `monthly_cost_by_activity`, recomputed after every `set_order_volume`, `create_activity`/`update_activity` event.
    - Data model: None new — a pure computation over existing `OrderVolume` and `Activity.unit_price`/`unit_variable_cost` data, not persisted (cheap enough at this scale — 60 months × N activities — to recompute on every read rather than cache).
      - `revenue/forecast_calculation_service.py:ForecastCalculationService`: `compute_monthly_revenue(project_id, user) -> Dict[str, List[Decimal]]` and `compute_monthly_variable_cost(project_id, user) -> Dict[str, List[Decimal]]`. For each activity and month: `revenue[m] = order_volume[m] * (unit_price or 0)`, `cost[m] = order_volume[m] * (unit_variable_cost or 0)`.
    - Flow: Any edit to order volumes, unit price, or unit variable cost triggers a recompute of the summary shown on the Revenue tab.
    - Edge cases: Activity with a null `unit_price`/`unit_variable_cost` (allowed since FISY-003) → treated as 0, not an error. Activity with all-zero order volumes → zero revenue/cost row, not an error.
    - Non-functional: none — pure, unpersisted read computation.
    - Out of scope: cash-vs-accrual split (FISY-016, P2); recurring revenue (FISY-017, P2); surfacing these totals in the Synthesis dashboard (FISY-041) or cash-flow statement (FISY-033) — those issues call this same service but own their own display integration.

- [ ] **FISY-016** `[D2]` Cash-vs-accrual revenue split
  - Type: feature
  - Priority: P2
  - Description: Using the payment-timing config (FISY-004), split computed revenue into a cash-received stream and an accrual stream.
  - Acceptance criteria: Given delivery lag and payment-split percentages, the app produces two distinct monthly series — cash-received revenue and accrual revenue — that differ whenever timing is non-trivial.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/16

- [ ] **FISY-017** `[D2]` Recurring revenue calculation
  - Type: feature
  - Priority: P2
  - Description: Combine fixed order-based revenue with recurring revenue (FISY-006), both cash and accrual.
  - Acceptance criteria: For an activity with recurring contracts configured, monthly revenue includes the recurring amount for each active contract's duration, in both cash and accrual views.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/17

- [ ] **FISY-018** `[D2]` Fixed-vs-recurring revenue reporting
  - Type: feature
  - Priority: P2
  - Description: A report/view showing fixed and recurring revenue separately and combined.
  - Acceptance criteria: The user can view fixed revenue, recurring revenue, and their combined total, per month, per activity, and in aggregate.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/18

- [ ] **FISY-019** `[D3]` Headcount & salary planning per role
  - Type: feature
  - Priority: P1
  - Description: Monthly gross salary and headcount input per role across the 5-year horizon.
  - Acceptance criteria: A user can add roles and enter monthly gross salary and headcount for each, for all 60 months.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/19
  - Spec:
    - Interfaces: Personnel tab of `/projects/[project_id]`. `RoleListState(rx.State)`: `@rx.var roles: List[RoleDTO]`; add/rename/remove roles — same CRUD shape as FISY-002's activity management (`create_role`, `update_role`, `delete_role`). `RolePayrollState(rx.State)`: `@rx.var gross_salary_by_role: Dict[str, List[Decimal]]`, `headcount_by_role: Dict[str, List[Decimal]]` (each 60-length, 0-filled), rendered as two stacked 60-month grids, one row per role. `set_role_payroll(role_id: str, month_index: int, gross_salary: str, headcount: str)` → service call.
    - Data model:
      - `payroll/role.py:Role(ModelWithUser)`: `project = ForeignKeyField(Project, on_delete="CASCADE", backref="roles")`, `name: CharField(max_length=255)`, `sort_order: IntegerField(default=0)`.
      - `payroll/role_monthly_entry.py:RoleMonthlyEntry(ModelWithUser)`: `role = ForeignKeyField(Role, on_delete="CASCADE", backref="monthly_entries")`, `month_index: SmallIntegerField()` (0–59), `gross_salary: DecimalField(max_digits=12, decimal_places=2, default=0)`, `headcount: DecimalField(max_digits=6, decimal_places=2, default=0)` (fractional allowed, e.g. `0.5` for a part-time hire). Unique `(role, month_index)`; sparse, 0-filled on read.
      - **Design decision (not pinned down by the acceptance criteria, decided here so FISY-020/FISY-021 have a fixed formula to build on):** `gross_salary` is the monthly gross salary **per employee** in that role, not the role's total payroll mass — matching the source spreadsheet's "Salaires annuels bruts" read as a per-employee figure. Total monthly salary mass for a role = `gross_salary × headcount`. This is the multiplier FISY-021's payroll cost calculation uses.
      - `payroll/role_dto.py`: `RoleDTO`; `CreateRoleDTO`/`UpdateRoleDTO` (name); `RoleMonthlyEntryDTO`; `SetRolePayrollDTO` (role_id, month_index, gross_salary, headcount).
      - `payroll/role_service.py:RoleService` (create/update/delete/list — mirrors `ActivityService`); `payroll/role_payroll_service.py:RolePayrollService.set_monthly_entry(role_id, month_index, gross_salary, headcount, user) -> RoleMonthlyEntry`, `.list_monthly_series_of_project(project_id, user) -> Dict[str, Dict[str, List[Decimal]]]`.
    - Flow: User opens the Personnel tab → adds roles (e.g. "Founder", "Developer") → for each role, enters monthly gross salary (per employee) and headcount across the 60 months.
    - Edge cases: Negative salary or headcount → `raise ReflexAppException(...)`. Empty role name → `raise ReflexAppException("Role name is required")` (mirrors FISY-002). Deleting a role cascades its monthly entries (`on_delete="CASCADE"`). Zero headcount with a nonzero salary is allowed (simply yields zero payroll mass downstream) — not treated as an error, since no business rule against it was stated.
    - Non-functional: none beyond the inherited auth/visibility model.
    - Out of scope: ETP computation (FISY-020); payroll burden/cost computation (FISY-021); R&D time-allocation (FISY-022/FISY-023, P2).

- [ ] **FISY-020** `[D3]` ETP (FTE) calculation
  - Type: feature
  - Priority: P1
  - Description: Automatic full-time-equivalent computation from headcount entries.
  - Acceptance criteria: Given monthly headcount per role, the app computes an ETP figure per role and in total for any selected period.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/20
  - Spec:
    - Interfaces: A computed "ETP" row per role plus a total row, shown per year (5 columns) alongside FISY-019's monthly grids on the Personnel tab. `@rx.var etp_by_role_by_year: Dict[str, List[Decimal]]` on `RolePayrollState`.
    - Data model: None new — matches the source spreadsheet's `=SUM(...)/12` pattern: ETP for a period = average monthly headcount over that period, not identical to any single month's headcount.
      - `payroll/role_payroll_service.py:RolePayrollService.compute_etp(project_id, period_start_month, period_end_month, user) -> Dict[str, Decimal]` — per role, `sum(headcount[m] for m in period) / number_of_months_in_period`. `compute_etp_by_year(project_id, user) -> Dict[str, List[Decimal]]` — 5 yearly aggregates using consecutive 12-month windows (months 0–11, 12–23, …).
    - Flow: The Personnel tab recomputes and displays ETP per role per year whenever any headcount entry changes.
    - Edge cases: A role with no monthly entries yet → ETP = 0 for every year, not an error.
    - Non-functional: none — pure, unpersisted computation.
    - Out of scope: any dashboard/reporting integration beyond the Personnel tab itself (ETP is not one of the Synthesis dashboard's stated metrics in FISY-041).

- [ ] **FISY-021** `[D3]` Payroll burden calculation
  - Type: feature
  - Priority: P1
  - Description: Apply the configured payroll burden rate(s) (FISY-008/FISY-009) to gross salaries to compute total payroll cost.
  - Acceptance criteria: Given gross salaries and a burden rate, total monthly payroll cost (gross + burden) is computed automatically.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/21
  - Spec:
    - Interfaces: A computed "Total payroll cost" summary below FISY-019's grids on the Personnel tab — per-role and total monthly cost across the 60 months. `@rx.var monthly_payroll_cost_by_role: Dict[str, List[Decimal]]` and `monthly_payroll_cost_total: List[Decimal]` on `RolePayrollState`.
    - Data model: None new — pure computation using FISY-019's per-employee `gross_salary`/`headcount` and FISY-008's project-wide `payroll_burden_rate`.
      - `payroll/role_payroll_service.py:RolePayrollService.compute_monthly_payroll_cost(project_id, user) -> Dict[str, List[Decimal]]`. For each role and month: `salary_mass[m] = gross_salary[m] × headcount[m]`; `total_cost[m] = salary_mass[m] × (1 + payroll_burden_rate)`.
    - Flow: Any change to a role's monthly gross salary/headcount, or to the project's payroll burden rate (FISY-008), triggers a recompute of this summary.
    - Edge cases: Role with null/zero entries for a given month → zero cost for that month, not an error.
    - Non-functional: none — pure, unpersisted computation.
    - Out of scope: JEI-adjusted / split employer-employee rates (FISY-009, P2); surfacing this total in the cash-flow statement (FISY-033) or break-even dashboard (FISY-041) — those issues consume this same service but own their own display integration.

- [ ] **FISY-022** `[D3]` R&D time-allocation tagging
  - Type: feature
  - Priority: P2
  - Description: Per employee per year, % of time on Recherche (CIR) vs. Innovation (CII), plus a "Jeune docteur" (young PhD) flag.
  - Acceptance criteria: Given an INNOVATION-tier project, each employee has editable CIR%/CII% and a young-PhD flag, feeding the CIR/CII computation (F6.5).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/22

- [ ] **FISY-023** `[D3]` Activity time-allocation
  - Type: feature
  - Priority: P2
  - Description: Split each employee's time percentage across activities/projects.
  - Acceptance criteria: Given an INNOVATION-tier project with multiple activities, each employee's time allocation across activities must sum to 100%, and the app rejects/flags entries that don't.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/23

- [ ] **FISY-024** `[D4]` External charges management
  - Type: feature
  - Priority: P1
  - Description: Manage expense lines (from FISY-007 templates or custom), each with a fixed amount and a variable component (by revenue or by headcount), monthly over 5 years.
  - Acceptance criteria: A user can add, edit, and remove expense lines, each computing a monthly cost from its fixed + variable components.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/24
  - Spec:
    - Interfaces: Costs & Investments tab of `/projects/[project_id]`, extending FISY-007's `OverheadChargeListState`/table with an "Add charge" control (creating rows with `is_custom=True`) and a read-only computed "Monthly cost" summary column/row spanning the 60 months, per line and total.
    - Data model: No new table — extends FISY-007's `OverheadCharge`. New capability: `overhead_charge/overhead_charge_service.py:OverheadChargeService.create_overhead_charge(dto: CreateOverheadChargeDTO, user) -> OverheadCharge` (`is_custom=True`).
      - `overhead_charge/overhead_charge_calculation_service.py:OverheadChargeCalculationService.compute_monthly_cost(project_id, user) -> Dict[str, List[Decimal]]` (keyed by charge id, plus a `"total"` entry). For each charge and month: `monthly_fixed = fixed_annual_amount / 12`; if `variable_basis == REVENUE`, `variable = variable_coefficient × total_monthly_revenue[m]` (from FISY-015's `ForecastCalculationService.compute_monthly_revenue`, summed across activities); if `HEADCOUNT`, `variable = variable_coefficient × total_monthly_headcount[m]` (from FISY-019's headcount series, summed across roles); `monthly_cost[m] = monthly_fixed + variable`.
    - Flow: User adds a custom charge line (name + fixed amount + basis + coefficient) → appears in the table alongside the seeded defaults from FISY-007 → the computed monthly-cost summary recalculates whenever any charge, total revenue, or total headcount changes.
    - Edge cases: New custom line with no fixed amount and no coefficient set yet → computes to zero, not an error. Deleting a charge (already covered by FISY-007) removes it from the computed summary. A project with zero total revenue or headcount in a given month → that month's variable component is zero, not an error.
    - Non-functional: none beyond the inherited auth/visibility model.
    - Out of scope: surfacing this total in the cash-flow statement (FISY-033) or break-even dashboard (FISY-041) — those issues consume this same service but own their own display integration; per-activity allocation of external charges (not requested by any issue in this backlog).

- [ ] **FISY-025** `[D4]` CapEx/investment tracking with depreciation
  - Type: feature
  - Priority: P1
  - Description: Add investment items with a per-line amortization duration (defaulting to 5 years, user-editable), auto-computing straight-line depreciation. Applies uniformly across all tiers.
  - Acceptance criteria: Given an investment amount and a duration, the app computes a straight-line monthly depreciation schedule; the default duration is 5 years but can be changed per line.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/25
  - Spec:
    - Interfaces: Costs & Investments tab. `InvestmentListState(rx.State)`: `@rx.var investments: List[InvestmentDTO]`. Table: name, purchase month, amount, amortization duration (years, default 5, editable), plus a read-only computed monthly depreciation summary (per line and total) across the 60 months. `create_investment`, `update_investment`, `delete_investment` events.
    - Data model:
      - `investment/investment.py:Investment(ModelWithUser)`: `project = ForeignKeyField(Project, on_delete="CASCADE", backref="investments")`, `name: CharField(max_length=255)`, `purchase_month_index: SmallIntegerField()` (0–59, month depreciation starts), `amount: DecimalField(max_digits=12, decimal_places=2)`, `amortization_years: PositiveSmallIntegerField(default=5)`.
      - `investment/investment_dto.py`: `InvestmentDTO`; `CreateInvestmentDTO`/`UpdateInvestmentDTO` (name, purchase_month_index, amount, amortization_years).
      - `investment/investment_service.py:InvestmentService`: standard create/update/delete/list, scoped through the project's creator (same visibility model as every other entity).
      - `investment/investment_calculation_service.py:InvestmentCalculationService.compute_monthly_depreciation(project_id, user) -> Dict[str, List[Decimal]]`. Straight-line: `monthly_depreciation = amount / (amortization_years × 12)`, applied from `purchase_month_index` for `amortization_years × 12` consecutive months (0 before/after that window), per line and a `"total"` sum.
    - Flow: User adds an investment (name, amount, purchase month) → duration defaults to 5 years, editable per line → the computed depreciation summary recalculates immediately.
    - Edge cases: `amortization_years` must be ≥ 1 (a 0-duration/non-depreciable line is out of scope here — see below). Negative or zero `amount` → `raise ReflexAppException("Investment amount must be positive")`. An investment whose depreciation window extends past month 59 (the 5-year horizon) → only the portion within months 0–59 is shown/summed; no error.
    - Non-functional: none beyond the inherited auth/visibility model.
    - Out of scope: leasing/crédit-bail redirection to a rent expense (FISY-026, P2); in-kind capital contributions (FISY-027, P2); non-depreciable investments (`amortization_years = 0` in the source spreadsheet) — not requested by this issue's acceptance criteria, flagging as a possible gap for gws-issue-define if needed later; surfacing this total in the cash-flow statement (FISY-033) or P&L — owned by those issues.

- [ ] **FISY-026** `[D4]` Leasing (crédit-bail) handling
  - Type: feature
  - Priority: P2
  - Description: Flag an investment line as leased, redirecting it to a rent expense instead of depreciation.
  - Acceptance criteria: Given an investment marked as leased, it produces a recurring rent expense in the P&L/cash flow instead of a depreciation schedule.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/26

- [ ] **FISY-027** `[D4]` In-kind capital contributions
  - Type: feature
  - Priority: P2
  - Description: Mark an investment as funded by an in-kind (non-cash) equity contribution (apport en nature).
  - Acceptance criteria: Given an investment flagged as an in-kind contribution, it still depreciates normally but does not appear as a cash outflow, and instead increases equity in the funding plan (F5.3).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/27

- [ ] **FISY-028** `[D4]` Subcontracting tracking with R&D-eligibility tagging
  - Type: feature
  - Priority: P2
  - Description: Itemize outsourced work, allocate it by activity, and tag each line's provider type (not eligible / labelled R&D provider / public laboratory).
  - Acceptance criteria: Given an INNOVATION-tier project, a user can add subcontracting lines tagged by provider type, and each line's cost feeds the CIR/CII eligible base (F6.5) weighted by its tag.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/28

- [ ] **FISY-029** `[D4]` Per-activity/R&D-usage allocation for capex & subcontracting
  - Type: feature
  - Priority: P2
  - Description: Split each investment's and subcontracting line's % usage for Research (CIR) vs. Innovation (CII), and by activity.
  - Acceptance criteria: Given an INNOVATION-tier investment or subcontracting line, the user can set CIR%/CII% usage splits, which change the eligible base computed in F6.5.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/29

- [ ] **FISY-030** `[D5]` Basic debt repayment & net debt tracking
  - Type: feature
  - Priority: P1
  - Description: Track total debt repayment and net debt balance per year (STARTER-level — no detailed amortization schedule).
  - Acceptance criteria: Given debt entered in FISY-011, the app computes a yearly repayment amount and resulting net debt balance.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/30
  - Spec:
    - Interfaces: Financing tab, below FISY-011's grid — a "Debt repayment" row (same 60-month editable grid shape) plus a read-only computed summary: yearly repayment total and net debt balance, one figure per year (5 columns). `@rx.var monthly_debt_repayment: List[Decimal]`, `yearly_repayment: List[Decimal]`, `net_debt_by_year: List[Decimal]` on `FinancingConfigState`.
    - Data model: **Design decision (STARTER has no rate/schedule config, per FISY-011/012's split — there's no basis to auto-compute a repayment amount, so it must be a direct user input, aggregated by the app into the yearly view the acceptance criteria describes):**
      - `financing/debt_repayment.py:DebtRepayment(ModelWithUser)`: `project = ForeignKeyField(Project, on_delete="CASCADE", backref="debt_repayments")`, `month_index: SmallIntegerField()` (0–59), `amount: DecimalField(max_digits=12, decimal_places=2, default=0)`. Same unique-`(project, month_index)` / sparse-storage shape as `FinancingEntry`.
      - `financing/debt_repayment_dto.py`: `DebtRepaymentDTO`; `SetDebtRepaymentDTO` (month_index, amount).
      - `financing/debt_repayment_service.py:DebtRepaymentService.set_amount(project_id, month_index, amount, user) -> DebtRepayment`, `.list_monthly_series(project_id, user) -> List[Decimal]`.
      - `financing/financing_calculation_service.py:FinancingCalculationService.compute_yearly_repayment(project_id, user) -> List[Decimal]` (5 values — sum of each consecutive 12-month window). `.compute_net_debt_by_year(project_id, user) -> List[Decimal]` — at each year-end month (11, 23, 35, 47, 59): `cumulative_debt_drawn (FISY-011's FinancingEntry where financing_type=DEBT) − cumulative_repayment`.
    - Flow: User enters monthly debt-repayment amounts on the Financing tab (same interaction pattern as FISY-011) → the yearly repayment total and net debt balance recompute automatically.
    - Edge cases: Negative repayment amount → `raise ReflexAppException("Repayment amount cannot be negative")`. Net debt going negative (cumulative repayment exceeds cumulative debt drawn) → displayed as-is, not blocked — the app doesn't validate real-world repayment plausibility beyond sign.
    - Non-functional: none beyond the inherited auth/visibility model.
    - Out of scope: interest rate and detailed monthly amortization schedule (FISY-031, P2); surfacing this in the cash-flow statement (FISY-033) — that issue consumes this service but owns its own display integration.

- [ ] **FISY-031** `[D5]` Detailed loan amortization schedule
  - Type: feature
  - Priority: P2
  - Description: Full monthly amortization schedule computed from loan terms (FISY-012): rate, duration, short/medium-long-term split.
  - Acceptance criteria: Given loan terms above STARTER tier, the app produces a monthly principal/interest amortization schedule per loan.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/31

- [ ] **FISY-032** `[D5]` Sources-and-uses funding plan
  - Type: feature
  - Priority: P2
  - Description: Automatic funding plan: uses (BFR variation, investment, financing outflows, negative CAF) vs. resources (capital, debt, subsidies, positive CAF).
  - Acceptance criteria: Given all upstream domains configured, the app produces an annual sources-and-uses statement with a period surplus/deficit figure.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/32

- [ ] **FISY-033** `[D5]` Monthly cash-flow statement (core lines)
  - Type: feature
  - Priority: P1
  - Description: Automatic monthly cash-in/cash-out statement covering financing, revenue, payroll, external charges, investments, variable costs, and debt repayment, with a running ending-cash balance. Full 60-month horizon (per the monthly-throughout decision).
  - Acceptance criteria: Given all STARTER-level domains configured, the app produces a month-by-month cash flow with a correct running balance for all 60 months.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/33
  - Spec:
    - Interfaces: New "Cash Flow" tab on `/projects/[project_id]`. `CashFlowState(rx.State)`: `@rx.var cash_flow: CashFlowStatementDTO` (see below), recomputed on tab load. Renders a table: one row per line item plus starting/ending balance, 60 month columns (grouped by year for readability).
    - Data model: No new table — a pure aggregation over every upstream P1 service, matching the source spreadsheet's Trésorerie sheet line-for-line:
      - **cash-in**: `financing_in[m]` = sum of FISY-011's 3 `FinancingEntry` types for month `m`; `revenue_in[m]` = FISY-015's `compute_monthly_revenue`, summed across activities (no cash/accrual split exists yet at this tier — FISY-016 is P2 — so computed revenue is treated as cash received in the same month).
      - **cash-out**: `payroll_out[m]` = FISY-021's `compute_monthly_payroll_cost` total; `external_charges_out[m]` = FISY-024's `compute_monthly_cost` total; `investments_out[m]` = **the investment's full `amount` in its `purchase_month_index`** (a one-time cash outflow — distinct from FISY-025's monthly *depreciation*, which is an accrual concept with no cash-flow role at this tier); `variable_costs_out[m]` = FISY-015's `compute_monthly_variable_cost`, summed across activities; `debt_repayment_out[m]` = FISY-030's `list_monthly_series`.
      - `treasury/cash_flow_dto.py:CashFlowStatementDTO(BaseModel)`: `financing_in`, `revenue_in`, `payroll_out`, `external_charges_out`, `investments_out`, `variable_costs_out`, `debt_repayment_out`, `net_change`, `ending_balance` — each a 60-element `List[Decimal]`.
      - `treasury/cash_flow_service.py:CashFlowService.compute_monthly_cash_flow(project_id, user) -> CashFlowStatementDTO`. `net_change[m] = financing_in[m] + revenue_in[m] − payroll_out[m] − external_charges_out[m] − investments_out[m] − variable_costs_out[m] − debt_repayment_out[m]`; `ending_balance[0] = net_change[0]` (starting cash is 0 — any opening capital is entered as a FISY-011 financing amount in month 0); `ending_balance[m] = ending_balance[m-1] + net_change[m]` for `m > 0`.
    - Flow: User opens the Cash Flow tab → the statement computes fresh from all upstream domains and renders as a 60-month table.
    - Edge cases: Any upstream series with gaps/nulls is already 0-filled by its own service, so no special handling needed here. `ending_balance` going negative is a valid, expected result (a projected cash shortfall) — displayed as-is, not an error.
    - Non-functional: Aggregating 7 series × 60 months × a handful of activities/roles/charges/investments is cheap enough to recompute on every tab load; no caching needed at this scale.
    - Out of scope: extended cash-flow lines — VAT, R&D credits, subcontracting, de-minimis (FISY-034, P2); the annual sources-and-uses funding plan (FISY-032, P2) is a separate statement, not part of this monthly cash flow.

- [ ] **FISY-034** `[D5]` Extended cash-flow lines
  - Type: feature
  - Priority: P2
  - Description: Add VAT encaissée/décaissée, additional named financing sources, CIR/CII/CICE cash-in, incubator advance repayment, subcontracting outflows, and EU de-minimis tracking to the cash-flow statement.
  - Acceptance criteria: Given a project above STARTER tier with the relevant domains configured, the cash-flow statement includes each of these lines with correct monthly values.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/34

- [ ] **FISY-035** `[D6]` VAT (TVA) engine
  - Type: feature
  - Priority: P2
  - Description: Automatic VAT receivable/payable computation per activity and generically, and its effect on working capital.
  - Acceptance criteria: Given VAT rates (FISY-010) and revenue/cost/investment flows, the app computes monthly VAT payable/receivable and the resulting BFR impact (F7.4).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/35

- [ ] **FISY-036** `[D6]` Corporate income tax (IS) computation
  - Type: feature
  - Priority: P2
  - Description: Compute corporate income tax using the current French bracket logic (reduced rate up to a threshold, standard rate above).
  - Acceptance criteria: Given a computed pre-tax result, the app applies the current statutory IS brackets and produces the resulting Résultat Net in the P&L (F7.2).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/36

- [ ] **FISY-037** `[D6]` Statutory payroll/business taxes
  - Type: feature
  - Priority: P2
  - Description: Compute taxe d'apprentissage, participation à la formation continue, effort de construction, C3S, CFE, and CVAE per their real statutory formulas and thresholds.
  - Acceptance criteria: Given payroll, revenue, and value-added figures, each of the six taxes is computed automatically using current statutory rates/thresholds and appears as a P&L/cash-flow line.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/37

- [ ] **FISY-038** `[D6]` JEI eligibility & exemption engine
  - Type: feature
  - Priority: P2
  - Description: Compute the JEI R&D-expense eligibility ratio and, if eligible, apply the payroll-tax exemption (capped per employee/company) and the IS exemption schedule (100%/50%/0% by year).
  - Acceptance criteria: Given an INNOVATION-tier project's R&D-eligible expenses, the app determines JEI eligibility (ratio > 15%) and, if eligible, applies the correct exemption caps and schedule.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/38

- [ ] **FISY-039** `[D6]` CIR/CII/CICE R&D tax-credit computation
  - Type: feature
  - Priority: P2
  - Description: Compute the three R&D tax credits from the eligible base (payroll, equipment depreciation, weighted subcontracting per FISY-028/029), net of subsidy/advance deductions, subject to statutory caps.
  - Acceptance criteria: Given R&D-eligible payroll, equipment, and subcontracting costs, the app computes CIR, CII, and CICE credit amounts, each net of applicable deductions and caps.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/39

- [ ] **FISY-040** `[D6]` EU de-minimis state-aid ceiling tracking
  - Type: feature
  - Priority: P2
  - Description: Track cumulative state aid received against the EU de-minimis ceiling.
  - Acceptance criteria: Given subsidies and R&D tax credits received, the app tracks the running total against the de-minimis ceiling and flags when it's exceeded.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/40

- [ ] **FISY-041** `[D7]` Break-even & ratios dashboard
  - Type: feature
  - Priority: P1
  - Description: Point mort (break-even, as an amount and as %CA), CA/marge brute/EBE/REx summary with %CA for each, and three ratios (debt/capital, debt/REx, dividend/capital) with guidance text on how to read each — matching STARTER's Synthèse.
  - Acceptance criteria: Given a STARTER-tier project's configured domains, the dashboard displays break-even, the CA/marge brute/EBE/REx summary, and the three ratios with their guidance text.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/41
  - Spec:
    - **Scope gap surfaced while speccing this issue:** the acceptance criteria requires a dividend/capital ratio, but no issue anywhere in D1–D8 captures a "dividends distributed" figure — it doesn't exist in the backlog. Rather than bounce this whole issue back to gws-issue-define for one missing field, this spec adds the minimal input needed (a yearly dividend amount) since it's the same size as other small config fields already scoped elsewhere. Flagging it explicitly here rather than folding it in silently.
    - Interfaces:
      - New "Synthesis" tab on `/projects/[project_id]`. `SynthesisState(rx.State)`: `@rx.var break_even_by_year: List[Optional[Decimal]]`, `break_even_pct_ca_by_year: List[Optional[Decimal]]`, `summary_metrics: List[SynthesisMetricRow]` (CA, Marge brute, EBE, REx — each a row with yearly values + %CA), `ratios: List[SynthesisRatioRow]` (the 3 ratios, yearly). `@dataclass SynthesisMetricRow: label: str; values_by_year: List[Decimal]; pct_of_ca_by_year: List[Decimal]` and `@dataclass SynthesisRatioRow: label: str; values_by_year: List[Optional[Decimal]]; guidance_text: str` (per the Reflex convention of preferring `@dataclass` over `dict` for structured display data).
      - Financing tab gains a small "Dividends distributed" row — one editable amount per year (5 columns, not 60 months; a dividend is inherently an annual decision, unlike the monthly-throughout data elsewhere). `set_dividend_amount(year_index: int, amount: str)`.
    - Data model:
      - `financing/dividend_distribution.py:DividendDistribution(ModelWithUser)`: `project = ForeignKeyField(Project, on_delete="CASCADE", backref="dividend_distributions")`, `year_index: PositiveSmallIntegerField()` (0–4), `amount: DecimalField(max_digits=12, decimal_places=2, default=0)`. Unique `(project, year_index)`.
      - `financing/dividend_distribution_service.py:DividendDistributionService.set_amount(project_id, year_index, amount, user) -> DividendDistribution`, `.list_by_year(project_id, user) -> List[Decimal]` (5 values, 0-filled).
      - No other new tables — the rest is pure computation in `synthesis/synthesis_calculation_service.py:SynthesisCalculationService`, aggregating every upstream P1 service into yearly figures (12-month windows over months 0–11, 12–23, …, 48–59):
        - `CA[year]` = sum of FISY-015 monthly revenue. `variable_costs[year]` = sum of FISY-015 monthly variable cost. `marge_brute[year] = CA[year] − variable_costs[year]`.
        - `external_charges[year]` = sum of FISY-024 monthly cost. `personnel_costs[year]` = sum of FISY-021 monthly payroll cost. `EBE[year] = marge_brute[year] − external_charges[year] − personnel_costs[year]` (mirrors the source spreadsheet's coaching text, "EBE = Revenus − Charges externes et de personnels", read together with Marge brute as an intermediate CA-minus-variable-costs step).
        - `depreciation[year]` = sum of FISY-025 monthly depreciation. `REx[year] = EBE[year] − depreciation[year]`.
        - Each of CA/marge brute/EBE/REx also reported as `% of CA[year]` (undefined/`None` when `CA[year] == 0`).
        - **Break-even (known simplification, flagged rather than silently precise):** `fixed_costs[year] = personnel_costs[year] + external_charges[year] + depreciation[year]` (treats all external charges, including any headcount-driven variable component, as fixed for this purpose — a deliberate STARTER-tier simplification, not a rigorous fixed/variable cost split); `contribution_margin_rate[year] = marge_brute[year] / CA[year]` (undefined when `CA[year] == 0`); `break_even[year] = fixed_costs[year] / contribution_margin_rate[year]` (undefined when the rate is undefined or zero); `break_even_pct_ca[year] = break_even[year] / CA[year]`.
        - `debt_over_capital[year] = net_debt_by_year[year] (FISY-030) / cumulative_capital_by_year[year]` (cumulative sum of FISY-011's CAPITAL-type entries through that year's end; undefined when cumulative capital is 0).
        - `debt_over_rex[year] = net_debt_by_year[year] / REx[year]` (undefined when `REx[year] == 0`).
        - `dividend_over_capital[year] = dividends_by_year[year] / cumulative_capital_by_year[year]` (undefined when cumulative capital is 0).
        - Guidance text for each ratio is a short static string (e.g. "Generally OK under 200%" for debt/capital, "Usually OK under 500%" for debt/REx, mirroring the source spreadsheet's inline notes) — exact wording finalized at implementation time from `specs/FISY-STARTER.xls`'s Synthèse sheet, column I.
    - Flow: User opens the Synthesis tab → all figures compute fresh from every upstream P1 domain and render as a 5-year table (one column per year, matching the yearly cadence of this dashboard even though underlying data is monthly).
    - Edge cases: Any ratio whose denominator is 0 → shown as "N/A" in the UI, not an error and not a computed `0`/`Infinity`. A project with no configured revenue/costs yet → all figures show as 0 or N/A, not an error.
    - Non-functional: Same cheap-recompute-on-load approach as FISY-033; no caching needed at this scale.
    - Out of scope: the with/without-state-aid break-even split (FISY-045, INNOVATION-only, P2); per-activity profitability analytics (FISY-046, P2); forecast charts (FISY-047, P2) — this issue is the tabular dashboard only.

- [ ] **FISY-042** `[D7]` Full P&L statement
  - Type: feature
  - Priority: P2
  - Description: Complete Comptes de résultats: CA → achats et charges de production → marge brute → charges externes → valeur ajoutée → charges de personnel → EBE → dotations aux amortissements → REx → charges financières → résultat courant → IS → résultat net.
  - Acceptance criteria: Given a project above STARTER tier with all domains configured, the app generates a full P&L down to résultat net, matching each intermediate line.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/42

- [ ] **FISY-043** `[D7]` Balance sheet
  - Type: feature
  - Priority: P2
  - Description: Automatic assets (immobilisations, stocks, créances, trésorerie) vs. liabilities (capital, dettes, réserves) statement.
  - Acceptance criteria: Given a project above STARTER tier, the app generates a balance sheet for each period that balances (assets = liabilities + equity).
  - GitHub: https://github.com/Constellab/gws_fisy/issues/43

- [ ] **FISY-044** `[D7]` Working capital requirement (BFR)
  - Type: feature
  - Priority: P2
  - Description: Per-activity and total BFR, computed from receivables/payables timing (including VAT-related BFR from F6.1).
  - Acceptance criteria: Given per-activity payment timing and VAT config, the app computes BFR per activity and in total, per period.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/44

- [ ] **FISY-045** `[D7]` Break-even split with/without state aid
  - Type: feature
  - Priority: P2
  - Description: Show break-even both including and excluding CIR/JEI/subsidies, for INNOVATION-tier projects.
  - Acceptance criteria: Given an INNOVATION-tier project with R&D credits/JEI/subsidies configured, the dashboard shows both a "with state aid" and "without state aid" break-even figure.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/45

- [ ] **FISY-046** `[D7]` Per-activity profitability & funding-need analytics
  - Type: feature
  - Priority: P2
  - Description: Breakdown of CA/marge brute/EBE/REx by activity (with % of total), and a ratio of cumulative EBE to cumulative funding need, per activity.
  - Acceptance criteria: Given an INNOVATION-tier project with multiple activities, the app shows each activity's CA/marge brute/EBE/REx and its cumulative-EBE-to-funding-need ratio.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/46

- [ ] **FISY-047** `[D7]` Forecast charts
  - Type: feature
  - Priority: P2
  - Description: Visualizations of results (CA/EBE/REx) and treasury/BFR over the 5-year horizon.
  - Acceptance criteria: Given a project above STARTER tier with computed statements, the app displays a results chart and a treasury/BFR chart covering all 5 years.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/47

- [ ] **FISY-048** `[D8]` Actuals entry
  - Type: feature
  - Priority: P2
  - Description: Monthly actual-value entry for orders, cash-received revenue, gross margin, payroll, headcount, and cash.
  - Acceptance criteria: For any past month, a user can enter actual values for each tracked metric.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/48

- [ ] **FISY-049** `[D8]` Forecast-vs-actual variance tracking
  - Type: feature
  - Priority: P2
  - Description: Cumulative variance computation and display between forecast and actuals, per tracked metric.
  - Acceptance criteria: Given actuals entered (FISY-048), the app displays forecast, cumulative forecast, actual, cumulative actual, and cumulative variance for each metric.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/49

- [ ] **FISY-050** `[D8]` Custom KPI tracking
  - Type: feature
  - Priority: P2
  - Description: A user-defined custom indicator tracked alongside the fixed metrics in FISY-049.
  - Acceptance criteria: A user can define a custom KPI label and enter forecast/actual values for it, tracked the same way as the fixed metrics.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/50

- [ ] **FISY-051** `[D8]` Business-plan export (CSV/Excel)
  - Type: feature
  - Priority: P2
  - Description: Export a project's assumptions and computed statements (P&L, balance sheet, cash flow, etc.) as CSV/Excel data.
  - Acceptance criteria: Given a project with computed statements, the user can trigger an export that produces a CSV/Excel file containing the assumptions and all generated statement tables.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/51

### Ongoing
_(none yet)_

### Doing
_(none yet)_

### Done

- [x] **FISY-052** `[D9]` Left sidebar app shell
  - Type: feature
  - Priority: P0
  - Description: A fixed left sidebar (branding + top-level navigation) and a shared page-layout wrapper every page uses, modeled on gws_care's `page_layout()`/`SidebarFoldState` pattern. App-level shell only — the tabbed in-project navigation from FISY-001 is unaffected.
  - Acceptance criteria: Given any page in the app, the page renders wrapped in a fixed left sidebar showing the app's branding and a "Projects" link (highlighted active when on a projects route), with a working fold/unfold toggle.
  - GitHub: https://github.com/Constellab/gws_fisy/issues/52
  - Spec:
    - Interfaces:
      - Scaffolds the Reflex app itself (`gws reflex generate fisy_app` inside `bricks/gws_fisy/src/gws_fisy/`), since no app code exists yet in this brick — this issue and FISY-001 both need the app to exist; the shell is built first since every page wraps in it.
      - New shared module `fisy_app/common/page_layout.py`, directly mirroring gws_care's `care_app/common/page_layout.py`:
        - `SidebarFoldState(rx.State)`: `is_folded: bool = False`; `toggle()`, `fold()`, `unfold()`; `@rx.var def current_path(self) -> str: return self.router.page.path`. (Named to match gws_care's class exactly since it's scoped to this app's own module — not prefixed `Fisy` as originally planned.)
        - `_sidebar_content()`: app logo/name header + one nav section containing a single item, "Projects" → `/projects`, built with the **reused** core `menu_item_component` from `gws_reflex_main` (`gws_core/.../reflex_sidebar_menu_component.py`) for active-route highlighting — not reimplemented, per the research showing this is the established reusable primitive.
        - `page_layout(*children) -> rx.Component`: fixed sidebar (`position="fixed", left="0", top="0", height="100vh"`) plus a margin-offset content area (`margin_left=sidebar_width`), reusing gws_care's exact width constants and transition style (`_SIDEBAR_FULL = "300px"`, `_SIDEBAR_FOLDED = "60px"`, `transition: width/margin-left 0.22s ease`).
      - Every page component wraps its body as `main_component(page_layout(<page content>))` — same convention as gws_care (`main_component` from `gws_reflex_main` is the outer auth/init gate; `page_layout` is the inner shell).
      - A minimal placeholder `/projects` page (an empty page with a heading) is created purely so there's a route for the sidebar to link to and highlight — its real content (project list, create dialog) is FISY-001's scope, not this issue's.
      - A `/` route added beyond the original spec, purely so the bare app URL lands somewhere useful: redirects to `/projects` via `rx.redirect` on mount.
    - Data model: None — pure UI/state, no persistence.
    - Flow: User loads any route → the page component wraps its content in `page_layout()` → sidebar renders with branding and the "Projects" link, highlighted active on `/projects` or any `/projects/*` route → clicking the fold toggle collapses the sidebar to icon-only width (`60px`) and back.
    - Edge cases: None beyond standard fold/unfold toggling — no data-driven states to handle since there's no persistence here.
    - Non-functional: none beyond the standard `main_component` auth/init gate already used by every Reflex app in this repo.
    - Out of scope (deliberately deferred, following gws_care's pattern but not reproducing what gws_fisy doesn't need yet): role-gated nav groups (gws_fisy has no roles/`RoleState` concept); badge counts (no notifications/messaging feature exists); per-group collapse (nothing to collapse with a single flat nav item); the responsive JS-resize-to-hidden-button auto-fold bridge (a real technique worth reusing later, not built now for a one-link sidebar); a user-menu footer with role-switching (gws_fisy has no roles to switch between) — a simple future "signed in as X" footer is a candidate for a later issue, not designed here.
  - Implementation notes: Fixed a gap found in gws_care's actual `page_layout.py` — its unfolded sidebar header has no visible fold button (only an auto-fold-on-resize JS bridge), so a user can't manually re-fold once unfolded. gws_fisy's version adds an explicit toggle button in both folded and unfolded header states, since this issue's acceptance criteria requires a working toggle in both directions. Verified by running the app in dev mode and screenshotting `/projects` unfolded, folded, and re-unfolded, plus confirming `/` redirects to `/projects` — all matched expectations with no console errors.
