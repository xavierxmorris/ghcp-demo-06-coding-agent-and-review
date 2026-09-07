"""A different API failure must not pass as the documented PATCH exercise."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_known_patch_failure_is_missing_title_validation(pytestconfig: pytest.Config) -> None:
    if not pytestconfig.getoption("--starter-baseline"):
        pytest.skip("This assertion protects only the intentionally incomplete starter")
    with TestClient(app) as client:
        response = client.patch("/tasks/does-not-exist", json={"done": True})
    assert response.status_code == 422
    assert any(
        error["loc"] == ["body", "title"] and error["type"] == "missing"
        for error in response.json()["detail"]
    )
