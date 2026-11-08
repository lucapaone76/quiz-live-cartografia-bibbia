#!/usr/bin/env python3
"""Prepara le slide dal vivo (slides.html per i telefoni, regia.html per chi presenta).

    pip install markdown beautifulsoup4 qrcode
    python3 slides/make_slides.py

Legge slides/src/parte-1.md e parte-2.md (stesso formato del markdown delle slide:
"## Slide N — Titolo", poi "### Testo della slide" e "### Note per chi parla"; le altre sezioni
sono ignorate, quindi va bene anche il file completo del Project) e scrive:

    slides/deck-1.json, deck-2.json            le pagine (HTML già pronto) e i passi di animazione
    slides/deck-1-note.json, deck-2-note.json  le note per chi parla (le carica solo la regia)
    slides/deck.css                            slides.css adattato: vale solo dentro le slide
    slides/src/assets/qr-quiz-1.svg, -2.svg    QR code dei quiz
    slides/src/assets/qr-approfondisci.svg     QR code di approfondisci.html (parte 2, slide 12)

Passi di animazione: in alcune impaginazioni gli elementi compaiono uno alla volta
(schede, livelli dell'iceberg, gradini, domande della bussola, righe delle tabelle).
Per toglierli da una slide: <!-- layout: cards; steps: no -->. Per una pagina con pagebreak valgono per ogni pagina.
"""
import json
import re
import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup, NavigableString

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
SITE = "https://lucapaone76.github.io/quiz-live-cartografia-bibbia/"
DECKS = {1: ("parte-1.md", "Cartografia della Parola"), 2: ("parte-2.md", "Come approcciare il testo biblico")}

SECTION_RE = re.compile(r"(?m)^## Slide (\d+) — (.+?)\s*$")
DIRECTIVE_RE = re.compile(r"<!--\s*(layout:[^>]*?)\s*-->")
PAGEBREAK_RE = re.compile(r"<!--\s*pagebreak\s*-->")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")


# ------------------------------------------------------------------ lettura del markdown (come build.py)
def section_part(section, name):
    head = re.search(rf"(?m)^### {name}\s*$", section)
    if not head:
        return None
    rest = section[head.end():]
    stop = re.search(r"(?m)^### ", rest)
    body = rest[: stop.start()] if stop else rest
    return re.sub(r"(?m)^---\s*$", "", body).strip()


def parse_slides(text):
    matches = list(SECTION_RE.finditer(text))
    slides = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[m.end():end]
        body = section_part(section, "Testo della slide")
        if body is None:
            print(f"[avviso] slide {m.group(1)}: manca '### Testo della slide'", file=sys.stderr)
            continue
        opts = {}
        d = DIRECTIVE_RE.search(body)
        if d:
            for part in d.group(1).split(";"):
                if ":" in part:
                    k, v = part.split(":", 1)
                    opts[k.strip()] = v.strip()
            body = body.replace(d.group(0), "")
        slides.append({"n": int(m.group(1)), "title": m.group(2).strip(), "opts": opts, "body": body.strip(),
                       "notes": section_part(section, "Note per chi parla") or ""})
    return slides


def blank_before_lists(body):
    out, prev = [], ""
    for line in body.split("\n"):
        if LIST_RE.match(line) and prev.strip() and not LIST_RE.match(prev) and not prev.lstrip().startswith((">", "|", "<!--")) and not prev.startswith(" "):
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def render_md(body):
    return markdown.markdown(blank_before_lists(body), extensions=["tables", "nl2br", "sane_lists"])


def inline_svgs(soup):
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.lower().endswith(".svg") and (SRC / src).exists():
            svg = BeautifulSoup((SRC / src).read_text(encoding="utf-8"), "html.parser").find("svg")
            fig = soup.new_tag("figure", attrs={"class": "art"})
            if img.get("alt"):
                svg["aria-label"] = img["alt"]
            fig.append(svg)
            parent = img.parent
            if parent.name == "p" and len(parent.contents) == 1:
                parent.replace_with(fig)
            else:
                img.replace_with(fig)


