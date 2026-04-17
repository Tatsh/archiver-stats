archiver-stats
==============

.. include:: badges.rst

Reusable live statistics and progress display for archiver-style CLIs.

Installation
------------

.. code-block:: shell

   pip install archiver-stats

Usage
-----

Declare counters and optional free-form status lines, then drive a live Rich display from the
:py:class:`~archiver_stats.stats.Stats` instance:

.. code-block:: python

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

:py:class:`~archiver_stats.stats.Stats` is a :py:class:`~collections.abc.MutableMapping` keyed by
category or status-line ``key``. Counter values are integers (update with ``stats[key] = value`` or
:py:meth:`~archiver_stats.stats.Stats.increment`), and status-line values are :py:class:`str` or
``None``. Keys are fixed at construction time and the mapping does not support deletion.

:py:class:`~archiver_stats.display.StatusDisplay` wraps a :py:class:`rich.live.Live` display: call
:py:meth:`~archiver_stats.display.StatusDisplay.start` and
:py:meth:`~archiver_stats.display.StatusDisplay.stop` around your work,
:py:meth:`~archiver_stats.display.StatusDisplay.refresh` to re-render after updating counters,
:py:meth:`~archiver_stats.display.StatusDisplay.set_message` to change the spinner text, and
:py:meth:`~archiver_stats.display.StatusDisplay.write` to print a persistent line above the live
region.

API reference
-------------

.. only:: html

   Top-level package
   ~~~~~~~~~~~~~~~~~

   .. automodule:: archiver_stats

   The following names are re-exported from the submodules below:

   * :py:class:`~archiver_stats.stats.Category`
   * :py:class:`~archiver_stats.stats.Stats`
   * :py:class:`~archiver_stats.stats.StatusLine`
   * :py:class:`~archiver_stats.display.StatusDisplay`
   * :py:data:`~archiver_stats.display.STATUS_REFRESH_HZ`

   Statistics container
   ~~~~~~~~~~~~~~~~~~~~

   .. automodule:: archiver_stats.stats
      :members:

   Live progress display
   ~~~~~~~~~~~~~~~~~~~~~

   .. automodule:: archiver_stats.display
      :members:

   Indices and tables
   ==================
   * :ref:`genindex`
   * :ref:`modindex`
