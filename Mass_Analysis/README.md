# Rooms 3D Visual — Script de Dynamo para Revit 2024

Genera volúmenes 3D (masas) a partir de los Rooms de un modelo Revit, incluyendo elementos de archivos vinculados con transformación propia. Las masas se asignan a un workset dedicado y se colorean en vista 3D según reglas configurables sobre los parámetros de los rooms.

---

## Requisitos previos

- Autodesk Revit 2024
- Dynamo 2.x / 3.x (incluido en Revit 2024)
- Modelo con **Worksharing activado**
- Workset `Rooms_3D_Visual` creado **manualmente** antes de ejecutar (`Gestionar → Worksets → Nuevo`)
- Los archivos vinculados deben estar **cargados** en el momento de la ejecución
- Tener una **vista 3D abierta y activa** antes de ejecutar el Nodo 3

---

## Estructura del script — 4 nodos

```
Nodo 1 (Limpiar)
    ↓
Nodo diagnóstico (opcional — solo primera vez)
    ↓
Nodo 2 (Crear masas)
    ↓
Nodo 3 (Colorear masas)
    ↓
Watch
```

Cada nodo es un `Python Script` independiente. La conexión entre nodos es únicamente para **forzar el orden de ejecución** — el OUT de cada nodo se conecta al IN[0] del siguiente.

> **Importante:** el Nodo 3 requiere que la vista activa en Revit sea una vista 3D. Si se ejecuta con una tabla o planta activa, mostrará un aviso en el Watch y no interrumpirá la cadena.

---

## Nodo 1 — Limpiar masas previas

Elimina todas las masas existentes en el workset `Rooms_3D_Visual` antes de regenerarlas. Evita la acumulación de versiones anteriores en las planificaciones.

### Configuración

```python
WORKSET_NAME = "Rooms_3D_Visual"  # nombre del workset a limpiar
```

### Comportamiento
- Si el workset no existe, sale limpiamente sin error
- Elimina **todas** las masas asignadas a ese workset, incluyendo las que fallaron en ejecuciones anteriores (DirectShapes vacíos sin nombre)
- El Watch muestra el total de masas encontradas y eliminadas

---

## Nodo diagnóstico — Verificar parámetros disponibles (opcional)

Útil únicamente la **primera vez** que se implementa el script en un nuevo proyecto. Lista todos los parámetros del primer room encontrado con sus valores reales.

### Cuándo usarlo
- Al adaptar el script a un nuevo caso de estudio
- Cuando los campos de `Comments` aparecen vacíos tras ejecutar el Nodo 2
- Para confirmar los nombres exactos de parámetros de proyecto antes de añadirlos al `PARAM_MAP`

### Uso
1. Conectar su `IN[0]` al `OUT` del Nodo 1
2. Conectar su `OUT` a un nodo `Watch`
3. Ejecutar y anotar los nombres y valores que interesan
4. Desconectarlo una vez confirmados los parámetros — no es necesario en ejecuciones posteriores

---

## Nodo 2 — Crear masas

Lee los rooms del modelo anfitrión y de todos los archivos vinculados cargados, aplica la transformación de posición de cada vínculo, valida la geometría y crea un `DirectShape` en la categoría `Mass` por cada room válido.

### Configuración principal

#### `WORKSET_NAME`
```python
WORKSET_NAME = "Rooms_3D_Visual"
```
Nombre del workset al que se asignarán las masas. El workset debe existir previamente en el modelo — créalo manualmente antes de ejecutar el script. Si no se encuentra, el script lanzará un error.

#### `PARAM_MAP`
Define qué parámetros del room se copian al campo `Comments` de cada masa. Es la única sección que hay que adaptar a cada proyecto.

```python
PARAM_MAP = [
    # Formato: ("label_en_comments", "nombre_del_parametro_en_revit")
    # Parámetros nativos — usar nombre en inglés tal como aparece en la API
    ("Room_Name",       "Name"),
    ("Room_Number",     "Number"),
    ("Room_Level",      "Level"),
    ("Room_Department", "Department"),
    ("Room_Area_m2",    "Area"),        # se convierte automáticamente de ft² a m²
    # Parámetros de proyecto — usar el nombre exacto que muestra el nodo diagnóstico
    ("VivNumero",       "DAT_TXT_VivNumero"),
    ("VivPlanta",       "DAT_TXT_VivPlanta"),
    ("VivTipo",         "DAT_TXT_VivTipo"),
    ("Bloque",          "DAT_TXT_VivBloque"),
    ("Categoria",       "AHM_CNT_00_Categoria"),
    ("AcabadoSuelo",    "AHM_MAT_AcabadodelSuelo"),
    ("AcabadoMuro",     "AHM_MAT_AcabadodelMuro"),
]
```

**Cómo adaptar a un nuevo proyecto:**
1. Ejecutar el nodo diagnóstico y anotar los nombres de parámetros disponibles
2. Añadir o eliminar entradas del `PARAM_MAP` según los parámetros del proyecto
3. El `label` (primer elemento) es libre — es el nombre que aparecerá en `Comments` y que usará el Nodo 3 para aplicar colores

### Rooms omitidos
Los rooms con geometría inválida (rooms abiertos, sin cerramiento completo, terrazas con límites al exterior) se omiten y se listan en el Watch. Son un problema de modelado del archivo de origen, no del script.

### Resultado en Comments
Cada masa generada tendrá un campo `Comments` con el formato:
```
Room_Name: DORMITORIO 1 | Room_Number: 082 | Room_Level: 04_BL01 | Room_Area_m2: 12.45 | VivPlanta: P02 | ...
```

---

