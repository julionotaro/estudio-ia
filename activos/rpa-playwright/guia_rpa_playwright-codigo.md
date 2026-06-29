## 5. Código completo y comentado

El proyecto tiene cuatro piezas: la **base de origen**, la **plataforma**
(en desarrollo, una simulada; en producción, la real), el **robot** y el
**orquestador**. Abajo va cada una.

### 5.1 Base de origen — `datos/registros.json`

Define qué cargar. En tu proyecto real esto puede ser una consulta a base de
datos; aquí es un JSON para que el robot sea independiente de la fuente.

```json
[
  {
    "id": "R-001",
    "tipo": "TIPO_A",
    "campo_clave": "ABC123",
    "campo_secundario": "XYZ789012345",
    "identificador": "11222333D",
    "nombre": "NOMBRE COMPLETO EJEMPLO",
    "entidad": "ENTIDAD EJEMPLO SL",
    "documento": "adjunto_ABC123.pdf"
  }
]
```

### 5.2 El robot — `robot/cargar.py`

Pieza central y reutilizable. Escrita de forma genérica: cambiando `URL`, los
selectores (`SEL`) y el bloque de login se adapta a cualquier plataforma.

```python
"""ROBOT DE CARGA — Playwright sobre una plataforma web sin API.
Flujo: leer base de origen -> abrir navegador -> (login si la sesion cayo) ->
por cada registro: rellenar formulario + adjuntar archivo + enviar + verificar.
Adaptacion a otra plataforma: cambiar URL, los SELECTORES y la funcion login().
Uso: python3 robot/cargar.py [--headed]"""
from __future__ import annotations
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, TimeoutError as PWTimeout

BASE = Path(__file__).resolve().parent.parent
DATOS = BASE / "datos" / "registros.json"
UPLOADS = BASE / "uploads"
SHOTS = BASE / "salida" / "capturas"; SHOTS.mkdir(parents=True, exist_ok=True)

URL = "http://127.0.0.1:5055"   # URL base de la plataforma
USUARIO = "gestor"              # en real: gestionar fuera del codigo
CLAVE = "demo1234"              # nunca hardcodear credenciales reales

SEL = {  # descubrir inspeccionando el HTML real
    "usuario": "#usuario", "clave": "#clave", "btn_login": "#btn-entrar",
    "tipo": "#tipo", "clave_1": "#matricula", "clave_2": "#bastidor",
    "ident": "#nif_adquirente", "nombre": "#nombre_adquirente",
    "entidad": "#gestoria", "archivo": "#documento", "btn_guardar": "#btn-guardar",
}
HEADLESS = "--headed" not in sys.argv

def _shot(page, nombre):
    page.screenshot(path=str(SHOTS / f"{nombre}.png"), full_page=True)

def sesion_viva(page) -> bool:
    # Si /panel redirige a /login, la sesion cayo. Aqui, en produccion, el robot
    # avisaria a un humano para re-loguear (certificado, 2FA) en vez de loguear solo.
    page.goto(f"{URL}/panel", wait_until="networkidle")
    return "/login" not in page.url

def login(page):
    page.goto(f"{URL}/login", wait_until="networkidle")
    page.fill(SEL["usuario"], USUARIO); page.fill(SEL["clave"], CLAVE)
    page.click(SEL["btn_login"]); page.wait_for_url(f"{URL}/panel", timeout=5000)

def cargar_registro(page, r, i):
    page.goto(f"{URL}/alta", wait_until="networkidle")
    page.select_option(SEL["tipo"], r["tipo"])
    page.fill(SEL["clave_1"], r["campo_clave"]); page.fill(SEL["clave_2"], r["campo_secundario"])
    page.fill(SEL["ident"], r["identificador"]); page.fill(SEL["nombre"], r["nombre"])
    page.fill(SEL["entidad"], r["entidad"])
    archivo = UPLOADS / r["documento"]
    if not archivo.exists(): raise FileNotFoundError(f"Falta archivo: {archivo}")
    page.set_input_files(SEL["archivo"], str(archivo))  # subida real, sin dialogo del SO
    _shot(page, f"alta_{i:02d}_{r['campo_clave']}")
    page.click(SEL["btn_guardar"]); page.wait_for_url(f"{URL}/panel**", timeout=5000)

def verificar(page, esperados) -> bool:
    page.goto(f"{URL}/panel", wait_until="networkidle")
    cuerpo = page.inner_text("body"); ok = True
    for r in esperados:
        ok = ok and (r["campo_clave"] in cuerpo)
    _shot(page, "panel_final"); return ok

def main() -> int:
    registros = json.loads(DATOS.read_text(encoding="utf-8"))
    with sync_playwright() as p:
        nav = p.chromium.launch(headless=HEADLESS)
        # Para PERSISTIR sesion entre ejecuciones usar launch_persistent_context(user_data_dir=...)
        ctx = nav.new_context(accept_downloads=True); page = ctx.new_page()
        try:
            if not sesion_viva(page): login(page)
            for i, r in enumerate(registros, 1): cargar_registro(page, r, i)
            todo_ok = verificar(page, registros)
        except PWTimeout as e:
            _shot(page, "error_timeout"); print(e); return 2
        finally:
            ctx.close(); nav.close()
    return 0 if todo_ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
```

### 5.3 Plataforma simulada para desarrollo — `sim/app.py`

Mientras no tengas acceso a la plataforma real, desarrollá contra una **simulación**
que reproduzca la mecánica (login por cookie, listado, alta con subida). Flask mínimo;
cuando exista la real, se descarta y se apunta el robot a la URL real. Lo único que el
robot necesita de las plantillas HTML es que cada campo tenga un `id` estable y que el
`<form>` de alta declare `enctype="multipart/form-data"` (olvido habitual que rompe la
subida de archivo).

### 5.4 Orquestador — disparar y monitorear

El robot no se agenda a sí mismo. Un scheduler lo dispara y reacciona a su **código de
salida** (`0` = ok, `≠0` = fallo).

**Cron (Linux):**
```bash
# cada dia 08:00; si falla, avisa por Telegram
0 8 * * * usuario cd /ruta && python3 robot/cargar.py || \
  curl -s -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
       -d chat_id=<CHAT> -d text="Robot de carga FALLO"
```

**n8n:** nodo *Schedule* -> *Execute Command* (o HTTP Request a un endpoint que lanza el
robot); si devuelve error, nodo siguiente avisa. n8n orquesta; el scraping no vive en n8n.

---
