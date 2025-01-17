# pre-commit-mypy-poetry-sync-hook
A pre-commit hook to keep mypy hook's additional_dependencies in sync with poetry by update `.pre-commit-config.yaml`

## Usage

Add the hook to your `.pre-commit-config.yaml`:

```yaml
- hooks:
  - id: sync-mypy-additional-dependencies
  repo: https://github.com/martin-schulze-e2m/pre-commit-mypy-poetry-sync-hook
  rev: v0.2.0
```

## Parameters

These can be added as args to the hook:

```yaml
- hooks:
  - id: sync-mypy-additional-dependencies
    args: --groups lint # only use dependencies from the lint group
  repo: https://github.com/martin-schulze-e2m/pre-commit-mypy-poetry-sync-hook
  rev: v0.2.0
```

All parameters are optional and have mostly sane defaults.
Running `sync-mypy-additinal-dependencies --help` (with this project installed!) will list all parameters.
The most important are as follows

### `--groups <comma separated group names>`

List of poetry groups to sync dependencies for

**default**: all non-optional groups

### `--extra-additional-dependencies <str>`

Strings that should be added as entries to mypy hook's `additional_dependencies` before the dependencies from poetry.
Can be repeated to add multiple entries.

This can be used to change the index used by pip: (See https://github.com/pre-commit/pre-commit/issues/1316#issuecomment-583011187)

```yaml
- hooks:
  - id: sync-mypy-additional-dependencies
    args: --extra_additional_dependencies "--index-url=<your private index>"
  repo: https://github.com/martin-schulze-e2m/pre-commit-mypy-poetry-sync-hook
  rev: v0.2.0
```

### `--pre-commit-config-yaml-path <path to .pre-commit-config.yaml>`

Path to the `.pre-commit-config.yaml` that should be patched.

**default**: `.pre-commit-config.yaml`

### `--pyproject-path <path to pyproject.toml>`

Path to the `pyproject.toml` to get the dependencies from.

**default**: `pyproject.toml`
