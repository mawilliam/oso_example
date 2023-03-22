from __future__ import annotations

from django.apps import AppConfig

from example_oso.oso import init_oso


class ExampleOsoConfig(AppConfig):
    name = "example_oso"

    def ready(self):
        _ = init_oso()
