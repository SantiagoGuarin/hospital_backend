from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register("regiones", RegionViewSet, basename="regiones")
router.register("sedes", SedeHospitalariaViewSet, basename="sedes")
router.register("historias", HistoriaClinicaViewSet, basename="historias")
router.register("departamentos", DepartamentoTrabajoViewSet, basename="departamentos")
router.register("cargos", CargoViewSet, basename="cargos")
router.register("roles", RolViewSet, basename="roles")
router.register("tipos-documento", TipoDocumentoViewSet, basename="tipos-documento")
router.register("tipos-servicio", TipoServicioViewSet, basename="tipos-servicio")
router.register("tipos-equipamiento", TipoEquipamientoViewSet, basename="tipos-equipamiento")
router.register("proveedores", ProveedorViewSet, basename="proveedores")
router.register("personas", PersonaViewSet, basename="personas")
router.register("citas", CitaViewSet, basename="citas")
router.register("medicamentos", MedicamentoViewSet, basename="medicamentos")
router.register("equipamento", EquipamentoViewSet, basename="equipamento")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("reportes/top-enfermedades/", TopEnfermedadesReporte.as_view()),
    path("reportes/medicamentos-recetados/", MedicamentosRecetadosReporte.as_view()),
    path("reportes/medicos-top-consultas/", MedicosTopConsultasReporte.as_view()),
    path("reportes/pacientes-por-sede/", PacientesPorSedeReporte.as_view()),
    path("reportes/tiempos-atencion/", TiemposAtencionReporte.as_view()),
    path("sedes/<int:id_sede>/telefonos/", TelefonosPorSedeView.as_view()),
    path("sedes/<int:id_sede>/telefonos/", TelefonosSedeView.as_view()),
    path("equipamiento/", EquipamientoReporteView.as_view()),
    path("empleados/", EmpleadosReporteView.as_view()),
    path("empleados/<int:id_emp>/", EmpleadoDetalleView.as_view()),
    path("pacientes/", PacientesReporteView.as_view()),

]
