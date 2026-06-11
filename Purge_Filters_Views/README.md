# Purge_Filters_Views

Script de Dynamo que identifica y elimina los filtros de vistas no utilizados en un modelo Revit.

## Objetivo

Limpiar la base de datos del modelo removiendo filtros de vistas que no están asignados a ninguna vista, lo que ayuda a mantener el archivo más limpio y optimizado.

## Contenido de la carpeta

- `purge_filters_views.dyn` — gráfico Dynamo principal que contiene el nodo de ejecución.
- `purge_filters_views.py` — script Python que implementa la lógica de análisis y eliminación.
- `purge_filters_views.png` — diagrama visual de referencia.

## Funcionamiento

El script realiza los siguientes pasos:

1. **Recopila** todos los filtros de vistas existentes en el modelo.
2. **Identifica** cuáles están asignados a alguna vista.
3. **Marca** los filtros no utilizados.
4. **Opcionalmente elimina** los filtros no usados según el parámetro de entrada.

## Flujo de uso

### Paso 1: Abrir el gráfico Dynamo

Abrir `purge_filters_views.dyn` en Dynamo dentro de Revit 2024.

### Paso 2: Seleccionar modo

El gráfico contiene un nodo booleano que controla el comportamiento:

- **False** (por defecto) — modo análisis seguro: solo detecta filtros no usados sin eliminar nada.
- **True** — modo eliminación: elimina los filtros detectados como no utilizados.

### Paso 3: Ejecutar

Ejecutar el gráfico haciendo clic en el botón de reproducción o presionando `Ctrl+Enter`.

### Paso 4: Revisar resultados

En el nodo `Watch` se mostrará:

- Cantidad total de filtros en el proyecto
- Cantidad de filtros no asignados (no en uso)
- Cantidad de filtros eliminados (si se ejecutó con `True`)
- Lista de nombres de filtros no usados
- Lista de errores (si los hay)

## Recomendaciones

### Primera ejecución: modo análisis

1. Conectar el nodo booleano a `False` (modo seguro).
2. Ejecutar el script y revisar los resultados en el Watch.
3. Anotar qué filtros se muestran como no utilizados.

### Verificación manual

- Abrir el gestor de filtros en Revit (`Vista → Filtros de vista`).
- Confirmar que los filtros identificados como no usados no están asignados a ninguna vista.
- Si es necesario conservar algún filtro, revisar si alguna vista lo está usando.

### Segunda ejecución: eliminación

1. Una vez confirmado que la detección es correcta, cambiar el nodo booleano a `True`.
2. Ejecutar nuevamente.
3. Revisar la lista de filtros eliminados.

## Requisitos

- Autodesk Revit 2024
- Dynamo 2.x / 3.x (incluido en Revit)
- El archivo debe estar abierto en Revit en el momento de la ejecución

## Manejo de errores

Si se produce un error durante la eliminación:

- El script no interrumpirá la cadena de ejecución.
- Se mostrará un listado de errores en el Watch con el nombre del filtro y el motivo del error.
- Los filtros sin errores se eliminarán normalmente.

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