"""Live progress display for archiver-style CLIs."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.console import Console, Group
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

if TYPE_CHECKING:
    from rich.console import RenderableType

    from .stats import Stats

__all__ = ('STATUS_REFRESH_HZ', 'StatusDisplay')

STATUS_REFRESH_HZ = 10
"""Default refresh rate used by the live status display.

:meta hide-value:
"""
_LABEL_WIDTH = 20
_VALUE_WIDTH = 6


class StatusDisplay:
    """
    Rich-based live progress display with a spinner line and queue statistics.

    Parameters
    ----------
    stats : Stats
        Statistics object whose counters and free-form status lines are rendered.
    stream : Any
        File-like object the underlying :py:class:`~rich.console.Console` writes to.
    initial_message : str
        Text shown next to the spinner before :py:meth:`set_message` is called.
    refresh_per_second : int
        Refresh rate passed to the underlying :py:class:`~rich.live.Live` display.
    label_width : int
        Minimum column width for counter and status-line labels.
    value_width : int
        Minimum column width for counter values.
    idle_text : str
        Text rendered when a status line's value is ``None``.
    """
    def __init__(self,
                 stats: Stats,
                 *,
                 stream: Any,
                 initial_message: str = 'Starting workers...',
                 refresh_per_second: int = STATUS_REFRESH_HZ,
                 label_width: int = _LABEL_WIDTH,
                 value_width: int = _VALUE_WIDTH,
                 idle_text: str = 'n/a') -> None:
        self._stats = stats
        self._message = initial_message
        self._label_width = label_width
        self._value_width = value_width
        self._idle_text = idle_text
        self._spinner = Spinner('dots', text=Text(self._message))
        self._console = Console(file=stream, force_terminal=True)
        self._live = Live(self._render(),
                          console=self._console,
                          refresh_per_second=refresh_per_second,
                          transient=True)

    def refresh(self) -> None:
        """Re-render the live display with the latest statistics."""
        self._live.update(self._render())

    def set_message(self, message: str) -> None:
        """
        Replace the status message shown next to the spinner.

        Parameters
        ----------
        message : str
            Text rendered beside the spinner glyph.
        """
        self._message = message
        self._spinner.update(text=Text(message))
        self._live.update(self._render())

    def start(self) -> None:
        """Start the live display."""
        self._live.start()

    def stop(self) -> None:
        """Stop the live display and clear the rendered region."""
        self._live.stop()

    def write(self, message: str) -> None:
        """
        Print a persistent status line above the live display.

        Parameters
        ----------
        message : str
            Text to print to the attached console.
        """
        self._console.print(message)

    def _render(self) -> RenderableType:
        stats = self._stats
        status_by_after: dict[str | None, list[Text]] = {}
        for line, text_value in stats.status_line_items():
            status_by_after.setdefault(line.after, []).append(
                _format_status_line(line.label, text_value, self._label_width, self._idle_text))
        lines: list[Text] = list(status_by_after.pop(None, []))
        for category, counter_value in stats.category_items():
            lines.append(
                _format_counter_line(category.label, counter_value, self._label_width,
                                     self._value_width))
            lines.extend(status_by_after.pop(category.key, []))
        return Group(self._spinner, Text('\n').join(lines))


def _format_counter_line(label: str, value: int, label_width: int, value_width: int) -> Text:
    return Text.assemble((label.ljust(label_width), 'bold'), ' ', str(value).rjust(value_width))


def _format_status_line(label: str, value: str | None, label_width: int, idle_text: str) -> Text:
    padded = label.ljust(label_width)
    if value is None:
        return Text.assemble((padded, 'bold'), ' ', idle_text)
    return Text.assemble((padded, 'bold'), ' ', value)
