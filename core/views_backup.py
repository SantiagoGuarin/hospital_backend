from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.conf import settings
import jwt
import bcrypt

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
    permission_classes = [AllowAny]

    def post(self, request):
        documento = request.data.get("documento")
        password = request.data.get("password")

        if not documento or not password:
            return Response({"error": "Faltan credenciales"}, status=400)

        try:
            empleado = Empleados.objects.select_related('rol', 'documento', 'cargo', 'id_dept').get(documento_id=documento)
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
        except (ValueError, AttributeError) as e:
            # Si falla bcrypt, intentar comparación directa
            password_valid = (password == empleado.hash_contra)
        
        if not password_valid:
            return Response({"error": "Credenciales inválidas"}, status=401)

        # Retornar datos del empleado sin token
        return Response({
            "success": True,
            "empleado": {
                "id_emp": empleado.id_emp,
                "documento": empleado.documento.documento,
                "nombre": empleado.documento.nom_persona,
                "rol": empleado.rol.nombre,
                "cargo": empleado.cargo.nombre,
                "departamento": empleado.id_dept.nom_dept
            }
        })


# ================================================================
#                        VIEWSETS
# ================================================================

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Regiones.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]


class SedeHospitalariaViewSet(viewsets.ModelViewSet):
    queryset = SedesHospitalarias.objects.all()
    serializer_class = SedeHospitalariaSerializer
    permission_classes = [AllowAny]


class DepartamentoTrabajoViewSet(viewsets.ModelViewSet):
    queryset = DepartamentosTrabajo.objects.all()
    serializer_class = DepartamentoTrabajoSerializer
    permission_classes = [AllowAny]


class DepartamentoSedeViewSet(viewsets.ModelViewSet):
    queryset = DepartamentosSede.objects.all()
    serializer_class = DepartamentoSedeSerializer
    permission_classes = [AllowAny]


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargos.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [AllowAny]


class RolViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolSerializer
    permission_classes = [AllowAny]


class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TiposDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer
    permission_classes = [AllowAny]


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TiposServicio.objects.all()
    serializer_class = TipoServicioSerializer
    permission_classes = [AllowAny]


class TipoEquipamientoViewSet(viewsets.ModelViewSet):
    queryset = TipoEquipamiento.objects.all()
    serializer_class = TipoEquipamientoSerializer
    permission_classes = [AllowAny]


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedores.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [AllowAny]


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Personas.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [AllowAny]


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleados.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [AllowAny]


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Pacientes.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [AllowAny]


class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamentos.objects.all()
    serializer_class = MedicamentosSerializer
    permission_classes = [AllowAny]


class StockMedicamentoViewSet(viewsets.ModelViewSet):
    queryset = StockMedicamento.objects.all()
    serializer_class = StockMedicamentoSerializer
    permission_classes = [AllowAny]


class TelefonoPersonaViewSet(viewsets.ModelViewSet):
    queryset = TelefonosPersona.objects.all()
    serializer_class = TelefonoPersonaSerializer
    permission_classes = [AllowAny]


class TelefonoSedeViewSet(viewsets.ModelViewSet):
    queryset = TelefonosSede.objects.all()
    serializer_class = TelefonoSedeSerializer
    permission_classes = [AllowAny]


class HistoriaClinicaViewSet(viewsets.ModelViewSet):
    queryset = HistoriasClinicas.objects.all()
    serializer_class = HistoriaClinicaSerializer
    permission_classes = [AllowAny]


class PrescripcionMedicamentoViewSet(viewsets.ModelViewSet):
    queryset = PrescripcionesMedicamentos.objects.all()
    serializer_class = PrescripcionMedicamentoSerializer
    permission_classes = [AllowAny]


class RegistroMedicamentoViewSet(viewsets.ModelViewSet):
    queryset = RegistroMedicamentos.objects.all()
    serializer_class = RegistroMedicamentoSerializer
    permission_classes = [AllowAny]


class ReporteMedicoViewSet(viewsets.ModelViewSet):
    queryset = ReportesMedicos.objects.all()
    serializer_class = ReporteMedicoSerializer
    permission_classes = [AllowAny]


class AuditoriaAccesoViewSet(viewsets.ModelViewSet):
    queryset = AuditoriaAccesos.objects.all()
    serializer_class = AuditoriaAccesoSerializer
    permission_classes = [AllowAny]


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Citas.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [AllowAny]
