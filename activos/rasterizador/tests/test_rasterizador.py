"""Tests del servicio rasterizador.

Los PDF de prueba se generan en el propio test con reportlab: nada de fixtures
binarios en el repo. Requiere `poppler-utils` instalado en el entorno (el mismo
que instala el Dockerfile).
"""

import base64
import io
import json
import os
import sys

import pytest
from fastapi.testclient import TestClient
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402

client = TestClient(app)

PNG_MAGIC = b"\x89PNG"

# A4 a 300 DPI: 210mm x 297mm = 8.27in x 11.69in -> ~2480 x 3508 px
A4_300DPI_ANCHO = 2480
A4_300DPI_ALTO = 3508
TOLERANCIA = 0.02


def pdf_a4(num_paginas: int = 1) -> bytes:
    """Devuelve los bytes de un PDF A4 con `num_paginas` páginas numeradas."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    for i in range(1, num_paginas + 1):
        c.drawString(100, 700, f"Pagina {i}")
        c.showPage()
    c.save()
    return buf.getvalue()


def post_pdf(data: bytes, **params):
    return client.post(
        "/rasterizar",
        files={"file": ("prueba.pdf", data, "application/pdf")},
        params=params,
    )


def assert_aprox(valor: int, esperado: int):
    assert abs(valor - esperado) <= esperado * TOLERANCIA, (
        f"{valor} px fuera de la tolerancia de ±{TOLERANCIA:.0%} sobre {esperado} px"
    )


def test_rasteriza_una_pagina_a4_a_300_dpi():
    r = post_pdf(pdf_a4(1))

    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["dpi"] == 300
    assert cuerpo["num_paginas"] == 1

    pagina = cuerpo["paginas"][0]
    assert pagina["pagina"] == 1
    assert_aprox(pagina["ancho"], A4_300DPI_ANCHO)
    assert_aprox(pagina["alto"], A4_300DPI_ALTO)
    assert base64.b64decode(pagina["png_base64"]).startswith(PNG_MAGIC)


def test_multipagina_devuelve_paginas_numeradas_en_orden():
    r = post_pdf(pdf_a4(3))

    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["num_paginas"] == 3
    assert [p["pagina"] for p in cuerpo["paginas"]] == [1, 2, 3]
    for pagina in cuerpo["paginas"]:
        assert base64.b64decode(pagina["png_base64"]).startswith(PNG_MAGIC)


def test_dpi_parametrizado_reduce_dimensiones_a_la_mitad():
    data = pdf_a4(1)

    r300 = post_pdf(data, dpi=300)
    r150 = post_pdf(data, dpi=150)

    assert r300.status_code == 200
    assert r150.status_code == 200
    assert r150.json()["dpi"] == 150

    p300 = r300.json()["paginas"][0]
    p150 = r150.json()["paginas"][0]
    assert_aprox(p150["ancho"], p300["ancho"] // 2)
    assert_aprox(p150["alto"], p300["alto"] // 2)


def test_dpi_fuera_de_rango_es_rechazado_por_validacion():
    r = post_pdf(pdf_a4(1), dpi=5000)

    assert r.status_code == 422


def test_archivo_vacio_devuelve_400():
    r = post_pdf(b"")

    assert r.status_code == 400
    assert r.json()["detail"] == "Archivo vacío."


def test_no_pdf_devuelve_400_y_nunca_500():
    r = post_pdf(b"esto no es un PDF, son bytes basura")

    assert r.status_code == 400
    assert r.json()["detail"] == "PDF ilegible o corrupto."


def test_health():
    r = client.get("/health")

    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


# --------------------------------------------------------------------------
# /rasterizar-regiones — recorte por región (Palanca B)
# --------------------------------------------------------------------------

A4_PT_ANCHO = 595.27
A4_PT_ALTO = 841.89


def pdf_con_marca() -> bytes:
    """PDF A4 con un rectángulo negro en el cuadrante superior izquierdo.

    En coordenadas relativas (0–1, y desde arriba) la marca ocupa ~[0..0.5]×[0..0.2].
    El resto de la página queda en blanco: sirve para distinguir un recorte con
    tinta de uno vacío.
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    # reportlab: origen abajo-izquierda. Top 20% => y en [0.8*alto, alto].
    c.rect(0, A4_PT_ALTO * 0.8, A4_PT_ANCHO * 0.5, A4_PT_ALTO * 0.2, fill=1)
    c.showPage()
    c.save()
    return buf.getvalue()


def post_regiones(data: bytes, regiones, **params):
    return client.post(
        "/rasterizar-regiones",
        files={"file": ("prueba.pdf", data, "application/pdf")},
        data={"regiones": json.dumps(regiones)},
        params=params,
    )


