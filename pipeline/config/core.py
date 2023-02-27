from pathlib import Path
from pydantic import BaseModel
from strictyaml import YAML, load
from typing import Dict

CONFIG_ROOT = Path(__file__).resolve().parent
CONFIG_FILE_PATH = CONFIG_ROOT / "config.yml"


class PipelineConfig(BaseModel):
    '''
    All configurations relevant to
    image transformations and solver.
    '''

    solver_mappings: Dict[str, str]
    image_mappings: Dict[str, int]
    percent_fill_thresh: float


class Config(BaseModel):
    '''
    Master config object.
    '''

    pipeline_config: PipelineConfig


def fetch_config_from_yaml() -> YAML:
    '''
    Parse YAML.
    '''

    try:
        with open(CONFIG_FILE_PATH, "r") as config_file:
            parsed_config = load(config_file.read())
            return parsed_config
    except:
        raise OSError(f"Did not find config file at path: {CONFIG_FILE_PATH}")


def create_and_validate_config() -> Config:
    '''
    Run validation on config values.
    '''
    parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        pipeline_config=PipelineConfig(**parsed_config.data)
    )
    return _config


config = create_and_validate_config()