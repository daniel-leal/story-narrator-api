from uuid import UUID

import pytest

from app.scenario.domain.entities.scenario import Scenario


def test_scenario_initialization():
    scenario_id = UUID("12345678-1234-5678-1234-567812345678")
    scenario_name = "Enchanted Forest"
    scenario_description = "A magical forest where trees whisper secrets..."

    scenario = Scenario(
        id=scenario_id, name=scenario_name, description=scenario_description
    )

    assert scenario.id == scenario_id
    assert scenario.name == scenario_name
    assert scenario.description == scenario_description


def test_scenario_name_validation():
    scenario_id = UUID("12345678-1234-5678-1234-567812345678")
    scenario_description = "A magical forest where trees whisper secrets..."

    with pytest.raises(ValueError):
        Scenario(id=scenario_id, name="", description=scenario_description)


def test_scenario_description_validation():
    scenario_id = UUID("12345678-1234-5678-1234-567812345678")
    scenario_name = "Enchanted Forest"

    with pytest.raises(ValueError):
        Scenario(id=scenario_id, name=scenario_name, description="")
        Scenario(id=scenario_id, name=scenario_name, description="")
