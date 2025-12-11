from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.conf import settings
import jwt
import bcrypt
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractWeek, ExtractYear
from django.db import connection



from core.permissions import RolePermission

from core.models import (
    Regiones, SedesHospitalarias, DepartamentosTrabajo, DepartamentosSede,
    Cargos, Roles, TiposDocumento, TiposServicio, TipoEquipamiento,
    Proveedores, Personas, Empleados, Pacientes, Medicamentos,
    StockMedicamento, TelefonosPersona, TelefonosSede, HistoriasClinicas,
    PrescripcionesMedicamentos, RegistroMedicamentos, ReportesMedicos,
    AuditoriaAccesos, Citas, Equipamento, SedesHospitalarias
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
    AuditoriaAccesoSerializer, CitaSerializer, EquipamentoSerializer
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
            empleado = Empleados.objects.select_related('rol').get(documento_id=documento)
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
    permission_classes = [AllowAny]


class SedeHospitalariaViewSet(viewsets.ModelViewSet):
    queryset = SedesHospitalarias.objects.all()
    serializer_class = SedeHospitalariaSerializer

    def perform_create(self, serializer):
        # sincronizar secuencia antes de insertar
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT setval(
                    pg_get_serial_sequence('sedes_hospitalarias', 'id_sede'),
                    (SELECT COALESCE(MAX(id_sede), 0) FROM sedes_hospitalarias)
                );
            """)

        serializer.save()



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
    
class EquipamientoReporteView(APIView):
    def get(self, request):

        sql = """
            SELECT 
                e.cod_eq,
                e.nom_eq,
                d.nom_dept AS departamento,
                e.estado,
                e.fecha_mantenimiento,
                emp.id_emp,
                per.nom_persona AS responsable_nombre
            FROM equipamento e
            JOIN departamentos_trabajo d ON e.id_dept = d.id_dept
            JOIN empleados emp ON e.responsable = emp.id_emp
            JOIN personas per ON emp.documento = per.documento
            ORDER BY e.cod_eq;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        data = []
        for row in rows:
            cod_eq = row[0]
            nom_eq = row[1]
            departamento = row[2]
            estado = row[3]
            fecha_mantenimiento = row[4]
            responsable_id = row[5]
            responsable_nombre = row[6]

            data.append({
                "cod_eq": cod_eq,
                "nom_eq": nom_eq,
                "departamento": departamento,
                "estado": estado,
                "fecha_mantenimiento": fecha_mantenimiento.isoformat() if fecha_mantenimiento else None,
                "responsable": responsable_nombre,
                "responsable_empleado": {
                    "id_emp": responsable_id,
                    "persona": {
                        "nombre": responsable_nombre
                    }
                }
            })

        return Response(data)

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

class EmpleadosReporteView(APIView):

    def get(self, request):
        sql = """
            SELECT 
                emp.id_emp,
                per.documento,
                emp.id_dept,

                c.cargo_id,
                c.nombre AS cargo_nombre,

                r.rol_id,
                r.nombre AS rol_nombre,

                per.nom_persona,
                per.correo_per,
                per.id_sede

            FROM empleados emp
            JOIN personas per ON emp.documento = per.documento
            JOIN cargos c ON emp.cargo_id = c.cargo_id
            JOIN roles r ON emp.rol_id = r.rol_id
            ORDER BY emp.id_emp;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        data = []
        for row in rows:
            (
                id_emp, documento, id_dept,
                cargo_id, cargo_nombre,
                rol_id, rol_nombre,
                nom_persona, correo, id_sede
            ) = row

            data.append({
                "id_emp": id_emp,
                "documento": documento,
                "id_dept": id_dept,

                "cargo": {
                    "cargo_id": cargo_id,
                    "nombre": cargo_nombre
                },

                "rol": {
                    "rol_id": rol_id,
                    "nombre": rol_nombre
                },

                "persona": {
                    "documento": documento,
                    "nombre": nom_persona,
                    "correo": correo,
                    "id_sede": id_sede
                }
            })

        return Response(data)

    def post(self, request):

        persona = request.data.get("persona")
        empleado = request.data.get("empleado")

        if not persona or not empleado:
            return Response({"error": "Debe enviar persona y empleado"}, status=400)

        documento = persona.get("documento")
        nombre = persona.get("nombre")
        correo = persona.get("correo")
        fecha_nac = persona.get("fecha_nac")
        genero = persona.get("genero")
        direccion = persona.get("direccion")
        tipo_doc_id = persona.get("tipo_doc_id")
        id_sede = persona.get("id_sede")

        id_dept = empleado.get("id_dept")
        cargo_id = empleado.get("cargo_id")
        rol_id = empleado.get("rol_id")
        hash_contra = empleado.get("hash_contra")

        sql_persona = """
            INSERT INTO personas (documento, nom_persona, fecha_nac, genero, dir_per, correo_per, tipo_doc_id, id_sede)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING documento;
        """

        sql_empleado = """
            INSERT INTO empleados (documento, id_dept, cargo_id, rol_id, hash_contra)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_emp;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_persona, [
                    documento, nombre, fecha_nac, genero,
                    direccion, correo, tipo_doc_id, id_sede
                ])
                cursor.execute(sql_empleado, [
                    documento, id_dept, cargo_id, rol_id, hash_contra
                ])
                id_emp = cursor.fetchone()[0]

            return Response({
                "mensaje": "Empleado creado exitosamente",
                "id_emp": id_emp
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

class EmpleadoDetalleView(APIView):

    def get(self, request, id_emp):
        sql = """
            SELECT 
                emp.id_emp,
                per.documento,
                emp.id_dept,

                c.cargo_id,
                c.nombre AS cargo_nombre,

                r.rol_id,
                r.nombre AS rol_nombre,

                per.nom_persona

            FROM empleados emp
            JOIN personas per ON emp.documento = per.documento
            JOIN cargos c ON emp.cargo_id = c.cargo_id
            JOIN roles r ON emp.rol_id = r.rol_id
            WHERE emp.id_emp = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [id_emp])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Empleado no encontrado"}, status=404)

        (
            id_emp,
            documento,
            id_dept,
            cargo_id,
            cargo_nombre,
            rol_id,
            rol_nombre,
            persona_nombre
        ) = row

        data = {
            "id_emp": id_emp,
            "documento": documento,
            "id_dept": id_dept,
            "cargo_id": cargo_id,
            "rol_id": rol_id,
            "persona": {
                "documento": documento,
                "nombre": persona_nombre
            },
            "cargo": {
                "cargo_id": cargo_id,
                "cargo_nombre": cargo_nombre
            },
            "rol": {
                "rol_id": rol_id,
                "rol_nombre": rol_nombre
            }
        }

        return Response(data)

    def put(self, request, id_emp):

        persona = request.data.get("persona")
        empleado = request.data.get("empleado")

        if not persona and not empleado:
            return Response({"error": "Debe enviar datos en persona o empleado"}, status=400)

        sql_doc = "SELECT documento FROM empleados WHERE id_emp = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql_doc, [id_emp])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Empleado no encontrado"}, status=404)

        documento = row[0]

        if persona:
            fields = []
            values = []

            field_map = {
                "nombre": "nom_persona",
                "correo": "correo_per",
                "fecha_nac": "fecha_nac",
                "genero": "genero",
                "direccion": "dir_per",
                "id_sede": "id_sede"
            }

            for key, column in field_map.items():
                if key in persona:
                    fields.append(f"{column} = %s")
                    values.append(persona[key])

            if fields:
                sql_update_persona = f"""
                    UPDATE personas
                    SET {", ".join(fields)}
                    WHERE documento = %s
                """
                values.append(documento)

                with connection.cursor() as cursor:
                    cursor.execute(sql_update_persona, values)
        if empleado:
            fields = []
            values = []

            field_map = {
                "id_dept": "id_dept",
                "cargo_id": "cargo_id",
                "rol_id": "rol_id",
                "hash_contra": "hash_contra"
            }

            for key, column in field_map.items():
                if key in empleado:
                    fields.append(f"{column} = %s")
                    values.append(empleado[key])

            if fields:
                sql_update_empleado = f"""
                    UPDATE empleados
                    SET {", ".join(fields)}
                    WHERE id_emp = %s
                """
                values.append(id_emp)

                with connection.cursor() as cursor:
                    cursor.execute(sql_update_empleado, values)

        return Response({"mensaje": "Empleado actualizado correctamente"})


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Pacientes.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [AllowAny]
    
class PacientesView(APIView):

    def get(self, request):
        sql = """
            SELECT 
                p.cod_pac,
                per.documento,
                per.nom_persona
            FROM pacientes p
            JOIN personas per ON p.documento = per.documento
            ORDER BY p.cod_pac;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        data = [
            {
                "cod_pac": row[0],
                "documento": row[1],
                "persona": {
                    "documento": row[1],
                    "nombre": row[2]
                }
            }
            for row in rows
        ]

        return Response(data)

    def post(self, request):

        persona = request.data.get("persona")

        if not persona:
            return Response({"error": "Debe enviar el objeto 'persona'"}, status=400)

        documento = persona.get("documento")
        nombre = persona.get("nombre")
        fecha_nac = persona.get("fecha_nac")
        genero = persona.get("genero")
        direccion = persona.get("direccion")
        correo = persona.get("correo")
        tipo_doc_id = persona.get("tipo_doc_id")
        id_sede = persona.get("id_sede")

        if not documento or not nombre:
            return Response({"error": "documento y nombre son obligatorios"}, status=400)

        sql_persona = """
            INSERT INTO personas (documento, nom_persona, fecha_nac, genero, dir_per, correo_per, tipo_doc_id, id_sede)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING documento;
        """

        sql_paciente = """
            INSERT INTO pacientes (documento)
            VALUES (%s)
            RETURNING cod_pac;
        """

        try:
            with connection.cursor() as cursor:

                cursor.execute(sql_persona, [
                    documento, nombre, fecha_nac, genero,
                    direccion, correo, tipo_doc_id, id_sede
                ])
                cursor.fetchone()

                cursor.execute(sql_paciente, [documento])
                cod_pac = cursor.fetchone()[0]

            data = {
                "cod_pac": cod_pac,
                "documento": documento,
                "persona": {
                    "documento": documento,
                    "nombre": nombre
                }
            }

            return Response(data, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

class PacienteDetalleView(APIView):

    def get(self, request, cod_pac):

        sql = """
            SELECT 
                p.cod_pac,
                per.documento,
                per.nom_persona
            FROM pacientes p
            JOIN personas per ON p.documento = per.documento
            WHERE p.cod_pac = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [cod_pac])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Paciente no encontrado"}, status=404)

        cod_pac, documento, nombre = row

        data = {
            "cod_pac": cod_pac,
            "documento": documento,
            "persona": {
                "documento": documento,
                "nombre": nombre
            }
        }

        return Response(data)

    def put(self, request, cod_pac):

        persona_data = request.data.get("persona")

        if not persona_data:
            return Response({"error": "Debe enviar el objeto 'persona'"}, status=400)

        sql_get_doc = "SELECT documento FROM pacientes WHERE cod_pac = %s;"

        with connection.cursor() as cursor:
            cursor.execute(sql_get_doc, [cod_pac])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Paciente no encontrado"}, status=404)

        documento = row[0]

        nombre = persona_data.get("nombre")
        fecha_nac = persona_data.get("fecha_nac")
        genero = persona_data.get("genero")
        direccion = persona_data.get("direccion")
        correo = persona_data.get("correo")
        tipo_doc_id = persona_data.get("tipo_doc_id")
        id_sede = persona_data.get("id_sede")

        campos = []
        valores = []

        if nombre is not None:
            campos.append("nom_persona = %s")
            valores.append(nombre)

        if fecha_nac is not None:
            campos.append("fecha_nac = %s")
            valores.append(fecha_nac)

        if genero is not None:
            campos.append("genero = %s")
            valores.append(genero)

        if direccion is not None:
            campos.append("dir_per = %s")
            valores.append(direccion)

        if correo is not None:
            campos.append("correo_per = %s")
            valores.append(correo)

        if tipo_doc_id is not None:
            campos.append("tipo_doc_id = %s")
            valores.append(tipo_doc_id)

        if id_sede is not None:
            campos.append("id_sede = %s")
            valores.append(id_sede)

        if not campos:
            return Response({"error": "No hay campos válidos para actualizar"}, status=400)

        valores.append(documento)

        sql_update = f"""
            UPDATE personas
            SET {", ".join(campos)}
            WHERE documento = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_update, valores)

        return Response({"mensaje": "Paciente actualizado correctamente"})

    def delete(self, request, cod_pac):

        sql_check = "SELECT documento FROM pacientes WHERE cod_pac = %s;"

        with connection.cursor() as cursor:
            cursor.execute(sql_check, [cod_pac])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Paciente no encontrado"}, status=404)

        documento = row[0]

        sql_delete = "DELETE FROM pacientes WHERE cod_pac = %s;"

        with connection.cursor() as cursor:
            cursor.execute(sql_delete, [cod_pac])

        return Response({
            "mensaje": "Paciente eliminado correctamente",
            "cod_pac": cod_pac,
            "documento": documento
        })


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


class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    permission_classes = [AllowAny]


class TelefonoSedeViewSet(viewsets.ModelViewSet):
    queryset = TelefonosSede.objects.all()
    serializer_class = TelefonoSedeSerializer
    permission_classes = [AllowAny]
    
class TelefonosSedeView(APIView):

    def get(self, request, id_sede):
        sql = """
            SELECT id_sede, numero
            FROM telefonos_sede
            WHERE id_sede = %s;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [id_sede])
            rows = cursor.fetchall()

        data = [
            {"id_sede": row[0], "numero": row[1]}
            for row in rows
        ]

        return Response(data)

    def post(self, request, id_sede):
        numero = request.data.get("numero")

        if not numero:
            return Response({"error": "El número es obligatorio"}, status=400)

        sql = """
            INSERT INTO telefonos_sede (id_sede, numero)
            VALUES (%s, %s)
            RETURNING id_sede, numero;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, [id_sede, numero])
                row = cursor.fetchone()

            return Response({
                "id_sede": row[0],
                "numero": row[1]
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def delete(self, request, id_sede):
        numero = request.query_params.get("numero")

        if not numero:
            return Response({"error": "Debe proporcionar ?numero=... en el query"}, status=400)

        sql = """
            DELETE FROM telefonos_sede
            WHERE id_sede = %s AND numero = %s
            RETURNING id_sede, numero;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [id_sede, numero])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "El número no existe en esta sede"}, status=404)

        return Response({
            "id_sede": row[0],
            "numero": row[1],
            "mensaje": "Número eliminado correctamente"
        })


class TelefonosPorSedeView(APIView):
    def get(self, request, id_sede):

        sql = """
            SELECT t.id_sede, t.numero
            FROM telefonos_sede t
            WHERE t.id_sede = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [id_sede])
            rows = cursor.fetchall()

        data = [
            {
                "id_sede": row[0],
                "numero": row[1]
            }
            for row in rows
        ]

        return Response(data)

class HistoriaClinicaViewSet(viewsets.ModelViewSet):
    queryset = HistoriasClinicas.objects.all()
    serializer_class = HistoriaClinicaSerializer

    def list(self, request):

        sql = """
            SELECT 
                h.cod_hist,
                h.fecha_hora,
                h.diagnostico,

                -- Paciente
                per_pac.nom_persona AS paciente_nombre,

                -- Empleado
                per_emp.nom_persona AS empleado_nombre

            FROM historias_clinicas h
            JOIN citas c ON h.id_cita = c.id_cita

            -- Paciente
            JOIN pacientes pac ON c.cod_pac = pac.cod_pac
            JOIN personas per_pac ON pac.documento = per_pac.documento

            -- Empleado
            JOIN empleados emp ON c.id_emp = emp.id_emp
            JOIN personas per_emp ON emp.documento = per_emp.documento

            ORDER BY h.cod_hist;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        data = []

        for row in rows:
            cod_hist = row[0]
            fecha = row[1]
            diagnostico = row[2]
            paciente_nombre = row[3]
            empleado_nombre = row[4]

            data.append({
                "cod_hist": cod_hist,
                "fecha_registro_hora": fecha.isoformat(),
                "diagnostico": diagnostico,
                "paciente": paciente_nombre,
                "empleado": empleado_nombre
            })

        return Response(data)

class PrescripcionMedicamentoViewSet(viewsets.ModelViewSet):
    queryset = PrescripcionesMedicamentos.objects.all()
    serializer_class = PrescripcionMedicamentoSerializer
    permission_classes = [AllowAny]

class HistoriaClinicaDetalleView(APIView):

    def get(self, request, cod_hist):

        sql_hist = """
            SELECT 
                h.cod_hist,
                h.fecha_hora,
                h.diagnostico,
                c.cod_pac,
                p_pac.nom_persona AS paciente_nombre,
                c.id_emp,
                p_emp.nom_persona AS empleado_nombre
            FROM historias_clinicas h
            JOIN citas c ON h.id_cita = c.id_cita
            
            -- Paciente
            JOIN pacientes pac ON c.cod_pac = pac.cod_pac
            JOIN personas p_pac ON pac.documento = p_pac.documento

            -- Empleado
            JOIN empleados e ON c.id_emp = e.id_emp
            JOIN personas p_emp ON e.documento = p_emp.documento

            WHERE h.cod_hist = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_hist, [cod_hist])
            row = cursor.fetchone()

        if not row:
            return Response({"error": "Historia clínica no encontrada"}, status=404)

        (
            cod_hist,
            fecha,
            diagnostico,
            cod_pac,
            paciente_nombre,
            id_emp,
            empleado_nombre
        ) = row

        sql_presc = """
            SELECT 
                id_presc,
                cod_med,
                dosis,
                frecuencia,
                duracion_dias,
                fecha_emision
            FROM prescripciones_medicamentos
            WHERE cod_hist = %s
            ORDER BY id_presc;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_presc, [cod_hist])
            presc_rows = cursor.fetchall()

        prescripciones = [
            {
                "id_presc": p[0],
                "cod_med": p[1],
                "dosis": p[2],
                "frecuencia": p[3],
                "duracion_dias": p[4],
                "fecha_emision": p[5].isoformat() if p[5] else None
            }
            for p in presc_rows
        ]

        data = {
            "cod_hist": cod_hist,
            "fecha_registro_hora": fecha.isoformat(),
            "diagnostico": diagnostico,
            "cod_pac": cod_pac,
            "id_emp": id_emp,
            "paciente_nombre": paciente_nombre,
            "empleado_nombre": empleado_nombre,
            "prescripciones": prescripciones
        }

        return Response(data, status=200)


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
    
# ================================================================
#                        DASHBOARD REPORTS
# ================================================================

class TopEnfermedadesReporte(APIView):
    def get(self, request):

        sql = """
            SELECT 
                h.diagnostico,
                s.nom_sede AS sede,
                COUNT(h.diagnostico) AS total
            FROM historias_clinicas h
            JOIN citas c ON h.id_cita = c.id_cita
            JOIN pacientes p ON c.cod_pac = p.cod_pac
            JOIN personas per ON p.documento = per.documento
            JOIN sedes_hospitalarias s ON per.id_sede = s.id_sede
            GROUP BY h.diagnostico, s.nom_sede
            ORDER BY total DESC
            LIMIT 5;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        data = [
            {
                "enfermedad": row[0],
                "sede": row[1],
                "casos": row[2]
            }
            for row in rows
        ]

        return Response(data)

    
class MedicamentosRecetadosReporte(APIView):
    def get(self, request):

        sql = """
            SELECT 
                m.nom_med AS nombre_medicamento,
                TO_CHAR(p.fecha_emision, 'YYYY-MM') AS mes,
                COUNT(*) AS cantidad
            FROM prescripciones_medicamentos p
            LEFT JOIN medicamentos m ON p.cod_med = m.cod_med
            GROUP BY nombre_medicamento, mes
            ORDER BY mes;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        data = [
            {
                "medicamento": row[0] if row[0] is not None else "(Desconocido)",
                "mes": row[1],
                "cantidad": row[2],
            }
            for row in rows
        ]

        return Response(data)


class MedicosTopConsultasReporte(APIView):
    def get(self, request):

        sql = """
            SELECT 
                per.nom_persona AS medico,
                DATE_PART('year', c.fecha_hora)::int AS anio,
                DATE_PART('week', c.fecha_hora)::int AS semana,
                COUNT(*) AS total_consultas
            FROM citas c
            JOIN empleados e ON c.id_emp = e.id_emp
            JOIN personas per ON e.documento = per.documento
            WHERE c.estado = 'Atendida'
            GROUP BY medico, anio, semana
            ORDER BY anio, semana;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        data = [
            {
                "medico": row[0] if row[0] else "(Nombre no disponible)",
                "semana": f"{int(row[1])}-W{int(row[2]):02d}",
                "consultas": row[3]
            }
            for row in rows
        ]

        return Response(data)


    
class PacientesPorSedeReporte(APIView):
    def get(self, request):

        sql = """
            SELECT 
                s.nom_sede AS sede,
                COUNT(pac.documento) AS total_pacientes
            FROM pacientes pac
            JOIN personas per ON pac.documento = per.documento
            JOIN sedes_hospitalarias s ON per.id_sede = s.id_sede
            GROUP BY s.nom_sede
            ORDER BY total_pacientes DESC;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        data = [
            {
                "sede": row[0],
                "total_pacientes": row[1]
            }
            for row in rows
        ]

        return Response(data)
    
class TiemposAtencionReporte(APIView):
    def get(self, request):
        sql = """
            SELECT 
                s.nom_sede AS sede,
                AVG(EXTRACT(EPOCH FROM (h.fecha_hora - c.fecha_hora)) / 60.0) AS tiempo_promedio
            FROM historias_clinicas h
            JOIN citas c ON h.id_cita = c.id_cita
            JOIN pacientes p ON c.cod_pac = p.cod_pac
            JOIN personas per ON p.documento = per.documento
            JOIN sedes_hospitalarias s ON per.id_sede = s.id_sede
            GROUP BY s.nom_sede
            ORDER BY s.nom_sede;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        data = [
            {"sede": row[0], "tiempo_promedio": float(row[1]) if row[1] is not None else None}
            for row in rows
        ]

        return Response(data)