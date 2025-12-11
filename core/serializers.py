from rest_framework import serializers
from .models import (
    Regiones, SedesHospitalarias, DepartamentosTrabajo, DepartamentosSede,
    Cargos, Roles, TiposDocumento, TiposServicio, TipoEquipamiento,
    Proveedores, Personas, Empleados, Pacientes, Medicamentos,
    StockMedicamento, TelefonosPersona, TelefonosSede, HistoriasClinicas,
    PrescripcionesMedicamentos, RegistroMedicamentos, ReportesMedicos,
    AuditoriaAccesos, Citas, Equipamento
)

# ============================================================
#   REGIONES / SEDES
# ============================================================

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regiones
        fields = "__all__"


class SedeHospitalariaSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    region_id = serializers.PrimaryKeyRelatedField(
        source="region",
        queryset=Regiones.objects.all()
    )

    class Meta:
        model = SedesHospitalarias
        fields = ["id_sede", "nom_sede", "ciudad", "region_id", "region"]




# ============================================================
#   DEPARTAMENTOS
# ============================================================

class DepartamentoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartamentosTrabajo
        fields = "__all__"


class DepartamentoSedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartamentosSede
        fields = "__all__"


# ============================================================
#   ROLES / CARGOS / DOCUMENTOS / SERVICIOS
# ============================================================

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargos
        fields = "__all__"


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposDocumento
        fields = "__all__"


class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposServicio
        fields = "__all__"


class TipoEquipamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipamiento
        fields = "__all__"


# ============================================================
#   PROVEEDORES
# ============================================================

class ProveedorSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        source="region", queryset=Regiones.objects.all(), write_only=True
    )

    class Meta:
        model = Proveedores
        fields = ["proveedor_id", "nombre", "region", "region_id"]


# ============================================================
#   PERSONAS / EMPLEADOS / PACIENTES
# ============================================================

class PersonaSerializer(serializers.ModelSerializer):
    tipo_doc = TipoDocumentoSerializer(read_only=True)
    tipo_doc_id = serializers.PrimaryKeyRelatedField(
        source="tipo_doc", queryset=TiposDocumento.objects.all(), write_only=True
    )

    id_sede = SedeHospitalariaSerializer(read_only=True)
    id_sede_id = serializers.PrimaryKeyRelatedField(
        source="id_sede", queryset=SedesHospitalarias.objects.all(), write_only=True
    )

    class Meta:
        model = Personas
        fields = [
            "documento", "nom_persona", "fecha_nac", "genero",
            "dir_per", "correo_per", "tipo_doc", "tipo_doc_id",
            "id_sede", "id_sede_id"
        ]


class EmpleadoSerializer(serializers.ModelSerializer):
    documento = PersonaSerializer(read_only=True)
    documento_id = serializers.PrimaryKeyRelatedField(
        source="documento", queryset=Personas.objects.all(), write_only=True
    )

    id_dept = DepartamentoTrabajoSerializer(read_only=True)
    id_dept_id = serializers.PrimaryKeyRelatedField(
        source="id_dept", queryset=DepartamentosTrabajo.objects.all(), write_only=True
    )

    cargo = CargoSerializer(read_only=True)
    cargo_id = serializers.PrimaryKeyRelatedField(
        source="cargo", queryset=Cargos.objects.all(), write_only=True
    )

    rol = RolSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(
        source="rol", queryset=Roles.objects.all(), write_only=True
    )

    class Meta:
        model = Empleados
        fields = [
            "id_emp", "documento", "documento_id",
            "id_dept", "id_dept_id", "cargo", "cargo_id",
            "rol", "rol_id", "hash_contra"
        ]
        extra_kwargs = {"hash_contra": {"write_only": True}}


class PacienteSerializer(serializers.ModelSerializer):
    documento = PersonaSerializer(read_only=True)
    documento_id = serializers.PrimaryKeyRelatedField(
        source="documento", queryset=Personas.objects.all(), write_only=True
    )

    class Meta:
        model = Pacientes
        fields = ["cod_pac", "documento", "documento_id"]


# ============================================================
#   MEDICAMENTOS / STOCK
# ============================================================

class MedicamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamentos
        fields = "__all__"


# ============================================================
#   EQUIPAMENTO
# ============================================================

class EquipamentoSerializer(serializers.ModelSerializer):
    id_dept = DepartamentoTrabajoSerializer(read_only=True)
    id_dept_id = serializers.PrimaryKeyRelatedField(
        source="id_dept", queryset=DepartamentosTrabajo.objects.all(), write_only=True
    )
    responsable = EmpleadoSerializer(read_only=True)
    responsable_id = serializers.PrimaryKeyRelatedField(
        source="responsable", queryset=Empleados.objects.all(), write_only=True
    )

    class Meta:
        model = Equipamento
        fields = [
            "cod_eq",
            "id_dept",
            "id_dept_id",
            "responsable",
            "responsable_id",
            "nom_eq",
            "estado",
            "fecha_mantenimiento",
        ]


class StockMedicamentoSerializer(serializers.ModelSerializer):
    medicamento = MedicamentosSerializer(read_only=True)
    medicamento_id = serializers.PrimaryKeyRelatedField(
        source="medicamento", queryset=Medicamentos.objects.all(), write_only=True
    )

    class Meta:
        model = StockMedicamento
        fields = ["id_stock", "medicamento", "medicamento_id", "cantidad", "fecha_actualizacion"]


# ============================================================
#   TELÉFONOS
# ============================================================

class TelefonoPersonaSerializer(serializers.ModelSerializer):
    documento = PersonaSerializer(read_only=True)
    documento_id = serializers.PrimaryKeyRelatedField(
        source="documento", queryset=Personas.objects.all(), write_only=True
    )

    class Meta:
        model = TelefonosPersona
        fields = ["id_tel", "documento", "documento_id", "numero"]


