from django.db import models


# ============================
#        TABLAS BASE
# ============================

class Cargos(models.Model):
    cargo_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'cargos'


class DepartamentosTrabajo(models.Model):
    id_dept = models.AutoField(primary_key=True)
    nom_dept = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'departamentos_trabajo'


class Regiones(models.Model):
    region_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'regiones'


class SedesHospitalarias(models.Model):
    id_sede = models.AutoField(primary_key=True)
    nom_sede = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=80)
    region = models.ForeignKey(Regiones, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sedes_hospitalarias'


class TiposDocumento(models.Model):
    tipo_doc_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tipos_documento'


class TiposServicio(models.Model):
    cod_servicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'tipos_servicio'


class TipoEquipamiento(models.Model):
    tipo_equipo_id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'tipo_equipamiento'


class Roles(models.Model):
    rol_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'roles'



# ============================
#        PERSONAS
# ============================

class Personas(models.Model):
    documento = models.IntegerField(primary_key=True)
    nom_persona = models.CharField(max_length=150)
    fecha_nac = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=1, blank=True, null=True)
    dir_per = models.CharField(max_length=150, blank=True, null=True)
    correo_per = models.CharField(max_length=120, blank=True, null=True)
    tipo_doc = models.ForeignKey(TiposDocumento, models.DO_NOTHING)
    id_sede = models.ForeignKey(SedesHospitalarias, models.DO_NOTHING, db_column='id_sede')

    class Meta:
        managed = False
        db_table = 'personas'



# ============================
#        EMPLEADOS
# ============================

class Empleados(models.Model):
    id_emp = models.AutoField(primary_key=True)
    documento = models.ForeignKey(Personas, models.DO_NOTHING, db_column='documento')
    id_dept = models.ForeignKey(DepartamentosTrabajo, models.DO_NOTHING, db_column='id_dept')
    cargo = models.ForeignKey(Cargos, models.DO_NOTHING)
    rol = models.ForeignKey(Roles, models.DO_NOTHING)
    hash_contra = models.TextField()

    @property
    def is_authenticated(self):
        return True

    class Meta:
        managed = False
        db_table = 'empleados'



# ============================
#        PACIENTES
# ============================

class Pacientes(models.Model):
    cod_pac = models.AutoField(primary_key=True)
    documento = models.ForeignKey(Personas, models.DO_NOTHING, db_column='documento')

    class Meta:
        managed = False
        db_table = 'pacientes'



# ============================
#        CITAS
# ============================

class Citas(models.Model):
    id_cita = models.AutoField(primary_key=True)
    cod_pac = models.ForeignKey(Pacientes, models.DO_NOTHING, db_column='cod_pac')
    id_emp = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_emp')
    cod_servicio = models.ForeignKey(TiposServicio, models.DO_NOTHING, db_column='cod_servicio')
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'citas'



# ============================
#     HISTORIAS CLÍNICAS
# ============================

class HistoriasClinicas(models.Model):
    cod_hist = models.AutoField(primary_key=True)
    id_cita = models.ForeignKey(Citas, models.DO_NOTHING, db_column='id_cita')
    fecha_hora = models.DateTimeField()
    diagnostico = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'historias_clinicas'



# ============================
#     PRESCRIPCIONES
# ============================

class Medicamentos(models.Model):
    cod_med = models.AutoField(primary_key=True)
    nom_med = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True, null=True)
    unidad = models.CharField(max_length=20)
    proveedor = models.ForeignKey('Proveedores', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'medicamentos'


class PrescripcionesMedicamentos(models.Model):
    id_presc = models.AutoField(primary_key=True)
    cod_hist = models.ForeignKey(HistoriasClinicas, models.DO_NOTHING, db_column='cod_hist')
    cod_med = models.ForeignKey(Medicamentos, models.DO_NOTHING, db_column='cod_med')
    dosis = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=50)
    duracion_dias = models.IntegerField()
    fecha_emision = models.DateField()

    class Meta:
        managed = False
        db_table = 'prescripciones_medicamentos'



# ============================
#        PROVEEDORES
# ============================

class Proveedores(models.Model):
    proveedor_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Regiones, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'proveedores'



# ============================
#       EQUIPAMIENTO
# ============================

class Equipamento(models.Model):
    cod_eq = models.AutoField(primary_key=True)
    id_dept = models.ForeignKey(DepartamentosTrabajo, models.DO_NOTHING, db_column='id_dept')
    responsable = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='responsable')
    nom_eq = models.CharField(max_length=120)
    estado = models.CharField(max_length=20)
    fecha_mantenimiento = models.DateField()

    class Meta:
        managed = False
        db_table = 'equipamento'



# ============================
#        REPORTES
# ============================

class ReportesMedicos(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    id_emp = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_emp')
    id_sede = models.ForeignKey(SedesHospitalarias, models.DO_NOTHING, db_column='id_sede')
    fecha_generacion = models.DateField()
    tipo_reporte = models.TextField()
    resumen = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reportes_medicos'



# ============================
#      TABLAS COMPUESTAS
# ============================

class DepartamentosSede(models.Model):
    id = models.AutoField(primary_key=True)
    id_sede = models.ForeignKey(SedesHospitalarias, models.DO_NOTHING, db_column='id_sede')
    id_dept = models.ForeignKey(DepartamentosTrabajo, models.DO_NOTHING, db_column='id_dept')

    class Meta:
        managed = False
        db_table = 'departamentos_sede'
        unique_together = (("id_sede", "id_dept"),)


class TelefonosPersona(models.Model):
    id = models.AutoField(primary_key=True)
    documento = models.ForeignKey(Personas, models.DO_NOTHING, db_column='documento')
    numero = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'telefonos_persona'
        unique_together = (("documento", "numero"),)


class TelefonosSede(models.Model):
    id = models.AutoField(primary_key=True)
    id_sede = models.ForeignKey(SedesHospitalarias, models.DO_NOTHING, db_column='id_sede')
    numero = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'telefonos_sede'
        unique_together = (("id_sede", "numero"),)


class StockMedicamento(models.Model):
    id = models.AutoField(primary_key=True)
    cod_med = models.ForeignKey(Medicamentos, models.DO_NOTHING, db_column='cod_med')
    id_sede = models.ForeignKey(SedesHospitalarias, models.DO_NOTHING, db_column='id_sede')
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stock_medicamento'
        unique_together = (("cod_med", "id_sede"),)


class RegistroMedicamentos(models.Model):
    id = models.AutoField(primary_key=True)
    cod_med = models.ForeignKey(Medicamentos, models.DO_NOTHING, db_column='cod_med')
    id_dept = models.ForeignKey(DepartamentosTrabajo, models.DO_NOTHING, db_column='id_dept')
    fecha_hora = models.DateTimeField()
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registro_medicamentos'
        unique_together = (("cod_med", "id_dept", "fecha_hora"),)



# ============================
#         AUDITORÍA
# ============================

class AuditoriaAccesos(models.Model):
    id_evento = models.AutoField(primary_key=True)
    id_emp = models.ForeignKey(Empleados, models.DO_NOTHING, db_column='id_emp')
    accion = models.CharField(max_length=20)
    tabla_afectada = models.CharField(max_length=50)
    fecha_evento = models.DateField()
    ip_origen = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditoria_accesos'
