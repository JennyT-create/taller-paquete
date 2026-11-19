from pathlib import Path

import pytest
from pydantic import ValidationError

from hotel_booking.config import ProjectConfig

CONFIG_PATH = Path(__file__).parent.parent / "project_config.yml"


def test_carga_entorno_dev() -> None:
    cfg = ProjectConfig.from_yaml(str(CONFIG_PATH), env="dev")

    assert cfg.catalog == "mlops_dev"
    assert cfg.target == "average_price"


def test_entorno_invalido_falla() -> None:
    with pytest.raises(ValueError):
        ProjectConfig.from_yaml(str(CONFIG_PATH), env="produccion")


def test_learning_rate_cero_falla(tmp_path: Path) -> None:
    texto = CONFIG_PATH.read_text().replace("learning_rate: 0.05", "learning_rate: 0")
    config_malo = tmp_path / "config.yml"
    config_malo.write_text(texto)

    with pytest.raises(ValidationError):
        ProjectConfig.from_yaml(str(config_malo))


def test_learning_rate_alto_se_acepta(tmp_path: Path) -> None:
    texto = CONFIG_PATH.read_text().replace("learning_rate: 0.05", "learning_rate: 0.5")
    config_alto = tmp_path / "config.yml"
    config_alto.write_text(texto)

    cfg = ProjectConfig.from_yaml(str(config_alto))

    assert cfg.parameters.learning_rate == 0.5
