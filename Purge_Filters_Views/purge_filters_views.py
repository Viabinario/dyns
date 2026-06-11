# =====================================================================
# DYNAMO SCRIPT: Limpiar Filtros de Vistas No Utilizados - Revit 2024
# =====================================================================
# INSTRUCCIONES:
#   1. En Dynamo, agrega un nodo "Python Script" (o "Python Script 3")
#   2. Pega este código completo en el editor del nodo
#   3. Conecta una entrada booleana al parámetro IN[0]:
#      - False = solo analizar (modo seguro, sin eliminar)
#      - True  = eliminar filtros de vista no utilizados
#   4. Ejecuta el script
#
# COMPATIBILIDAD: Revit 2024 / Dynamo 2.x / Python 3
# Francisco Sánchez A. Architect - jun 2026
# =====================================================================

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitServices')
clr.AddReference('RevitNodes')

from Autodesk.Revit.DB import (
    FilteredElementCollector,
    View,
    ParameterFilterElement,
    Transaction
)
from RevitServices.Persistence import DocumentManager

try:
    doc = DocumentManager.Instance.CurrentDBDocument
    ejecutar_eliminacion = IN[0] if IN[0] is not None else False

    # PASO 1: Recopilar todos los filtros del proyecto
    todos_filtros = {}
    collector_filtros = FilteredElementCollector(doc).OfClass(ParameterFilterElement)

    for filtro in collector_filtros:
        todos_filtros[filtro.Id.IntegerValue] = {
            "id": filtro.Id,
            "nombre": filtro.Name,
            "en_uso": False
        }

    # PASO 2: Detectar cuáles están asignados a alguna vista
    filtros_usados_ids = set()
    collector_vistas = FilteredElementCollector(doc).OfClass(View)

    for vista in collector_vistas:
        if not vista.IsTemplate:
            try:
                ids_filtros_vista = vista.GetFilters()
                for id_filtro in ids_filtros_vista:
                    filtros_usados_ids.add(id_filtro.IntegerValue)
            except:
                pass

    # PASO 3: Marcar filtros en uso
    for id_int in filtros_usados_ids:
        if id_int in todos_filtros:
            todos_filtros[id_int]["en_uso"] = True

    filtros_no_usados = [f for f in todos_filtros.values() if not f["en_uso"]]
    eliminados = []
    errores = []

    # PASO 4: Eliminar si ejecutar_eliminacion = True
    if ejecutar_eliminacion:
        with Transaction(doc, "Eliminar filtros no utilizados") as t:
            t.Start()
            for filtro in filtros_no_usados:
                try:
                    doc.Delete(filtro["id"])
                    eliminados.append(filtro["nombre"])
                except Exception as e:
                    errores.append("{}: {}".format(filtro["nombre"], str(e)))
            t.Commit()

    OUT = [
        "filtros en el proyecto: {}".format(len(todos_filtros)),
        "filtros sin asignar: {}".format(len(filtros_no_usados)),
        "eliminados: {}".format(len(eliminados)),
        [f["nombre"] for f in filtros_no_usados],
        errores if errores else ["sin errores"]
    ]

except Exception as e:
    OUT = ["ERROR GENERAL: {}".format(str(e))]