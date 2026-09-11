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

# Comandos de integrante 3
def comando_ayuda(chat_id):
    # muestra todos los comandos disponibles y una descripcion de ellos
    mensaje = (
        "*Panel de Comandos - Grupo #9*\n"
        "-------------------------------------\n\n"
        "*Comandos Generales*\n"
        "`/hola` — Saluda al usuario de forma personalizada.\n"
        "`/menu` — Muestra el menú interactivo con botones.\n"
        "`/ayuda` — Muestra este listado de comandos.\n\n"
        "*Información del Grupo*\n"
        "`/hora` — Muestra la fecha y hora actual.\n"
        "`/contacto` — Muestra la información de contacto del grupo.\n"
        "`/integrantes` — Muestra los integrantes y carnets.\n\n"
        "*Herramientas y Cálculos*\n"
        "`/calcular <n1> <operador> <n2>` — Operaciones aritméticas (+, -, x, /).\n"
        "`/tabla <numero>` — Genera la tabla de multiplicar de un número.\n"
        "`/convertir <cantidad> <origen> <destino>` — Convierte longitud (cm, m, km, mi, ft).\n"
        "`/aleatorio <min> <max>` — Genera un número aleatorio en un rango.\n\n"
        "-------------------------------------\n"
    )
    enviar_mensaje(chat_id, mensaje)

def comando_menu(chat_id):
    
    # Muestra un menú interactivo con botones.
    
    parametros = {
        "chat_id": chat_id,
        "text": "Seleccione una opción del menú:",
        "reply_markup": json.dumps({
            "inline_keyboard": [
                [{"text": "Saludar", "callback_data": "/hola"}],
                [{"text": "Hora Actual", "callback_data": "/hora"}],
                [{"text": "Contacto", "callback_data": "/contacto"}],
                [{"text": "Integrantes", "callback_data": "/integrantes"}],
                [{"text": "Ayuda", "callback_data": "/ayuda"}]
            ]
        })
    }
    llamar_api("sendMessage", parametros)

# ==============================================================================
# COMANDOS INTEGRANTE 4
# ==============================================================================

def formatear_numero(numero):
    """
    Evita mostrar decimales innecesarios.
    """
    return f"{numero:g}"


def comando_calcular(chat_id, partes):
    """
    Comando /calcular <numero1> <operador> <numero2>.
    Realiza suma, resta, multiplicaci\u00f3n y divisi\u00f3n.
    """

    if len(partes) != 4:
        mensaje = (
            "*Error: par\u00e1metros incorrectos*\n\n"
            "Forma correcta:\n"
            "`/calcular <numero1> <operador> <numero2>`\n\n"
            "Ejemplo:\n"
            "`/calcular 10 + 5`"
        )
        enviar_mensaje(chat_id, mensaje)
        return

    try:
        numero1 = float(partes[1])
        numero2 = float(partes[3])
    except ValueError:
        mensaje = (
            "*Error: valores inv\u00e1lidos*\n\n"
            "Los valores utilizados en la operaci\u00f3n deben ser n\u00fameros.\n\n"
            "Ejemplo:\n"
            "`/calcular 10 + 5`"
        )
        enviar_mensaje(chat_id, mensaje)
        return

    operador = partes[2].lower()

    if operador == "+":
        resultado = numero1 + numero2

    elif operador == "-":
        resultado = numero1 - numero2

    elif operador in ("*", "x"):
        resultado = numero1 * numero2

    elif operador == "/":
        if numero2 == 0:
            mensaje = (
                "*Error matem\u00e1tico*\n\n"
                "No es posible realizar una divisi\u00f3n entre cero."
            )
            enviar_mensaje(chat_id, mensaje)
            return

        resultado = numero1 / numero2

    else:
        mensaje = (
            "*Error: operador incorrecto*\n\n"
            "Los operadores permitidos son:\n"
            "`+` suma\n"
            "`-` resta\n"
            "`*` o `x` multiplicaci\u00f3n\n"
            "`/` divisi\u00f3n\n\n"
            "Ejemplo:\n"
            "`/calcular 10 * 5`"
        )
        enviar_mensaje(chat_id, mensaje)
        return

    mensaje = (
        "*Resultado de la operaci\u00f3n*\n\n"
        f"`{formatear_numero(numero1)} "
        f"{partes[2]} "
        f"{formatear_numero(numero2)} = "
        f"{formatear_numero(resultado)}`"
    )

    enviar_mensaje(chat_id, mensaje)


def comando_tabla(chat_id, partes):
    """
    Comando /tabla <numero>.
    Genera la tabla de multiplicar desde 1 hasta 10.
    """

    if len(partes) != 2:
        mensaje = (
            "*Error: par\u00e1metros incorrectos*\n\n"
            "Forma correcta:\n"
            "`/tabla <numero>`\n\n"
            "Ejemplo:\n"
            "`/tabla 5`"
        )
        enviar_mensaje(chat_id, mensaje)
        return

    try:
        numero = float(partes[1])
    except ValueError:
        mensaje = (
            "*Error: valor inv\u00e1lido*\n\n"
            "El par\u00e1metro ingresado debe ser un n\u00famero.\n\n"
            "Ejemplo:\n"
            "`/tabla 5`"
        )
        enviar_mensaje(chat_id, mensaje)
        return

    numero_texto = formatear_numero(numero)
    lineas = []

    for i in range(1, 11):
        resultado = numero * i
        lineas.append(
            f"{numero_texto} x {i} = {formatear_numero(resultado)}"
        )

    mensaje = (
        f"*Tabla de multiplicar del {numero_texto}*\n\n"
        + "\n".join(lineas)
    )

    enviar_mensaje(chat_id, mensaje)


# ==============================================================================
# PROCESAMIENTO PRINCIPAL DE MENSAJES
# ==============================================================================

def procesar_mensaje(mensaje):
    """
    Procesa un mensaje recibido y lo direcciona al comando correspondiente.
    """

    # si da clic al boton
    if "callback_query" in mensaje:
        cq = mensaje["callback_query"]
        cq_id = cq["id"]
        chat_id = cq["message"]["chat"]["id"]
        cmd = cq.get("data", "").strip().lower().split("@")[0]
        
        try:
            llamar_api("answerCallbackQuery", {"callback_query_id": cq_id})
        except Exception:
            pass
        # Ejecutar el comando del boton
        if cmd == "/hola":
            # Le pasa la estructura
            comando_hola(chat_id, {"message": {"from": cq.get("from", {})}})
        elif cmd == "/hora":
            comando_hora(chat_id)
        elif cmd == "/contacto":
            comando_contacto(chat_id)
        elif cmd == "/integrantes":
            comando_integrantes(chat_id)
        elif cmd == "/ayuda":
            comando_ayuda(chat_id)
        elif cmd == "/menu":
            comando_menu(chat_id)
        return
    
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
    elif cmd == "/ayuda":
        comando_ayuda(chat_id)
    elif cmd == "/menu":
        comando_menu(chat_id)
    elif cmd == "/calcular":
        comando_calcular(chat_id, partes)
    elif cmd == "/tabla":
        comando_tabla(chat_id, partes)

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
