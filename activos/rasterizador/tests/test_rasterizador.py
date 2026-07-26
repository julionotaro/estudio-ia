"""Tests del servicio rasterizador.

Los PDF de prueba se generan en el propio test con reportlab: nada de fixtures
binarios en el repo. Requiere `poppler-utils` instalado en el entorno (el mismo
que instala el Dockerfile).
"""

import base64
import io
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
