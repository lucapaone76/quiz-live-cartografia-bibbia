"""Genera metodo-lettura-bibbia.html da metodo-lettura-bibbia.md.

La versione .md è la sorgente. La versione .html è quella che il prompt passa
all'intelligenza artificiale: alcune app (per esempio ChatGPT) non leggono le
pagine servite come text/markdown, ma leggono bene una pagina HTML semplice.

    pip install markdown
    python3 make_metodo.py
"""
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
SRC = ROOT / "metodo-lettura-bibbia.md"
OUT = ROOT / "metodo-lettura-bibbia.html"

text = SRC.read_text(encoding="utf-8")
title = text.splitlines()[0].lstrip("# ").strip()
body = markdown.markdown(text, extensions=["tables", "sane_lists"], output_format="html5")

html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Metodo cattolico per leggere un brano della Bibbia, in italiano controllato: principi, procedura in sei passi, regole per l'assistente di intelligenza artificiale.">
<style>
  body {{ font-family: Georgia, 'Times New Roman', serif; max-width: 760px; margin: 0 auto; padding: 24px 16px 48px;
         line-height: 1.55; color: #1f1a33; background: #fbfaf7; }}
  h1 {{ font-size: 1.7em; line-height: 1.2; }}
  h2 {{ margin-top: 2em; border-bottom: 1px solid #d8d2e6; padding-bottom: .2em; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; font-size: .95em; }}
  th, td {{ border: 1px solid #d8d2e6; padding: 6px 8px; text-align: left; vertical-align: top; }}
  th {{ background: #efeaf7; }}
  a {{ color: #4a1d8f; overflow-wrap: anywhere; }}
</style>
</head>
<body>
<main>
{body}
<p><small>Questa pagina è generata da <a href="metodo-lettura-bibbia.md">metodo-lettura-bibbia.md</a>.</small></p>
</main>
</body>
</html>
"""
OUT.write_text(html, encoding="utf-8")
print(f"Scritto {OUT.name} ({len(html)} caratteri)")
