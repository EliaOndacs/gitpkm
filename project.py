import os
from pathlib import Path
import json
from typing import List, TypedDict
from pydantic import BaseModel, ValidationError


class _GitRepo(TypedDict):
    url: str
    dir: str


class GitRepo(BaseModel):
    url: str
    dir: str


class _GitConfigurations(TypedDict):
    repositories: List[_GitRepo]
    name: str
    description: str
    version: str


class GitConfigurations(BaseModel):
    name: str
    description: str
    version: str
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
        config = GitConfigurations(**json_data, name=json_data["name"], description=json_data["description"], version=json_data["version"])  # type: ignore # Validate and parse the data
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
    cwd = Path(os.getcwd())

    with open("git-package.json", "w") as file:
        json.dump(
            {
                "repositories": [],
                "name": cwd.name,
                "description": "YOUR PROJECT DESCRIPTION",
                "version": "0.1.0",
            },
            file,
            indent=4,
        )
