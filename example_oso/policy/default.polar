# Super admin can do anything
allow(_actor: Employee{admin_site: true}, _action, _resource);

# Executive can view analtyics on any resource
allow(_actor: Employee{site_role: "executive"}, "view_analytics", _resource);

# Site admin has admin role everywhere
has_role(_actor: Employee{site_role: "site_admin"}, "ADMIN", _resource: Resource);

allow(actor, action, resource) if
  has_permission(actor, action, resource);

# Roles assigned at the office
has_role(user: Employee, name: String, office: Office) if
  office_role in user.locationrole_set.values("role__name", "office_id") and
  office_role.role__name = name and
  office_role.office_id = office.id;

# Ownership roles
has_role(user: Employee, "owner", preference: Preference) if
  preference.employee = user;

has_role(user: Employee, "ADMIN", preference: Preference) if
  preference.employee matches Employee and
  is_manager(preference.employee, "SCHEDULER", user);

is_manager(employee: Employee, name: String, manager: Employee) if
  office_role in employee.officerole_set.all() and
  office_role.office matches Office and
  has_role(manager, name, office_role.office);

actor Employee {
}

resource Office {
  roles = ["ADMIN", "executive", "MANAGER", "SCHEDULER", "EMPLOYEE"];
  permissions = [
    "view",
    "administer_roles",
  ];

  # has_permission rules
  "view" if "ADMIN";
  "administer_roles" if "ADMIN";
}

resource Preference {
  roles = ["ADMIN", "owner"];
  permissions = ["view", "change"];

  # has_permission rules
  "change" if "owner";
  "view" if "owner";
  "view" if "ADMIN";
}
