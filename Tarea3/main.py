import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Obtener el token desde la variable de entorno
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró la variable TELEGRAM_BOT_TOKEN")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def llamar_api(metodo, parametros=None):
    """
    Realiza una petición HTTP a la Telegram Bot API.
    """
    url = f"{BASE_URL}/{metodo}"

    if parametros:
        datos = urllib.parse.urlencode(parametros).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=datos,
            method="POST"
        )
    else:
        request = urllib.request.Request(
            url,
            method="GET"
        )
    with urllib.request.urlopen(request) as respuesta:
        contenido = respuesta.read().decode("utf-8")
        return json.loads(contenido)


def enviar_mensaje(chat_id, texto, parse_mode="Markdown"):
    """
    Envía un mensaje al usuario.
    """
    parametros = {
        "chat_id": chat_id,
        "text": texto
    }
    if parse_mode:
        parametros["parse_mode"] = parse_mode

    return llamar_api("sendMessage", parametros)


def obtener_actualizaciones(offset=None):
    """
    Obtiene nuevos mensajes enviados al bot.
    """
    parametros = {
        "timeout": 30
    }
    if offset is not None:
        parametros["offset"] = offset

    return llamar_api("getUpdates", parametros)


# ==============================================================================
# COMANDOS INTEGRANTE 1
# ==============================================================================

def comando_hola(chat_id, mensaje):
    """
    Comando /hola: Saluda al usuario utilizando su nombre de Telegram.
    """
    usuario = mensaje["message"].get("from", {})
    nombre = usuario.get("first_name", "usuario")
    enviar_mensaje(
        chat_id,
        f"¡Hola, *{nombre}*! 👋\n"
        "Bienvenido al bot del *Grupo #9*."
    )


# ==============================================================================
# COMANDOS INTEGRANTE 2
# ==============================================================================

def comando_hora(chat_id):
    """
    Comando /hora: Muestra la fecha y hora actual obtenida dinámicamente (UTC-6).
    """
    tz_guatemala = timezone(timedelta(hours=-6))
    ahora = datetime.now(tz_guatemala)
    fecha_str = ahora.strftime("%d/%m/%Y")
    hora_str = ahora.strftime("%H:%M:%S")

    mensaje = (
        " *Fecha y Hora Actual*\n\n"
        f" *Fecha:* `{fecha_str}`\n"
        f" *Hora:* `{hora_str}` (UTC-6)"
    )
    enviar_mensaje(chat_id, mensaje)


def comando_contacto(chat_id):
    """
    Comando /contacto: Muestra información de contacto definida por el grupo.
    """
    mensaje = (
        " *Información de Contacto - Grupo #9*\n\n"
        " *Curso:* Inteligencia Artificial 1\n"
        "*Universidad:* USAC - Facultad de Ingeniería\n"
        " *Correo de Contacto:* `grupo9.ia1.usac@gmail.com`\n"
        " *Bot de Telegram:* @G9_tarea3_bot"
    )
    enviar_mensaje(chat_id, mensaje)


def comando_integrantes(chat_id):
    """
    Comando /integrantes: Muestra los nombres y carnets del Grupo #9.
    """
    mensaje = (
        "👥 *Integrantes del Grupo #9*\n\n"
        "1. Fernando Misael Morales Ortiz - `202001950`\n"
        "2. Cristofher Antonio Saquilmer Rodas - `201700686`\n"
        "3. Daniel Estuardo Salvatierra Macajola - `202202768`\n"
        "4. Marco Fernando Cruz Mendoza - `202001076`\n"
        "5. Erick Noe Gómez López - `201700866`"
    )
    enviar_mensaje(chat_id, mensaje)


# ==============================================================================
# PROCESAMIENTO PRINCIPAL DE MENSAJES
# ==============================================================================

def procesar_mensaje(mensaje):
    """
    Procesa un mensaje recibido y lo direcciona al comando correspondiente.
    """
    if "message" not in mensaje:
        return

    chat_id = mensaje["message"]["chat"]["id"]
    texto = mensaje["message"].get("text", "").strip()

    if not texto:
        return

    # Extraer comando base ignorando mayúsculas/minúsculas y menciones (@bot)
    partes = texto.split()
    cmd = partes[0].lower().split("@")[0]

    if cmd == "/hola":
        comando_hola(chat_id, mensaje)
    elif cmd == "/hora":
        comando_hora(chat_id)
    elif cmd == "/contacto":
        comando_contacto(chat_id)
    elif cmd == "/integrantes":
        comando_integrantes(chat_id)


def iniciar_bot():
    """
    Bucle principal del bot (Long Polling).
    """
    print("Bot iniciado correctamente.")

    offset = None
    while True:
        try:
            respuesta = obtener_actualizaciones(offset)
            if not respuesta.get("ok"):
                print("Error al obtener actualizaciones.")
                continue
            actualizaciones = respuesta.get("result", [])
            for actualizacion in actualizaciones:
                offset = actualizacion["update_id"] + 1
                procesar_mensaje(actualizacion)
        except Exception as e:
            print(f"Error en el bucle principal: {e}")


if __name__ == "__main__":
    iniciar_bot()
