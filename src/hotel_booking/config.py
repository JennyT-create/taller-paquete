"""Configuración del proyecto, leída desde project_config.yml."""

import yaml
from pydantic import BaseModel, Field


class Parameters(BaseModel):
    """Hiperparámetros del modelo, con rangos válidos."""

    learning_rate: float = Field(gt=0, le=0.2)
    n_estimators: int = Field(ge=10, le=10000)
    max_depth: int = Field(ge=1, le=50)


class ProjectConfig(BaseModel):
    """Configuración del proyecto para un entorno (dev, acc o prd)."""

    num_features: list[str]
    cat_features: list[str]
    target: str
    catalog: str
    schema_name: str
    parameters: Parameters

    @classmethod
    def from_yaml(cls, config_path: str, env: str = "dev") -> "ProjectConfig":
        """Lee el archivo YAML y devuelve la configuración del entorno pedido."""
        if env not in ["dev", "acc", "prd"]:
            raise ValueError(f"Entorno no válido: {env}. Se espera 'dev', 'acc' o 'prd'.")

        with open(config_path) as f:
            config_dict = yaml.safe_load(f)
        config_dict["catalog"] = config_dict[env]["catalog"]
        config_dict["schema_name"] = config_dict[env]["schema"]
        for key in ["dev", "acc", "prd"]:
            config_dict.pop(key)
        return cls(**config_dict)
