# =====================================================================
# DYNAMO SCRIPT: Limpiar Plantillas de Vistas No Utilizadas - Revit 2024
# =====================================================================
# INSTRUCCIONES:
#   1. En Dynamo, agrega un nodo "Python Script" (o "Python Script 3")
#   2. Pega este código completo en el editor del nodo
#   3. Conecta una entrada booleana al parámetro IN[0]:
#      - False = solo analizar (modo seguro, sin eliminar)
#      - True  = eliminar plantillas no utilizadas
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
    ElementId,
    BuiltInParameter,
    Transaction
)
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

try:
    doc = DocumentManager.Instance.CurrentDBDocument
    ejecutar_eliminacion = IN[0] if IN[0] is not None else False

    todas_plantillas = {}
    collector_vistas = FilteredElementCollector(doc).OfClass(View)

    for vista in collector_vistas:
        if vista.IsTemplate:
            todas_plantillas[vista.Id.IntegerValue] = {
                "id": vista.Id,
                "nombre": vista.Name,
                "en_uso": False
            }

    plantillas_usadas_ids = set()
    for vista in collector_vistas:
        if not vista.IsTemplate:
            param_plantilla = vista.get_Parameter(BuiltInParameter.VIEW_TEMPLATE)
            if param_plantilla is not None:
                id_plantilla = param_plantilla.AsElementId()
                if id_plantilla is not None and id_plantilla != ElementId.InvalidElementId:
                    if id_plantilla.IntegerValue != -1:
                        plantillas_usadas_ids.add(id_plantilla.IntegerValue)

    for id_int in plantillas_usadas_ids:
        if id_int in todas_plantillas:
            todas_plantillas[id_int]["en_uso"] = True

    plantillas_no_usadas = [p for p in todas_plantillas.values() if not p["en_uso"]]
    eliminadas = []
    errores = []

    if ejecutar_eliminacion:
        with Transaction(doc, "Eliminar plantillas no usadas") as t:
            t.Start()
            for plantilla in plantillas_no_usadas:
                try:
                    doc.Delete(plantilla["id"])
                    eliminadas.append(plantilla["nombre"])
                except Exception as e:
                    errores.append("{}: {}".format(plantilla["nombre"], str(e)))
            t.Commit()

    OUT = [
        "no usadas: {}".format(len(plantillas_no_usadas)),
        "eliminadas: {}".format(len(eliminadas)),
        errores if errores else ["sin errores"]
    ]

except Exception as e:
    OUT = ["ERROR GENERAL: {}".format(str(e))]