class TelefonoSedeSerializer(serializers.ModelSerializer):
    id_sede = SedeHospitalariaSerializer(read_only=True)
    id_sede_id = serializers.PrimaryKeyRelatedField(
        source="id_sede", queryset=SedesHospitalarias.objects.all(), write_only=True
    )

    class Meta:
        model = TelefonosSede
        fields = ["id_tel_sede", "id_sede", "id_sede_id", "numero"]


# ============================================================
#   HISTORIAS / PRESCRIPCIONES / REGISTROS / REPORTES
# ============================================================

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citas
        fields = "__all__"
        
class HistoriaClinicaSerializer(serializers.ModelSerializer):

    cita = CitaSerializer(source="id_cita", read_only=True)

    paciente_nombre = serializers.SerializerMethodField()

    medico_nombre = serializers.SerializerMethodField()

    id_cita = serializers.PrimaryKeyRelatedField(
        queryset=Citas.objects.all()
    )

    class Meta:
        model = HistoriasClinicas
        fields = [
            "cod_hist",
            "id_cita",
            "cita",
            "fecha_hora",
            "diagnostico",
            "paciente_nombre",
            "medico_nombre",
        ]

    def get_paciente_nombre(self, obj):
        try:
            documento = obj.id_cita.cod_pac.documento
            persona = Personas.objects.get(documento=documento)
            return persona.nom_persona
        except Personas.DoesNotExist:
            return None
        except Exception:
            return None

    def get_medico_nombre(self, obj):
        try:
            documento = obj.id_cita.id_emp.documento
            persona = Personas.objects.get(documento=documento)
            return persona.nom_persona
        except Personas.DoesNotExist:
            return None
        except Exception:
            return None



class PrescripcionMedicamentoSerializer(serializers.ModelSerializer):
    id_historia = HistoriaClinicaSerializer(read_only=True)
    id_historia_id = serializers.PrimaryKeyRelatedField(
        source="id_historia", queryset=HistoriasClinicas.objects.all(), write_only=True
    )

    medicamento = MedicamentosSerializer(read_only=True)
    medicamento_id = serializers.PrimaryKeyRelatedField(
        source="medicamento", queryset=Medicamentos.objects.all(), write_only=True
    )

    class Meta:
        model = PrescripcionesMedicamentos
        fields = [
            "id_prescripcion", "id_historia", "id_historia_id",
            "medicamento", "medicamento_id", "dosis",
            "frecuencia", "duracion"
        ]


class RegistroMedicamentoSerializer(serializers.ModelSerializer):
    id_emp = EmpleadoSerializer(read_only=True)
    id_emp_id = serializers.PrimaryKeyRelatedField(
        source="id_emp", queryset=Empleados.objects.all(), write_only=True
    )

    medicamento = MedicamentosSerializer(read_only=True)
    medicamento_id = serializers.PrimaryKeyRelatedField(
        source="medicamento", queryset=Medicamentos.objects.all(), write_only=True
    )

    class Meta:
        model = RegistroMedicamentos
        fields = [
            "id_registro", "medicamento", "medicamento_id",
            "id_emp", "id_emp_id",
            "cantidad", "fecha", "tipo_movimiento"
        ]


class ReporteMedicoSerializer(serializers.ModelSerializer):
    id_historia = HistoriaClinicaSerializer(read_only=True)
    id_historia_id = serializers.PrimaryKeyRelatedField(
        source="id_historia", queryset=HistoriasClinicas.objects.all(), write_only=True
    )

    id_emp = EmpleadoSerializer(read_only=True)
    id_emp_id = serializers.PrimaryKeyRelatedField(
        source="id_emp", queryset=Empleados.objects.all(), write_only=True
    )

    class Meta:
        model = ReportesMedicos
        fields = [
            "id_reporte", "id_historia", "id_historia_id",
            "id_emp", "id_emp_id", "reporte", "fecha"
        ]


class AuditoriaAccesoSerializer(serializers.ModelSerializer):
    id_emp = EmpleadoSerializer(read_only=True)
    id_emp_id = serializers.PrimaryKeyRelatedField(
        source="id_emp", queryset=Empleados.objects.all(), write_only=True
    )

    class Meta:
        model = AuditoriaAccesos
        fields = ["id_auditoria", "id_emp", "id_emp_id", "accion", "fecha", "detalle"]


# ============================================================
#   CITA — ***ESTA ES LA QUE DIO EL ERROR***
# ============================================================

class CitaSerializer(serializers.ModelSerializer):
    cod_pac = PacienteSerializer(read_only=True)
    cod_pac_id = serializers.PrimaryKeyRelatedField(
        source="cod_pac", queryset=Pacientes.objects.all(), write_only=True
    )

    id_emp = EmpleadoSerializer(read_only=True)
    id_emp_id = serializers.PrimaryKeyRelatedField(
        source="id_emp", queryset=Empleados.objects.all(), write_only=True
    )

    cod_servicio = TipoServicioSerializer(read_only=True)
    cod_servicio_id = serializers.PrimaryKeyRelatedField(
        source="cod_servicio", queryset=TiposServicio.objects.all(), write_only=True
    )

    class Meta:
        model = Citas
        fields = [
            "id_cita",
            "cod_pac", "cod_pac_id",
            "id_emp", "id_emp_id",
            "cod_servicio", "cod_servicio_id",
            "fecha_hora", "estado"
        ]


# ============================================================
#   LOGIN
# ============================================================

class LoginSerializer(serializers.Serializer):
    documento = serializers.IntegerField()
    password = serializers.CharField(write_only=True)
