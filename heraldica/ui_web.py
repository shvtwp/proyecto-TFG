from flask import Flask, request, abort

def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def home():
        return (
            "<!doctype html><meta charset='utf-8'>"
            "<title>Heraldica para todas</title>"
            "<h1>Heráldica para todas (estructura mínima)</h1>"
            "<p>Formulario y resultados llegarán en los siguientes PRs.</p>"
        )

    @app.get("/search")
    def search():
        q = (request.args.get("q") or "").strip()
        return (
            "<!doctype html><meta charset='utf-8'>"
            f"<h1>Resultados para “{q}”</h1>"
            "<p>Resultados (vacío) — PR1 sin datos.</p>"
            "<p><a href='/'>Volver</a></p>"
        )

    @app.get("/escudo/<rid>")
    def escudo(rid: str):
        abort(404)

    return app

app = create_app()
