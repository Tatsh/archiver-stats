<!-- markdownlint-configure-file {"MD024": { "siblings_only": true } } -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.1/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] - 2026-04-17

### Added

- Initial extraction from [`patreon-archiver`](https://github.com/Tatsh/patreon-archiver):
  - `Stats` `MutableMapping` container with declared `Category` counters and
    free-form `StatusLine` entries, including key validation, ordered
    iteration, and `increment` helper.
  - `StatusDisplay`, a Rich-based live progress display combining a spinner
    line with aligned counters and status lines, and `STATUS_REFRESH_HZ`
    default refresh rate.

[Unreleased]: https://github.com/Tatsh/archiver-stats/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/Tatsh/archiver-stats/releases/tag/v0.0.1
