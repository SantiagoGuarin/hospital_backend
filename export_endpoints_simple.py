#!/usr/bin/env python
"""
Script para exportar todos los endpoints y sus estructuras de datos
"""
import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from core.serializers import *
from rest_framework import serializers

def get_serializer_fields(serializer_class):
    """Extrae los campos de un serializer"""
    try:
        serializer = serializer_class()
        fields = {}
        for field_name, field in serializer.fields.items():
            field_info = {
                'type': field.__class__.__name__,
                'required': field.required,
                'read_only': field.read_only,
                'allow_null': field.allow_null,
            }
            
            if hasattr(field, 'max_length') and field.max_length:
                field_info['max_length'] = field.max_length
            if hasattr(field, 'help_text') and field.help_text:
                field_info['help_text'] = str(field.help_text)
                
            fields[field_name] = field_info
        return fields
    except Exception as e:
        return {'error': str(e)}

def generate_endpoints_doc():
    """Genera la documentación de endpoints"""
    endpoints = []
    
    # Endpoints del router
    router_endpoints = [
        {'name': 'regiones', 'serializer': 'RegionSerializer'},
        {'name': 'sedes', 'serializer': 'SedeHospitalariaSerializer'},
        {'name': 'departamentos', 'serializer': 'DepartamentoTrabajoSerializer'},
        {'name': 'cargos', 'serializer': 'CargoSerializer'},
        {'name': 'roles', 'serializer': 'RolSerializer'},
        {'name': 'tipos-documento', 'serializer': 'TipoDocumentoSerializer'},
        {'name': 'tipos-servicio', 'serializer': 'TipoServicioSerializer'},
        {'name': 'tipos-equipamiento', 'serializer': 'TipoEquipamientoSerializer'},
        {'name': 'proveedores', 'serializer': 'ProveedorSerializer'},
        {'name': 'personas', 'serializer': 'PersonaSerializer'},
        {'name': 'empleados', 'serializer': 'EmpleadoSerializer'},
        {'name': 'pacientes', 'serializer': 'PacienteSerializer'},
        {'name': 'citas', 'serializer': 'CitaSerializer'},
    ]
    
    # Agregar endpoints del router
    for endpoint in router_endpoints:
        serializer_name = endpoint['serializer']
        try:
            serializer_class = globals()[serializer_name]
            fields = get_serializer_fields(serializer_class)
            
            endpoints.append({
                'path': f'/api/{endpoint["name"]}/',
                'methods': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
                'description': f'CRUD operations for {endpoint["name"]}',
                'response_fields': fields,
                'examples': {
                    'list': f'GET /api/{endpoint["name"]}/',
                    'create': f'POST /api/{endpoint["name"]}/',
                    'retrieve': f'GET /api/{endpoint["name"]}/{{id}}/',
                    'update': f'PUT /api/{endpoint["name"]}/{{id}}/',
                    'partial_update': f'PATCH /api/{endpoint["name"]}/{{id}}/',
                    'delete': f'DELETE /api/{endpoint["name"]}/{{id}}/',
                }
            })
        except KeyError:
            print(f"⚠️  No se encontró serializer: {serializer_name}")
    
    # Agregar endpoint de login
    endpoints.append({
        'path': '/api/login/',
        'methods': ['POST'],
        'description': 'Authentication endpoint - returns JWT token',
        'request_fields': {
            'documento': {'type': 'integer', 'required': True, 'description': 'Employee document number'},
            'password': {'type': 'string', 'required': True, 'description': 'Employee password'},
        },
        'response_fields': {
            'token': {'type': 'string', 'description': 'JWT authentication token'},
            'empleado': {'type': 'object', 'description': 'Employee data'},
        },
        'example_request': {
            'documento': 12345678,
            'password': 'password123'
        }
    })
    
    return endpoints

def save_endpoints_json():
    """Guarda los endpoints en formato JSON"""
    endpoints = generate_endpoints_doc()
    
    output = {
        'project': 'Hospital Backend API',
        'version': '1.0.0',
        'base_url': 'http://localhost:8000',
        'api_prefix': '/api',
        'endpoints': endpoints,
        'total_endpoints': len(endpoints),
    }
    
    with open('ENDPOINTS.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("✅ Endpoints exportados a ENDPOINTS.json")
    return output

def save_endpoints_markdown():
    """Guarda los endpoints en formato Markdown"""
    endpoints = generate_endpoints_doc()
    
    md_content = """# Hospital Backend API - Endpoints Documentation

## Base URL
```
http://localhost:8000
```

## API Prefix
```
/api
```

---

"""
    
    for i, endpoint in enumerate(endpoints, 1):
        md_content += f"## {i}. {endpoint['path']}\n\n"
        md_content += f"**Description:** {endpoint['description']}\n\n"
        md_content += f"**Methods:** {', '.join(endpoint['methods'])}\n\n"
        
        if 'examples' in endpoint:
            md_content += "### Examples\n```\n"
            for key, value in endpoint['examples'].items():
                md_content += f"{value}\n"
            md_content += "```\n\n"
        
        if 'example_request' in endpoint:
            md_content += "### Example Request\n"
            md_content += "```json\n"
            md_content += json.dumps(endpoint['example_request'], indent=2, ensure_ascii=False)
            md_content += "\n```\n\n"
        
        if 'request_fields' in endpoint:
            md_content += "### Request Fields\n"
            for field_name, field_info in endpoint['request_fields'].items():
                md_content += f"- **{field_name}** ({field_info['type']}) - {'Required' if field_info.get('required') else 'Optional'}"
                if 'description' in field_info:
                    md_content += f": {field_info['description']}"
                md_content += "\n"
            md_content += "\n"
        
        if 'response_fields' in endpoint:
            md_content += "### Response Fields\n"
            md_content += "```json\n"
            md_content += json.dumps(endpoint['response_fields'], indent=2, ensure_ascii=False)
            md_content += "\n```\n\n"
        
        md_content += "---\n\n"
    
    with open('ENDPOINTS.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print("✅ Endpoints exportados a ENDPOINTS.md")

def print_endpoints_table():
    """Imprime una tabla de endpoints en la consola"""
    endpoints = generate_endpoints_doc()
    
    print("\n" + "="*100)
    print("HOSPITAL BACKEND - ENDPOINTS SUMMARY")
    print("="*100 + "\n")
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"{i}. {endpoint['path']}")
        print(f"   Methods: {', '.join(endpoint['methods'])}")
        print(f"   Description: {endpoint['description']}")
        
        if 'response_fields' in endpoint and endpoint['response_fields']:
            fields = endpoint['response_fields']
            if 'error' not in fields:
                print(f"   Response Fields: {len(fields)} fields")
                for field_name in list(fields.keys())[:5]:
                    print(f"     - {field_name} ({fields[field_name].get('type', 'Unknown')})")
                if len(fields) > 5:
                    print(f"     ... and {len(fields) - 5} more")
        print()
    
    print("="*100)
    print(f"Total Endpoints: {len(endpoints)}")
    print("="*100 + "\n")

if __name__ == '__main__':
    try:
        print("Generando documentación de endpoints...\n")
        
        # Generar tablas
        print_endpoints_table()
        
        # Guardar en JSON
        save_endpoints_json()
        
        # Guardar en Markdown
        save_endpoints_markdown()
        
        print("\n✅ Documentación generada exitosamente!")
        print("📄 Archivos creados:")
        print("  - ENDPOINTS.json")
        print("  - ENDPOINTS.md")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
