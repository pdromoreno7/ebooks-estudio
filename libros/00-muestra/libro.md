---
libro: 0
serie: Ebooks de estudio · Muestra del sistema
titulo: Cómo se arma un libro de esta serie
titulo_corto: Muestra del sistema
subtitulo: Todos los componentes en un solo capítulo, para copiar y adaptar a cualquier tema
autor: Pedro Moreno · notas de estudio
fecha: Noviembre 2026
lang: es
recuadros:
  analogia: Analogía
  practica: En la práctica
  ejemplo: Ejemplo
  dato: Dato clave
---

# Un libro, un archivo de texto

:::lede
Cada libro es un único archivo Markdown con bloques especiales. El script lo convierte en un PDF pensado para leerse en un Kindle: páginas de 120 × 160 mm, todo legible en escala de grises.
:::

## De dónde sale el PDF

Escribes el contenido en `libro.md`. Los diagramas van en `diagramas/` como SVG y los pantallazos en `capturas/` como PNG o JPG. Luego ejecutas `build.py` y obtienes el PDF con portada, índice y numeración automáticos.

:::figura "<b>Figura 1.1</b> · Del Markdown al PDF. Las imágenes viven junto al libro y se enlazan con rutas relativas." src=diagramas/flujo.svg
:::

:::concepto "Agnóstico al tema"
El motor no sabe de qué trata el libro. Las etiquetas de los recuadros se definen en el encabezado de cada libro (clave `recuadros`), así que sirven igual para programación, marketing o idiomas.
:::

## Recuadros

Hay seis tipos. Cada uno se reconoce por su borde y su etiqueta, nunca solo por el color.

:::analogia "Como una receta de cocina"
El Markdown es la lista de ingredientes y pasos; `build.py` es quien cocina; el PDF es el plato servido. Cambias la receta, no la cocina.
:::

:::ojo "Pantallazos completos"
Una captura de la pantalla entera se vuelve ilegible en un Kindle de 6 pulgadas. Recorta solo la parte que explica la idea y, si hace falta, amplíala antes de guardarla.
:::

:::practica
«Cuando estudio un tema nuevo, primero escribo el resumen del capítulo y luego relleno las secciones. Así sé qué es lo esencial antes de escribir lo accesorio.»
:::

:::dato "60 %"
Altura máxima aproximada de una captura respecto a la caja de texto. Más alta, y la página queda sin espacio para explicarla.
:::

:::ejemplo "Un bloque de ejemplo con pasos"
1. Copia la carpeta `libros/00-muestra/` con otro nombre.
2. Cambia el encabezado: número, serie, título y etiquetas.
3. Escribe los capítulos con `#` y las secciones con `##`.
4. Ejecuta `python3 design-system/build.py libros/01-tema/libro.md`.
:::

## Capturas de pantalla

Las capturas se insertan con el bloque `:::captura`. Llevan marco fino, pie de figura y, si quieres, un ancho menor con `ancho=70%`.

:::captura "<b>Figura 1.2</b> · Panel de estadísticas de ejemplo. Recortado a las tarjetas y la gráfica que se comentan en el texto." src=capturas/panel-ejemplo.png
:::

| Elemento | Cuándo usarlo | Formato |
|---|---|---|
| Diagrama | Explicar una relación o un flujo | SVG dibujado a mano |
| Captura | Mostrar una herramienta real | PNG o JPG recortado |
| Tabla | Comparar opciones con los mismos criterios | Markdown, máx. 3 columnas |

:::pull "Idea para recordar"
Un buen libro de estudio se escribe para el lector cansado de las 10 de la noche.
:::

:::pregunta "¿Dónde se cambian las etiquetas de los recuadros?"
En el encabezado del libro, con la clave `recuadros`. También se puede cambiar una sola con `etiqueta="..."` en la línea que abre el bloque.
:::

:::pregunta "¿Por qué conviene recortar las capturas?"
Porque el Kindle muestra la página a unos 104 mm de ancho y en grises: una pantalla completa queda con textos diminutos. Recortar deja solo lo que el lector necesita ver.
:::

:::resumen "Lo esencial del sistema"
1. Un libro = un `libro.md` + carpetas `diagramas/` y `capturas/`.
2. `# ` crea un capítulo; `## ` una sección numerada.
3. Seis recuadros: concepto, analogía, ojo, práctica, ejemplo y dato.
4. Las etiquetas de los recuadros se definen por libro en `recuadros`.
5. Diagramas en SVG con `:::figura`; pantallazos con `:::captura`.
6. Las preguntas de autoevaluación llevan sus respuestas al final del capítulo.
7. Antes de dar un libro por bueno, revisa las páginas en gris con `--png`.

**Siguiente paso:** copia esta carpeta y empieza tu propio libro.
:::

# Glosario {.apendice}

Captura <span class="pos">componente</span>
: Imagen rasterizada (PNG o JPG) de una herramienta real, recortada y con pie de figura.
: Ver también: [Diagrama](#g-diagrama)

Diagrama <span class="pos">componente</span>
: Figura vectorial en SVG que explica una relación o un flujo. Se escala sin perder nitidez.
: Ver también: [Captura](#g-captura)
