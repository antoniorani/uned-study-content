# UNED Study Content

Repositorio de contenidos académicos para **UNED Study**, separado deliberadamente de la aplicación y del progreso de los usuarios.

## Estructura

```text
uned-study-content/
├── AGENTS.md
├── schema/
│   └── subject.schema.json
├── examples/
│   ├── test-subject.json
│   └── flashcards-subject.json
├── subjects/
│   └── <subject_id>/
│       ├── subject.json
│       └── assets/
└── tools/
    └── validate_content.py
```

Cada asignatura real se almacena en `subjects/<subject_id>/subject.json`. El progreso de los estudiantes **nunca** se guarda aquí.

## Antes de crear o editar contenido

Los autores humanos y, especialmente, los LLM deben leer **`AGENTS.md`**. Allí se definen:

- estabilidad permanente de IDs;
- escala de importancia 1–5;
- criterios de calidad para test y tarjetas;
- reglas de Markdown y assets;
- trazabilidad de fuentes;
- prohibición de inventar convocatorias, artículos, páginas o referencias;
- reglas para actualizar una asignatura sin romper el progreso previo.

El contrato formal es `schema/subject.schema.json`.

## Validación

```bash
python -m pip install jsonschema
python tools/validate_content.py
```

GitHub Actions ejecuta esta validación en cada pull request y en los cambios que llegan a `main`.

## Añadir una asignatura

Crear:

```text
subjects/<subject_id>/subject.json
```

con `schema_version: 1` y un `id` idéntico al nombre de la carpeta. Si necesita diagramas o imágenes, utilizar `subjects/<subject_id>/assets/`.

Los ejemplos de `examples/` son ficticios y sirven únicamente para mostrar la estructura.
