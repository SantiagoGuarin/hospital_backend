from rest_framework.permissions import BasePermission

ROLE_PERMISSIONS = {
    "administrador": {
        "allow_all": True,
    },
    "medico": {
        "GET": ["pacientes", "citas", "historias_clinicas", "prescripciones"],
        "POST": ["historias_clinicas", "prescripciones"],
        "PUT": ["historias_clinicas", "prescripciones"],
        "PATCH": ["historias_clinicas", "prescripciones"],
    },
    "enfermero": {
        "GET": ["pacientes", "citas", "equipamento"],
        "PATCH": ["citas", "equipamento"],
    },
    "administrativo": {
        "GET": ["*"],
        "POST": ["citas", "pacientes", "personas", "empleados", "equipamento"],
        "PUT": ["citas", "pacientes", "personas", "empleados"],
        "PATCH": ["citas", "pacientes", "empleados"],
        "DELETE": ["empleados", "equipamento"],
    },
    "auditor": {
        "GET": ["*"]
    }
}


class RolePermission(BasePermission):
    """
    Valida si el usuario (empleado) puede acceder a la vista según su rol.
    """

    def has_permission(self, request, view):
        empleado = getattr(request, "empleado", None)
        if not empleado:
            return False

        rol = empleado.rol.nombre.lower()

        # Administrador tiene full access
        if ROLE_PERMISSIONS.get(rol, {}).get("allow_all", False):
            return True

        metodo = request.method
        recurso = view.basename  # ej: "citas", "pacientes", etc.

        permisos = ROLE_PERMISSIONS.get(rol, {})

        # Si el rol solo puede leer
        if metodo == "GET" and "*" in permisos.get("GET", []):
            return True

        # Si el rol tiene permisos explícitos
        lista = permisos.get(metodo, [])
        return recurso in lista
