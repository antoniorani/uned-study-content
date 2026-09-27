# Subjects

Cada asignatura real ocupa una carpeta propia:

```text
subjects/
└── <subject_id>/
    ├── subject.json
    └── assets/
        └── ...
```

## Reglas

- El nombre de la carpeta y `subject.json.id` deben coincidir exactamente.
- El identificador debe ser estable y no depender del curso académico.
- `subject.json` contiene todo el contenido estructurado de la asignatura en la versión 1.
- `assets/` es opcional y contiene imágenes/esquemas referenciados mediante rutas relativas.
- El progreso de estudiantes no pertenece a este repositorio.
- Antes de crear o modificar contenido, cualquier autor automatizado debe leer `/AGENTS.md`.
- El contrato formal está en `/schema/subject.schema.json`.

Ejemplo:

```text
subjects/
└── derecho_constitucional_i/
    ├── subject.json
    └── assets/
        └── esquema_fuentes.svg
```

Añadir una carpeta válida debe ser suficiente para que la aplicación pueda descubrir una nueva asignatura una vez implementada la sincronización del catálogo.
