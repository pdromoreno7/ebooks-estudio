#!/usr/bin/env python3
"""
build.py — Markdown de estudio -> PDF (WeasyPrint) con el sistema de diseño.
Agnóstico al tema: sirve para programación, marketing, idiomas o lo que sea.

Uso:
    python3 build.py libro.md                    # -> libro.pdf (fondo marfil)
    python3 build.py libro.md -o out/x.pdf
    python3 build.py libro.md --paper white      # fondo blanco puro (máximo contraste en Kindle)
    python3 build.py libro.md --html             # guarda también el HTML intermedio (depuración)
    python3 build.py libro.md --png 1,3,8        # + PNG 1236x1648 en gris de esas páginas (pdftoppm)

Requisitos: pip install weasyprint markdown pygments pyyaml
La carpeta del sistema (este archivo, base.css, template.html, fonts/) debe ir junta.
La sintaxis del Markdown está en build.md.
"""
import argparse, html, re, subprocess, sys, unicodedata
from pathlib import Path

import markdown
import yaml
from pygments import lex
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.token import Keyword, Comment, String, Name, Number, Literal

HERE = Path(__file__).resolve().parent

# ------------------------------------------------------------------ glifos
# SVG 12x12, líneas de 1.2. Se colorean con el acento del recuadro.
GLYPH = {
    "concepto": '<path d="M6 0.8 11.2 6 6 11.2 0.8 6Z" fill="{c}"/>',
    "analogia": '<path d="M1 4h9M7.5 1.5 10 4 7.5 6.5M11 8H2M4.5 5.5 2 8l2.5 2.5" fill="none" stroke="{c}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>',
    "ojo":      '<path d="M6 1 11.3 10.8H.7Z" fill="none" stroke="{c}" stroke-width="1.2" stroke-linejoin="round"/><path d="M6 4.6v3" stroke="{c}" stroke-width="1.3" stroke-linecap="round"/><circle cx="6" cy="9.2" r=".75" fill="{c}"/>',
    "practica": '<path d="M1.2 1.6h9.6v6.6H5.4L2.8 10.6V8.2H1.2Z" fill="none" stroke="{c}" stroke-width="1.2" stroke-linejoin="round"/><path d="M3.4 4.9h5.2" stroke="{c}" stroke-width="1.1" stroke-linecap="round"/>',
    "ejemplo":  '<path d="M4 1.2C2.6 1.2 2.6 2 2.6 3.4S2.4 5.6 1.2 6c1.2.4 1.4 1.2 1.4 2.6s0 2.2 1.4 2.2M8 1.2c1.4 0 1.4.8 1.4 2.2S9.6 5.6 10.8 6c-1.2.4-1.4 1.2-1.4 2.6s0 2.2-1.4 2.2" fill="none" stroke="{c}" stroke-width="1.2" stroke-linecap="round"/>',
    "dato":     '<path d="M1.2 10.8h9.6" stroke="{c}" stroke-width="1.2" stroke-linecap="round"/><path d="M2.4 9.6V6.6h1.8v3ZM5.1 9.6V3.6h1.8v6ZM7.8 9.6V1.2h1.8v8.4Z" fill="{c}"/>',
    "resumen":  '<path d="M1.2 2.4h9.6M1.2 6h9.6M1.2 9.6h6" stroke="{c}" stroke-width="1.3" stroke-linecap="round"/>',
}
# tipo -> (etiqueta por defecto, color del glifo). La etiqueta se cambia por libro
# en el front matter (clave `recuadros`) o por bloque con etiqueta="...".
BOX = {
    "concepto": ("Concepto clave",     "#FAF7F0"),   # va sobre etiqueta invertida
    "analogia": ("Analogía",           "#4A3D78"),
    "ojo":      ("Ojo · Error común",  "#7B2D26"),
    "practica": ("En la práctica",     "#74552A"),
    "ejemplo":  ("Ejemplo",            "#1C1A17"),
    "dato":     ("Dato clave",         "#1C1A17"),
}
# nombres antiguos (libros de la serie de backend) -> tipo actual
ALIAS = {"entrevista": "practica", "nestjs": "ejemplo"}
LABELS = {}     # se llena con el front matter de cada libro
QUESTIONS = []  # (capítulo, n, título del capítulo, pregunta, respuesta HTML) para --anki
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif")

