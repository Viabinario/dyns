# Purge_Templates_Views

Script de Dynamo que identifica y elimina las plantillas de vistas no utilizadas en un modelo Revit.

## Objetivo

Limpiar la base de datos del modelo removiendo plantillas de vistas que no están asignadas a ninguna vista, lo que ayuda a mantener el archivo más limpio y optimizado.

## Contenido de la carpeta

- `purge_templates_views.dyn` — gráfico Dynamo principal que contiene el nodo de ejecución.
- `Purge_Templates_Views.py` — script Python que implementa la lógica de análisis y eliminación.
- `purge_templates_views.png` — diagrama visual de referencia.

## Funcionamiento

El script realiza los siguientes pasos:

1. **Recopila** todas las plantillas de vistas existentes en el modelo.
2. **Identifica** cuáles están en uso (asignadas a vistas regulares).
3. **Marca** las plantillas no utilizadas.
4. **Opcionalmente elimina** las plantillas no usadas según el parámetro de entrada.

## Flujo de uso

### Paso 1: Abrir el gráfico Dynamo

Abrir `purge_templates_views.dyn` en Dynamo dentro de Revit 2024.

### Paso 2: Seleccionar modo

El gráfico contiene un nodo booleano que controla el comportamiento:

- **False** (por defecto) — modo análisis seguro: solo detecta plantillas no usadas sin eliminar nada.
- **True** — modo eliminación: elimina las plantillas detectadas como no utilizadas.

### Paso 3: Ejecutar

Ejecutar el gráfico haciendo clic en el botón de reproducción o presionando `Ctrl+Enter`.

### Paso 4: Revisar resultados

En el nodo `Watch` se mostrará:

- Cantidad de plantillas no usadas encontradas
- Cantidad de plantillas eliminadas (si se ejecutó con `True`)
- Lista de errores (si los hay)

## Recomendaciones

### Primera ejecución: modo análisis

1. Conectar el nodo booleano a `False` (modo seguro).
2. Ejecutar el script y revisar los resultados en el Watch.
3. Anotar qué plantillas se mostran como no usadas.

### Verificación manual

- Abrir la ventana de "Tipos de vista" en Revit (`Vista → Ventanas → Tipos de vista`).
- Confirmar que las plantillas identificadas como no usadas no están asignadas a ninguna vista.
- Si es necesario conservar alguna plantilla, marcar la vista que la usa en el paso anterior.

### Segunda ejecución: eliminación

1. Una vez confirmado que la detección es correcta, cambiar el nodo booleano a `True`.
2. Ejecutar nuevamente.
3. Revisar la lista de plantillas eliminadas.

## Requisitos

- Autodesk Revit 2024
- Dynamo 2.x / 3.x (incluido en Revit)
- El archivo debe estar abierto en Revit en el momento de la ejecución

## Manejo de errores

Si se produce un error durante la eliminación:

- El script no interrumpirá la cadena de ejecución.
- Se mostrará un listado de errores en el Watch con el nombre de la plantilla y el motivo del error.
- Las plantillas sin errores se eliminarán normalmente.

## Adaptación a otros casos

El script es agnóstico del proyecto — funciona en cualquier modelo Revit 2024. No requiere configuración adicional ni parámetros específicos.

## Notas de seguridad

- **Hacer copia de seguridad** del archivo antes de ejecutar con `True`.
- **Modo análisis recomendado** en modelos grandes o desconocidos.
- **Transacción única** — la eliminación se ejecuta en una sola transacción; si falla, toda la operación se revierte automáticamente.

## Compatibilidad

- Revit 2024
- Dynamo 2.x / 3.x (en Revit 2024)
- Python 3