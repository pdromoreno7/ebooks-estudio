# Sistema de diseño · Ebooks de estudio (v1.1)

Dirección **A · Cuaderno editorial**: Opennote como base (marfil, serif 400, sin sombras, estructura con bordes de 1 px, mucho aire) + la disciplina de Medium (texto primero, casi monocromo) + O'Reilly/Tufte para código, cifras y advertencias.

**Agnóstico al tema.** El sistema no sabe de qué trata el libro: sirve igual para programación, creación de contenido, idiomas o finanzas. Lo que cambia por tema son las etiquetas de los recuadros (front matter `recuadros`, ver `build.md`), no el diseño.

Lectura principal: **Kindle Paperwhite** (e-ink, 16 grises, 1236×1648 px, 3:4, ~300 ppi). Secundaria: Mac/iPhone.

**Regla madre — grayscale-first:** ningún significado depende del color. Cada componente se reconoce por *forma* (tipo de borde), *texto* (etiqueta visible) y *glifo*. El color es un acento opcional que, convertido a gris, conserva ≥ 4.5:1.

---

## 1. Página

| Token | Valor | Nota |
|---|---|---|
| Tamaño | 120 × 160 mm | 3:4 exacto, igual que la pantalla. Nada de A4. |
| Márgenes | 13 mm arriba/abajo · 10 mm lados | Arriba/abajo alojan encabezado y folio. |
| Caja de texto | 100 × 134 mm | ≈ 60–65 caracteres por línea a 10.5 pt. |
| Escala en Kindle | ×0.87 | 120 mm se muestran en ~104 mm de pantalla: 10.5 pt se ven como ~9.2 pt. Por eso nada baja de 6.4 pt en el PDF. |

Tipos de página (`@page`): `cover` (sin márgenes ni encabezados), `front` (índice, folio romano), `opener` (apertura de capítulo, sin encabezado), y la página normal con encabezado + folio.

## 2. Color

Gris equivalente (luma) entre paréntesis. Contraste medido sobre `paper`.

| Token | Hex | Gris | Contraste | Uso |
|---|---|---|---|---|
| `paper` | `#FAF7F0` | 247 | — | Fondo marfil. `--paper white` lo cambia a `#FFFFFF`. |
| `ink` | `#1C1A17` | 26 | 16.2:1 | Texto, bordes fuertes, etiqueta invertida, filete de "Dato". |
| `ink-2` | `#45403A` | 65 | 9.6:1 | Texto secundario, lede, citas, pies de figura. |
| `ink-3` | `#625C53` | 93 | 6.2:1 | Etiquetas, encabezados de página, comentarios de código. |
| `rule` | `#4F4A43` | 75 | 8.2:1 | Bordes de 1 px. Oscuro a propósito: en e-ink un gris claro de 1 px desaparece. |
| `rule-soft` | `#9A9388` | 148 | decorativo | Solo filetes internos (filas de tabla, glosario). |
| `wash` | `#EFEAE0` | 234 | — | Fondo de código, cabeceras de tabla, barra de "Ejemplo". |
| `wash-2` | `#E2DACB` | 218 | ink 12.5:1 | `<mark>` y líneas de código resaltadas. |
| `sepia` | `#74552A` | 89 | 6.4:1 | Acento de "En la práctica". |
| `oxblood` | `#7B2D26` | 66 | 8.7:1 | Acento de "Ojo / Error común". |
| `violet` | `#4A3D78` | 70 | 8.8:1 | Acento de "Analogía". |

## 3. Tipografía

Fuentes OFL, incrustadas (WOFF2 de `@fontsource`, subconjunto *latin*: cubre español). Carpeta `fonts/`.

| Familia | Pesos | Rol |
|---|---|---|
| Source Serif 4 | 400, 400 i, 600, 600 i | Títulos (**siempre 400**), cuerpo y cifras de "Dato". 600 solo para `<strong>`. |
| Inter | 400, 500, 600 | Etiquetas, encabezados de página, tablas, pies de figura. |
| JetBrains Mono | 400, 400 i, 700, 700 i | Código, nombres de archivo, atajos de teclado. |

