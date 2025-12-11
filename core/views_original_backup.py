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

        if not bcrypt.checkpw(password.encode(), empleado.hash_contra.encode()):
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


# ================================================================
#                        VIEWSETS
# ================================================================

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Regiones.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class SedeHospitalariaViewSet(viewsets.ModelViewSet):
    queryset = SedesHospitalarias.objects.all()
    serializer_class = SedeHospitalariaSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class DepartamentoTrabajoViewSet(viewsets.ModelViewSet):
    queryset = DepartamentosTrabajo.objects.all()
    serializer_class = DepartamentoTrabajoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class DepartamentoSedeViewSet(viewsets.ModelViewSet):
    queryset = DepartamentosSede.objects.all()
    serializer_class = DepartamentoSedeSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargos.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class RolViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TiposDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TiposServicio.objects.all()
    serializer_class = TipoServicioSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class TipoEquipamientoViewSet(viewsets.ModelViewSet):
    queryset = TipoEquipamiento.objects.all()
    serializer_class = TipoEquipamientoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedores.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Personas.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleados.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Pacientes.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamentos.objects.all()
    serializer_class = MedicamentosSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class StockMedicamentoViewSet(viewsets.ModelViewSet):
    queryset = StockMedicamento.objects.all()
    serializer_class = StockMedicamentoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class TelefonoPersonaViewSet(viewsets.ModelViewSet):
    queryset = TelefonosPersona.objects.all()
    serializer_class = TelefonoPersonaSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class TelefonoSedeViewSet(viewsets.ModelViewSet):
    queryset = TelefonosSede.objects.all()
    serializer_class = TelefonoSedeSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class HistoriaClinicaViewSet(viewsets.ModelViewSet):
    queryset = HistoriasClinicas.objects.all()
    serializer_class = HistoriaClinicaSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class PrescripcionMedicamentoViewSet(viewsets.ModelViewSet):
    queryset = PrescripcionesMedicamentos.objects.all()
    serializer_class = PrescripcionMedicamentoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class RegistroMedicamentoViewSet(viewsets.ModelViewSet):
    queryset = RegistroMedicamentos.objects.all()
    serializer_class = RegistroMedicamentoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class ReporteMedicoViewSet(viewsets.ModelViewSet):
    queryset = ReportesMedicos.objects.all()
    serializer_class = ReporteMedicoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class AuditoriaAccesoViewSet(viewsets.ModelViewSet):
    queryset = AuditoriaAccesos.objects.all()
    serializer_class = AuditoriaAccesoSerializer
    permission_classes = [IsAuthenticated, RolePermission]


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Citas.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated, RolePermission]
