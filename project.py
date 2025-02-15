import os
from pathlib import Path
import json
from typing import List, TypedDict
from pydantic import BaseModel, ValidationError


class _GitRepo(TypedDict):
    url: str
    target_dir: str


class GitRepo(BaseModel):
    url: str
    target_dir: str


class _GitConfigurations(TypedDict):
    repositories: List[_GitRepo]


class GitConfigurations(BaseModel):
    repositories: List[GitRepo]


def get_config_raw() -> _GitConfigurations:
    file = Path("git-package.json")
    if not file.exists():
        print(
            "error: `git-package.json` git package manager configuration file not found!"
        )
        os._exit(-1)
    return json.loads(file.read_text())


def get_config() -> GitConfigurations:
    try:
        json_data: _GitConfigurations = get_config_raw()
        for index, repo in enumerate(json_data["repositories"]):
            json_data["repositories"][index] = GitRepo(**repo)  # type: ignore
        config = GitConfigurations(**json_data)  # type: ignore # Validate and parse the data
        return config
    except ValidationError as e:
        print("error: Invalid configuration data!")
        print(e.json())  # Print detailed validation errors
        os._exit(-1)
    except json.JSONDecodeError as e:
        print("error: Failed to decode JSON!")
        print(e)
        os._exit(-1)


def overwrite_config_raw(data: _GitConfigurations):
    with open("git-package.json", "w") as f:
        json.dump(data, f, indent=4)


def overwrite_config(data: GitConfigurations):
    with open("git-package.json", "w") as f:
        json.dump(data.model_dump(), f, indent=4)


def new_proj():
    with open("git-package.json", "w") as file:
        json.dump({"repositories": []}, file, indent=4)
