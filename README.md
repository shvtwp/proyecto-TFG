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