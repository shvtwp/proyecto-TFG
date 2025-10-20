#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import pathlib
import re
import unicodedata
from typing import Any, Dict, List, Optional, Tuple
import urllib.parse
import requests
from bs4 import BeautifulSoup, Tag

BASE = "https://es.wikipedia.org"
DEFAULT_CATEGORIA = "https://es.wikipedia.org/wiki/Categor%C3%ADa:Her%C3%A1ldica_de_Andaluc%C3%ADa"
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "catalogo_scraping.json"
DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "data"
MUEBLES_PATH = DATA_DIR / "muebles.json"
ESMALTES_PATH = DATA_DIR / "mapeo_esmaltes.json"

HEADERS = {
    "User-Agent": "TFG-Heraldica/1.0 (+github.com)",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cache-Control": "no-cache",
}

REQUIRED_ANEXOS = [
    "https://es.wikipedia.org/wiki/Anexo:Armorial_municipal_de_la_provincia_de_Granada",
]

def get_html(url: str, timeout: float = 30.0) -> str:
    r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return r.text

def _lower_no_accents(s: str) -> str:
    s = s or ""
    s = s.strip().lower()
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def _limpiar_texto(x: str) -> str:
    x = re.sub(r"\[\d+\]", "", x or "")
    x = re.sub(r"\s+", " ", x).strip()
    return x

def normalizar_portador(titulo: str) -> str:
    t = (titulo or "").strip()
    t = re.sub(r"(?i)^escudo(?:s)?\s+de\s+", "", t).strip()
    t = re.sub(r"\s*\(.*?\)\s*$", "", t).strip()
    t = unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode("ascii")
    return t

