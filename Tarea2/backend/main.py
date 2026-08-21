
# ==============================================================================
# SERVIDOR BACKEND PYTHON - FASTAPI + PYSWIP (main.py)
# Tarea 2 - Inteligencia Artificial 1
# ==============================================================================

from pathlib import Path
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pyswip import Prolog

# ------------------------------------------------------------------------------
# 1. INICIALIZACIÓN DE LA APLICACIÓN FASTAPI
# ------------------------------------------------------------------------------

# Instancia principal del framework FastAPI para la API REST.
app = FastAPI(
    title="API Inventario RPG",
    description="API REST que conecta Python con Prolog (PySwip) para procesar el inventario de un aventurero.",
    version="1.0.0",
)

# Configuración del Middleware CORS para permitir peticiones cross-origin desde navegadores web.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Permite peticiones desde cualquier origen (Frontend HTML/JS)
    allow_credentials=False,   # Deshabilita el envío de credenciales para peticiones genéricas
    allow_methods=["GET"],     # Define explícitamente el método GET permitido según el requerimiento
    allow_headers=["*"],       # Permite todos los encabezados HTTP estándar
)

# ------------------------------------------------------------------------------
# 2. CONFIGURACIÓN E INTEGRACIÓN CON PYSWIP (PROLOG)
# ------------------------------------------------------------------------------

# Obtiene la ruta absoluta del directorio raíz donde se encuentra main.py.
BASE_DIR = Path(__file__).resolve().parent

# Define la ruta absoluta hacia el archivo de hechos y reglas de Prolog (inventario.pl).
PROLOG_FILE = BASE_DIR / "inventario.pl"

# Crea la instancia del intérprete de Prolog mediante la biblioteca PySwip.
prolog = Prolog()

# Carga y compila dinámicamente el archivo inventario.pl dentro del motor de Prolog.
prolog.consult(PROLOG_FILE.as_posix())


# ------------------------------------------------------------------------------
# 3. FUNCIÓN AUXILIAR DE TRANSFORMACIÓN DE DATOS
# ------------------------------------------------------------------------------

def convertir_prolog(valor):
    """
    Función recursiva para convertir los tipos de datos retornados por PySwip 
    (como Atom o listas internas de Prolog) en tipos nativos de Python (str, int, float, list)
    compatibles con la serialización JSON.
    """
    if isinstance(valor, list):
        return [convertir_prolog(elemento) for elemento in valor]
    if isinstance(valor, (int, float)):
        return valor
    return str(valor)


# ------------------------------------------------------------------------------
# 4. ENDPOINT PRINCIPAL REST GET /inventario
# ------------------------------------------------------------------------------

@app.get("/inventario")
def consultar_inventario(item: str):
    """
    Endpoint GET que recibe un parámetro 'item' vía Query Parameter,
    valida la entrada, inyecta la consulta al motor Prolog mediante PySwip,
    captura la unificación de variables y retorna una respuesta estructurada en JSON.
    """
    # Normaliza la cadena ingresada quitando espacios y convirtiendo a minúsculas
    item = item.strip().lower()

    # Validación de seguridad del parámetro para prevenir inyección sintáctica en el motor Prolog
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", item):
        raise HTTPException(
            status_code=400,
            detail="El nombre del ítem contiene caracteres no permitidos. Use solo letras, números y guion bajo.",
        )

    # Inyección del parámetro ingresado en la consulta del predicado procesar_inventario/5
    consulta = f"""
        procesar_inventario(
            {item},
            TotalItems,
            InventarioInvertido,
            InventarioUnico,
            InventarioOrdenado
        )
    """

    # Ejecuta la consulta en Prolog y convierte el generador de resultados en una lista de diccionarios Python
    resultados = list(prolog.query(consulta))

    # Si Prolog retorna lista vacía, significa que member/2 falló (el ítem no existe en el inventario)
    if not resultados:
        raise HTTPException(
            status_code=404,
            detail=f"El ítem '{item}' no existe en el inventario del aventurero.",
        )

    # Extrae el primer resultado unificado devuelto por Prolog
    resultado = resultados[0]

    # Construye y retorna la respuesta JSON formateando las variables unificadas por Prolog
    return {
        "item_buscado": item,
        "total_items": convertir_prolog(resultado["TotalItems"]),
        "inventario_invertido": convertir_prolog(resultado["InventarioInvertido"]),
        "inventario_unico": convertir_prolog(resultado["InventarioUnico"]),
        "inventario_ordenado": convertir_prolog(resultado["InventarioOrdenado"]),
    }


# ------------------------------------------------------------------------------
# 5. ENDPOINT BASE DE VERIFICACIÓN /
# ------------------------------------------------------------------------------

@app.get("/")
def inicio():
    """Endpoint de comprobación de estado de la API."""
    return {
        "mensaje": "API de Inventario RPG con PySwip y Prolog funcionando correctamente."
    }