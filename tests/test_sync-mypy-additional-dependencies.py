import shutil
from pathlib import Path

import pytest
import yaml

from pre_commit_mypy_poetry_sync_hook.sync_mypy_additional_dependencies import _sync

project_root = Path(__file__).parent.parent

@pytest.mark.parametrize("source_file,additional_args", [
        ("pre-commit-config-no-mypy.yaml", {}),
        ("pre-commit-config-no-additional_dependencies.yaml", {}),
        ("pre-commit-config-existing-additional_dependencies.yaml", {}),
        ("pre-commit-config-only-dev-group.yaml", dict(groups=["dev"]))
])
def test_sync(tmp_path, source_file, additional_args):
    source_file_path = Path(__file__).parent / source_file
    pre_commit_config_yaml_path = tmp_path / source_file
    shutil.copy(source_file_path, pre_commit_config_yaml_path)

    _sync(pyproject_path=project_root/"pyproject.toml", pre_commit_config_yaml_path=pre_commit_config_yaml_path, **additional_args)

    with open(pre_commit_config_yaml_path) as pre_commit_config_yaml_stream:
        pre_commit_config_yaml = yaml.safe_load(pre_commit_config_yaml_stream)
    with open(source_file_path.with_suffix(".expectation.yaml")) as expectation_stream:
        pre_commit_config_yaml_expectation = yaml.safe_load(expectation_stream)
    assert pre_commit_config_yaml == pre_commit_config_yaml_expectation