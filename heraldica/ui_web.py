from flask import Flask, request, abort, render_template
from heraldica.catalogo import Catalogo


def _obtener_resultados(repo: Catalogo):
    """Extrae parámetros de búsqueda y devuelve resultados filtrados."""
    query = request.args.get("q", "").strip()
    filtro_esmalte = request.args.get("esmalte", "").strip()
    filtro_mueble = request.args.get("mueble", "").strip()
    filtro_adorno = request.args.get("adorno", "").strip()

    if query or filtro_esmalte or filtro_mueble or filtro_adorno:
        resultados = repo.buscar_combinada(
            texto=query,
            esmalte=filtro_esmalte,
            mueble=filtro_mueble,
            adorno=filtro_adorno,
        )
    else:
        resultados = repo.obtener_todos()

    return resultados, query, filtro_esmalte, filtro_mueble, filtro_adorno


def create_app() -> Flask:
    app = Flask(__name__)
    repo = Catalogo()
    repo.listar_desde_bd()
    app.config["repo"] = repo

    @app.get("/")
    def home():
        repo: Catalogo = app.config["repo"]
        resultados, query, filtro_esmalte, filtro_mueble, filtro_adorno = (
            _obtener_resultados(repo)
        )

        return render_template(
            "index.html",
            query=query,
            filtros={
                "esmalte": filtro_esmalte,
                "mueble": filtro_mueble,
                "adorno": filtro_adorno,
            },
            esmaltes=repo.obtener_esmaltes(),
            muebles=repo.obtener_muebles(),
            adornos=repo.obtener_adornos(),
            resultados=resultados,
            total=len(resultados),
        )

    @app.get("/search")
    def search():
        repo: Catalogo = app.config["repo"]
        resultados, query, filtro_esmalte, filtro_mueble, filtro_adorno = (
            _obtener_resultados(repo)
        )

        return render_template(
            "resultados.html", resultados=resultados, total=len(resultados)
        )

    @app.get("/escudo/<rid>")
    def escudo(rid: str):
        abort(404)

    return app


app = create_app()


def run():
    # Equivalent to: flask --app heraldica/ui_web.py run
    app.run()


def run_debug():
    # Equivalent to: flask --app heraldica/ui_web.py --debug run
    app.run(debug=True)
