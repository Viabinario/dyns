# Write_Project_Data

Este proyecto usa un gráfico Dynamo como punto de entrada para leer datos de un CSV y escribirlos en los parámetros de "Información del proyecto" de varios documentos Revit abiertos.

## Objetivo

Automatizar el proceso completo de:
- obtener los documentos Revit abiertos,
- importar los datos del CSV,
- repetir los valores de cada columna por documento,
- escribir los parámetros de `ProjectInformation` en cada archivo.

## Contenido de la carpeta

- `URB01_ProjectData.dyn` — gráfico Dynamo principal que coordina el proceso.
- `URB01_nodo1_get_documents.py` — script Python para el nodo 1, encargado de devolver la lista de documentos Revit abiertos.
- `URB01_nodo2_write_parameters.py` — script Python para el nodo 2, encargado de escribir los parámetros en cada documento.
- `URB01_ProjectData.csv` — ejemplo de datos de proyecto en formato CSV.
- `Write_Project_Data.png` — diagrama visual del flujo completo del gráfico Dynamo.

## Diagrama del flujo

El archivo `Write_Project_Data.png` muestra el proceso completo en Dynamo:

1. `File Path` / `Data.ImportCSV` para cargar el CSV.
2. `List.RestOfItems` y `List.Transpose` para reorganizar las columnas en listas por parámetro.
3. `URB01_nodo1_get_documents.py` para obtener los documentos abiertos.
4. `URB01_nodo2_write_parameters.py` para escribir los valores en los parámetros de proyecto.

## Flujo de uso

1. Abrir los archivos Revit que se desean actualizar.
2. Abrir el gráfico Dynamo `URB01_ProjectData.dyn`.
3. Ejecutar el nodo 1 (`URB01_nodo1_get_documents.py`) para obtener la lista de documentos Revit abiertos y entregarla como `IN[0]` al nodo 2.
4. Importar el CSV con `Data.ImportCSV`, usar `List.RestOfItems` y `List.Transpose` para generar las sublistas de columnas, y conectar esas sublistas como `IN[1]` al nodo 2.
5. Ejecutar el nodo 2 (`URB01_nodo2_write_parameters.py`) para escribir los parámetros en cada documento.

## Estructura esperada del CSV

El CSV debe tener 12 columnas, incluida la primera columna de identificación de archivo que no se usa directamente para escribir parámetros:

- columna 0: `Archivo` (solo referencia, no se copia)
- columna 1: `Project Name`
- columna 2: `Project Number`
- columna 3: `Building Name`
- columna 4: `Client Name`
- columna 5: `Project Address`
- columna 6: `Organization Name`
- columna 7: `INF_proyecto_nombre`
- columna 8: `INF_promotor_nombre`
- columna 9: `INF_promotor_direccion`
- columna 10: `INF_proyecto_descripcion`
- columna 11: `SiteName`

Cada columna del CSV se transforma en una lista y se entrega al script como una sublista dentro de `IN[1]`.

## Parámetros que escribe el script

El script asigna los valores del CSV en el siguiente orden a los parámetros de `ProjectInformation` de cada documento:

1. `Project Name`
2. `Project Number`
3. `Building Name`
4. `Client Name`
5. `Project Address`
6. `Organization Name`
7. `INF_proyecto_nombre`
8. `INF_promotor_nombre`
9. `INF_promotor_direccion`
10. `INF_proyecto_descripcion`
11. `SiteName`

## Requisitos y notas importantes

- Ejecutar el script desde Dynamo con Revit abierto.
- El script puede escribir en varios documentos abiertos, incluidos documentos no activos.
- Si el documento es el documento activo de Dynamo, la transacción se maneja con `TransactionManager`.
- Para documentos no activos, el script crea una transacción manual de Revit.
- Los parámetros deben existir en la pestaña `Información del proyecto` y no deben ser de solo lectura.

## Cómo adaptar el script a otro proyecto

1. Confirmar los nombres exactos de los parámetros de `ProjectInformation` en el proyecto destino.
2. Si los nombres de los parámetros cambian, actualizar la lista `param_names` en el script.
3. Ajustar el CSV para que conserve el mismo orden de columnas y nombres de encabezado descritos arriba.
4. Si se añaden columnas nuevas, agregar el nombre del parámetro en la lista `param_names` y el valor correspondiente en el CSV.

## Ejemplo de uso

- `IN[0]`: lista de documentos Revit ordenados según el orden de filas del CSV.
- `IN[1]`: lista de columnas del CSV con su contenido como sublistas.

El script genera como salida una lista de resultados por documento:

- `OK: <nombre del documento>` si la escritura fue correcta
- `ERROR: <nombre del documento> — <mensaje>` si hubo un problema

## Mejor práctica

- Realizar una copia de seguridad de los documentos antes de ejecutar el script.
- Probar primero con un subconjunto de archivos y verificarlos manualmente.
- Si un parámetro no se escribe, comprobar que el nombre del parámetro exista exactamente y que no sea de solo lectura.

## Licencia

Este material está creado como ejemplo de flujo de trabajo para el proyecto URB01 y puede adaptarse a otros casos de estudio según los nombres de parámetros de cada proyecto.