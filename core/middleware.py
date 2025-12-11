import jwt
from django.conf import settings
from core.models import Empleados


class EmpleadoAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        token = request.headers.get("Authorization")

        if token:
            try:
                token = token.replace("Bearer ", "")
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                emp_id = payload.get("id_emp")
                empleado = Empleados.objects.select_related("rol").get(id_emp=emp_id)
                request.empleado = empleado
            except Exception:
                request.empleado = None
        else:
            request.empleado = None

        return self.get_response(request)
