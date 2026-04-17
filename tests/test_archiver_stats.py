"""Tests for the public :py:mod:`archiver_stats` API."""

from __future__ import annotations

import io

from archiver_stats import STATUS_REFRESH_HZ, Category, Stats, StatusDisplay, StatusLine
import pytest


def test_stats_counters_start_at_zero() -> None:
    stats = Stats((('a', 'A:'), ('b', 'B:')))
    assert stats['a'] == 0
    assert stats['b'] == 0


def test_stats_setitem_and_increment_update_counter() -> None:
    stats = Stats((('hits', 'Hits:'),))
    stats['hits'] = 3
    assert stats['hits'] == 3
    assert stats.increment('hits') == 4
    assert stats.increment('hits', 5) == 9


def test_stats_increment_unknown_key_raises_key_error() -> None:
    stats = Stats((('hits', 'Hits:'),))
    with pytest.raises(KeyError):
        stats.increment('missing')


def test_stats_setitem_rejects_non_int_counter_value() -> None:
    stats = Stats((('hits', 'Hits:'),))
    with pytest.raises(TypeError):
        stats['hits'] = 'oops'


def test_stats_setitem_rejects_bool_counter_value() -> None:
    stats = Stats((('hits', 'Hits:'),))
    with pytest.raises(TypeError):
        stats['hits'] = True


def test_stats_setitem_rejects_non_string_status_line_value() -> None:
    stats = Stats(status_lines=(('message', 'Message:'),))
    with pytest.raises(TypeError):
        stats['message'] = 42


def test_stats_status_line_value_accepts_str_or_none() -> None:
    stats = Stats(status_lines=(('message', 'Message:'),))
    assert list(stats.items()) == [('message', None)]
    stats['message'] = 'hello'
    assert list(stats.items()) == [('message', 'hello')]
    stats['message'] = None
    assert list(stats.items()) == [('message', None)]


def test_stats_getitem_raises_key_error_for_unknown_name() -> None:
    stats = Stats((('hits', 'Hits:'),))
    with pytest.raises(KeyError):
        _ = stats['missing']


def test_stats_setitem_raises_key_error_for_unknown_name() -> None:
    stats = Stats((('hits', 'Hits:'),))
    with pytest.raises(KeyError):
        stats['missing'] = 1


def test_stats_rejects_attribute_deletion() -> None:
    stats = Stats((('hits', 'Hits:'),))
    with pytest.raises(TypeError):
        del stats['hits']


def test_stats_category_items_preserves_declaration_order() -> None:
    stats = Stats((('b', 'B:'), ('a', 'A:')))
    stats['a'] = 2
    stats['b'] = 1
    assert [(cat.key, value) for cat, value in stats.category_items()] == [('b', 1), ('a', 2)]


def test_stats_iter_includes_categories_then_status_lines() -> None:
    stats = Stats((('b', 'B:'), ('a', 'A:')), status_lines=(('note', 'Note:'),))
    assert list(stats) == ['b', 'a', 'note']
    assert len(stats) == 3
    assert 'a' in stats
    assert 'note' in stats
    assert 'missing' not in stats


def test_stats_items_yields_all_values() -> None:
    stats = Stats((('hits', 'Hits:'),), status_lines=(('note', 'Note:'),))
    stats['hits'] = 7
    stats['note'] = 'hello'
    assert dict(stats.items()) == {'hits': 7, 'note': 'hello'}


def test_stats_accepts_category_and_status_line_instances() -> None:
    stats = Stats((Category('hits', 'Hits:'),), status_lines=(StatusLine('note', 'Note:', 'hits'),))
    assert stats.categories == (Category('hits', 'Hits:'),)
    assert stats.status_lines == (StatusLine('note', 'Note:', 'hits'),)


def test_stats_status_line_after_must_reference_known_category() -> None:
    with pytest.raises(KeyError):
        Stats((('hits', 'Hits:'),), status_lines=(('note', 'Note:', 'missing'),))


def test_stats_rejects_duplicate_category_keys() -> None:
    with pytest.raises(ValueError, match='Duplicate category'):
        Stats((('a', 'A:'), ('a', 'Other:')))


def test_stats_rejects_duplicate_status_line_keys() -> None:
    with pytest.raises(ValueError, match='Duplicate status line'):
        Stats(status_lines=(('note', 'Note:'), ('note', 'Again:')))


def test_stats_rejects_status_line_key_matching_category_key() -> None:
    with pytest.raises(ValueError, match='collides'):
        Stats((('shared', 'Shared:'),), status_lines=(('shared', 'Clash:'),))


def test_status_line_items_preserves_declaration_order() -> None:
    stats = Stats(status_lines=(('b', 'B:'), ('a', 'A:')))
    stats['a'] = 'first'
    stats['b'] = 'second'
    pairs = [(line.key, value) for line, value in stats.status_line_items()]
    assert pairs == [('b', 'second'), ('a', 'first')]


def test_status_display_renders_categories_status_lines_and_writes_persistent_line() -> None:
    stats = Stats((('hits', 'Hits:'), ('misses', 'Misses:')),
                  status_lines=(('progress', 'Progress:', 'hits'),))
    stats['hits'] = 2
    stats['misses'] = 5
    stats['progress'] = 'https://example.com/1 (1/3)'
    stream = io.StringIO()
    display = StatusDisplay(stats, stream=stream)
    display.start()
    try:
        display.set_message('Working...')
        display.refresh()
        display.write('persistent line')
    finally:
        display.stop()
    assert 'persistent line' in stream.getvalue()


def test_status_display_renders_without_status_lines() -> None:
    stats = Stats((('hits', 'Hits:'),))
    stream = io.StringIO()
    display = StatusDisplay(stats, stream=stream)
    display.start()
    try:
        display.refresh()
    finally:
        display.stop()


def test_status_display_status_line_before_categories_when_after_is_none() -> None:
    stats = Stats((('hits', 'Hits:'),), status_lines=(('note', 'Note:'),))
    stats['note'] = 'pinned at top'
    stream = io.StringIO()
    display = StatusDisplay(stats, stream=stream)
    display.start()
    try:
        display.refresh()
    finally:
        display.stop()


def test_status_display_idle_status_line_shows_idle_text() -> None:
    stats = Stats((('hits', 'Hits:'),), status_lines=(('note', 'Note:', 'hits'),))
    stream = io.StringIO()
    display = StatusDisplay(stats, stream=stream, idle_text='idle')
    display.start()
    try:
        display.refresh()
    finally:
        display.stop()


def test_status_refresh_hz_is_positive_int() -> None:
    assert isinstance(STATUS_REFRESH_HZ, int)
    assert STATUS_REFRESH_HZ > 0
