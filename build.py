#!/usr/bin/env python3
"""
Build script for the Southern Cross German Shepherd Rescue prototype.

It stitches the editable source in ./src into a single self-contained
./preview.html, embedding the two logo variants from ./assets as data URIs
and loading the brand fonts (Cinzel, EB Garamond, Raleway) from Google Fonts.

./index.html is the hand-authored Coming Soon page and is NOT overwritten
by this script.

Usage (from the project root):
    python3 build.py

No dependencies beyond the Python standard library.
"""
import base64, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "preview.html")

def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()

def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

logo_navy = data_uri(os.path.join(ASSETS, "logo-navy.png"))
logo_cream = data_uri(os.path.join(ASSETS, "logo-cream.png"))

head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Southern Cross German Shepherd Rescue</title>
<meta name="description" content="Southern Cross German Shepherd Rescue is a foster-based nonprofit dedicated to rescuing, rehabilitating, and responsibly rehoming German Shepherds throughout Georgia and the Southeast.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Raleway:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{
  --logo-navy:url("{logo_navy}");
  --logo-cream:url("{logo_cream}");
}}
{read("css.txt")}
</style>
</head>
<body>
"""

body = "\n".join([
    read("icons.html"),
    read("page_home.html"),
    read("page_about.html"),
    read("page_foster.html"),
    read("page_adopt.html"),
    read("pages_edu_donate.html"),
    read("footer.html"),
])

html = head + body + "\n</body>\n</html>\n"
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {OUT}  ({round(os.path.getsize(OUT)/1024,1)} KB, {html.count(chr(10))} lines)")
