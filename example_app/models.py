from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy


class Office(models.Model):
    name = models.CharField(max_length=30)


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{}: {}".format(
            self.id,
            self.name,
        )


class OfficeRole(models.Model):
    """Active role assignments for an office."""

    office = models.ForeignKey("Office", on_delete=models.CASCADE)
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)

    class Meta:
        unique_together = [["office", "employee"]]

    def __str__(self):
        return f"{self.id}: ({self.office} - {self.employee}) -> {self.role}"


class Employee(AbstractBaseUser):
    # Authentication fields
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    has_changed_default_password = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    # Personal Info
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    # Authorization
    admin_site = models.BooleanField(default=False)
    class SiteRole(models.TextChoices):
        ADMIN = "site_admin", gettext_lazy("site admin")
        EXECUTIVE = "executive", gettext_lazy("executive")
        MEMBER = "member", gettext_lazy("member")

    site_role = models.CharField(
        max_length=20,
        default=SiteRole.MEMBER,
        choices=SiteRole.choices,
    )

    office_roles = models.ManyToManyField(
        "Office",
        through="OfficeRole",
        related_name="employee_roles",
    )


class PreferenceType(models.Model):
    type = models.CharField(
        max_length=15,
        unique=True,
        editable=False,
    )
    definition = models.CharField(
        max_length=150,
    )

    def __str__(self):
        return "{}: {}".format(
            self.id,
            self.type,
        )


class Preference(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    type = models.ForeignKey("PreferenceType", on_delete=models.CASCADE)
    value = models.FloatField(default=0.0)

    class Meta:
        unique_together = [["employee", "type"]]

    def __str__(self):
        return f"{self.id}: ({self.type}) -> ({self.employee})"
