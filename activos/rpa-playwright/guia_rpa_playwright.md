# Automatización de plataformas web sin API con Playwright

Guía técnica completa y reutilizable. Describe la lógica, las herramientas, el
flujo y el desarrollo de un robot que opera una plataforma web (login, carga de
datos y subida de archivos) cuando esa plataforma **no ofrece API**. Está escrita
para ser portada a cualquier proyecto: el ejemplo usa una plataforma de trámites,
pero el patrón aplica a cualquier web detrás de login.

---

## 1. El problema y por qué este enfoque

Muchas plataformas críticas (administraciones, ERPs antiguos, portales B2B) no
exponen API. La única vía de integración es **operar la interfaz web como lo
haría una persona**: abrir el navegador, loguearse, navegar, rellenar formularios,
adjuntar archivos y enviar. A esto se le llama **RPA** (Robotic Process Automation)
o, más concretamente cuando ocurre dentro del navegador, *browser automation*.

Hay dos familias de herramientas:

1. **RPA visuales** (Power Automate Desktop, UiPath, Axiom, UI.Vision): grabás
   clics y los reproducís. No requieren programar. Su debilidad es que muchas
   localizan elementos por posición o imagen en pantalla, lo que se rompe con
   cambios de resolución, layout o idioma del navegador.

2. **Automatización por código** (Playwright, Selenium, Puppeteer): escribís un
   programa que controla el navegador. Localiza elementos por su **estructura
   HTML** (un campo por su `id`, no por su posición en pantalla), lo que lo hace
   mucho más estable. Permite lógica condicional real (reintentos, detección de
   errores, ramas según el estado de la página).

Esta guía usa **Playwright** porque es la opción más robusta, moderna y mantenible,
y porque convive de forma natural con un backend en Python.

### Principio rector: automatización asistida, no desatendida

Las plataformas serias ponen barreras deliberadas en puntos concretos: **login**
(a veces con certificado digital o segundo factor), **CAPTCHA** y **firma**. Esas
barreras existen para exigir presencia humana. El diseño correcto **no intenta
eliminarlas**: deja que el humano resuelva esos puntos puntuales y el robot hace
todo el trabajo repetitivo entre medio. Intentar saltar un CAPTCHA o automatizar
una firma sistemáticamente suele violar los términos de uso y traslada
responsabilidad legal al operador. La regla práctica:

> El humano hace los puntos de fricción deliberada (login, CAPTCHA, firma).
> El robot hace lo repetitivo (navegar, leer, rellenar, descargar, subir).

---

## 2. Herramientas utilizadas

| Herramienta | Rol en el sistema | Por qué |
|---|---|---|
| **Playwright (Python)** | Controla el navegador real (Chromium/Firefox/WebKit) | Localización por HTML, esperas automáticas, manejo nativo de subida/descarga de archivos, headless o con ventana |
| **Chromium** | El navegador que Playwright conduce | Incluido y gestionado por Playwright |
| **Python 3.10+** | Lenguaje del robot y del backend | Mismo stack que el resto del proyecto; ecosistema rico |
| **Flask** *(solo en la demo)* | Plataforma simulada para probar el robot sin tocar el sistema real | Servidor mínimo para desarrollar contra algo realista |
| **Cron / n8n / scheduler** *(en producción)* | Dispara el robot periódicamente y avisa si falla | Orquestación; no ejecuta el scraping, solo lo agenda y monitorea |

**Por qué un orquestador separado:** el robot es lógica de navegación; el
scheduler es "cuándo correrlo y qué hacer si falla". Mantenerlos separados hace
que el robot sea testeable de forma aislada y reutilizable desde cualquier
disparador (cron, webhook, cola de tareas).

---

## 3. Conceptos de Playwright que hacen falta

Playwright modela tres objetos principales:

- **Browser**: el navegador lanzado. `p.chromium.launch(headless=True)`.
- **Context**: una sesión aislada dentro del navegador (sus propias cookies y
  almacenamiento). Equivale a un "perfil". Permite persistir la sesión entre
  ejecuciones.
- **Page**: una pestaña. Sobre ella se ejecutan las acciones.

Las acciones esenciales:

```python
page.goto(url)                          # navegar a una URL
page.fill("#campo", "valor")            # escribir en un <input> por su id
page.select_option("#tipo", "VALOR")    # elegir opción de un <select>
page.click("#boton")                    # pulsar un elemento
page.set_input_files("#documento", ruta)# adjuntar un archivo a un <input type=file>
page.wait_for_url("**/panel")           # esperar a que la navegación ocurra
page.inner_text("body")                 # leer texto de la página (para verificar)
page.screenshot(path="captura.png")     # evidencia visual
```

### Localizadores: la clave de la robustez

Un robot frágil busca "el botón verde de arriba a la derecha". Un robot robusto
busca `#btn-guardar` (el elemento cuyo `id` es `btn-guardar`). Tipos de
localizador, de más a menos estable:

1. **Por `id`**: `page.fill("#matricula", v)`. El más estable si el sitio usa ids.
2. **Por atributo de test**: `page.click("[data-testid='guardar']")`.
3. **Por rol y texto**: `page.get_by_role("button", name="Guardar")`.
4. **Por CSS/posición**: frágil; evitar salvo que no haya alternativa.

Cuando trabajes contra una plataforma real, el primer paso del desarrollo es
**inspeccionar el HTML** (clic derecho → Inspeccionar) para descubrir los
localizadores estables de cada campo.

### Esperas automáticas

A diferencia de scripts ingenuos que ponen `sleep(3)`, Playwright **espera
automáticamente** a que un elemento exista y sea interactuable antes de actuar.
Esto elimina la mayoría de los fallos por tiempos. Para navegaciones, se usa
`wait_for_url(...)` o `wait_until="networkidle"` en `goto`.

---

## 4. Flujo completo del robot

```
┌─────────────────────────────────────────────────────────────────┐
│ DISPARADOR (cron / n8n / manual)                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. LEER BASE DE ORIGEN                                            │
│    Qué hay que cargar. Puede ser un JSON, una consulta a BD,     │
│    un export de otro sistema, una cola de tareas.                │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. ABRIR NAVEGADOR (con perfil/sesión persistente)               │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. ¿SESIÓN VIVA?                                                  │
│    Ir a una página protegida. Si redirige a /login → sesión caída.│
│    ├── Viva  → continuar                                          │
│    └── Caída → LOGIN (en real: avisar al humano / sesión          │
│                asistida con certificado)                          │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. POR CADA REGISTRO DE LA BASE:                                 │
│    a. abrir el formulario de alta                                │
│    b. rellenar cada campo (fill / select_option)                 │
│    c. adjuntar el/los archivo(s) (set_input_files)               │
│    d. enviar (click) y esperar confirmación (wait_for_url)       │
│    e. capturar evidencia (screenshot)                            │
│    f. registrar resultado (ok / error) en un log                 │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. VERIFICAR                                                      │
│    Releer el listado de la plataforma y confirmar que cada       │
│    registro aparece. Es el control de calidad del robot.         │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. CERRAR Y REPORTAR                                             │
│    Cerrar navegador. Devolver código de salida.                  │
│    Si hubo fallos → el orquestador avisa (Telegram, email).      │
└─────────────────────────────────────────────────────────────────┘
```

---
