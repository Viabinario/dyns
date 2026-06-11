"""
URB01_nodo2_write_parameters.py
================================
Nodo 2 del grafico Dynamo URB01_ProjectData.dyn

Funcion: Leer los valores del CSV (via List.Create en Dynamo) y
escribirlos en la Informacion del Proyecto de cada archivo Revit abierto.

Uso en Dynamo:
  - Copiar este codigo en un nodo Python Script
  - Requiere 2 entradas:
      IN[0]: lista de documentos Revit (salida del Nodo 1)
      IN[1]: lista de columnas del CSV (salida de List.Create)
  - Salida: lista de resultados OK / ERROR por archivo

Estructura esperada de IN[1]:
  Lista de 11 sublistas, una por columna del CSV (indices 1 a 11).
  Cada sublista contiene 8 valores, uno por archivo Revit.
  Columna 0 (Archivo) se omite — no corresponde a ningun parametro.

Parametros que escribe (en orden segun columnas del CSV):
  1  Project Name
  2  Project Number
  3  Building Name
  4  Client Name
  5  Project Address
  6  Organization Name
  7  INF_proyecto_nombre
  8  INF_promotor_nombre
  9  INF_promotor_direccion
  10 INF_proyecto_descripcion
  11 SiteName

Proyecto: URB01 Urbanizacion Residencial
Norma: UNE-EN ISO 19650-1 y 19650-2

# Francisco Sánchez A. Architect - jun 2026
"""

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

docs       = IN[0]   # Lista de documentos Revit ordenados (salida Nodo 1)
all_values = IN[1]   # Lista de columnas del CSV (salida de List.Create)

# Nombres de parametros en Revit
# Deben coincidir exactamente con los nombres en Informacion del Proyecto
param_names = [
    "Project Name",             # columna indice 1 del CSV
    "Project Number",           # columna indice 2
    "Building Name",            # columna indice 3
    "Client Name",              # columna indice 4
    "Project Address",          # columna indice 5
    "Organization Name",        # columna indice 6
    "INF_proyecto_nombre",      # columna indice 7
    "INF_promotor_nombre",      # columna indice 8
    "INF_promotor_direccion",   # columna indice 9
    "INF_proyecto_descripcion", # columna indice 10
    "SiteName",                 # columna indice 11
]

active_doc = DocumentManager.Instance.CurrentDBDocument
results = []

for i, doc in enumerate(docs):
    try:
        if doc.Title == active_doc.Title:
            # Documento activo: usar TransactionManager de Dynamo
            TransactionManager.Instance.EnsureInTransaction(doc)
            pi = doc.ProjectInformation
            for j, pname in enumerate(param_names):
                p = pi.LookupParameter(pname)
                if p and not p.IsReadOnly:
                    p.Set(str(all_values[j + 1][i]))
            TransactionManager.Instance.TransactionTaskDone()
        else:
            # Documentos no activos: transaccion manual de la API de Revit
            # Dynamo solo gestiona transacciones automaticas en el doc. activo
            t = Transaction(doc, "ISO19650: Project Info")
            t.Start()
            pi = doc.ProjectInformation
            for j, pname in enumerate(param_names):
                p = pi.LookupParameter(pname)
                if p and not p.IsReadOnly:
                    p.Set(str(all_values[j + 1][i]))
            t.Commit()

        results.append("OK: " + doc.Title)

    except Exception as e:
        results.append("ERROR: " + doc.Title + " — " + str(e))

OUT = results
