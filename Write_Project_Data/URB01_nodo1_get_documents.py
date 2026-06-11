"""
URB01_nodo1_get_documents.py
============================
Nodo 1 del grafico Dynamo URB01_ProjectData.dyn

Funcion: Obtener y ordenar los documentos Revit abiertos que pertenecen
al proyecto URB01, en el mismo orden que las filas del CSV.

Uso en Dynamo:
  - Copiar este codigo en un nodo Python Script
  - No requiere entradas (IN[0] no se usa)
  - Salida: lista ordenada de documentos Revit

Proyecto: URB01 Urbanizacion Residencial
Norma: UNE-EN ISO 19650-1 y 19650-2

Francisco Sánchez A. Architect - jun 2026
"""

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

import RevitServices
from RevitServices.Persistence import DocumentManager

app = DocumentManager.Instance.CurrentUIApplication.Application

# Orden esperado segun filas del CSV (sin contar encabezado)
# Debe coincidir exactamente con el orden de filas del archivo
# URB01_ProjectData.csv
orden = [
    "URB01-ARQ-00-00-M3-UR-AP-0001",
    "URB01-ARQ-E01-00-M3-AR-AP-0001",
    "URB01-ARQ-E02-00-M3-AR-AP-0001",
    "URB01-ARQ-E03-00-M3-AR-AP-0001",
    "URB01-ARQ-E04-00-M3-AR-AP-0001",
    "URB01-ARQ-E05-00-M3-AR-AP-0001",
    "URB01-ARQ-E06-00-M3-AR-AP-0001",
    "URB01-ARQ-E07-00-M3-AR-AP-0001",
]

# Recoger todos los documentos del proyecto
# Se filtran documentos de familia y documentos vinculados
docs_raw = []
for doc in app.Documents:
    if not doc.IsFamilyDocument and not doc.IsLinked:
        if "URB01" in doc.Title:
            docs_raw.append(doc)

# Ordenar segun el CSV
docs_ordenados = []
for nombre in orden:
    for doc in docs_raw:
        if nombre in doc.Title:
            docs_ordenados.append(doc)
            break

OUT = docs_ordenados
