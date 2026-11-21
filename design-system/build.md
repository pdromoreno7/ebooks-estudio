# build.md · Cómo generar un ebook

## 1. Instalación (una vez)

```bash
pip install weasyprint markdown pygments pyyaml     # en Linux: --break-system-packages
# macOS: brew install pango   (WeasyPrint lo necesita)
# opcional, para PNG de verificación: poppler (pdftoppm)
```

Estructura del repo (rutas relativas):

```
design-system/
  base.css  template.html  build.py  DESIGN.md  build.md
  fonts/    (12 .woff2 de @fontsource + licencias OFL)
libros/
  00-muestra/
    libro.md
    diagramas/*.svg
    capturas/*.png
  01-<tema>/
    libro.md
    ...
```

Fuentes: si falta `fonts/`, se recrea con
`npm pack @fontsource/source-serif-4 @fontsource/inter @fontsource/jetbrains-mono`
y copiando de `files/` los pesos listados en DESIGN.md §3 (subconjunto `latin`).

## 2. Uso

```bash
python3 design-system/build.py libros/01-tema/libro.md                 # -> libro.pdf (marfil)
python3 design-system/build.py libro.md -o out/01.pdf --paper white    # fondo blanco (máximo contraste)
python3 design-system/build.py libro.md --html                         # guarda el HTML intermedio
python3 design-system/build.py libro.md --png 1,6,8                    # + PNG 1236×1648 en gris para revisar
```

Pasar el PDF al Kindle: correo *Send to Kindle* **sin** "convert" en el asunto (si se convierte, se pierde la maquetación) o por USB a `documents/`.

## 3. Empezar un libro nuevo

1. Copia `libros/00-muestra/` como `libros/NN-tema/`.
2. Cambia el front matter (número, serie, título, etiquetas de recuadros).
3. Borra el contenido de muestra y escribe el tuyo.
4. Compila con `--png` y revisa las páginas en gris.

## 4. Sintaxis del Markdown

### Front matter (portada, encabezados y etiquetas)

```yaml
---
libro: 1
serie: Serie de estudio · Creación de contenido
titulo: Cómo funciona el algoritmo de YouTube
titulo_corto: Algoritmo de YouTube     # encabezado de página
subtitulo: Qué mide, qué premia y qué puedes controlar
autor: Pedro Moreno · notas de estudio
fecha: Noviembre 2026
lang: es
recuadros:                             # opcional: etiquetas de este libro
  analogia: Analogía
  practica: En la práctica
  ejemplo: Caso real
  dato: Dato clave
---
```

Si no defines `recuadros`, se usan las etiquetas por defecto (DESIGN.md §6.5). Las que no menciones conservan su valor por defecto.

### Estructura
- `# Título` = **capítulo** (salto de página, número automático, entra al índice).
- `# Glosario {.apendice}` = materia final sin número.
- `## …` = sección numerada (1.1, 1.2) y en el índice. `### …` subsección. `#### …` etiqueta.

### Bloques `:::`
Se abren con `:::tipo "Título opcional"` y se cierran con `:::` sola. Se pueden anidar (código o captura dentro de un recuadro). Cualquier recuadro acepta `etiqueta="Otra etiqueta"` para cambiar la suya solo en ese bloque.

| Bloque | Resultado |
|---|---|
| `:::lede` | Entradilla en itálica (la primera del capítulo va en la apertura). |
| `:::concepto "Término"` | Concepto clave. |
| `:::analogia "Título"` | Analogía. |
| `:::ojo "Nombre del error"` | Ojo / Error común. |
| `:::practica` | En la práctica (primera persona, entre «»). Alias: `:::entrevista`. |
| `:::ejemplo "Título opcional"` | Caso desarrollado: prosa, pasos, código o captura. Alias: `:::nestjs`. |
| `:::dato "4,5 %"` | Cifra grande + 1–2 líneas que la explican. |
| `:::pull "Atribución"` | Pull quote. |
| `:::figura "<b>Figura 1.1</b> · Pie" src=diagramas/x.svg` + `:::` | Diagrama SVG incrustado. |
| `:::captura "<b>Figura 1.2</b> · Pie" src=capturas/x.png` + `:::` | Pantallazo PNG/JPG con marco. Opcional: `ancho=70%`. |
| `:::pregunta "¿Pregunta?"` … respuesta … `:::` | Tarjeta de autoevaluación; la respuesta se mueve al final del capítulo. |
| `:::resumen "Título"` + lista numerada + párrafo opcional | Resumen de 1 página (el párrafo tras la lista va al pie). |

`:::figura` con un `src` que termine en `.png`/`.jpg` se trata como captura.

### Texto
- `==texto==` → destacado. `**negrita**`, `*itálica*`, `` `código` ``.
- `> cita` → cita normal.
- Tablas Markdown estándar (máx. 3 columnas de contenido).

### Código

````markdown
```ts title="src/pedidos/pedidos.module.ts" numbers hl="3,6-7"
...
```
````
- `title` → cabecera con ruta. `numbers` → números de línea. `hl` → líneas resaltadas.
- Lenguajes: cualquiera de Pygments (`ts`, `js`, `bash`, `json`, `sql`, `yaml`, `python`…).

### Glosario

```markdown
Retención <span class="pos">métrica</span>
: Definición.
: Ver también: [CTR](#g-ctr), [Tiempo de visualización](#g-tiempo-de-visualizacion)
```
Ancla de cada término: `#g-` + término en minúsculas, sin tildes, con guiones.

## 5. Checklist antes de dar por bueno un libro
1. `--png` de portada, una página con recuadros, una con captura y el resumen; mirarlas en gris.
2. El resumen ocupa **una** página (si no, recortar texto).
3. `pdffonts libro.pdf` no muestra `DejaVu` (si aparece, hay un carácter fuera del subconjunto: cámbialo o usa SVG).
4. Ninguna línea de código pasa de ~70 caracteres.
5. Las capturas se leen en el PNG de verificación; si no, recórtalas más.
