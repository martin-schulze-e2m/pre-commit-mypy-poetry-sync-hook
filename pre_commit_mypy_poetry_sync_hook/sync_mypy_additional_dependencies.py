from pathlib import Path

import ruamel.yaml
from poetry.core.factory import Factory
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pre_commit_config_yaml_path', type=Path)
    parser.add_argument("--pyproject_path", type=Path, help="Path to the pyproject.toml", default=Path("pyproject.toml"))
    parser.add_argument("--groups", nargs="*", help="List of groups to sync dependencies for")
    parser.add_argument("--yaml-map-indent", type=int, default=2)
    parser.add_argument("--yaml-sequence-indent", type=int, default=2)
    parser.add_argument("--yaml-sequence-dash-offset", type=int, default=0)

    args = parser.parse_args()

    _sync(**vars(args))

def _sync(pre_commit_config_yaml_path: Path, pyproject_path: Path | None = None, groups: list[str] | None = None, yaml_map_indent: int = 2, yaml_sequence_indent: int = 2, yaml_sequence_dash_offset: int = 0):
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
        groups = sorted(poetry_package.dependency_group_names())

    dependencies = (dependency for group in groups for dependency in poetry_package.dependency_group(group).dependencies)

    update = False
    for repo in pre_commit_config["repos"]:
        for hook in repo["hooks"]:
            if hook["id"] == "mypy":
                hook["additional_dependencies"] = [dependency.to_pep_508() for dependency in dependencies]
                update = True

    if update:
        yaml_config.dump(pre_commit_config, pre_commit_config_yaml_path)

if __name__ == '__main__':
    main()