def glyph(kind, color):
    return f'<svg viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{GLYPH[kind].format(c=color)}</svg>'

def slug(s):
    s = unicodedata.normalize("NFKD", re.sub(r"<[^>]+>", "", s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def arg(args, name):
    """Lee name="valor con espacios" o name=valor de la línea de apertura de un bloque."""
    m = re.search(name + r'="([^"]*)"', args) or re.search(name + r"=(\S+)", args)
    return m.group(1) if m else ""

# ------------------------------------------------------------------ código
LANG = {"ts": "typescript", "js": "javascript", "sh": "bash", "": "text"}

def tok_class(t):
    if t in Comment: return "c"
    if t in Keyword.Type: return "t"
    if t in Keyword: return "k"
    if t in Name.Decorator: return "d"
    if t in Name.Class or t in Name.Builtin.Pseudo: return "t"
    if t in String: return "s"
    if t in Number: return "n"
    return None

def render_code(src, lang="", title="", numbers=False, hl=()):
    try:
        lexer = get_lexer_by_name(LANG.get(lang, lang), stripnl=False)
    except Exception:
        lexer = TextLexer()
    lines, cur = [], []
    for ttype, val in lex(src.rstrip("\n") + "\n", lexer):
        cls = tok_class(ttype)
        parts = val.split("\n")
        for i, part in enumerate(parts):
            if i > 0:
                lines.append("".join(cur)); cur = []
            if part:
                esc = html.escape(part)
                cur.append(f'<span class="{cls}">{esc}</span>' if cls else esc)
    if cur: lines.append("".join(cur))
    while lines and lines[-1] == "": lines.pop()
    out = []
    for n, ln in enumerate(lines, 1):
        cls = "ln hl" if n in hl else "ln"
        # sangría -> padding (sangría francesa): las líneas que se ajustan quedan alineadas
        ind = 0
        m = re.match(r"((?:<span[^>]*>)?)( +)", ln)
        if m:
            ind = len(m.group(2))
            ln = m.group(1) + ln[m.end():]
        out.append(f'<span class="{cls}" data-n="{n}"><span class="lc" style="padding-left:{ind + 2}ch">{ln or "&#8203;"}</span></span>')
    head = ""
    if title or lang:
        head = (f'<div class="code__file"><b>{html.escape(title)}</b>'
                f'<span class="lang">{html.escape(lang)}</span></div>')
    return (f'<div class="code{" numbered" if numbers else ""}">{head}'
            f'<pre>{"".join(out)}</pre></div>')

FENCE = re.compile(r"^```([\w+-]*)([^\n]*)\n(.*?)^```[ \t]*$", re.M | re.S)

# ------------------------------------------------------------------ markdown
STASH = []
def stash(h):
    STASH.append(h); return f"\n\nXSTASHX{len(STASH)-1}X\n\n"

def unstash(h):
    for _ in range(4):
        h = re.sub(r"<p>XSTASHX(\d+)X</p>", lambda m: STASH[int(m.group(1))], h)
        h = re.sub(r"XSTASHX(\d+)X", lambda m: STASH[int(m.group(1))], h)
    return h

def md(src):
    src = re.sub(r"==(.+?)==", r"<mark>\1</mark>", src)
    return markdown.markdown(src, extensions=["extra", "sane_lists", "smarty"],
                             extension_configs={"smarty": {"smart_angled_quotes": True}})

def stash_fences(src):
    def rep(m):
        lang, attrs, body = m.group(1), m.group(2), m.group(3)
        title = (re.search(r'title="([^"]*)"', attrs) or [None, ""])[1]
        numbers = bool(re.search(r"\bnumbers\b", attrs))
        hlm = re.search(r'hl="([\d,\- ]+)"', attrs)
        hl = set()
        if hlm:
            for p in hlm.group(1).split(","):
                a, _, b = p.strip().partition("-")
                hl.update(range(int(a), int(b or a) + 1))
        return stash(render_code(body, lang, title, numbers, hl))
    return FENCE.sub(rep, src)

BLOCK_OPEN = re.compile(r'^:::\s*([\w-]+)\s*(?:"([^"]*)")?\s*(.*)$')

class Chapter:
    def __init__(self): self.questions = []

def render_image(src, title, args, kind):
    """Captura o imagen rasterizada (png/jpg). ancho=70% limita el ancho."""
    if not (BASE_DIR / src).exists():
        sys.exit(f"ERROR: no encuentro la imagen {src} (ruta relativa al .md)")
    width = arg(args, "ancho")
    style = f' style="width:{width}"' if width else ""
    cap = f"<figcaption>{md_inline(title)}</figcaption>" if title else ""
    return stash(f'<figure class="shot"><img src="{html.escape(src)}" alt=""{style}>{cap}</figure>')

def render_block(kind, title, args, inner, ch):
    kind = ALIAS.get(kind, kind)
    if kind == "captura" or (kind == "figura" and arg(args, "src").lower().endswith(IMG_EXT)):
        return render_image(arg(args, "src"), title, args, kind)
    body = md_blocks(inner, ch)
    if kind == "dato":
        label = arg(args, "etiqueta") or LABELS.get(kind, BOX[kind][0])
        fig = f'<p class="dato__cifra">{md_inline(title)}</p>' if title else ""
        return stash(f'<aside class="box box--dato"><div class="box__label">{glyph(kind, BOX[kind][1])}<span>{label}</span></div>{fig}{body}</aside>')
    if kind in BOX:
        label = arg(args, "etiqueta") or LABELS.get(kind, BOX[kind][0])
        col = BOX[kind][1]
        t = f'<p class="box__title">{md_inline(title)}</p>' if title else ""
        return stash(f'<aside class="box box--{kind}"><div class="box__label">{glyph(kind, col)}<span>{label}</span></div>{t}{body}</aside>')
    if kind == "lede":
        return stash(body.replace("<p>", '<p class="lede">', 1))
    if kind == "pull":
        by = f'<span class="pull__by">{md_inline(title)}</span>' if title else ""
        inner_h = body.replace("</p>", by + "</p>", 1) if by else body
        return stash(f'<div class="pull">{inner_h}</div>')
    if kind == "pregunta":
        n = len(ch.questions) + 1
        qid = f"r-{ch.num}-{n}"
        ch.questions.append((n, qid, title, body))
        return stash(f'<div class="qa"><div class="qa__n">{n}</div><div class="qa__body">'
                     f'<div class="qa__label">Autoevaluación · {ch.num}.{n}</div>'
                     f'<p class="qa__q">{md_inline(title)}</p><div class="qa__lines"></div>'
                     f'<a class="qa__goto" href="#{qid}">Respuesta en la p. </a></div></div>')
    if kind == "resumen":
        head, sep, foot = body.partition("</ol>")
        foot = f'<div class="summary__foot">{foot}</div>' if foot.strip() else ""
        return stash(f'<section class="summary" id="resumen-{ch.num}"><div class="summary__label">{glyph("resumen", "#625C53")}<span>Resumen · Capítulo {ch.num}</span></div>'
                     f'<h2 class="no-num">{md_inline(title or "Lo esencial")}</h2>{head}{sep}{foot}</section>')
    if kind == "figura":
        src = arg(args, "src")
        svg = (BASE_DIR / src).read_text(encoding="utf-8") if src else body
        svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
        cap = f"<figcaption>{md_inline(title)}</figcaption>" if title else ""
        return stash(f'<figure class="diagram">{svg}{cap}</figure>')
    return stash(f'<div class="{kind}">{body}</div>')

def md_inline(s):
    h = md(s)
    return re.sub(r"^<p>(.*)</p>$", r"\1", h.strip(), flags=re.S)

def md_blocks(src, ch):
    """Resuelve bloques ::: (anidables) y luego Markdown."""
    lines, out, i = src.split("\n"), [], 0
    while i < len(lines):
        m = BLOCK_OPEN.match(lines[i])
        if m and m.group(1):
            depth, j, inner = 1, i + 1, []
            while j < len(lines):
                if BLOCK_OPEN.match(lines[j]) and BLOCK_OPEN.match(lines[j]).group(1): depth += 1
                elif lines[j].strip() == ":::":
                    depth -= 1
                    if depth == 0: break
                inner.append(lines[j]); j += 1
            out.append(render_block(m.group(1), m.group(2) or "", m.group(3) or "", "\n".join(inner), ch))
            i = j + 1
        else:
            out.append(lines[i]); i += 1
    return unstash(md("\n".join(out)))

# ------------------------------------------------------------------ libro
def load_source(path: Path):
    """Devuelve (meta, markdown, carpeta base).
    - Archivo .md: front matter YAML + contenido (formato clásico).
    - Carpeta: libro.yml (metadatos) + capitulos/*.md en orden alfabético
      (01-..., 02-..., 99-glosario.md). Las rutas de imágenes son relativas a la carpeta."""
    if path.is_dir():
        meta = yaml.safe_load((path / "libro.yml").read_text(encoding="utf-8")) or {}
        files = sorted((path / "capitulos").glob("*.md"))
        if not files:
            sys.exit(f"ERROR: {path}/capitulos/ no tiene archivos .md")
        raw = "\n\n".join(f.read_text(encoding="utf-8").strip() for f in files) + "\n"
        return meta, raw, path
    raw = path.read_text(encoding="utf-8")
    meta = {}
    if raw.startswith("---"):
        _, fm, raw = raw.split("---", 2)
        meta = yaml.safe_load(fm) or {}
    return meta, raw, path.parent

def build_html(src_path: Path, paper: str):
    global BASE_DIR
    meta, raw, BASE_DIR = load_source(src_path)
    md_path = src_path if src_path.is_file() else src_path / "libro"
    QUESTIONS.clear()
    LABELS.clear()
    for k, v in (meta.get("recuadros") or {}).items():
        LABELS[ALIAS.get(k, k)] = str(v)
    raw = stash_fences(raw)

    # Partir en capítulos por H1. "# Título {.apendice}" = materia final sin número.
    parts = re.split(r"^# (.+)$", raw, flags=re.M)
    body, toc = [], ['<ol>']
    chnum = 0
    for k in range(1, len(parts), 2):
        title, src = parts[k].strip(), parts[k + 1]
        apx = "{.apendice}" in title
        title = title.replace("{.apendice}", "").strip()
        ch = Chapter()
        if not apx: chnum += 1
        ch.num = chnum
        cid = ("ap-" if apx else f"cap-{chnum}-") + slug(title)
        h = md_blocks(src, ch)
        # numerar e identificar H2
        sec = [0]
        def h2(m):
            attrs, txt = m.group(1) or "", m.group(2)
            if "no-num" in attrs: return m.group(0)
            sec[0] += 1
            hid = f"{cid}-{slug(txt)}"
            if not apx:
                toc.append(f'<li class="toc-sec"><a href="#{hid}">{txt}</a></li>')
            num = "" if apx else f'<span class="h-num">{chnum}.{sec[0]}</span>'
            return f'<h2 id="{hid}"{attrs}>{num}{txt}</h2>'
        toc_ch_idx = len(toc)
        h = re.sub(r"<h2([^>]*)>(.*?)</h2>", h2, h)
        # glosario: ids en <dt> y "Ver también"
        h = re.sub(r"<dt>(.*?)</dt>", lambda m: f'<dt id="g-{slug(re.sub(r"<span.*", "", m.group(1)))}">{m.group(1)}</dt>', h)
        h = re.sub(r"<dd>\s*(?:<p>)?Ver también:\s*", '<dd class="see">', h)
        if apx:
            toc.insert(toc_ch_idx, f'<li class="toc-back"><a href="#{cid}">{title}</a></li>')
            body.append(f'<section class="backmatter" id="{cid}"><h1>{title}</h1>{h}</section>')
        else:
            toc.insert(toc_ch_idx, f'<li class="toc-ch"><a href="#{cid}"><span class="n">{chnum:02d}</span>{title}</a></li>')
            kicker = f'Capítulo {chnum}'
            opener = (f'<header class="chapter__opener"><p class="chapter__kicker">{kicker}</p>'
                      f'<div class="chapter__num">{chnum:02d}</div><h1 id="{cid}">{title}</h1>')
            # la primera .lede del capítulo va dentro de la apertura
            lm = re.match(r'\s*(<p class="lede">.*?</p>)', h, re.S)
            if lm: opener += lm.group(1); h = h[lm.end():]
            opener += "</header>"
            ans = ""
            for n, qid, q, a in ch.questions:
                QUESTIONS.append((chnum, n, title, q, a))
            if ch.questions:
                aid = f"{cid}-respuestas"
                toc.append(f'<li class="toc-sec"><a href="#{aid}">Respuestas de autoevaluación</a></li>')
                items = "".join(
                    f'<div class="answer" id="{qid}"><div class="answer__head">Respuesta {chnum}.{n}</div>'
                    f'<p class="answer__q">{md_inline(q)}</p>{a}</div>' for n, qid, q, a in ch.questions)
                ans = f'<section class="answers"><h2 id="{aid}" class="no-num">Respuestas de autoevaluación</h2>{items}</section>'
            body.append(f'<section class="chapter">{opener}{h}{ans}</section>')
    toc.append("</ol>")

    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    over = "@page { background: #FFFFFF; } :root { --paper: #FFFFFF; }" if paper == "white" else ""
    fill = {
        "lang": meta.get("lang", "es"), "titulo": meta.get("titulo", md_path.stem),
        "titulo_corto": meta.get("titulo_corto", meta.get("titulo", md_path.stem)),
        "subtitulo": meta.get("subtitulo", ""), "serie": meta.get("serie", ""),
        "libro": f'{int(meta.get("libro", 1)):02d}', "autor": meta.get("autor", ""),
        "fecha": str(meta.get("fecha", "")), "css_href": (HERE / "base.css").as_uri(),
        "css_overrides": over, "toc": "".join(toc), "body": "\n".join(body),
    }
    for k, v in fill.items():
        tpl = tpl.replace("{{" + k + "}}", str(v))
    return tpl

def write_anki(path: Path, meta: dict):
    """Preguntas de autoevaluación -> archivo de texto importable en Anki
    (Archivo > Importar; separador tabulación; HTML activado)."""
    tag_book = slug(str(meta.get("titulo_corto") or meta.get("titulo") or path.stem)).replace("-", "_")
    rows = ["#separator:tab", "#html:true", "#tags column:3"]
    clean = lambda s: re.sub(r"\s+", " ", s).replace("\t", " ").strip()
    for chnum, n, chtitle, q, a in QUESTIONS:
        tags = f"{tag_book} cap{chnum:02d}"
        rows.append(f"{clean(md_inline(q))}\t{clean(a)}\t{tags}")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Anki -> {path} ({len(QUESTIONS)} tarjetas)")

def check_fonts(pdf: Path):
    """Avisa si el PDF usa una fuente de reserva (carácter fuera del subconjunto latino)."""
    try:
        r = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True)
    except FileNotFoundError:
        return
    bad = [l.split()[0] for l in r.stdout.splitlines()[2:] if not re.search(r"Inter|SourceSerif|Source-Serif|JetBrains", l, re.I)]
    if bad:
        print(f"AVISO fuentes de reserva en el PDF: {', '.join(sorted(set(bad)))} -> ejecuta check.py para ver qué carácter las provoca")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="libro.md o carpeta del libro (libro.yml + capitulos/)")
    ap.add_argument("-o", "--out")
    ap.add_argument("--paper", choices=["ivory", "white"], default="ivory")
    ap.add_argument("--html", action="store_true")
    ap.add_argument("--png", help="páginas a exportar en gris 1236x1648, p.ej. 1,3,8")
    ap.add_argument("--anki", action="store_true", help="exporta las preguntas a <libro>.anki.txt")
    ap.add_argument("--no-check", action="store_true", help="no ejecutar check.py antes de compilar")
    a = ap.parse_args()
    src = Path(a.src).resolve()
    default_out = (src / "libro.pdf") if src.is_dir() else src.with_suffix(".pdf")
    out = Path(a.out).resolve() if a.out else default_out
    out.parent.mkdir(parents=True, exist_ok=True)
    if not a.no_check:
        sys.path.insert(0, str(HERE))
        import check
        for w in check.check(src):
            print(f"AVISO {w}")
    doc = build_html(src, a.paper)
    if a.html: out.with_suffix(".html").write_text(doc, encoding="utf-8")
    from weasyprint import HTML
    HTML(string=doc, base_url=str(BASE_DIR)).write_pdf(str(out))
    print(f"PDF -> {out}")
    check_fonts(out)
    if a.anki:
        write_anki(out.with_suffix(".anki.txt"), load_source(src)[0])
    if a.png:
        for p in a.png.split(","):
            base = out.with_name(f"{out.stem}-p{int(p):02d}")
            subprocess.run(["pdftoppm", "-f", p, "-l", p, "-gray", "-png", "-singlefile",
                            "-scale-to-x", "1236", "-scale-to-y", "1648", str(out), str(base)], check=True)
            print(f"PNG -> {base}.png")

if __name__ == "__main__":
    main()