def test_regiones_recorta_a_las_dimensiones_pedidas():
    r = post_regiones(
        pdf_a4(1),
        [{"nombre": "mitad_sup", "x0": 0.0, "y0": 0.0, "x1": 1.0, "y1": 0.5}],
    )

    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["num_paginas"] == 1
    pagina = cuerpo["paginas"][0]
    recorte = pagina["regiones"][0]
    assert recorte["nombre"] == "mitad_sup"
    # ancho completo, alto la mitad de la página.
    assert_aprox(recorte["ancho"], pagina["ancho"])
    assert_aprox(recorte["alto"], pagina["alto"] // 2)
    assert base64.b64decode(recorte["png_base64"]).startswith(PNG_MAGIC)


def test_region_con_tinta_no_parece_vacio_y_region_en_blanco_si():
    r = post_regiones(
        pdf_con_marca(),
        [
            {"nombre": "con_marca", "x0": 0.0, "y0": 0.0, "x1": 0.5, "y1": 0.2},
            {"nombre": "en_blanco", "x0": 0.5, "y0": 0.8, "x1": 1.0, "y1": 1.0},
        ],
    )

    assert r.status_code == 200
    recortes = {x["nombre"]: x for x in r.json()["paginas"][0]["regiones"]}
    assert recortes["con_marca"]["parece_vacio"] is False
    assert recortes["con_marca"]["tinta_ratio"] > 0.05
    # Recorte desalineado/vacío -> señal de fallback a página completa.
    assert recortes["en_blanco"]["parece_vacio"] is True


def test_incluir_pagina_completa_agrega_png_de_pagina():
    r = post_regiones(
        pdf_a4(1),
        [{"nombre": "banda", "x0": 0.0, "y0": 0.0, "x1": 1.0, "y1": 0.3}],
        incluir_pagina_completa=True,
    )

    assert r.status_code == 200
    pagina = r.json()["paginas"][0]
    assert "png_base64" in pagina
    assert base64.b64decode(pagina["png_base64"]).startswith(PNG_MAGIC)
    # Y sigue trayendo la región recortada.
    assert pagina["regiones"][0]["nombre"] == "banda"


def test_pagina_especifica_solo_devuelve_esa_pagina():
    r = post_regiones(
        pdf_a4(3),
        [{"nombre": "banda", "x0": 0.0, "y0": 0.0, "x1": 1.0, "y1": 0.3, "pagina": 2}],
    )

    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["num_paginas"] == 3  # el doc tiene 3
    assert [p["pagina"] for p in cuerpo["paginas"]] == [2]  # solo rasterizó la 2


def test_region_sin_pagina_se_aplica_a_todas():
    r = post_regiones(
        pdf_a4(3),
        [{"nombre": "banda", "x0": 0.0, "y0": 0.0, "x1": 1.0, "y1": 0.3}],
    )

    assert r.status_code == 200
    paginas = r.json()["paginas"]
    assert [p["pagina"] for p in paginas] == [1, 2, 3]
    for p in paginas:
        assert [x["nombre"] for x in p["regiones"]] == ["banda"]


def test_dpi_mayor_amplia_el_recorte():
    data = pdf_a4(1)
    reg = [{"nombre": "b", "x0": 0.0, "y0": 0.0, "x1": 1.0, "y1": 0.3}]

    r300 = post_regiones(data, reg, dpi=300)
    r600 = post_regiones(data, reg, dpi=600)

    a300 = r300.json()["paginas"][0]["regiones"][0]["ancho"]
    a600 = r600.json()["paginas"][0]["regiones"][0]["ancho"]
    assert_aprox(a600, a300 * 2)


def test_coordenadas_invalidas_devuelven_422():
    # x1 < x0
    r = post_regiones(
        pdf_a4(1),
        [{"nombre": "mala", "x0": 0.8, "y0": 0.0, "x1": 0.2, "y1": 0.5}],
    )
    assert r.status_code == 422


def test_pagina_fuera_de_rango_devuelve_400():
    r = post_regiones(
        pdf_a4(1),
        [{"nombre": "b", "x0": 0.0, "y0": 0.0, "x1": 1.0, "y1": 0.3, "pagina": 9}],
    )
    assert r.status_code == 400


def test_regiones_json_invalido_devuelve_400():
    r = client.post(
        "/rasterizar-regiones",
        files={"file": ("prueba.pdf", pdf_a4(1), "application/pdf")},
        data={"regiones": "esto no es json"},
    )
    assert r.status_code == 400


def test_lista_de_regiones_vacia_devuelve_400():
    r = post_regiones(pdf_a4(1), [])
    assert r.status_code == 400


def test_regiones_archivo_no_pdf_devuelve_400():
    r = post_regiones(
        b"bytes basura",
        [{"nombre": "b", "x0": 0.0, "y0": 0.0, "x1": 1.0, "y1": 0.3}],
    )
    assert r.status_code == 400