| Estilo | Fuente / tamaño / interlineado | Detalle |
|---|---|---|
| Número de libro (portada) | Serif 400 · 64 pt | |
| Título portada | Serif 400 · 23 pt / 1.12 | |
| Número de capítulo | Serif 400 · 40 pt | "01" |
| H1 (título de capítulo) | Serif 400 · 22 pt / 1.15 | Filete de 1 px debajo. |
| Lede | Serif 400 itálica · 11.2 pt / 1.45 | `ink-2` |
| H2 | Serif 400 · 14.5 pt / 1.25 | Prefijo "1.2" en Inter 600 7.2 pt `ink-3`. |
| H3 | Serif 400 itálica · 11.5 pt | |
| H4 / etiqueta | Inter 600 · 6.8 pt · versalitas · tracking .12–.16 em | |
| Cuerpo | Serif 400 · **10.5 pt / 1.45** | Alineado a la izquierda, con guionado. |
| Cuerpo en recuadros | Serif 400 · 9.8 pt / 1.42 | |
| Cifra de "Dato" | Serif 400 · 24 pt / 1.05 | |
| Código en bloque | Mono 400 · 8.1 pt / 1.42 | ≈ 50 caracteres por línea; ajusta línea. |
| Tabla | Inter 400 · 7.9 pt / 1.38 | |
| Pie de figura | Inter 400 · 7.4 pt | |
| Encabezado / folio | Inter 500 · 6.6–7.2 pt | |
| **Mínimo absoluto** | 6.4 pt en PDF (≈ 5.6 pt en Kindle) | Solo etiquetas en mayúsculas. |

## 4. Espaciado y bordes

Escala de 4 pt: `s1 2 · s2 4 · s3 6 · s4 8 · s5 12 · s6 16 · s7 24 · s8 32` (pt).

- Párrafo: margen inferior `s4`. Recuadro: `s5` arriba y abajo, padding `s4 s5`.
- H2: `s7` arriba, `s4` abajo. H3: `s6` arriba.
- Borde estándar: **0.75 pt (1 px CSS)** en `rule` o `ink`. Fuerte: 2 pt (filete superior de "Ojo", filete izquierdo de "Dato"). Doble: 2.2 pt `double` (solo "En la práctica"). Discontinuo: 1 px `dashed` (solo "Analogía").
- Sin sombras, sin esquinas redondeadas (salvo 1.5 pt en código en línea), sin degradados.

## 5. Qué hacer y qué no

**Sí**
- Títulos en serif 400; el peso lo da el tamaño, no la negrita.
- Diferenciar por forma + etiqueta + glifo. Si tapas el color, todo debe seguir identificable.
- Bordes oscuros (`rule`/`ink`); los claros solo para separaciones internas.
- Un recuadro por idea; máximo ~2 recuadros seguidos sin prosa entre ellos.
- Figuras y capturas después del párrafo que las introduce.
- Capturas recortadas a lo que se explica (ver 6.13).

**No**
- Negrita en títulos. Mayúsculas en cuerpo. Itálica en párrafos largos (salvo lede y "En la práctica").
- Grises claros para texto (nada por encima de `ink-3`).
- Color como único rasgo (p. ej. "lo rojo es error").
- Caracteres fuera del subconjunto latino en prosa (flechas `→`, `■`, emojis): no están en las fuentes y caen en una fuente de reserva. Para símbolos, usa SVG.
- Tablas de más de 3–4 columnas: a 100 mm no caben. Divide la tabla o usa una lista.
- Capturas de pantalla completa: en 104 mm de ancho el texto queda ilegible.

---

## 6. Componentes

Sintaxis Markdown completa en `build.md`. Aquí, la especificación visual.

### 6.1 Portada
Página `cover`, marfil a sangre, marco de 1 px a 7 mm del borde. De arriba abajo: serie (Inter 600 6.8 pt versalitas) · "LIBRO" + número de dos dígitos (Serif 64 pt) · título (Serif 23 pt) · subtítulo (Serif itálica 11 pt `ink-2`) · pie con filete: autor a la izquierda, fecha a la derecha. Datos desde el *front matter*.

