# Tarea #3 - Bot Interactivo de Telegram

## Integrantes

| Integrante   | Carnet |
| ------------ | ------ | 
| FERNANDO MISAEL MORALES ORTIZ | 202001950 | 
| CRISTOFHER ANTONIO SAQUILMER RODAS | 201700686 | 
| DANIEL ESTUARDO SALVATIERRA MACAJOLA | 202202768 | 
| MARCO FERNANDO CRUZ MENDOZA | 202001076 | 
| ERICK NOE GÓMEZ LÓPEZ | 201700866 | 

---

## Descripción

Esta tarea consiste en el desarrollo de un bot interactivo para Telegram utilizando **Python** y la **Telegram Bot API** usando **BotFather**.

El bot permite a los usuarios interactuar mediante comandos y posteriormente contará con un menú interactivo mediante botones de Telegram.

La comunicación con Telegram se realiza directamente mediante solicitudes HTTP a la **Telegram Bot API**, sin utilizar bibliotecas externas.

El token de autenticación del bot se maneja mediante una **variable de entorno**, evitando almacenarlo directamente en el código fuente.

---

## Bot de Telegram usando @BotFather

**Nombre del bot:** `G9_tarea3_bot`

**Enlace:** `https://t.me/G9_tarea3_bot`


---

## Tecnologías utilizadas

* Python
* Telegram Bot API
* Variables de entorno
* `urllib` para realizar solicitudes HTTP
* `python-dotenv` para cargar variables de entorno desde `.env`
* Git y GitHub

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

El token del bot se almacena mediante una variable de entorno para evitar incluir información sensible directamente en el código.

El archivo `.env.example` contiene la estructura necesaria:

```env
TELEGRAM_BOT_TOKEN=token_bot_father_aqui
```

Para ejecutar el proyecto localmente, se debe crear un archivo `.env` a partir de `.env.example` y colocar el token real proporcionado por **BotFather**:

```env
TELEGRAM_BOT_TOKEN=TOKEN_REAL_DEL_BOT
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

Ingresar a la carpeta de la tarea:

```bash
cd Tarea3
```

### 2. Crear un entorno virtual

En Windows:

```bash
python -m venv .venv
```

Activar el entorno virtual:

```bash
.venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crear un archivo llamado:

```text
.env
```

Agregar:

```env
TELEGRAM_BOT_TOKEN=TOKEN_REAL_DEL_BOT
```

### 5. Ejecutar el bot

```bash
python main.py
```

Si la configuración es correcta, se mostrará:

```text
Bot iniciado correctamente.
```

Posteriormente se puede acceder al bot desde el enlace del bot en Telegram proporcionado anteriormente en la seccion `Bot de Telegram usando @BotFather` y presionar **START** para comenzar la interacción.

---

## Comandos implementados

### `/hola`

Saluda al usuario utilizando el nombre configurado en su cuenta de Telegram.

Ejemplo:

```text
/hola
```

Respuesta:

```text
¡Hola, Mazariegos! 
Bienvenido a el bot de Grupo #9.
```

El nombre se obtiene dinámicamente de la información proporcionada por Telegram para el usuario que envía el mensaje.

### `/convertir <cantidad> <origen> < destino>`

Realiza conversiones entre las unidades de longitud: cm, m, km, mi, ft.

Ejemplo:

```text
/convertir 1 km cm
```

Respuesta:

```text
📏 Conversión de Longitud

• Entrada: 1.0 km
• Resultado: 100000.0000 cm
```

### `/aleatorio <min> < max>`

Genera un número entero aleatorio dentro del rango [min, max].

Ejemplo:

```text
/aleatorio 1 100
```

Respuesta:

```text
🎲 Generador Aleatorio

• Rango: [1, 100]
• Número obtenido: 12
```

---

## Comandos que puede ejecutar el Bot

Los siguientes comandos forman parte de los requisitos de la tarea como funcionalidades del Bot:

| Comando        | Descripción                                              | Estado       |
| -------------- | -------------------------------------------------------- | ------------ |
| `/hola`        | Saluda al usuario utilizando su nombre de Telegram       | Implementado |
| `/hora`        | Muestra la fecha y hora actual                           | Implementado |
| `/contacto`    | Muestra la información de contacto del grupo             | Implementado |
| `/integrantes` | Muestra los nombres y carnets de los integrantes         | Implementado |
| `/ayuda`       | Muestra los comandos disponibles y su descripción        | Pendiente    |
| `/menu`        | Muestra un menú interactivo mediante botones de Telegram | Pendiente    |
| `/calcular`    | Realiza operaciones matemáticas básicas                  | Pendiente    |
| `/tabla`       | Muestra la tabla de multiplicar de un número del 1 al 10 | Pendiente    |
| `/convertir`   | Convierte unidades de longitud                           | Implementado    |
| `/aleatorio`   | Genera un número entero aleatorio dentro de un rango     | Implementado    |

---

## Comunicación con Telegram

El proyecto realiza la comunicación directamente con la Telegram Bot API mediante solicitudes HTTP.

No se utilizan librerías específicas de Telegram.

La estructura general de comunicación es:

```text
Usuario --> comando Telegram --> Telegram Bot API --> main.py (Procesamiento) --> Telegram Bot API --> Telegram --> Usuario recibe respuesta
```

El programa obtiene los mensajes mediante `getUpdates` y envía las respuestas mediante `sendMessage`.

---


