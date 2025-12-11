from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
import jwt
import bcrypt

from core.permissions import RolePermission

from core.models import (
    Regiones, SedesHospitalarias, DepartamentosTrabajo, DepartamentosSede,
    Cargos, Roles, TiposDocumento, TiposServicio, TipoEquipamiento,
    Proveedores, Personas, Empleados, Pacientes, Medicamentos,
    StockMedicamento, TelefonosPersona, TelefonosSede, HistoriasClinicas,
    PrescripcionesMedicamentos, RegistroMedicamentos, ReportesMedicos,
    AuditoriaAccesos, Citas
)

from core.serializers import (
    RegionSerializer, SedeHospitalariaSerializer,
    DepartamentoTrabajoSerializer, DepartamentoSedeSerializer,
    CargoSerializer, RolSerializer, TipoDocumentoSerializer,
    TipoServicioSerializer, TipoEquipamientoSerializer,
    ProveedorSerializer, PersonaSerializer, EmpleadoSerializer,
    PacienteSerializer, MedicamentosSerializer, StockMedicamentoSerializer,
    TelefonoPersonaSerializer, TelefonoSedeSerializer,
    HistoriaClinicaSerializer, PrescripcionMedicamentoSerializer,
    RegistroMedicamentoSerializer, ReporteMedicoSerializer,
    AuditoriaAccesoSerializer, CitaSerializer
)

# ================================================================
#                           LOGIN
# ================================================================

class LoginView(APIView):
    permission_classes = []   # login no requiere token

    def post(self, request):
        documento = request.data.get("documento")
        password = request.data.get("password")

        if not documento or not password:
            return Response({"error": "Faltan credenciales"}, status=400)

        try:
            empleado = Empleados.objects.get(documento_id=documento)
        except Empleados.DoesNotExist:
            return Response({"error": "Credenciales inválidas"}, status=401)

        # Validar contraseña - manejar múltiples formatos
        password_valid = False
        try:
            # Intentar validar con bcrypt
            if empleado.hash_contra.startswith('$2b$') or empleado.hash_contra.startswith('$2a$'):
                password_valid = bcrypt.checkpw(password.encode(), empleado.hash_contra.encode())
            else:
                # Si no es bcrypt, comparar directamente (para desarrollo)
                password_valid = (password == empleado.hash_contra)
        except Exception as e:
            # Si falla bcrypt, intentar comparación directa
            password_valid = (password == empleado.hash_contra)
        
        if not password_valid:
            return Response({"error": "Credenciales inválidas"}, status=401)

        payload = {
            "id_emp": empleado.id_emp,
            "rol": empleado.rol.nombre
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({
            "token": token,
            "rol": empleado.rol.nombre,
            "id_emp": empleado.id_emp
        })
