"""Statistics container for archiver-style CLIs."""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import TYPE_CHECKING, NamedTuple

from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

__all__ = ('Category', 'Stats', 'StatusLine')


class Category(NamedTuple):
    """
    Declared counter category for a :py:class:`Stats` instance.

    Parameters
    ----------
    key : str
        Key used to read and update the counter on the owning :py:class:`Stats`.
    label : str
        Human-readable label rendered by :py:class:`~archiver_stats.display.StatusDisplay`.
    """

    key: str
    """Key used to read and update the counter."""
    label: str
    """Human-readable label rendered alongside the counter value."""


class StatusLine(NamedTuple):
    """
    Declared free-form status line for a :py:class:`Stats` instance.

    Unlike a :py:class:`Category` (which tracks an integer counter), a status line
    holds an arbitrary text value that the caller sets at will, or ``None`` to
    render as ``n/a``.

    Parameters
    ----------
    key : str
        Key used to read and update the value on the owning :py:class:`Stats`.
    label : str
        Human-readable label rendered by :py:class:`~archiver_stats.display.StatusDisplay`.
    after : str | None
        Category key after which this line should render. When ``None``, the line
        renders before all categories.
    """

    key: str
    """Key used to read and update the value."""
    label: str
    """Human-readable label rendered alongside the value."""
    after: str | None = None
    """Category key after which this line should render."""


class Stats(MutableMapping[str, 'int | str | None']):
    """
    Live statistics container with named counters and free-form status lines.

    Instances behave as a :py:class:`~collections.abc.MutableMapping` keyed by the
    category or status-line ``key``. Counter values are integers; status-line
    values are ``str`` or ``None``. Keys are fixed at construction time: writing
    to an unknown key raises :py:class:`KeyError`, and the mapping does not
    support deletion.

    Parameters
    ----------
    categories : Iterable[Category | tuple[str, str]]
        Ordered counter categories exposed as integer entries.
    status_lines : Iterable[StatusLine | tuple[str, str] | tuple[str, str, str | None]]
        Free-form status lines whose values can be any string or ``None``.

    Raises
    ------
    KeyError
        If a status line's ``after`` is not a registered category key.
    ValueError
        If a category key and a status line key collide, or if any keys within
        ``categories`` or ``status_lines`` are duplicated.
    """
    def __init__(
        self,
        categories: Iterable[Category | tuple[str, str]] = (),
        *,
        status_lines: Iterable[StatusLine | tuple[str, str]
                               | tuple[str, str, str | None]] = ()
    ) -> None:
        normalised_categories = tuple(
            c if isinstance(c, Category) else Category(*c) for c in categories)
        normalised_lines = tuple(
            line if isinstance(line, StatusLine) else StatusLine(*line) for line in status_lines)
        counters: dict[str, int] = {}
        for category in normalised_categories:
            if category.key in counters:
                msg = f'Duplicate category key: {category.key!r}.'
                raise ValueError(msg)
            counters[category.key] = 0
        values: dict[str, str | None] = {}
        for line in normalised_lines:
            if line.key in counters:
                msg = f'Status line key {line.key!r} collides with a category.'
                raise ValueError(msg)
            if line.key in values:
                msg = f'Duplicate status line key: {line.key!r}.'
                raise ValueError(msg)
            if line.after is not None and line.after not in counters:
                raise KeyError(line.after)
            values[line.key] = None
        self._categories = normalised_categories
        self._status_lines = normalised_lines
        self._counters = counters
        self._values = values

    @property
    def categories(self) -> tuple[Category, ...]:
        """Declared counter categories in rendering order."""
        return self._categories

    @property
    def status_lines(self) -> tuple[StatusLine, ...]:
        """Declared free-form status lines in declaration order."""
        return self._status_lines

    def category_items(self) -> Iterator[tuple[Category, int]]:
        """
        Yield ``(category, value)`` pairs in declaration order.

        Yields
        ------
        tuple[Category, int]
            Each declared category paired with its current counter value.
        """
        for category in self._categories:
            yield category, self._counters[category.key]

    def increment(self, key: str, amount: int = 1) -> int:
        """
        Add ``amount`` to the counter named ``key`` and return the new value.

        Parameters
        ----------
        key : str
            Name of the counter.
        amount : int
            Amount to add. May be negative.

        Returns
        -------
        int
            The updated counter value.

        Raises
        ------
        KeyError
            If ``key`` is not a registered counter.
        """
        if key not in self._counters:
            raise KeyError(key)
        self._counters[key] += amount
        return self._counters[key]

    def status_line_items(self) -> Iterator[tuple[StatusLine, str | None]]:
        """
        Yield ``(status_line, value)`` pairs in declaration order.

        Yields
        ------
        tuple[StatusLine, str | None]
            Each declared status line paired with its current value.
        """
        for line in self._status_lines:
            yield line, self._values[line.key]

    @override
    def __getitem__(self, key: str) -> int | str | None:
        if key in self._counters:
            return self._counters[key]
        if key in self._values:
            return self._values[key]
        raise KeyError(key)

    @override
    def __setitem__(self, key: str, value: int | str | None) -> None:
        if key in self._counters:
            if not isinstance(value, int) or isinstance(value, bool):
                msg = f'Counter {key!r} requires a non-bool int value.'
                raise TypeError(msg)
            self._counters[key] = value
            return
        if key in self._values:
            if value is not None and not isinstance(value, str):
                msg = f'Status line {key!r} requires a str or None value.'
                raise TypeError(msg)
            self._values[key] = value
            return
        raise KeyError(key)

    @override
    def __delitem__(self, key: str) -> None:
        msg = f'{type(self).__name__} does not support key deletion.'
        raise TypeError(msg)

    @override
    def __iter__(self) -> Iterator[str]:
        for category in self._categories:
            yield category.key
        for line in self._status_lines:
            yield line.key

    @override
    def __len__(self) -> int:
        return len(self._counters) + len(self._values)

    @override
    def __contains__(self, key: object) -> bool:
        return key in self._counters or key in self._values
