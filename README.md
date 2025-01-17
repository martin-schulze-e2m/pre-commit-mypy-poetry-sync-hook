# pre-commit-mypy-poetry-sync-hook
A pre-commit hook to keep mypy hook's additional_dependencies in sync with poetry by update `.pre-commit-config.yaml`

## Usage

Add the hook to your `.pre-commit-config.yaml`:

```yaml
- hooks:
  - id: sync-mypy-additional-dependencies
  repo: https://github.com/martin-schulze-e2m/pre-commit-mypy-poetry-sync-hook
  rev: v0.1.0
```

## Parameters

These can be added as args to the hook:

```yaml
- hooks:
  - id: sync-mypy-additional-dependencies
    args: --groups lint # only use dependencies from the lint group
  repo: https://github.com/martin-schulze-e2m/pre-commit-mypy-poetry-sync-hook
  rev: v0.1.0
```

All parameters are optional and have mostly sane defaults.
Running `sync-mypy-additinal-dependencies --help` (with this project installed!) will list all parameters.
The most important are as follows

### `--groups <comma separated group names>`

List of poetry groups to sync dependencies for

**default**: all non-optional groups

### `--pre-commit-config-yaml-path <path to .pre-commit-config.yaml>`

Path to the `.pre-commit-config.yaml` that should be patched.

**default**: `.pre-commit-config.yaml`

### `--pyproject-path <path to pyproject.toml>`

Path to the `pyproject.toml` to get the dependencies from.

**default**: `pyproject.toml`
