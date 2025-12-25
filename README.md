# Constellab Fisy

**Fisy** is a comprehensive financial forecasting and modeling application built with Reflex. It provides an intuitive interface for creating financial projections, analyzing cash flows, and generating detailed financial statements.

## Overview

Constellab Fisy enables users to build complete financial models by entering assumptions about their business operations, and automatically generates professional financial statements and visualizations. The application is designed for entrepreneurs, financial analysts, and business planners who need to forecast their financial performance.

## Credits

This application is a web-based translation of the **Fisy Excel spreadsheet**, originally created by [Rémi BERTHIER](https://fisy.fr). We extend our heartfelt gratitude to Rémi for developing such an excellent and comprehensive financial modeling tool that has helped countless entrepreneurs plan their ventures. This Reflex application brings the power of Fisy to the web, making it more accessible and collaborative within the Constellab platform.

For more information about the original Fisy tool, visit: [https://fisy.fr](https://fisy.fr)

## Features

### 📊 Comprehensive Financial Modeling
- **Income Statement (P&L)**: Detailed profit and loss projections with revenue and expense tracking
- **Cash Flow Analysis**: Monitor cash movements and liquidity over time
- **Balance Sheet**: Track assets, liabilities, and equity
- **Funding Plan**: Plan and visualize financing needs and sources

### 💼 Input Management
- **Activities & Revenue Streams**: Define your core business activities and pricing models
- **One-time Sales**: Track individual sales transactions
- **Subscriptions**: Model recurring revenue with MRR tracking
- **Staff & Personnel**: Plan headcount and associated costs
- **External Charges**: Manage operational expenses
- **Investments**: Capital expenditure planning
- **Funding Sources**: Model various financing options

### 📈 Visualization & Analysis
- **Interactive Charts**: Switch between line and bar charts
- **Flexible Time Periods**: View data by month or year
- **Multi-unit Display**: View amounts in units, thousands (k€), or millions (M€)
- **Responsive Design**: Fixed headers, fixed sidebar navigation, and smooth scroll preservation

### 🌐 Internationalization
- Full support for English and French
- Configurable currency and display preferences

## Technical Stack

- **Framework**: Reflex 0.8.14.post1
- **Backend**: Python with async support
- **Frontend**: React-based components via Reflex
- **State Management**: Reflex reactive state system
- **Charts**: Recharts integration
- **Styling**: Radix UI theming

## Project Structure

```
gws_fisy/
├── src/
│   └── gws_fisy/
│       ├── core/                      # Core database and models
│       │   ├── fisy_db_manager.py    # Database management
│       │   └── model_with_user.py    # User-aware models
│       ├── scenario/                  # Scenario management
│       │   ├── scenario.py           # Scenario model
│       │   ├── scenario_dto.py       # Data transfer objects
│       │   └── scenario_service.py   # Business logic
│       ├── user/                      # User management
│       │   ├── user.py               # User model
│       │   └── fisy_user_sync_service.py
│       └── fisy_app/                  # Reflex application
│           ├── generate_fisy_app.py  # App generator task
│           └── _fisy_app/            # App root
│               ├── rxconfig.py       # Reflex configuration
│               ├── dev_config.json   # Development config
│               └── fisy_app/         # Main app package
│                   ├── fisy_app.py   # Entry point
│                   ├── state.py      # Application state
│                   ├── i18n/         # Translations
│                   ├── calc/         # Calculation engine
│                   └── pages/        # UI pages
│                       ├── layout.py # Layout & navigation
│                       ├── config.py # Configuration page
│                       ├── index.py  # Home page
│                       ├── input/    # Input pages
│                       └── results/  # Results pages
├── tests/                             # Test suite
└── settings.json                      # Brick settings
```

## Getting Started

### Prerequisites
- Python 3.10+
- GWS Core framework
- Reflex 0.8.14.post1

### Running in Development Mode

1. Navigate to the brick directory:
```bash
cd bricks/gws_fisy
```

2. Run the Reflex app with the development configuration:
```bash
gws reflex run src/gws_fisy/fisy_app/_fisy_app/dev_config.json
```

The app features a **fixed sidebar** that remains visible during navigation, with scroll position preservation for improved user experience.

3. Wait for the initialization (approximately 20 seconds). The app is ready when you see:
```
Running app in dev mode, DO NOT USE IN PRODUCTION. You can access the app at http://...
```

4. Open the URL in your browser to access the application.

### Running Tests

From the brick directory:
```bash
gws server test all
```

Or run a specific test:
```bash
gws server test test_scenario
```

## Configuration

The application supports the following configuration parameters (defined in `dev_config.json` or passed via Constellab):

- `app_title`: Custom application title
- `language`: Default language (en/fr)
- `currency`: Display currency
- `scale`: Amount display scale (units/thousands/millions)

## Usage

### Basic Workflow

1. **Configure**: Set your general parameters (language, currency, display preferences)
2. **Define Activities**: Create your revenue-generating activities
3. **Add Revenue**: Enter one-time sales and subscriptions
4. **Plan Expenses**: Add staff, external charges, and investments
5. **Model Funding**: Configure financing sources
6. **Analyze Results**: Review charts and tables in the Results section

### Key Concepts

- **Scenario-based**: All data is organized into scenarios for easy comparison
- **Real-time Calculations**: Financial statements update automatically as you enter data
- **User-specific Data**: Each user maintains their own scenarios and data
- **Persistent Storage**: All data is saved to the database automatically

## Architecture Highlights

### State Management
- Centralized state in `state.py` with reactive computed variables
- Automatic UI updates when state changes
- Background processing for database operations

### Calculation Engine
The `calc/` module contains:
- **engine.py**: Core financial calculation logic
- **models.py**: Financial data structures
- **sale_ranges.py**: Revenue modeling utilities

### Database Layer
- User-aware models with automatic user context
- Transaction support for data integrity
- Efficient querying with SQLAlchemy

## Contributing

When contributing to this brick:
- Follow the existing code patterns and conventions
- Add type hints to all functions and methods
- Write comprehensive docstrings in Markdown format
- Add tests for new functionality
- Update this README for significant feature additions

## License

Part of the Constellab platform.
