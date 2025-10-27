from flask import Flask, request, abort
from heraldica.ui_catalogo import CatalogoUI
import os

repo = CatalogoUI()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["repo"] = CatalogoUI()
    print("DEBUG DATABASE_URL =", os.environ.get("DATABASE_URL"))

    @app.get("/")
    def home():
        return (
            "<!doctype html><meta charset='utf-8'>"
            "<title>Heraldica para todas</title>"
            "<h1>Heráldica para todas (estructura mínima)</h1>"
            "<p>Formulario y resultados llegarán en los siguientes PRs.</p>"
            "<p><a href='/search'>Ver catálogo completo</a></p>"
        )

    @app.get("/search")
    def search():
        q = (request.args.get("q") or "").strip()
        repo: CatalogoUI = app.config["repo"]

        # Si no hay criterio, mostrar todo el catálogo
        results = repo.buscar_libre(q) if q else repo.obtener_todos()

        def _badge(label: str, value: str) -> str:
            return f"<span style='display:inline-block;padding:0.15rem 0.5rem;margin:0 0.3rem 0.3rem 0;border:1px solid #ccc;border-radius:999px;font-size:0.9rem'>{label}: {value}</span>"

        def _maybe_img(src: str) -> str:
            if not src:
                return ""
            return f"<img src='{src}' alt='' style='height:36px;vertical-align:middle;margin-right:8px;border:1px solid #eee;border-radius:6px'/>"

        items_parts = []
        for r in results:
            nombre = str(r.get("nombre", ""))
            campo = str(r.get("campo", ""))
            muebles = [str(x) for x in (r.get("muebles") or [])]
            pieza = str(r.get("pieza_heraldica") or "")
            adorno = str(r.get("adorno_exterior") or "")
            portador = str(r.get("portador") or "")
            img = str(r.get("imagen_src") or "")

            badges = []
            if campo:
                badges.append(_badge("campo", campo))
            if muebles:
                badges.append(_badge("muebles", ", ".join(muebles)))
            if pieza:
                badges.append(_badge("pieza", pieza))
            if adorno:
                badges.append(_badge("adorno", adorno))
            if portador:
                badges.append(_badge("portador", portador))

            card = (
                "<li style='list-style:none;margin:0 0 1rem 0;padding:0.75rem;border:1px solid #e6e6e6;border-radius:10px'>"
                f"{_maybe_img(img)}"
                f"<strong style='font-size:1.05rem'>{nombre}</strong>"
                f"<div style='margin-top:0.25rem'>{''.join(badges)}</div>"
                "</li>"
            )
            items_parts.append(card)

        # Cambiar el título según si hay búsqueda o no
        titulo = f'Resultados para "{q}"' if q else "Catálogo completo"
        items_html = "<ul style='padding-left:0;'>" + "".join(items_parts) + "</ul>" if items_parts else "<p>Resultados (vacío)</p>"

        html = (
            "<!doctype html><meta charset='utf-8'>"
            f"<h1>{titulo}</h1>"
            f"{items_html}"
            "<p><a href='/'>Volver</a></p>"
        )
        return html


    @app.get("/escudo/<rid>")
    def escudo(rid: str):
        abort(404)

    return app

app = create_app()