### 6.2 Índice
Página `front`, folio romano. Título "Índice" (Serif 18 pt) con filete. Capítulos en Serif 11 pt con número "01" en Inter; secciones H2 en Serif 9 pt `ink-2` con sangría de 7 mm; materia final en itálica. Número de página alineado a la derecha. Se genera solo.

### 6.3 Apertura de capítulo y jerarquía
Salto de página, sin encabezado, 18 mm de aire arriba. "CAPÍTULO 1" (etiqueta) → "01" (Serif 40 pt) → H1 con filete → lede opcional. Luego H2 numerados (1.1, 1.2…), H3 en itálica, H4 como etiqueta.

### 6.4 Texto
- **Párrafo**: ver tipografía.
- **Listas**: viñeta "–" en `ink-2`; numeradas con número en negrita. Sangría 5 mm.
- **Cita** (`>`): itálica `ink-2`, sangría 5 mm, sin barra lateral.
- **Pull quote**: Serif 13.5 pt centrado entre dos filetes de 1 px, atribución opcional en etiqueta.
- **Texto destacado** (`==texto==`): fondo `wash-2` + peso 600 (en e-ink el fondo solo no basta).
- **Código en línea**: Mono 0.84 em sobre `wash`.

### 6.5 Recuadros

La etiqueta de cada tipo es configurable por libro; la forma no.

| Tipo | Borde | Etiqueta por defecto | Glifo | Acento | Para qué |
|---|---|---|---|---|---|
| `concepto` | 1 px sólido `ink`, 4 lados | "Concepto clave", **invertida** | rombo relleno | — | Definiciones cortas (2–4 líneas). Título opcional. |
| `analogia` | 1 px **discontinuo** | "Analogía" | dos flechas opuestas | violet | Explicar algo nuevo con algo conocido. |
| `ojo` | **2 pt arriba** + 1 px en los demás | "Ojo · Error común" | triángulo con ! | oxblood | Errores frecuentes. Título = nombre del error. |
| `practica` | **sin laterales**, doble filete arriba y abajo | "En la práctica" | globo de diálogo | sepia | Lo que dirías o harías en la vida real. Cuerpo en itálica. |
| `ejemplo` | 1 px sólido + **barra de cabecera rellena** (`wash`) | "Ejemplo" | llaves `{ }` | — | Caso desarrollado: código, pasos o captura. Puede partirse entre páginas. |
| `dato` | **2 pt a la izquierda**, sin más bordes | "Dato clave" | barras | — | Una cifra protagonista (Serif 24 pt) + 1–2 líneas que la explican. |

Etiqueta: Inter 600 6.8 pt, versalitas, tracking .13 em, glifo SVG de 3.1 mm a la izquierda. Todos menos "Ejemplo" evitan partirse entre páginas.

Nombres antiguos aceptados: `entrevista` = `practica`, `nestjs` = `ejemplo`.

### 6.6 Bloque de código
Borde 1 px, fondo `wash`. Cabecera opcional en fondo `paper` con ruta del archivo (Inter 500/600 6.6 pt) y lenguaje a la derecha en versalitas. `pre-wrap` + `overflow-wrap: anywhere`: **nunca desborda**. Números de línea opcionales, líneas resaltadas con fondo `wash-2`.

Resaltado en grises (forma, no color): palabra reservada **negrita**, comentario *itálica* `ink-3`, decorador ***negrita itálica***, tipo/clase *itálica*, string `ink-2`.

### 6.7 Tabla comparativa
Ancho completo, Inter 7.9 pt. Cabecera sobre `wash` con filetes de 1 px `ink` arriba y abajo; filas separadas por 0.5 pt `rule-soft`; filete final 1 px `ink`. Primera columna (criterio) en 600, 21 % de ancho. Las filas no se parten. Máximo 3 columnas de contenido.

### 6.8 Diagrama (SVG)
`figure.diagram`: marco 1 px, padding 8 pt, pie de figura bajo filete fino ("**Figura 1.1** · texto").

