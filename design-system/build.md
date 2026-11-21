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
    libro.yml          (metadatos: portada, serie, etiquetas)
    capitulos/
      01-....md        (un archivo por capítulo, en orden alfabético)
      99-glosario.md
    diagramas/*.svg
    capturas/*.png
```

Un libro también puede ser un único `libro.md` con front matter (formato clásico); los dos se compilan igual. Para libros de más de un capítulo, usa la carpeta: editar un capítulo no obliga a tocar el resto.

Fuentes: si falta `fonts/`, se recrea con
`npm pack @fontsource/source-serif-4 @fontsource/inter @fontsource/jetbrains-mono`
y copiando de `files/` los pesos listados en DESIGN.md §3 (subconjunto `latin`).

## 2. Uso

```bash
python3 design-system/build.py libros/01-tema                 # -> libros/01-tema/libro.pdf (marfil)
python3 design-system/build.py libros/01-tema --paper white   # fondo blanco (máximo contraste)
python3 design-system/build.py libros/01-tema --png 1,6,8     # + PNG 1236×1648 en gris para revisar
python3 design-system/build.py libros/01-tema --anki          # + libro.anki.txt con las preguntas
python3 design-system/build.py libros/01-tema --html          # guarda el HTML intermedio
python3 design-system/check.py libros/01-tema                 # solo revisar, sin compilar
```

`build.py` ejecuta `check.py` antes de compilar e imprime avisos (`--no-check` lo desactiva). Después de compilar avisa si el PDF usó una fuente de reserva.

### Tarjetas para Anki
`--anki` exporta las preguntas de autoevaluación a `libro.anki.txt`. En Anki: *Archivo > Importar*, elige el archivo y un mazo; el separador (tabulación), el HTML y las etiquetas (`libro` + `capNN`) ya vienen indicados en el archivo.

Pasar el PDF al Kindle: correo *Send to Kindle* **sin** "convert" en el asunto (si se convierte, se pierde la maquetación) o por USB a `documents/`.

## 3. Empezar un libro nuevo

1. Copia `libros/00-muestra/` como `libros/NN-tema/`.
2. Cambia `libro.yml` (número, serie, título, etiquetas de recuadros).
3. Borra los capítulos de muestra y escribe los tuyos en `capitulos/`.
4. Compila con `--png`, resuelve los avisos y revisa las páginas en gris.

## 4. Sintaxis del Markdown

### Metadatos: `libro.yml` (o front matter de `libro.md`)

En la carpeta, `libro.yml` lleva estas claves sin las líneas `---`. En el formato clásico, van como front matter al inicio de `libro.md`.

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
1. `build.py` termina **sin avisos** (caracteres sin fuente, código largo, imágenes faltantes o pequeñas, resúmenes largos, preguntas vacías, datos sin fuentes).
2. `--png` de portada, una página con recuadros, una con captura y un resumen; mirarlas en gris.
3. Cada resumen ocupa **una** página (si no, recortar texto).
4. Las capturas se leen en el PNG de verificación; si no, recórtalas más.

## 6. Fuentes
Todo capítulo con datos actuales (cifras, plataformas, herramientas) termina con `## Fuentes` y una lista de enlaces. `check.py` avisa si un capítulo usa `:::dato` sin esa sección.
