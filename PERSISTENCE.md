# FISY Data Persistence Architecture

## Overview

FISY now implements database persistence using the same architecture as gws_project, storing user data and configuration permanently using Peewee ORM.

## Architecture Components

### 1. Database Manager (`core/fisy_db_manager.py`)
- **FisyDbManager**: Singleton database manager inheriting from `LazyAbstractDbManager`
- Manages database connection and initialization
- Uses Peewee `DatabaseProxy` for lazy connection

### 2. Base Model (`core/model_with_user.py`)
- **ModelWithUser**: Base class for all FISY models
- Automatically tracks:
  - `created_by`: User who created the record (FK to local User)
  - `last_modified_by`: User who last modified the record (FK to local User)
  - `created_at`: Creation timestamp
  - `last_modified_at`: Last modification timestamp
- Uses hooks `_before_insert()` and `_before_update()` for automatic user tracking

### 3. User Model and Sync (`user/user.py`, `user/fisy_user_sync_service.py`)
- **User**: Local User model in FISY database (mirrors gws_core User structure)
- **FisyUserSyncService**: Auto-syncs users from gws_core to FISY database
- Decorated with `@event_listener` to automatically sync on user events
- **Why local User?**: Peewee foreign keys require models in same database

### 4. Scenario Model (`scenario/scenario.py`)
- **Scenario**: Main model storing all financial planning data
- **Fields:**
  - Basic info: `title`, `description`
  - Configuration: `months`, `tva_default`, `start_year`, `start_month`, `dso_days`, `dpo_days`, `dio_days`, `initial_cash`
  - UI preferences: `language_code`, `currency_code`, `scale_mode`
  - Data (JSON): `activities`, `one_time_ranges`, `subscription_ranges`, `personnel`, `charges`, `investments`, `loans`, `capital_injections`, `subsidies`
- **Table:** `gws_fisy_scenarios`

### 5. DTO (`scenario/scenario_dto.py`)
- **ScenarioDTO**: Data transfer object for API responses (inherits from `BaseModelDTO`)
- Includes all scenario fields plus user and timestamp metadata

### 6. Service Layer (`scenario/scenario_service.py`)
- **ScenarioService**: Business logic for scenario management
- **Methods:**
  - `create_scenario()`: Create new scenario
  - `get_scenario()`: Retrieve by ID
  - `get_scenario_dto()`: Get DTO representation
  - `update_scenario()`: Update fields
  - `delete_scenario()`: Delete scenario
  - `list_user_scenarios()`: List user's scenarios
  - `save_state_to_scenario()`: Save Reflex state to database

### 7. State Integration (`fisy_app/state.py`)
- **Reflex State** now persists data automatically
- **New fields:**
  - `current_scenario_id`: Active scenario ID
- **Lifecycle:**
  1. `on_load()`: Load or create scenario on app start
  2. `_load_scenario()`: Load from database
  3. `_create_default_scenario()`: Create with sample data
  4. `_save_scenario()`: Auto-save on data changes
- **Auto-save triggers:** All state mutation methods now marked with `@rx.event(background=True)` and call `_save_scenario()`
- **Type conversions:** Peewee fields converted to Python types when loading (e.g., `int(scenario.months)`)

## Key Implementation Details

### Transaction Management
Uses `@FisyDbManager.transaction()` decorator (not context manager):
```python
@staticmethod
@FisyDbManager.transaction()
def create_scenario(title: str, **config) -> Scenario:
    scenario = Scenario.create(title=title, **config)
    return scenario
```

### DTO Conversion
The `to_dto()` method explicitly casts Peewee fields to Python types:
```python
def to_dto(self) -> ScenarioDTO:
    return ScenarioDTO(
        id=str(self.id),
        months=int(self.months),  # type: ignore - Peewee field conversion
        tva_default=float(self.tva_default),  # type: ignore
        # ... other fields
    )
```

## Data Flow

### Initial Load
```
1. User opens app
2. on_load() checks for scenario_id in params
3. If exists: Load scenario from DB
4. If not: Create default scenario with sample data
5. Convert JSON data to dataclass instances
6. Populate Reflex state
```

### Data Modification
```
1. User edits data (e.g., adds personnel)
2. Event handler updates Reflex state
3. async with self: block ensures state consistency
4. _save_scenario() converts dataclasses to dicts
5. ScenarioService.save_state_to_scenario() persists to DB
6. UI updates reactively
```

## Key Differences from gws_project

| Aspect | gws_project | gws_fisy |
|--------|-------------|----------|
| **Data Model** | Multiple models (Project, Task) with relations | Single Scenario model with JSON fields |
| **Granularity** | Fine-grained relational data | Denormalized JSON storage |
| **Relationships** | ForeignKeys between models | Embedded data structures |
| **Use Case** | Complex hierarchical tasks | Financial calculation snapshots |

## Configuration

### Development Mode
In `dev_config.json`, optionally specify:
```json
{
  "params": {
    "scenario_id": "existing-scenario-id",
    "app_title": "My Financial App",
    "corporate_tax_rate": "0.25",
    "months": "60"
  }
}
```

### Production Mode
Scenario ID passed via Constellab task parameters.

## User Isolation

- Each scenario is linked to `created_by` user
- Users can only see/edit their own scenarios (when list_user_scenarios filtered by user_id)
- Automatic user tracking on all modifications

## Best Practices

1. **Always use Service Layer**: Never directly manipulate Scenario model from state
2. **Transaction Decorator**: Use `@FisyDbManager.transaction()` decorator (not `with transaction()` context)
3. **Error Handling**: State methods fail silently to avoid UI disruption
4. **Type Conversion**: Always convert Peewee fields to Python types when loading (use `int()`, `str()`, `float()`)
5. **JSON Serialization**: Use `vars()` to convert dataclasses to dicts before saving
6. **DTO Base Class**: Use `BaseModelDTO` from gws_core (not `BaseDTO`)

## Future Enhancements

- Scenario versioning/history
- Collaborative editing
- Scenario templates
- Export/import functionality
- Scenario comparison
