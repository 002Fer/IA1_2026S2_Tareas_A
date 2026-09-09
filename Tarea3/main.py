import os
import json
import urllib.request
import urllib.parse
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


def enviar_mensaje(chat_id, texto):
    """
    Envía un mensaje al usuario.
    """
    return llamar_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": texto
        }
    )


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


def procesar_mensaje(mensaje):
    """
    Procesa un mensaje recibido.
    """
    if "message" not in mensaje:
        return

    chat_id = mensaje["message"]["chat"]["id"]
    texto = mensaje["message"].get("text", "")

    if texto.startswith("/hola"):
        comando_hola(chat_id, mensaje)


def comando_hola(chat_id, mensaje):
    """
    Comando /hola.
    """
    usuario = mensaje["message"].get("from", {})
    nombre = usuario.get("first_name", "usuario")
    enviar_mensaje(
        chat_id,
        f"¡Hola, {nombre}! \n"
        "Bienvenido a el bot de Grupo #9."
    )


def iniciar_bot():
    """
    Bucle principal del bot.
    """
    print("Bot iniciado correctamente.")

    offset = None
    while True:
        respuesta = obtener_actualizaciones(offset)
        if not respuesta.get("ok"):
            print("Error al obtener actualizaciones.")
            continue
        actualizaciones = respuesta.get("result", [])
        for actualizacion in actualizaciones:
            offset = actualizacion["update_id"] + 1
            procesar_mensaje(actualizacion)

if __name__ == "__main__":
    iniciar_bot()