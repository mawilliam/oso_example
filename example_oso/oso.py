from __future__ import annotations

import logging

from django.apps import apps
from oso import Oso
from oso import Relation


LOGGER = logging.getLogger()

my_oso = Oso()
# my_oso.set_data_filtering_adapter(DjangoAdapter())


def init_oso():
    """Registers the requisite classes and loads the policy."""
    my_oso.host.get_field = lambda model, field: model._meta.get_field(field).related_model
    my_oso.register_class(
        apps.get_model("example_app.Employee"),
        name="Employee",
        fields={
            "id": int,
            "admin_site": bool,
            "site_role": str,
            "office_roles": Relation(
                kind="many",
                other_type="OfficeRole",
                my_field="id",
                other_field="employee_id",
            ),  # this relation field was why I couldn't do employee.office_roles.all()
        },
    )

    my_oso.register_class(
        apps.get_model("example_app.Role"),
        name="Role",
        fields={
            "id": int,
            "name": str,
        },
    )

    my_oso.register_class(
        apps.get_model("example_app.Office"),
        name="Office",
        fields={
            "id": int,
        },
    )

    my_oso.register_class(
        apps.get_model("example_app.OfficeRole"),
        name="OfficeRole",
        fields={
            "id": int,
            "employee": Relation(
                kind="one",
                other_type="Employee",
                my_field="employee_id",
                other_field="id",
            ),
            "office": Relation(
                kind="one", other_type="Office", my_field="office_id", other_field="id"
            ),
            "role": Relation(
                kind="one", other_type="Role", my_field="role_id", other_field="id"
            ),
        },
    )

    my_oso.register_class(
        apps.get_model("example_app.Preference"),
        name="Preference",
        # fields={
        #     "id": int,
        #     "employee_relation": Relation(
        #         kind="one", other_type="Employee", my_field="employee_id", other_field="id"
        #     ),
        # }
    )

    my_oso.load_files(["example_oso/policy/default.polar"])
    LOGGER.info("Loaded the policy at: 'example_oso/policy/default.polar'")
