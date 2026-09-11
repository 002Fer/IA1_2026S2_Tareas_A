# Tarea #3 - Bot Interactivo de Telegram

## Integrantes

| Integrante | Carnet | Rol / Asignación |
| ------------ | ------ | ---------------- |
| FERNANDO MISAEL MORALES ORTIZ | 202001950 | Integrante 1: Configuración general, BotFather, .env, main.py, /hola |
| CRISTOFHER ANTONIO SAQUILMER RODAS | 201700686 | Integrante 2: /hora, /contacto, /integrantes |
| DANIEL ESTUARDO SALVATIERRA MACAJOLA | 202202768 | Integrante 3: /ayuda, /menu con botones interactivos |
| MARCO FERNANDO CRUZ MENDOZA | 202001076 | Integrante 4: /calcular, /tabla |
| ERICK NOE GÓMEZ LÓPEZ | 201700866 | Integrante 5: /convertir, /aleatorio y manejo de errores |

---

## Descripción

Esta tarea consiste en el desarrollo de un bot interactivo para Telegram utilizando **Python** y la **Telegram Bot API** configurada a través de **BotFather**.

El bot permite a los usuarios interactuar mediante comandos con parámetros y cuenta con un menú interactivo con botones de respuesta rápida de Telegram (*Inline Keyboards*).

La comunicación con Telegram se realiza directamente mediante solicitudes HTTP (`urllib`) a la **Telegram Bot API**, sin utilizar bibliotecas externas.

El token de autenticación del bot se maneja mediante una **variable de entorno** (`.env`), evitando almacenarlo directamente en el código fuente.

---

## Bot de Telegram

**Nombre del bot:** `G9_tarea3_bot`  
**Enlace:** `https://t.me/G9_tarea3_bot`

---

## Tecnologías utilizadas

* **Python 3**
* **Telegram Bot API** (sin librerías de terceros)
* **`urllib`** para realizar solicitudes HTTP (POST/GET)
* **`python-dotenv`** para cargar variables de entorno desde `.env`
* **Variables de entorno** para credenciales sensibles
* **Git y GitHub**

---

## Estructura del proyecto

```text
Tarea3/
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Variables de entorno

El token del bot se almacena mediante una variable de entorno para evitar incluir información sensible en el repositorio.

El archivo `.env.example` contiene la estructura necesaria:

```env
TELEGRAM_BOT_TOKEN=token_bot_father_aqui
```

Para ejecutar el proyecto localmente, se debe crear un archivo `.env` a partir de `.env.example` y colocar el token real de **BotFather**:

```env
TELEGRAM_BOT_TOKEN=TOKEN_REAL_DEL_BOT
```

---

## Instalación y Ejecución

### 1. Clonar el repositorio e ingresar a la carpeta
```bash
git clone https://github.com/002Fer/IA1_2026S2_Tareas_A.git
cd IA1_2026S2_Tareas_A/Tarea3
```

### 2. Crear y activar el entorno virtual
En Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno
Crear un archivo `.env` e ingresar la clave del bot:
```env
TELEGRAM_BOT_TOKEN=TU_TOKEN_DE_BOTFATHER
```

### 5. Ejecutar el bot
```bash
python main.py
```

Si la configuración es correcta, se mostrará:
```text
Bot iniciado correctamente.
```

---

## Comandos Implementados

### `/hola`
Saluda al usuario utilizando su nombre configurado en Telegram.
```text
Sintaxis: /hola
```

### `/hora`
Muestra la fecha y hora actual generada dinámicamente en formato UTC-6.
```text
Sintaxis: /hora
```

### `/contacto`
Muestra la información de contacto oficial definida para el Grupo #9.
```text
Sintaxis: /contacto
```

### `/integrantes`
Muestra el listado de nombres completos y carnets de los 5 integrantes del grupo.
```text
Sintaxis: /integrantes
```

### `/ayuda`
Muestra un panel estructurado con todos los comandos disponibles y su descripción.
```text
Sintaxis: /ayuda
```

### `/menu`
Despliega un menú interactivo con botones de respuesta (*Inline Keyboard*) para acceder rápidamente a los comandos.
```text
Sintaxis: /menu
```

### `/calcular <n1> <operador> <n2>`
Realiza operaciones matemáticas básicas: suma (`+`), resta (`-`), multiplicación (`*` o `x`) y división (`/`).
```text
Ejemplo: /calcular 10 / 2
```

### `/tabla <numero>`
Genera la tabla de multiplicar del número ingresado del 1 al 10.
```text
Ejemplo: /tabla 7
```

### `/convertir <cantidad> <unidad_origen> <unidad_destino>`
Realiza la conversión entre unidades de longitud (`cm`, `m`, `km`, `mi`, `ft`).
```text
Ejemplo: /convertir 1 km cm
```

### `/aleatorio <min> <max>`
Genera un número entero aleatorio dentro del rango de valores indicado `[min, max]`.
```text
Ejemplo: /aleatorio 1 100
```

---

## Estado de Comandos

Los 10 comandos solicitados en la especificación están 100% implementados y validados:

| Comando | Descripción | Estado |
| ------- | ----------- | ------ |
| `/hola` | Saluda al usuario utilizando su nombre de Telegram | Implementado |
| `/hora` | Muestra la fecha y hora actual dinámicamente | Implementado |
| `/contacto` | Muestra la información de contacto del grupo | Implementado |
| `/integrantes` | Muestra los nombres y carnets de los integrantes | Implementado |
| `/ayuda` | Muestra la lista de comandos disponibles y su descripción | Implementado |
| `/menu` | Muestra un menú interactivo mediante botones de Telegram | Implementado |
| `/calcular` | Realiza operaciones matemáticas (+, -, *, /) con validación | Implementado |
| `/tabla` | Muestra la tabla de multiplicar de un número del 1 al 10 | Implementado |
| `/convertir` | Convierte unidades de longitud (cm, m, km, mi, ft) | Implementado |
| `/aleatorio` | Genera un número entero aleatorio dentro de un rango | Implementado |

---

## Comunicación con Telegram Bot API

El proyecto interactúa directamente con la Telegram Bot API mediante la biblioteca estándar de Python (`urllib`):
* `getUpdates`: Para recibir nuevos mensajes mediante Long Polling.
* `sendMessage`: Para enviar mensajes formateados en Markdown y teclados interactivos (`inline_keyboard`).
* `answerCallbackQuery`: Para responder a los clics de botones del menú.