def guardar_json(items: List[Dict[str, Any]], path: pathlib.Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

def _cargar_muebles(path: pathlib.Path) -> Dict[str, List[str]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return {k: (v if isinstance(v, list) else [v]) for k, v in data.items()}

def _cargar_esmaltes(path: pathlib.Path) -> Tuple[Dict[str, str], re.Pattern]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    validos = data.get("validos", [])
    mapeo = data.get("mapeo", {})
    universe = sorted(set(list(validos) + list(mapeo.keys())), key=len, reverse=True)
    pat = re.compile("|".join(map(re.escape, universe)), re.IGNORECASE) if universe else re.compile(r"$a")
    def _map_fn(tok: str) -> str:
        t = tok.lower()
        return mapeo.get(t, t if t in validos else t)
    return (_map_fn, pat)

MUEBLES_CANON = _cargar_muebles(MUEBLES_PATH)
ESMALTE_MAP_FN, ESMALTE_RE = _cargar_esmaltes(ESMALTES_PATH)

def extraer_muebles(txt: str) -> List[str]:
    t = _lower_no_accents(txt)
    encontrados = set()
    for canon, patrones in MUEBLES_CANON.items():
        for pat in patrones:
            if re.search(pat, t, flags=re.IGNORECASE):
                encontrados.add(canon)
                break
    return sorted(encontrados)

def parsear_campos(descripcion: str) -> Tuple[Optional[str], Optional[str], List[str]]:
    desc = descripcion or ""
    esmaltes_seq: List[str] = [ESMALTE_MAP_FN(m.group(0)) for m in ESMALTE_RE.finditer(desc)]
    campo = esmaltes_seq[0] if esmaltes_seq else None
    complejo = re.search(r"(?i)\b(cuartel|cuartelado|cortado|terciado|entado|partido|tronchado|tajado|mantelado)\b", desc)
    pieza = None
    if not complejo and len(esmaltes_seq) >= 2:
        for c in esmaltes_seq[1:]:
            if c != campo:
                pieza = c
                break
    muebles = extraer_muebles(desc)
    return campo, pieza, muebles

_ANEXO_TEXT_PAT = re.compile(r"^\s*Anexo\s*:\s*Armorial\s+municipal\s+de\s+la\s+provincia\s+de\s+", re.IGNORECASE)

def _es_href_anexo(href: str) -> bool:
    if not href:
        return False
    if href.startswith("http"):
        return "/wiki/Anexo:" in href
    return href.startswith("/wiki/Anexo:")

def _enlaces_anexos_desde_categoria(url_categoria: str) -> List[str]:
    print(f"Buscando anexos en categoría: {url_categoria}")
    anexos: List[str] = []
    vistos: set[str] = set()
    url = url_categoria
    while url and url not in vistos:
        vistos.add(url)
        try:
            html = get_html(url)
        except Exception:
            html = get_html(url + ("&action=render" if "?" in url else "?action=render"))
        soup = BeautifulSoup(html, "html.parser")
        cont = soup.select_one("#mw-pages") or soup
        for a in cont.select("a[href]"):
            text = (a.get_text(" ", strip=True) or "")
            href = a.get("href", "")
            if _ANEXO_TEXT_PAT.search(text) and _es_href_anexo(href):
                full = href if href.startswith("http") else (BASE + href)
                if full not in anexos:
                    anexos.append(full)
        next_link = None
        for a in soup.select("a[href]"):
            t = (a.get_text(" ", strip=True) or "").lower()
            if t in ("siguiente página", "página siguiente", "next page"):
                h = a.get("href", "")
                next_link = h if h.startswith("http") else (BASE + h)
                break
        url = next_link
    for extra in REQUIRED_ANEXOS:
        if extra not in anexos:
            anexos.append(extra)
    seen = set()
    anexos = [u for u in anexos if not (u in seen or seen.add(u))]
    print(f"[INFO] Anexos detectados: {len(anexos)}")
    for u in anexos:
        print("  -", u)
    return anexos

def _provincia_desde_titulo(soup: BeautifulSoup, url_anexo: str) -> Optional[str]:
    h1 = soup.select_one("#firstHeading")
    if h1:
        t = h1.get_text(" ", strip=True)
        m = re.search(r"provincia\s+de\s+([^)]+)", t, flags=re.IGNORECASE)
        if m:
            prov = re.sub(r"\s*\(.*?\)\s*$", "", m.group(1).strip())
            if prov:
                return prov
    try:
        path = urllib.parse.urlparse(url_anexo).path
        slug = urllib.parse.unquote(path.rsplit("/", 1)[-1])
        m2 = re.search(r"provincia_de_(.+)$", slug, flags=re.IGNORECASE)
        if m2:
            return re.sub(r"\s*\(.*?\)\s*$", "", m2.group(1).replace("_", " ").strip())
    except Exception:
        pass
    return None

def get_img(tr: Tag) -> Optional[str]:
    """Devuelve la URL directa (src) de la imagen del escudo si existe."""
    img = tr.select_one("a.image img") or tr.find("img")
    if not img:
        return None
    src = (
        img.get("src")
        or img.get("data-src")
        or (img.get("srcset", "").split()[0] if img.get("srcset") else None)
        or (img.get("data-srcset", "").split()[0] if img.get("data-srcset") else None)
    )
    if not src:
        return None
    if src.startswith("//"):
        src = "https:" + src
    elif src.startswith("/"):
        src = BASE + src
    return src

def _parse_tablas_anexo(body: Tag, provincia: Optional[str], url_anexo: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    tablas = body.find_all("table")
    print(f"[INFO] Tablas encontradas en anexo: {len(tablas)}")
    filas_total = 0
    filas_validas = 0
    for tabla in tablas:
        contenedor = tabla.find("tbody") or tabla
        filas = contenedor.find_all("tr", recursive=False) or contenedor.find_all("tr")
        if not filas:
            continue
        for tr in filas:
            filas_total += 1
            tds = tr.find_all("td")
            if not tds:
                continue
            nombre = None
            for a in tr.find_all("a", href=True):
                txt = a.get_text(strip=True)
                if txt:
                    nombre = txt
                    break
            if not nombre:
                for td in tds:
                    cand = _limpiar_texto(td.get_text(" ", strip=True))
                    if cand:
                        cand = re.sub(r"^\s*(Escudo(?:s)? de|Armas de)\s+", "", cand, flags=re.I)
                        nombre = cand.split(".")[0].strip()
                        break
            if not nombre:
                continue
            blason = _limpiar_texto(tr.get_text(" ", strip=True))
            campo, pieza, muebles = parsear_campos(blason)
            if not campo:
                continue
            adorno = "corona" if "corona" in _lower_no_accents(blason) else None
            img_src = get_img(tr)
            out.append({
                "nombre": nombre,
                "campo": campo,
                "muebles": muebles,
                "pieza_heraldica": pieza,
                "portador": normalizar_portador(nombre),
                "adorno_exterior": adorno,
                "provincia": provincia or "",
                "imagen_src": img_src,
            })
            filas_validas += 1
    print(f"[INFO] Filas inspeccionadas (anexo): {filas_total} | Filas válidas: {filas_validas}")
    return out

def scrapear_anexo(url_anexo: str) -> List[Dict[str, Any]]:
    print(f"\nScrapeando ANEXO: {url_anexo}")
    try:
        html = get_html(url_anexo + ("&action=render" if "?" in url_anexo else "?action=render"))
        print(f"[INFO] Descargado render anexo: {len(html)} bytes")
    except Exception as e:
        print(f"[WARN] Falló action=render anexo: {e}")
        html = get_html(url_anexo)
        print(f"[INFO] Descargado anexo normal: {len(html)} bytes")
    soup = BeautifulSoup(html, "html.parser")
    body = soup.select_one("div.mw-parser-output") or soup.select_one("div#content") or soup
    if not body:
        print("[ERROR] No se encontró el cuerpo del anexo.")
        return []
    provincia = _provincia_desde_titulo(soup, url_anexo)
    resultados = _parse_tablas_anexo(body, provincia, url_anexo)
    print(f"[INFO] Total entradas en este anexo: {len(resultados)}")
    return resultados

def _key(item: Dict[str, Any]) -> str:
    return item.get("portador") or normalizar_portador(item.get("nombre", ""))

def fusionar_sin_duplicados(listas: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for lst in listas:
        for it in lst:
            k = _key(it)
            if k not in idx:
                idx[k] = it.copy()
            else:
                base = idx[k]
                for field in ("campo", "pieza_heraldica", "provincia", "imagen_archivo", "imagen_src"):
                    if not base.get(field) and it.get(field):
                        base[field] = it[field]
                m1 = set(base.get("muebles") or [])
                m2 = set(it.get("muebles") or [])
                base["muebles"] = sorted(m1 | m2) if (m1 or m2) else []
                if not base.get("adorno_exterior") and it.get("adorno_exterior"):
                    base["adorno_exterior"] = it["adorno_exterior"]
                idx[k] = base
    return list(idx.values())

def main():
    ap = argparse.ArgumentParser(description="Scraper heráldica (Wikipedia) — anexos Andalucía")
    ap.add_argument("--categoria", type=str, default=DEFAULT_CATEGORIA, help="URL de la categoría")
    ap.add_argument("--outfile", type=str, default=str(OUT), help="Ruta de salida JSON")
    args = ap.parse_args()
    anexos = _enlaces_anexos_desde_categoria(args.categoria)
    if not anexos:
        print("[WARN] No se encontraron anexos en la categoría dada.")
    lotes: List[List[Dict[str, Any]]] = []
    for url in anexos:
        lotes.append(scrapear_anexo(url))
    fusion = fusionar_sin_duplicados(lotes)
    guardar_json(fusion, pathlib.Path(args.outfile))
    print("\n--- RESUMEN ---")
    print(f"ANEXOS detectados: {len(anexos)} | TOTAL fusionado: {len(fusion)}")
    print(f"OK: guardado en {args.outfile}")

if __name__ == "__main__":
    main()
