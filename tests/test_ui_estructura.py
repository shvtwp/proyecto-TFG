from importlib import import_module

def test_app_factory_exists():
    mod = import_module("heraldica.ui_web")
    assert hasattr(mod, "create_app"), "Falta create_app() en heraldica/ui_web.py"

def test_routes_exist_and_return_200():
    app = import_module("heraldica.ui_web").create_app()
    client = app.test_client()

    r = client.get("/")
    assert r.status_code == 200
    body = r.data.decode("utf-8")
    assert "Heráldica para todas (estructura mínima)" in bodyyy 

def test_detail_returns_404_for_now():
    app = import_module("heraldica.ui_web").create_app()
    client = app.test_client()

    r = client.get("/escudo/TEST")
    assert r.status_code == 404