Reglas para el SVG:
- `viewBox` de **240 de ancho** (1 u ≈ 0.39 mm a ancho completo). Texto mínimo **6.8 u**; títulos de caja 7.6 u Inter 600; nombre central en Source Serif 10.5 u.
- Trazo 1 u, tinta `#1C1A17`. Sin `<marker>`: las puntas de flecha se dibujan como `<polygon>` de 6×6.
- Rellenos solo: `#FAF7F0` (papel), `#EFEAE0` (capa), `#1C1A17` (elemento sólido).
- Diferenciar por línea: sólido = elemento propio / flujo principal; discontinuo `3 2` = externo u opcional; relleno negro = resultado o pieza central. Siempre con leyenda si hay más de dos estilos.
- Colores escritos como atributos (no clases CSS) y `font-family="Inter"` / `"Source Serif 4"`.
- Deja margen en las cajas: Inter renderiza un poco más ancho de lo que parece en el editor.

### 6.9 Entrada de glosario
Lista de definiciones. Término en Serif 11 pt + categoría en etiqueta (Inter 600 6.4 pt versalitas). Definición en Serif 9.8 pt. "VER TAMBIÉN" en etiqueta + enlaces internos en Inter 7.6 pt. El glosario va como materia final (`# Glosario {.apendice}`) y cada término recibe el ancla `#g-<termino-sin-tildes>`.

### 6.10 Tarjeta de autoevaluación
Marco 1 px con columna izquierda de 9 mm para el número (Serif 15 pt). Etiqueta "AUTOEVALUACIÓN · 1.2", pregunta en Serif 10.5 pt, dos renglones para pensar la respuesta, y "Respuesta en la p. **N**". Las respuestas se recogen solas al final del capítulo.

### 6.11 Resumen de capítulo
Siempre **una página**: marco 1 px `ink`, etiqueta "RESUMEN · CAPÍTULO N", título H2 sin número, lista numerada "01…07" con filetes finos (Serif 9.4 pt), pie opcional. Máximo ~7 puntos de 2 líneas; si no cabe, recorta texto, no tamaño.

### 6.12 Encabezado y pie
Encabezado: título corto del libro a la izquierda (Inter 500 6.6 pt versalitas `ink-3`) y título del capítulo actual a la derecha (Serif itálica 7.6 pt). Pie: folio centrado. Ocultos en portada y aperturas; folio romano en el índice.

### 6.13 Captura de pantalla (PNG / JPG)
`figure.shot`: la imagen lleva su propio marco de 1 px `rule`, centrada, ancho completo por defecto (o el que indique `ancho=`), **altura máxima 84 mm** (~60 % de la caja de texto); pie de figura igual que el diagrama.

Reglas para preparar la captura:
- **Recorta** a la zona que explica el texto: un panel, un menú, una métrica. Nunca la pantalla completa.
- Exporta a ~2× el tamaño final: para el ancho completo, **≥ 1200 px de ancho**. Más no aporta en un Kindle.
- Piensa en grises: si la captura distingue cosas solo por color (verde/rojo), señálalo en el pie o márcalo con un recuadro.
- PNG para interfaces y texto; JPG solo para fotos.
- Anotaciones (flechas, círculos): dibújalas en la imagen antes de insertarla, en negro y con trazo grueso.
- Las capturas de herramientas reales son para estudio personal: no publiques el PDF con capturas de terceros sin revisar sus condiciones.

---

## 7. Archivos

| Archivo | Rol |
|---|---|
| `base.css` | Todos los tokens y componentes. Única hoja de estilos. |
| `template.html` | Esqueleto: portada + índice + `{{body}}`. |
| `build.py` | Markdown → HTML → PDF (WeasyPrint); resaltado Pygments; índice, numeración, respuestas y capturas automáticos; exportación a Anki. |
| `check.py` | Revisión previa sin renderizar: caracteres sin fuente, código largo, imágenes, resúmenes, preguntas, fuentes. |
| `build.md` | Instalación, uso y sintaxis del Markdown. |
| `fonts/` | 12 WOFF2 + licencias OFL. |
| `../libros/00-muestra/` | Libro de muestra con todos los componentes: referencia viva y plantilla para copiar. |