def tidy(soup):
    for p in soup.find_all(["p", "li"]):
        if p.find_parent("blockquote"):
            continue
        first = next((c for c in p.contents if not (isinstance(c, NavigableString) and not c.strip())), None)
        if first is not None and getattr(first, "name", None) == "strong":
            nxt = first.next_sibling
            if getattr(nxt, "name", None) == "br":
                nxt.decompose()
                first["class"] = first.get("class", []) + ["lead"]
            elif p.name == "li" and isinstance(nxt, NavigableString) and nxt.startswith(":"):
                nxt.replace_with(NavigableString(nxt[1:].lstrip()))
                first["class"] = first.get("class", []) + ["lead"]


def build_compass(soup):
    ul = soup.find("ul")
    if ul is None:
        return
    wheel = soup.new_tag("div", attrs={"class": "wheel"})
    for li in ul.find_all("li", recursive=False):
        card = soup.new_tag("div", attrs={"class": "dir-card"})
        strong = li.find("strong")
        m = re.match(r"^([NESO])\s+—\s+(.*)$", strong.get_text()) if strong else None
        if m:
            badge = soup.new_tag("span", attrs={"class": "dir"})
            badge.string = m.group(1)
            card.append(badge)
            strong.string = m.group(2)
        inner = soup.new_tag("div")
        for c in list(li.contents):
            inner.append(c.extract())
        card.append(inner)
        wheel.append(card)
    centre = soup.new_tag("div", attrs={"class": "wheel-centre"})
    centre.append(BeautifulSoup((SRC / "assets/bussola.svg").read_text(encoding="utf-8"), "html.parser").find("svg"))
    wheel.append(centre)
    ul.replace_with(wheel)


def build_split(soup):
    fig = soup.find("figure", class_="art")
    if fig is None:
        return
    side = soup.new_tag("div", attrs={"class": "side"})
    for el in list(fig.next_siblings):
        if getattr(el, "name", None):
            side.append(el.extract())
    fig.insert_after(side)


# ------------------------------------------------------------------ passi di animazione
def fragments(soup, layout):
    """Restituisce gli elementi che compaiono uno alla volta, nell'ordine."""
    top = [c for c in soup.children if getattr(c, "name", None)]
    if layout in ("cards", "depth"):
        return [c for c in top if c.name in ("p", "blockquote")]
    if layout == "steps":
        ol = soup.find("ol")
        return ol.find_all("li", recursive=False) if ol else []
    if layout == "compass":
        return soup.select(".dir-card") + [c for c in top if c.name == "blockquote"]
    if layout == "pillars":
        ps = [c for c in top if c.name == "p"]
        return [c for c in top if c.name == "table"] + ps[1:2] + [c for c in top if c.name == "blockquote"]
    if layout == "table":
        return soup.select("tbody > tr")
    if layout == "split":
        side = soup.find("div", class_="side")
        return [c for c in side.children if getattr(c, "name", None)][1:] if side else []
    return []


def page_html(s, total, chunk, label):
    opts = s["opts"]
    layout = opts.get("layout", "base")
    cols = opts.get("columns")
    soup = BeautifulSoup(render_md(chunk), "html.parser")
    inline_svgs(soup)
    tidy(soup)
    if layout == "compass":
        build_compass(soup)
    if layout in ("split", "quiz"):
        build_split(soup)
    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href.startswith(SITE):                 # link al quiz: resta sul sito, stessa scheda
            a["href"] = href[len(SITE):]
        elif href.startswith("http"):
            a["target"] = "_blank"
            a["rel"] = "noopener"
    if layout == "table":                        # sul telefono ogni cella mostra il titolo della sua colonna
        for table in soup.find_all("table"):
            heads = [th.get_text(" ", strip=True) for th in table.select("thead th")]
            for tr in table.select("tbody tr"):
                for td, h in zip(tr.find_all("td"), heads):
                    if h:
                        td["data-label"] = h
    frags = [] if opts.get("steps", "").lower() in ("no", "0", "off") else fragments(soup, layout)
    for i, el in enumerate(frags, 1):
        el["class"] = el.get("class", []) + ["frag"]
        el["data-f"] = str(i)
    has_h1 = soup.find("h1") is not None
    cls = f"slide layout-{layout}" + (f" cols-{cols}" if cols else "")
    vars_ = ([f"--cols:{cols}"] if cols else []) + ([f"--fs:{opts['size']}px"] if opts.get("size") else [])
    style = f' style="{";".join(vars_)}"' if vars_ else ""
    head = "" if has_h1 else f'<h2 class="slide-title">{s["title"]}{label}</h2>'
    html = (f'<section class="{cls}" data-n="{s["n"]}"{style}>{head}<div class="body">{soup.decode()}</div>'
            f'<footer><span>Cartografia della Parola</span><span>{s["n"]} / {total}</span></footer></section>')
    return html, len(frags)


