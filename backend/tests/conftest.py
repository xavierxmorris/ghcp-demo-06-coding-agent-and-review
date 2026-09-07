"""Expose the known PATCH exercise as a strict, opt-in expected failure."""

from __future__ import annotations

import pytest

STARTER_TEST = "tests/test_tasks.py::test_update_unknown_task_returns_404"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--starter-baseline", action="store_true", help="Require the documented PATCH starter failure")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--starter-baseline"):
        if STARTER_TEST not in {item.nodeid for item in items}:
            raise pytest.UsageError(f"Starter baseline test is missing: {STARTER_TEST}")
        for item in items:
            if item.nodeid == STARTER_TEST:
                item.add_marker(pytest.mark.xfail(
                    strict=True,
                    raises=AssertionError,
                    reason="Workshop exercise: PATCH requires title and returns 422 before lookup",
                ))
