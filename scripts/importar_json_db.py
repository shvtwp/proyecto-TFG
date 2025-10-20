import sys, pathlib, json
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from heraldica.db.session import crear_bd, get_session
from heraldica.db.models import Campo as CampoDB, Mueble as MuebleDB, Escudo as EscudoDB
from heraldica.esmalte import Esmalte
from heraldica.mueble import Mueble as MuebleDomain
from heraldica.adorno import AdornoExterior
from heraldica.escudo import normalizar_texto
from sqlmodel import delete

CATALOGO = pathlib.Path(__file__).resolve().parents[1] / "data" / "catalogo_scraping.json"

def cargar():
    crear_bd()
    data = json.loads(CATALOGO.read_text(encoding="utf-8"))
    with get_session() as s:
        s.exec(delete(MuebleDB))
        s.exec(delete(EscudoDB))
        s.exec(delete(CampoDB))
        s.commit()

        for item in data:
            esmalte = Esmalte(item["campo"]).nombre
            pieza = Esmalte(item["pieza_heraldica"]).nombre if item.get("pieza_heraldica") else None
            muebles = [MuebleDomain(m).nombre for m in item.get("muebles", [])]
            adorno = AdornoExterior(item["adorno_exterior"]).nombre if item.get("adorno_exterior") else None
            portador = normalizar_texto(item["portador"])

            campo = CampoDB(esmalte=esmalte, pieza_heraldica=pieza)
            s.add(campo); s.commit(); s.refresh(campo)

            for m in muebles:
                s.add(MuebleDB(campo_id=campo.id, nombre=m))
            s.commit()

            esc = EscudoDB(
                nombre=item["nombre"],
                portador=portador,
                adorno_exterior=adorno,
                campo_id=campo.id,
                provincia=item.get("provincia"),
                addimagen=item.get("imagen_src")
            )
            s.add(esc); s.commit()

if __name__ == "__main__":
    cargar()
    print("OK: catálogo cargado en la BD.")
