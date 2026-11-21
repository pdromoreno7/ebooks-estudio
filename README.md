# Ebooks de estudio

Sistema para escribir libros de estudio en Markdown y convertirlos en PDF pensados para leer en un **Kindle Paperwhite**: páginas de 120 × 160 mm, tipografía editorial y todo legible en escala de grises.

Sirve para cualquier tema. Cada libro define las etiquetas de sus recuadros, y el diseño se mantiene.

## Qué incluye

- Portada, índice y numeración de capítulos y secciones automáticos.
- Seis recuadros: concepto clave, analogía, error común, en la práctica, ejemplo y dato clave.
- Diagramas en SVG y capturas de pantalla en PNG/JPG.
- Bloques de código con resaltado en grises.
- Preguntas de autoevaluación con las respuestas al final de cada capítulo.
- Resumen de una página por capítulo y glosario con enlaces internos.
- Revisión automática antes de compilar (`check.py`) y exportación de las preguntas a Anki.

## Uso rápido

```bash
pip install weasyprint markdown pygments pyyaml   # macOS: brew install pango
python3 design-system/build.py libros/00-muestra --png 3,7 --anki
```

Genera `libros/00-muestra/libro.pdf`, dos PNG en gris para revisar y `libro.anki.txt` con las preguntas.

Para un libro nuevo, copia `libros/00-muestra/`, edita `libro.yml` y escribe un archivo por capítulo en `capitulos/`.

## Documentación

- [`design-system/build.md`](design-system/build.md): instalación, uso y sintaxis del Markdown.
- [`design-system/DESIGN.md`](design-system/DESIGN.md): especificación visual (colores, tipografía, componentes, reglas para diagramas y capturas).

## Pasar el PDF al Kindle

Envíalo con *Send to Kindle* **sin** la palabra "convert" en el asunto (si se convierte, se pierde la maquetación), o cópialo por USB a la carpeta `documents/`.

## Licencias

Las fuentes (Source Serif 4, Inter, JetBrains Mono) son OFL; sus licencias están en `design-system/fonts/`.
