# Hospital Backend API - Endpoints Documentation

## Base URL
```
http://localhost:8000
```

## API Prefix
```
/api
```

---

## 1. /api/regiones/

**Description:** CRUD operations for regiones

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/regiones/
POST /api/regiones/
GET /api/regiones/{id}/
PUT /api/regiones/{id}/
PATCH /api/regiones/{id}/
DELETE /api/regiones/{id}/
```

### Response Fields
```json
{
  "region_id": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "nombre": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 100
  }
}
```

---

## 2. /api/sedes/

**Description:** CRUD operations for sedes

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/sedes/
POST /api/sedes/
GET /api/sedes/{id}/
PUT /api/sedes/{id}/
PATCH /api/sedes/{id}/
DELETE /api/sedes/{id}/
```

### Response Fields
```json
{
  "id_sede": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "nom_sede": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 100
  },
  "ciudad": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 80
  },
  "region": {
    "type": "RegionSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "region_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  }
}
```

---

## 3. /api/departamentos/

**Description:** CRUD operations for departamentos

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/departamentos/
POST /api/departamentos/
GET /api/departamentos/{id}/
PUT /api/departamentos/{id}/
PATCH /api/departamentos/{id}/
DELETE /api/departamentos/{id}/
```

### Response Fields
```json
{
  "id_dept": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "nom_dept": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 100
  }
}
```

---

## 4. /api/cargos/

**Description:** CRUD operations for cargos

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/cargos/
POST /api/cargos/
GET /api/cargos/{id}/
PUT /api/cargos/{id}/
PATCH /api/cargos/{id}/
DELETE /api/cargos/{id}/
```

### Response Fields
```json
{
  "cargo_id": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "nombre": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 100
  }
}
```

---

## 5. /api/roles/

**Description:** CRUD operations for roles

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/roles/
POST /api/roles/
GET /api/roles/{id}/
PUT /api/roles/{id}/
PATCH /api/roles/{id}/
DELETE /api/roles/{id}/
```

### Response Fields
```json
{
  "rol_id": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "nombre": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 80
  }
}
```

---

## 6. /api/tipos-documento/

**Description:** CRUD operations for tipos-documento

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/tipos-documento/
POST /api/tipos-documento/
GET /api/tipos-documento/{id}/
PUT /api/tipos-documento/{id}/
PATCH /api/tipos-documento/{id}/
DELETE /api/tipos-documento/{id}/
```

### Response Fields
```json
{
  "tipo_doc_id": {
    "type": "IntegerField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "nombre": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 50
  }
}
```

---

## 7. /api/tipos-servicio/

**Description:** CRUD operations for tipos-servicio

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/tipos-servicio/
POST /api/tipos-servicio/
GET /api/tipos-servicio/{id}/
PUT /api/tipos-servicio/{id}/
PATCH /api/tipos-servicio/{id}/
DELETE /api/tipos-servicio/{id}/
```

### Response Fields
```json
{
  "cod_servicio": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "nombre": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 80
  }
}
```

---

## 8. /api/tipos-equipamiento/

**Description:** CRUD operations for tipos-equipamiento

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/tipos-equipamiento/
POST /api/tipos-equipamiento/
GET /api/tipos-equipamiento/{id}/
PUT /api/tipos-equipamiento/{id}/
PATCH /api/tipos-equipamiento/{id}/
DELETE /api/tipos-equipamiento/{id}/
```

### Response Fields
```json
{
  "tipo_equipo_id": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "nombre": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 80
  }
}
```

---

## 9. /api/proveedores/

**Description:** CRUD operations for proveedores

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/proveedores/
POST /api/proveedores/
GET /api/proveedores/{id}/
PUT /api/proveedores/{id}/
PATCH /api/proveedores/{id}/
DELETE /api/proveedores/{id}/
```

### Response Fields
```json
{
  "proveedor_id": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "nombre": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 100
  },
  "region": {
    "type": "RegionSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "region_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  }
}
```

---

## 10. /api/personas/

**Description:** CRUD operations for personas

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/personas/
POST /api/personas/
GET /api/personas/{id}/
PUT /api/personas/{id}/
PATCH /api/personas/{id}/
DELETE /api/personas/{id}/
```

### Response Fields
```json
{
  "documento": {
    "type": "IntegerField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "nom_persona": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 150
  },
  "fecha_nac": {
    "type": "DateField",
    "required": false,
    "read_only": false,
    "allow_null": true
  },
  "genero": {
    "type": "CharField",
    "required": false,
    "read_only": false,
    "allow_null": true,
    "max_length": 1
  },
  "dir_per": {
    "type": "CharField",
    "required": false,
    "read_only": false,
    "allow_null": true,
    "max_length": 150
  },
  "correo_per": {
    "type": "CharField",
    "required": false,
    "read_only": false,
    "allow_null": true,
    "max_length": 120
  },
  "tipo_doc": {
    "type": "TipoDocumentoSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "tipo_doc_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "id_sede": {
    "type": "SedeHospitalariaSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "id_sede_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  }
}
```

---

## 11. /api/empleados/

**Description:** CRUD operations for empleados

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/empleados/
POST /api/empleados/
GET /api/empleados/{id}/
PUT /api/empleados/{id}/
PATCH /api/empleados/{id}/
DELETE /api/empleados/{id}/
```

### Response Fields
```json
{
  "id_emp": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "documento": {
    "type": "PersonaSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "documento_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "id_dept": {
    "type": "DepartamentoTrabajoSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "id_dept_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "cargo": {
    "type": "CargoSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "cargo_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "rol": {
    "type": "RolSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "rol_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "hash_contra": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false
  }
}
```

---

## 12. /api/pacientes/

**Description:** CRUD operations for pacientes

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/pacientes/
POST /api/pacientes/
GET /api/pacientes/{id}/
PUT /api/pacientes/{id}/
PATCH /api/pacientes/{id}/
DELETE /api/pacientes/{id}/
```

### Response Fields
```json
{
  "cod_pac": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "documento": {
    "type": "PersonaSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "documento_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  }
}
```

---

## 13. /api/citas/

**Description:** CRUD operations for citas

**Methods:** GET, POST, PUT, PATCH, DELETE

### Examples
```
GET /api/citas/
POST /api/citas/
GET /api/citas/{id}/
PUT /api/citas/{id}/
PATCH /api/citas/{id}/
DELETE /api/citas/{id}/
```

### Response Fields
```json
{
  "id_cita": {
    "type": "IntegerField",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "cod_pac": {
    "type": "PacienteSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "cod_pac_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "id_emp": {
    "type": "EmpleadoSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "id_emp_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "cod_servicio": {
    "type": "TipoServicioSerializer",
    "required": false,
    "read_only": true,
    "allow_null": false
  },
  "cod_servicio_id": {
    "type": "PrimaryKeyRelatedField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "fecha_hora": {
    "type": "DateTimeField",
    "required": true,
    "read_only": false,
    "allow_null": false
  },
  "estado": {
    "type": "CharField",
    "required": true,
    "read_only": false,
    "allow_null": false,
    "max_length": 20
  }
}
```

---

## 14. /api/login/

**Description:** Authentication endpoint - returns JWT token

**Methods:** POST

### Example Request
```json
{
  "documento": 12345678,
  "password": "password123"
}
```

### Request Fields
- **documento** (integer) - Required: Employee document number
- **password** (string) - Required: Employee password

### Response Fields
```json
{
  "token": {
    "type": "string",
    "description": "JWT authentication token"
  },
  "empleado": {
    "type": "object",
    "description": "Employee data"
  }
}
```

---

