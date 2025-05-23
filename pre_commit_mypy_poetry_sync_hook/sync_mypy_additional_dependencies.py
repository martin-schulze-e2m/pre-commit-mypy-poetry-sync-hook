import collections
from pathlib import Path

import ruamel.yaml
from packaging.utils import canonicalize_name
from poetry.factory import Factory
import argparse


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames", nargs="*", help="Files pre-commit wants to check (we ignore this!)"
    )
    parser.add_argument(
        "--extra-additional-dependencies",
        action="append",
        help="These will be prepended to mypy hook's additional_dependencies before the poetry dependencies",
    )
    parser.add_argument(
        "--pre-commit-config-yaml-path",
        type=Path,
        help="Path to .pre-commit-config.yaml",
    )
    parser.add_argument(
        "--pyproject-path", type=Path, help="Path to the pyproject.toml"
    )
    parser.add_argument(
        "--groups",
        help="Comma separated list of groups to sync dependencies for",
    )
    parser.add_argument("--yaml-map-indent", type=int, default=2)
    parser.add_argument("--yaml-sequence-indent", type=int, default=2)
    parser.add_argument("--yaml-sequence-dash-offset", type=int, default=0)

    parser.add_argument(
        "--exclude-dependencies",
        action="append",
        help="Dependencies that should never be added to the list of additional_dependencies",
    )

    args = parser.parse_args(args)

    _sync(**vars(args))


def _sync(
    filenames: list[str] | None = None,
    pre_commit_config_yaml_path: Path | None = None,
    pyproject_path: Path | None = None,
    groups: str | None = None,
    extra_additional_dependencies: list[str] | None = None,
    yaml_map_indent: int = 2,
    yaml_sequence_indent: int = 2,
    yaml_sequence_dash_offset: int = 0,
    exclude_dependencies: list[str] | None = None,
):
    if pre_commit_config_yaml_path is None:
        pre_commit_config_yaml_path = Path.cwd() / ".pre-commit-config.yaml"
    if pyproject_path is None:
        pyproject_path = Path.cwd() / "pyproject.toml"
    if extra_additional_dependencies is None:
        extra_additional_dependencies = []
    if exclude_dependencies is None:
        exclude_dependencies = []

    yaml_config = ruamel.yaml.YAML()
    yaml_config.preserve_quotes = True
    yaml_config.map_indent = yaml_map_indent
    yaml_config.sequence_indent = yaml_sequence_indent
    yaml_config.sequence_dash_offset = yaml_sequence_dash_offset

    pre_commit_config = yaml_config.load(pre_commit_config_yaml_path)

    factory = Factory()
    poetry = factory.create_poetry(cwd=pyproject_path)
    poetry_package = poetry.package
    if groups is None:
        groups_list = sorted(poetry_package.dependency_group_names())
    else:
        groups_list = groups.split(",")

    dependencies = (
        dependency
        for group in groups_list
        for dependency in poetry_package.dependency_group(group).dependencies
    )

    package_map = {
        canonicalize_name(package["name"]): package
        for package in poetry.locker.lock_data["package"]
    }

    # find the set of all (transitive) dependencies
    additional_dependencies_set = set()
    dependencies_to_check = collections.deque([dep.name for dep in dependencies])
    while len(dependencies_to_check) > 0:
        dependency = dependencies_to_check.popleft()
        if (
            dependency not in additional_dependencies_set
            and dependency not in exclude_dependencies
        ):
            additional_dependencies_set.add(dependency)
            if dependency in package_map:
                for transitive_dependency in package_map[dependency].get(
                    "dependencies", []
                ):
                    dependencies_to_check.append(
                        canonicalize_name(transitive_dependency)
                    )

    additional_dependencies_list = list(sorted(additional_dependencies_set))

    # add the found dependencies to mypy
    update = False
    for repo in pre_commit_config["repos"]:
        for hook in repo["hooks"]:
            if hook["id"] == "mypy":
                hook["additional_dependencies"] = extra_additional_dependencies + [
                    f"{dependency}=={package_map[dependency]['version']}"
                    for dependency in additional_dependencies_list
                ]
                update = True

    if update:
        yaml_config.dump(pre_commit_config, pre_commit_config_yaml_path)


if __name__ == "__main__":
    main()
