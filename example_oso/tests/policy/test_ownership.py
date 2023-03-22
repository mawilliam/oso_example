from __future__ import annotations

import pytest
from model_bakery import baker

from example_oso.oso import my_oso


@pytest.mark.django_db
def test_ownership(member):
    """Models where an employee has ownership permissions."""
    preference = baker.make("example_app.Preference", employee=member)

    my_oso.authorize(member, "change", preference) is None
    my_oso.authorize(member, "view", preference) is None


@pytest.mark.django_db
def test_scheduler_view_ownership(member, roles):
    """Models where a SCHEDULER is able to view records."""
    office = baker.make("example_app.Office")
    _ = baker.make("example_app.OfficeRole", office=office, employee=member, role=roles["EMPLOYEE"])
    actor = baker.make("example_app.Employee")
    _ = baker.make("example_app.OfficeRole", office=office, employee=actor, role=roles["SCHEDULER"])
    preference = baker.make("example_app.Preference", employee=member)

    for office in member.office_roles.all():
        print(f"OfficeRole: {office}")

    my_oso.authorize(actor, "view", preference) is None
