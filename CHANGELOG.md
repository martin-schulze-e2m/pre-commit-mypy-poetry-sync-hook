# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.3.0]

### Fixed

- use exact versions instead of "loose" constraints

## [v0.2.1]

### Fixed

- fix argument `--extra-additional-dependencies` adding `- ` before each entry in `additional_dependencies`

## [v0.2.0]

### Added

- argument `--extra-additional-dependencies <dependencies>` to add verbatim before the poetry dependencies

## [v0.1.0]

### Added
- initial implementation of the `sync-mypy-additional-dependencies` pre-commit hook