# ------------------------------------------------------------------ foglio di stile limitato alle slide
def split_top(sel):
    out, depth, cur = [], 0, ""
    for ch in sel:
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    return out + [cur]


def scope_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = css.replace("url(assets/fonts/", "url(../fonts/").replace("url(assets/contorni.svg)", "url(src/assets/contorni.svg)")
    out, i = [], 0
    while i < len(css):
        j = css.find("{", i)
        if j < 0:
            break
        sel = css[i:j].strip()
        depth, k = 1, j + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        block = css[j:k]
        i = k
        if sel.startswith("@font-face"):
            out.append(sel + block)
            continue
        if sel.startswith("@"):                    # @page, @media screen: servono solo al PDF
            continue
        sels = []
        for s in split_top(sel):
            s = s.strip()
            if s in ("html",):
                continue
            if s in (":root", "body"):
                sels.append(".deck")
            elif s == "*":
                sels.append(".deck *")
            else:
                sels.append(".deck " + s)
        if sels:
            out.append(",".join(sels) + block)
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ QR code
def make_qr():
    try:
        import qrcode
    except ImportError:
        print("[avviso] pip install qrcode per rigenerare i QR code", file=sys.stderr)
        return
    targets = {f"qr-quiz-{n}": (f"{SITE}vote.html?quiz={n}", f"QR code del quiz {n}") for n in (1, 2)}
    targets["qr-approfondisci"] = (f"{SITE}approfondisci.html", "QR code della pagina per approfondire un brano")
    for name, (url, label) in targets.items():
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2)
        q.add_data(url)
        q.make(fit=True)
        m = q.get_matrix()
        size, d = len(m), []
        for y, row in enumerate(m):
            x = 0
            while x < size:
                if row[x]:
                    s = x
                    while x < size and row[x]:
                        x += 1
                    d.append(f"M{s} {y}h{x - s}v1h-{x - s}z")
                else:
                    x += 1
        (SRC / f"assets/{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" shape-rendering="crispEdges" role="img" '
            f'aria-label="{label}"><rect width="{size}" height="{size}" fill="#ffffff"/>'
            f'<path fill="#14284b" d="{"".join(d)}"/></svg>', encoding="utf-8")


def main():
    make_qr()
    for deck, (fname, title) in DECKS.items():
        slides = parse_slides((SRC / fname).read_text(encoding="utf-8"))
        total = max(s["n"] for s in slides)
        pages, notes = [], []
        for s in slides:
            chunks = [c.strip() for c in PAGEBREAK_RE.split(s["body"]) if c.strip()]
            note_html = render_md(s["notes"]) if s["notes"] else ""
            for i, chunk in enumerate(chunks):
                label = f" ({i + 1}/{len(chunks)})" if len(chunks) > 1 else ""
                html, steps = page_html(s, total, chunk, label)
                quiz = None
                if s["opts"].get("layout") == "quiz":
                    m = re.search(r"qr-quiz-(\d)", chunk)
                    quiz = int(m.group(1)) if m else None   # layout quiz senza QR del quiz (es. pagina approfondisci)
                pages.append({"n": s["n"], "title": s["title"] + label, "steps": steps, "quiz": quiz, "html": html})
                notes.append(note_html if i == 0 else f"<p><em>(continua la slide {s['n']})</em></p>" + note_html)
        (HERE / f"deck-{deck}.json").write_text(json.dumps({"deck": deck, "title": title, "pages": pages}, ensure_ascii=False), encoding="utf-8")
        (HERE / f"deck-{deck}-note.json").write_text(json.dumps(notes, ensure_ascii=False), encoding="utf-8")
        print(f"parte {deck}: {len(slides)} slide, {len(pages)} pagine, {sum(p['steps'] for p in pages)} passi di animazione")
    (HERE / "deck.css").write_text(scope_css((SRC / "slides.css").read_text(encoding="utf-8")), encoding="utf-8")


if __name__ == "__main__":
    main()
