from __future__ import annotations

import pytest
from model_bakery import baker


@pytest.fixture
def roles():
    roles = ["ADMIN", "MANAGER", "SCHEDULER", "EMPLOYEE"]
    return {role: baker.make("example_app.Role", name=role) for role in roles}


@pytest.fixture
def super_admin():
    return baker.make("example_app.Employee", admin_site=True)


@pytest.fixture
def site_admin():
    return baker.make("example_app.Employee", site_role="site_admin")


@pytest.fixture
def executive():
    return baker.make("example_app.Employee", site_role="executive")


@pytest.fixture
def member():
    return baker.make("example_app.Employee")
