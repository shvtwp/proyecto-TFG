# Trabajo de Fin de Grado: *Heráldica para todas*
- **Autora:** Lucía González Sánchez  
- **Tutor:** Juan Julián Merelo Guervós

---

## Documentación

La documentación de este proyecto está realizada con `LaTeX`, por lo tanto para generar el archivo PDF necesitaremos compilar la memoria. Para ello es necesario tener instalado 
`Tex Live`.

Seguidamente debemos situarnos en el directorio `doc` y ejecutar:
```
pdflatex proyecto.tex
bibtex proyecto
pdflatex proyecto.tex
```

O simplemente:

```
make
```

Para comprobar la gramática de la memoria, es conveniente crear un alias con:

```
echo 'alias textidote="java -jar ~/ruta/de/textidote.jar"' >> ~/.bashrc
source ~/.bashrc
```
Una vez creado el alias, solo habría que situarse en `doc` y ejecutar:

```
textidote proyecto.tex > /ruta/para/el/report.html
```
## Pre-requisitos

- Python >= 3.10
- Poetry >= 2.0.0
- Java (para TeXtidote)
- TeX Live (para compilar documentación)

## Instalación de dependencias

Para instalar las dependencias del proyecto, primero instala Poetry si no lo tienes:

```bash
curl -sSL https://install.python-poetry.org | python -
```

Después, desde la raíz del proyecto:

```bash
poetry install
```

## Puesta en marcha

Para ejecutar la aplicación web en modo desarrollo:

```bash
poetry run flask --app heraldica/ui_web.py --debug run
```

Para desactivar el modo desarrollo simplemente hay que prescindir del ```--debug```.
La aplicación estará disponible en `http://localhost:5000`

Para cargar los datos a la base de datos:

```bash
poetry run python scripts/importar_json_db.py
```

## Lint

Para analizar y corregir el código automáticamente con Ruff:

```bash
poetry run ruff check --fix heraldica tests
```

Para formatear el código:

```bash
poetry run ruff format heraldica tests
```

## Tests

El proyecto incluye pruebas unitarias y de integración para verificar la funcionalidad.
Se ejecutan con:

```bash
poetry run pytest
```

Esto comprobará que las rutas principales y los componentes del sistema funcionan correctamente.

## Licencia
Este proyecto se distribuye bajo la licencia GPLv3, lo que permite su uso, modificación y redistribución bajo los mismos términos.
Consulta el archivo LICENSE para más detalles.