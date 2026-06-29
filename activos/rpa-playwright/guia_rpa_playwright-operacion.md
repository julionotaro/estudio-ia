## 6. Instalación y ejecución

```bash
# 1. Dependencias del robot
pip install playwright
python3 -m playwright install chromium

# 2. (solo si usas la simulacion para desarrollar)
pip install flask

# 3. Arrancar la simulacion en una terminal
cd sim && python3 app.py        # queda en http://127.0.0.1:5055

# 4. Correr el robot en otra terminal
python3 robot/cargar.py           # headless
python3 robot/cargar.py --headed  # con ventana, para verlo operar
```

En un servidor sin pantalla, el robot corre **headless** sin cambios. Si el
sistema operativo del servidor pide librerías del navegador, se instalan con
`python3 -m playwright install-deps chromium`.

---

## 7. Adaptar a una plataforma real (checklist)

1. **Inspeccionar el HTML** de la plataforma real (clic derecho → Inspeccionar)
   y anotar el localizador estable de cada campo (preferir `id` o `data-testid`).
2. **Sustituir** en el robot: `URL`, el diccionario `SEL` de selectores, y la URL
   de las páginas (`/panel`, `/alta`, `/login`) por las reales.
3. **Login**: si la plataforma usa certificado digital o segundo factor, no
   automatizar el login. Usar `launch_persistent_context(user_data_dir=...)` para
   que un humano inicie sesión una vez y el robot reutilice ese perfil. Detectar
   sesión caída con `sesion_viva()` y avisar para re-loguear.
4. **Credenciales**: nunca hardcodearlas. Leerlas de variables de entorno o de un
   gestor de secretos.
5. **Ritmo humano**: si la plataforma tiene detección de bots, añadir pequeñas
   esperas entre acciones y evitar velocidades inhumanas.
6. **Idempotencia**: antes de cargar, comprobar si el registro ya existe en la
   plataforma para no duplicar (buscar por el campo clave en el listado).
7. **Manejo de errores por registro**: envolver cada `cargar_registro` en su
   propio try/except para que un fallo no detenga el lote completo; registrar
   cuáles fallaron y reintentarlos después.

---

## 8. Errores frecuentes y cómo evitarlos

| Síntoma | Causa habitual | Solución |
|---|---|---|
| `ERR_CONNECTION_REFUSED` | La plataforma/servidor no está levantada | Verificar que el servicio responde antes de correr el robot |
| `Timeout` al esperar un elemento | Selector incorrecto o la página cambió | Re-inspeccionar el HTML; usar un localizador más estable |
| La subida de archivo no llega | Falta `enctype="multipart/form-data"` en el `<form>` | Añadir el `enctype` |
| El robot "pierde" la sesión cada vez | Sin contexto persistente | Usar `launch_persistent_context(user_data_dir=...)` |
| Funciona con ventana pero no headless | Diferencias de viewport o JS dependiente de foco | Fijar `viewport` y revisar esperas; capturar screenshot del fallo |
| Se duplican registros | Sin control de idempotencia | Comprobar existencia por campo clave antes de cargar |
| Detección de bot / bloqueo | Velocidad inhumana, huella del navegador | Espaciar acciones; en última instancia, plataforma sin alternativa a la API |

---

## 9. Consideraciones legales y de diseño

- **Términos de uso**: automatizar una plataforma puede estar restringido por sus
  términos. Revisarlos antes de desplegar en producción.
- **CAPTCHA y firma**: son barreras intencionales de presencia humana. El diseño
  correcto las deja al humano; evadirlas con servicios de terceros suele violar
  términos y trasladar responsabilidad legal.
- **Sesiones cortas**: las plataformas serias caducan sesiones por inactividad,
  por sesión única o por re-autenticación periódica. Diseñar asumiendo que la
  sesión puede estar muerta en cualquier corrida, detectarlo y reaccionar.
- **Trazabilidad**: capturar screenshots y logs por cada acción da evidencia de
  lo que el robot hizo, útil para auditoría y para depurar.
- **Cuando exista API, usar la API**: el RPA web es siempre un equilibrio frágil.
  Es la solución correcta solo cuando no hay integración programática disponible.

---

## 10. Resumen de la arquitectura

```
Base de origen  -->  ROBOT (Playwright)  -->  Plataforma web (sin API)
  (JSON/BD)            |  login asistido        |  formularios + subida
                       |  rellenar + subir      |
                       |  verificar             v
                       |                     Confirmacion
                       v
                  Evidencia (screenshots + log)
                       ^
                       |
              Orquestador (cron/n8n): agenda y avisa si falla
```

La fortaleza del patrón está en la separación de responsabilidades: la **fuente**
de datos es intercambiable, el **robot** es lógica de navegación pura y testeable,
la **plataforma** se simula en desarrollo y se cambia por la real en producción
tocando solo configuración, y el **orquestador** decide cuándo y qué hacer ante
fallos sin contaminar la lógica del robot.

---

*Esta guía se divide en tres archivos: `guia_rpa_playwright.md` (intro, conceptos,
flujo), `guia_rpa_playwright-codigo.md` (código completo) y
`guia_rpa_playwright-operacion.md` (este: instalación, checklist, errores, legal).
La demo funcional está en `demo_rpa_playwright.zip`.*
