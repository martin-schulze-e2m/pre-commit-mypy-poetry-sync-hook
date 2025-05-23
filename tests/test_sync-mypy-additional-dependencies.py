import shutil
from pathlib import Path

import pytest

from pre_commit_mypy_poetry_sync_hook.sync_mypy_additional_dependencies import main

project_root = Path(__file__).parent.parent


def readlines(path: Path) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


@pytest.mark.parametrize(
    "source_file,additional_args",
    [
        (
            "pre-commit-config-no-additional_dependencies.yaml",
            [
                "--extra-additional-dependencies",
                "foo",
                "--extra-additional-dependencies",
                "bar",
            ],
        ),
        (
            "pre-commit-config-existing-additional_dependencies.yaml",
            ["--groups", "dev,main"],
        ),
        ("pre-commit-config-only-dev-group.yaml", ["--groups", "dev"]),
        (
            "pre-commit-config-exclude-dependencies.yaml",
            ["--exclude-dependencies", "pytest", "--groups", "dev"],
        ),
    ],
)
def test_sync(tmp_path, source_file, additional_args):
    source_file_path = Path(__file__).parent / source_file
    pre_commit_config_yaml_path = tmp_path / source_file
    shutil.copy(source_file_path, pre_commit_config_yaml_path)

    main(
        [
            "--pyproject-path",
            str(project_root / "pyproject.toml"),
            "--pre-commit-config-yaml-path",
            str(pre_commit_config_yaml_path),
        ]
        + additional_args
    )

    formatted_pre_commit_config_yaml = readlines(pre_commit_config_yaml_path)

    expectation = readlines(source_file_path.with_suffix(".expectation.yaml"))

    assert formatted_pre_commit_config_yaml == expectation


def test_sync_no_mypy(tmp_path):
    source_file = "pre-commit-config-no-mypy.yaml"
    source_file_path = Path(__file__).parent / source_file
    pre_commit_config_yaml_path = tmp_path / source_file
    shutil.copy(source_file_path, pre_commit_config_yaml_path)

    pre_sync_contents = readlines(pre_commit_config_yaml_path)

    main(
        [
            "--pyproject-path",
            str(project_root / "pyproject.toml"),
            "--pre-commit-config-yaml-path",
            str(pre_commit_config_yaml_path),
        ]
    )

    post_sync_contents = readlines(pre_commit_config_yaml_path)

    assert pre_sync_contents == post_sync_contents
