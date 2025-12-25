"""
Service layer for Scenario management.

Handles business logic for creating, reading, updating, and deleting scenarios.
"""

from typing import Optional

from ..core.fisy_db_manager import FisyDbManager
from .scenario import Scenario
from .scenario_dto import ScenarioDTO


class ScenarioService:
    """Service for managing financial scenarios."""

    @staticmethod
    @FisyDbManager.transaction()
    def create_scenario(
        title: str,
        description: str | None = None,
        **config_data
    ) -> Scenario:
        """
        Create a new scenario with default values.

        :param title: Scenario title
        :param description: Scenario description
        :param config_data: Additional configuration data
        :return: Created scenario
        """
        scenario = Scenario.create(
            title=title,
            description=description,
            **config_data
        )
        return scenario

    @staticmethod
    def get_scenario(scenario_id: str) -> Scenario:
        """
        Get scenario by ID.

        :param scenario_id: Scenario ID
        :return: Scenario instance
        :raises: DoesNotExist if scenario not found
        """
        return Scenario.get_by_id(scenario_id)

    @staticmethod
    def get_scenario_dto(scenario_id: str) -> ScenarioDTO:
        """
        Get scenario DTO by ID.

        :param scenario_id: Scenario ID
        :return: Scenario DTO
        """
        scenario = ScenarioService.get_scenario(scenario_id)
        return scenario.to_dto()

    @staticmethod
    @FisyDbManager.transaction()
    def update_scenario(scenario_id: str, **update_data) -> Scenario:
        """
        Update scenario data.

        :param scenario_id: Scenario ID
        :param update_data: Fields to update
        :return: Updated scenario
        """
        scenario = ScenarioService.get_scenario(scenario_id)
        for key, value in update_data.items():
            if hasattr(scenario, key):
                setattr(scenario, key, value)
        scenario.save()
        return scenario
    @staticmethod
    @FisyDbManager.transaction()
    def delete_scenario(scenario_id: str) -> None:
        """
        Delete a scenario.

        :param scenario_id: Scenario ID
        """
        scenario = ScenarioService.get_scenario(scenario_id)
        scenario.delete_instance()
    @staticmethod
    def list_user_scenarios(user_id: str | None = None) -> list[Scenario]:
        """
        List all scenarios for a user.

        :param user_id: User ID (if None, returns all scenarios)
        :return: List of scenarios
        """
        query = Scenario.select()
        if user_id:
            query = query.where(Scenario.created_by == user_id)
        return list(query.order_by(Scenario.last_modified_at.desc()))

    @staticmethod
    @FisyDbManager.transaction()
    def save_state_to_scenario(scenario_id: str, state_data: dict) -> Scenario:
        """
        Save state data to scenario.

        :param scenario_id: Scenario ID
        :param state_data: State data dictionary
        :return: Updated scenario
        """
        scenario = ScenarioService.get_scenario(scenario_id)

        # Update configuration fields
        if 'months' in state_data:
            scenario.months = state_data['months']
        if 'tva_default' in state_data:
            scenario.tva_default = state_data['tva_default']
        if 'start_year' in state_data:
            scenario.start_year = state_data['start_year']
        if 'start_month' in state_data:
            scenario.start_month = state_data['start_month']
        if 'dso_days' in state_data:
            scenario.dso_days = state_data['dso_days']
        if 'dpo_days' in state_data:
            scenario.dpo_days = state_data['dpo_days']
        if 'dio_days' in state_data:
            scenario.dio_days = state_data['dio_days']
        if 'initial_cash' in state_data:
            scenario.initial_cash = state_data['initial_cash']

        # Update UI preferences
        if 'language_code' in state_data:
            scenario.language_code = state_data['language_code']
        if 'currency_code' in state_data:
            scenario.currency_code = state_data['currency_code']
        if 'scale_mode' in state_data:
            scenario.scale_mode = state_data['scale_mode']

        # Update data lists
        if 'activities' in state_data:
            scenario.activities = state_data['activities']
        if 'one_time_ranges' in state_data:
            scenario.one_time_ranges = state_data['one_time_ranges']
        if 'subscription_ranges' in state_data:
            scenario.subscription_ranges = state_data['subscription_ranges']
        if 'personnel' in state_data:
            scenario.personnel = state_data['personnel']
        if 'charges' in state_data:
            scenario.charges = state_data['charges']
        if 'investments' in state_data:
            scenario.investments = state_data['investments']
        if 'loans' in state_data:
            scenario.loans = state_data['loans']
        if 'capital_injections' in state_data:
            scenario.capital_injections = state_data['capital_injections']
        if 'subsidies' in state_data:
            scenario.subsidies = state_data['subsidies']

        scenario.save()
        return scenario
