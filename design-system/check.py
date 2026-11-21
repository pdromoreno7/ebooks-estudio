#!/usr/bin/env python3
"""
check.py — revisión rápida de un libro antes de compilar (sin renderizar nada).

Uso:
    python3 check.py libros/01-tema          # carpeta (libro.yml + capitulos/)
    python3 check.py libros/00-x/libro.md    # archivo único

build.py lo ejecuta solo antes de compilar. Imprime avisos; no modifica nada.
Sale con código 1 si hay avisos (útil en CI), 0 si todo está bien.

Revisa:
  - caracteres fuera del subconjunto latino de las fuentes (flechas, emojis...)
  - líneas de código de más de 70 caracteres
  - imágenes que no existen y capturas de menos de 1200 px de ancho
  - resúmenes de más de 7 puntos o demasiado largos para una página
  - preguntas sin respuesta
  - recuadros :::dato en capítulos sin sección "## Fuentes"
"""
import re, sys
from pathlib import Path

# Cobertura del subconjunto "latin" de @fontsource (Source Serif 4, Inter, JetBrains Mono)
LATIN_RANGES = [(0x0000, 0x00FF), (0x0131, 0x0131), (0x0152, 0x0153), (0x02BB, 0x02BC),
                (0x02C6, 0x02C6), (0x02DA, 0x02DA), (0x02DC, 0x02DC), (0x0304, 0x0304),
                (0x0308, 0x0308), (0x0329, 0x0329), (0x2000, 0x206F), (0x20AC, 0x20AC),
                (0x2122, 0x2122), (0x2191, 0x2191), (0x2193, 0x2193), (0x2212, 0x2212),
                (0x2215, 0x2215), (0xFEFF, 0xFEFF), (0xFFFD, 0xFFFD)]
MAX_CODE = 70
MIN_SHOT_W = 1200
MAX_SUMMARY_ITEMS = 7
MAX_SUMMARY_WORDS = 190

def in_latin(ch):
    o = ord(ch)
    return any(a <= o <= b for a, b in LATIN_RANGES)

def sources(src: Path):
    """[(nombre, texto)] de los archivos del libro y la carpeta base."""
    if src.is_dir():
        return [(f"capitulos/{f.name}", f.read_text(encoding="utf-8"))
                for f in sorted((src / "capitulos").glob("*.md"))], src
    return [(src.name, src.read_text(encoding="utf-8"))], src.parent

def blocks(text, kind):
    """Contenido de cada bloque :::kind (sin anidar el mismo tipo)."""
    return re.findall(rf'^:::\s*{kind}\b([^\n]*)\n(.*?)^:::\s*$', text, flags=re.M | re.S)

def check(src) -> list:
    src = Path(src).resolve()
    files, base = sources(src)
    warns = []
    for name, text in files:
        lines = text.split("\n")
        # 1. caracteres fuera del subconjunto
        for i, line in enumerate(lines, 1):
            bad = sorted({c for c in line if not in_latin(c)})
            if bad:
                shown = " ".join(f"'{c}' (U+{ord(c):04X})" for c in bad)
                warns.append(f"{name}:{i} caracteres sin fuente: {shown}. Cámbialos o usa SVG.")
        # 2. código largo
        for m in re.finditer(r"^```[^\n]*\n(.*?)^```", text, flags=re.M | re.S):
            start = text[:m.start()].count("\n") + 2
            for j, cl in enumerate(m.group(1).split("\n")):
                if len(cl) > MAX_CODE:
                    warns.append(f"{name}:{start + j} línea de código de {len(cl)} caracteres (máx. {MAX_CODE}).")
        # 3. imágenes
        for i, line in enumerate(lines, 1):
            m = re.match(r'^:::\s*(figura|captura)\b.*?src=("[^"]+"|\S+)', line)
            if not m:
                continue
            rel = m.group(2).strip('"')
            p = base / rel
            if not p.exists():
                warns.append(f"{name}:{i} no existe la imagen {rel}.")
                continue
            if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
                try:
                    from PIL import Image
                    w = Image.open(p).size[0]
                    if w < MIN_SHOT_W:
                        warns.append(f"{name}:{i} {rel} mide {w} px de ancho; con menos de {MIN_SHOT_W} px se verá borrosa a ancho completo (usa ancho=60% o una captura más grande).")
                except ImportError:
                    pass
        # 4. resúmenes
        for args, body in blocks(text, "resumen"):
            items = re.findall(r"^\s*\d+\.\s", body, flags=re.M)
            words = len(re.findall(r"\w+", body))
            if len(items) > MAX_SUMMARY_ITEMS:
                warns.append(f"{name}: resumen {args.strip()} con {len(items)} puntos (máx. {MAX_SUMMARY_ITEMS}).")
            if words > MAX_SUMMARY_WORDS:
                warns.append(f"{name}: resumen {args.strip()} con {words} palabras; probablemente no cabe en una página (recorta a ~{MAX_SUMMARY_WORDS}).")
        # 5. preguntas sin respuesta
        for args, body in blocks(text, "pregunta"):
            if not body.strip():
                warns.append(f"{name}: la pregunta {args.strip()} no tiene respuesta.")
        # 6. datos sin fuentes, por capítulo
        for chap in re.split(r"^# ", text, flags=re.M)[1:]:
            title = chap.split("\n", 1)[0].strip()
            if "{.apendice}" in title:
                continue
            if re.search(r"^:::\s*dato\b", chap, flags=re.M) and not re.search(r"^##\s+Fuentes\b", chap, flags=re.M):
                warns.append(f"{name}: el capítulo «{title}» tiene recuadros :::dato pero no una sección '## Fuentes'.")
    return warns

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ws = check(sys.argv[1])
    for w in ws:
        print(f"AVISO {w}")
    print("Sin avisos." if not ws else f"{len(ws)} aviso(s).")
    sys.exit(1 if ws else 0)
