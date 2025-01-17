import shutil
from pathlib import Path

import pytest

from pre_commit_mypy_poetry_sync_hook.sync_mypy_additional_dependencies import _sync

project_root = Path(__file__).parent.parent

def readlines(path: Path) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()

@pytest.mark.parametrize("source_file,additional_args", [
        ("pre-commit-config-no-additional_dependencies.yaml", {}),
        ("pre-commit-config-existing-additional_dependencies.yaml", {}),
        ("pre-commit-config-only-dev-group.yaml", dict(groups=["dev"]))
])
def test_sync(tmp_path, source_file, additional_args):
    source_file_path = Path(__file__).parent / source_file
    pre_commit_config_yaml_path = tmp_path / source_file
    shutil.copy(source_file_path, pre_commit_config_yaml_path)

    _sync(pyproject_path=project_root/"pyproject.toml", pre_commit_config_yaml_path=pre_commit_config_yaml_path, **additional_args)

    formatted_pre_commit_config_yaml = readlines(pre_commit_config_yaml_path)

    expectation = readlines(source_file_path.with_suffix(".expectation.yaml"))

    assert formatted_pre_commit_config_yaml == expectation

def test_sync_no_mypy(tmp_path):
    source_file = "pre-commit-config-no-mypy.yaml"
    source_file_path = Path(__file__).parent / source_file
    pre_commit_config_yaml_path = tmp_path / source_file
    shutil.copy(source_file_path, pre_commit_config_yaml_path)

    pre_sync_contents =  readlines(pre_commit_config_yaml_path)

    _sync(pyproject_path=project_root / "pyproject.toml", pre_commit_config_yaml_path=pre_commit_config_yaml_path)

    post_sync_contents = readlines(pre_commit_config_yaml_path)

    assert pre_sync_contents == post_sync_contents