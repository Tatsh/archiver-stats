# archiver-stats

<!-- WISWA-GENERATED-README:START -->

[![Python versions](https://img.shields.io/pypi/pyversions/archiver-stats.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![PyPI - Version](https://img.shields.io/pypi/v/archiver-stats)](https://pypi.org/project/archiver-stats/)
[![GitHub tag (with filter)](https://img.shields.io/github/v/tag/Tatsh/archiver-stats)](https://github.com/Tatsh/archiver-stats/tags)
[![License](https://img.shields.io/github/license/Tatsh/archiver-stats)](https://github.com/Tatsh/archiver-stats/blob/master/LICENSE.txt)
[![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/Tatsh/archiver-stats/v0.0.1/master)](https://github.com/Tatsh/archiver-stats/compare/v0.0.1...master)
[![CodeQL](https://github.com/Tatsh/archiver-stats/actions/workflows/codeql.yml/badge.svg)](https://github.com/Tatsh/archiver-stats/actions/workflows/codeql.yml)
[![QA](https://github.com/Tatsh/archiver-stats/actions/workflows/qa.yml/badge.svg)](https://github.com/Tatsh/archiver-stats/actions/workflows/qa.yml)
[![Tests](https://github.com/Tatsh/archiver-stats/actions/workflows/tests.yml/badge.svg)](https://github.com/Tatsh/archiver-stats/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Tatsh/archiver-stats/badge.svg?branch=master)](https://coveralls.io/github/Tatsh/archiver-stats?branch=master)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-blue?logo=dependabot)](https://github.com/dependabot)
[![Documentation Status](https://readthedocs.org/projects/archiver-stats/badge/?version=latest)](https://archiver-stats.readthedocs.org/?badge=latest)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![uv](https://img.shields.io/badge/uv-261230?logo=astral)](https://docs.astral.sh/uv/)
[![pytest](https://img.shields.io/badge/pytest-zz?logo=Pytest&labelColor=black&color=black)](https://docs.pytest.org/en/stable/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Downloads](https://static.pepy.tech/badge/archiver-stats/month)](https://pepy.tech/project/archiver-stats)
[![Stargazers](https://img.shields.io/github/stars/Tatsh/archiver-stats?logo=github&style=flat)](https://github.com/Tatsh/archiver-stats/stargazers)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Prettier](https://img.shields.io/badge/Prettier-black?logo=prettier)](https://prettier.io/)

[![@Tatsh](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpublic.api.bsky.app%2Fxrpc%2Fapp.bsky.actor.getProfile%2F%3Factor=did%3Aplc%3Auq42idtvuccnmtl57nsucz72&query=%24.followersCount&label=Follow+%40Tatsh&logo=bluesky&style=social)](https://bsky.app/profile/Tatsh.bsky.social)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Tatsh-black?logo=buymeacoffee)](https://buymeacoffee.com/Tatsh)
[![Libera.Chat](https://img.shields.io/badge/Libera.Chat-Tatsh-black?logo=liberadotchat)](irc://irc.libera.chat/Tatsh)
[![Mastodon Follow](https://img.shields.io/mastodon/follow/109370961877277568?domain=hostux.social&style=social)](https://hostux.social/@Tatsh)
[![Patreon](https://img.shields.io/badge/Patreon-Tatsh2-F96854?logo=patreon)](https://www.patreon.com/Tatsh2)

<!-- WISWA-GENERATED-README:STOP -->

Reusable live statistics and progress display for archiver-style CLIs.

## Installation

```shell
pip install archiver-stats
```

## Usage

Declare counters and optional free-form status lines, then drive a live Rich display from the
`Stats` instance:

```python
import sys

from archiver_stats import Category, Stats, StatusDisplay, StatusLine

stats = Stats(
    (Category('hits', 'Hits:'), Category('misses', 'Misses:')),
    status_lines=(StatusLine('progress', 'Progress:', after='hits'),),
)
display = StatusDisplay(stats, stream=sys.stderr, initial_message='Working...')
display.start()
try:
    stats.increment('hits')
    stats['progress'] = 'https://example.com/1 (1/3)'
    display.refresh()
finally:
    display.stop()
```

`Stats` is a `MutableMapping` keyed by category or status-line `key`. Counter values are integers
(update with `stats[key] = value` or `stats.increment(key, amount)`), and status-line values are
`str` or `None`. Keys are fixed at construction time and the mapping does not support deletion.

`StatusDisplay` wraps a Rich `Live` display: call `start()` and `stop()` around your work,
`refresh()` to re-render after updating counters, `set_message()` to change the spinner text, and
`write()` to print a persistent line above the live region.