## Nodo 3 — Colorear masas

Lee el campo `Comments` de cada masa del workset y aplica overrides de color en la vista 3D activa según las reglas definidas.

### Configuración principal

#### `COLOR_RULES`
Lista de reglas evaluadas en orden. Se aplica la **primera regla que coincida**.

```python
COLOR_RULES = [
    # Formato: ("label", "modo", "valor", (R, G, B))
    ("Room_Level", "contains",   "BL01", (255, 100, 100)),
    ("Room_Level", "contains",   "BL2",  (255, 180,  80)),
    ("Room_Level", "contains",   "BL03", ( 80, 180, 255)),
    ("Room_Level", "contains",   "BL04", (120, 220, 120)),
    ("Room_Level", "contains",   "GARAJE",(160,160, 160)),
    ("VivTipo",    "equals",     "TR",   (200, 200, 100)),
]
```

#### Modos de comparación disponibles

| Modo | Comportamiento | Ejemplo |
|---|---|---|
| `equals` | Coincidencia exacta (ignora mayúsculas) | `"TR"` == `"tr"` ✓ |
| `contains` | El valor está contenido en el parámetro | `"BL04"` en `"04_BL04"` ✓ |
| `startswith` | Empieza por el valor | `"04"` en `"04_BL04"` ✓ |
| `endswith` | Termina en el valor | `"BL04"` en `"04_BL04"` ✓ |

#### `DEFAULT_COLOR`
Color aplicado a masas que no cumplen ninguna regla. Usar `None` para no aplicar nada.
```python
DEFAULT_COLOR = (220, 220, 220)  # gris claro
```

#### `TRANSPARENCY`
Transparencia de las masas en la vista 3D. Rango 0 (opaco) a 100 (invisible).
```python
TRANSPARENCY = 30
```

### Requisito de vista
El Nodo 3 debe ejecutarse con una **vista 3D activa** en Revit. Si la vista activa es una tabla o planta, el nodo muestra un aviso en el Watch y no aplica ningún color — sin interrumpir la cadena ni afectar las masas ya creadas.

### Resultado en el Watch
```
✓ 980 masas coloreadas por regla
○ 216 masas con color por defecto
Sin regla: ['TRASTERO 045', 'GARAJE...']
```

---

## Adaptación a un nuevo caso de estudio

### Paso 1 — Workset
Verificar que el modelo tiene Worksharing activo. Crear el workset `Rooms_3D_Visual` **manualmente** en Revit (`Gestionar → Worksets → Nuevo`) antes de ejecutar el script. Si se prefiere otro nombre, cambiar `WORKSET_NAME` en los **4 nodos** de forma consistente y crear el workset con ese mismo nombre.

### Paso 2 — Identificar parámetros
Ejecutar el **nodo diagnóstico** con el nuevo modelo y anotar:
- Los nombres exactos de los parámetros de proyecto disponibles
- Los valores reales de `Level` (pueden incluir prefijos numéricos como `"04_BL01"`)

### Paso 3 — Actualizar PARAM_MAP
En el Nodo 2, actualizar `PARAM_MAP` con los parámetros relevantes del nuevo proyecto. Los parámetros nativos (`Name`, `Number`, `Level`, `Department`, `Area`) funcionan en cualquier proyecto sin cambios.

### Paso 4 — Definir reglas de color
En el Nodo 3, usar los valores reales obtenidos del nodo de inspección para definir `COLOR_RULES`. Ejecutar el nodo de inspección si es necesario:

```python
# Nodo de inspección — conectar entre Nodo 2 y Nodo 3
# Muestra los valores únicos de los parámetros clave
OUT = [
    "Room_Level únicos: {}".format(sorted(levels)),
    "VivPlanta únicos: {}".format(sorted(plantas)),
    "VivTipo únicos: {}".format(sorted(tipos)),
]
```

### Paso 5 — Visibilidad en vistas
En cada vista 3D donde se quieran ver las masas:
1. `VG` → pestaña **Worksets** → activar `Rooms_3D_Visual`
2. `VG` → pestaña **Model Categories** → `Mass` → activar checkbox

---

## Notas sobre planificaciones de masas

- Las masas generadas aparecen en planificaciones de tipo `Mass`
- El campo `Comments` contiene todos los parámetros del room en formato `label: valor | label: valor`
- Para tener cada parámetro en su propia columna de planificación es necesario crear **Parámetros Compartidos** asignados a la categoría `Mass` y modificar el Nodo 2 para escribir en ellos individualmente
- Ejecutar siempre el script completo (Nodos 1 + 2 + 3) para evitar acumulación en las planificaciones — el Nodo 1 garantiza que solo existe una versión de las masas en cada ejecución

---

## Problemas conocidos

| Problema | Causa | Solución |
|---|---|---|
| Rooms omitidos con error `pGeomArr` | Geometría degenerada — rooms abiertos o sin cerramiento | Revisar el modelado del room en el archivo de origen |
| `Room_Level` con prefijo numérico | Nomenclatura de niveles del proyecto | Usar modo `contains` en `COLOR_RULES` |
| Nodo 3 no aplica colores | Vista activa no es 3D | Abrir una vista 3D antes de ejecutar |
| Masas acumuladas en planificación | Nodo 1 no ejecutado o fallido | Verificar que el Watch del Nodo 1 confirma eliminaciones |
| Masas de vínculos descolocadas | Transformación no aplicada | El script aplica `GetTotalTransform()` automáticamente |
| Parámetros vacíos en Comments | Nombre de parámetro incorrecto en `PARAM_MAP` | Verificar nombre exacto con el nodo diagnóstico |
