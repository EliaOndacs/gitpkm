import os
import sys
import click
from git_cmd import useGit  # pack: ignore
from project import (  # pack: ignore
    _GitConfigurations,  # pack: ignore
    get_config,  # pack: ignore
    get_config_raw,  # pack: ignore
    new_proj,  # pack: ignore
    overwrite_config_raw,  # pack: ignore
)  # pack: ignore
from rich import get_console

console = get_console()


# Function to disable stdout and stderr
def disable_output():
    # Redirect stdout and stderr to os.devnull
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")


# Function to restore stdout and stderr
def restore_output():
    # Restore stdout and stderr to their original values
    sys.stdout.close()
    sys.stderr.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__


@click.group
@click.option("--quiet", is_flag=True, help="Run in quiet mode.")
def cli(quiet):
    """
    a package manager for git repositories
    allows you to install, remove and update your libraries using their git repository locally
    """
    if quiet:
        disable_output()


@cli.command
@click.argument("url")
@click.argument("target_dir")
def add(url, target_dir):
    "add a new package to the registry"
    cfg: _GitConfigurations = get_config_raw()
    for repo in cfg["repositories"]:
        if repo["url"] == url:
            print("repo already added to the list of packages.")
            os._exit(0)
    cfg["repositories"].append({"url": url, "dir": target_dir})
    overwrite_config_raw(cfg)
    os._exit(0)


@cli.command
@click.argument("url")
def remove(url):
    "remove a package by its url"
    cfg: _GitConfigurations = get_config_raw()
    for index, repo in enumerate(cfg["repositories"]):
        if repo["url"] == url:
            del cfg["repositories"][index]
    overwrite_config_raw(cfg)
    print(f"removed the package with the url {url!r}.")
    os._exit(0)


@cli.command
def init():
    "create a new git package manager repository"
    if os.path.exists("git-package.json"):
        print("git configuration already exists in this directory.")
        if not click.confirm("do you want to overwrite it"):
            print("[canceled]")
            return
    new_proj()
    useGit("init")
    useGit("commit", "-m", "init repo", "-a")
    print("successfully initiated a new git project.")
    os._exit(0)


@cli.command
def sync():
    "update all the packages and install the ones that aren't installed yet"
    cfg = get_config()
    with console.status("cloning the git repositories"):
        for repo in cfg.repositories:
            if os.path.exists(repo.dir):
                os.rmdir(repo.dir)
                print(f"updating: {repo.url!r}")
            else:
                print(f"installing: {repo.url!r}")
            useGit("clone", repo.url, repo.dir)
    print("installed all the git packages")
    os._exit(0)


@cli.command
def list():
    "list all the registered repository packages"
    cfg = get_config()
    for repo in cfg.repositories:
        print(f"`{repo.url}` (at {repo.dir})")
    os._exit(0)


if __name__ == "__main__":
    cli()
    restore_output()
# end main
