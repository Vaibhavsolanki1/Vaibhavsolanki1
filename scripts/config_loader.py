"""
GitHub Profile 2.0 - Configuration Loader

Type-safe YAML parser using Pydantic schemas to load and validate config.yml.
"""

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class ProfileConfigModel(BaseModel):
    name: str
    title: str
    identity: list[str] = Field(default_factory=list)
    status: str
    location: str
    focus: str
    availability: str = "Open to opportunities"


class DesignConfigModel(BaseModel):
    accent_color: str = "#58A6FF"
    theme: str = "dark"
    font_family: str = "JetBrains Mono"


class GitHubConfigModel(BaseModel):
    username: str
    data_mode: str = "live"


class ProjectItemModel(BaseModel):
    name: str
    description: str
    status: str = "Active"
    tech: list[str] = Field(default_factory=list)
    url: str | None = None
    demo: str | None = None


class SystemConfigModel(BaseModel):
    cache_ttl: int = 86400
    log_level: str = "INFO"
    optimize_svg: bool = True
    output_dir: str = "generated"


class ProfileConfig(BaseModel):
    version: str = "2.0"
    profile: ProfileConfigModel
    design: DesignConfigModel = Field(default_factory=DesignConfigModel)
    github: GitHubConfigModel
    projects: list[ProjectItemModel] = Field(default_factory=list)
    system: SystemConfigModel = Field(default_factory=SystemConfigModel)


def load_config(config_path: Path | str = "config.yml") -> ProfileConfig:
    """Read, parse, and validate config.yml file into a ProfileConfig model."""
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {path.absolute()}")

    with open(path, encoding="utf-8") as f:
        raw_data = yaml.safe_load(f)

    if not raw_data:
        raise ValueError(f"Configuration file at {path} is empty.")

    return ProfileConfig(**raw_data)
