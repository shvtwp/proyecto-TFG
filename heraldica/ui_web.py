from flask import Flask, request, abort, render_template
from heraldica.ui_catalogo import CatalogoUI
import os


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["repo"] = CatalogoUI()

    @app.get("/")
    def home():
        repo: CatalogoUI = app.config["repo"]
        
        query = request.args.get("q", "").strip()
        filtro_esmalte = request.args.get("esmalte", "").strip()
        filtro_mueble = request.args.get("mueble", "").strip()
        filtro_adorno = request.args.get("adorno", "").strip()
        
        if query or filtro_esmalte or filtro_mueble or filtro_adorno:
            resultados = repo.buscar_combinada(
                texto=query,
                esmalte=filtro_esmalte,
                mueble=filtro_mueble,
                adorno=filtro_adorno
            )
        else:
            resultados = repo.obtener_todos()
        
        return render_template(
            "index.html",
            query=query,
            filtros={
                "esmalte": filtro_esmalte,
                "mueble": filtro_mueble,
                "adorno": filtro_adorno
            },
            esmaltes=repo.obtener_esmaltes(),
            muebles=repo.obtener_muebles(),
            adornos=repo.obtener_adornos(),
            resultados=resultados,
            total=len(resultados)
        )

    @app.get("/search")
    def search():
        repo: CatalogoUI = app.config["repo"]
        
        query = request.args.get("q", "").strip()
        filtro_esmalte = request.args.get("esmalte", "").strip()
        filtro_mueble = request.args.get("mueble", "").strip()
        filtro_adorno = request.args.get("adorno", "").strip()
        
        if query or filtro_esmalte or filtro_mueble or filtro_adorno:
            resultados = repo.buscar_combinada(
                texto=query,
                esmalte=filtro_esmalte,
                mueble=filtro_mueble,
                adorno=filtro_adorno
            )
        else:
            resultados = repo.obtener_todos()
        
        return render_template(
            "resultados.html",
            resultados=resultados,
            total=len(resultados)
        )

    @app.get("/escudo/<rid>")
    def escudo(rid: str):
        abort(404)

    return app

app = create_app()