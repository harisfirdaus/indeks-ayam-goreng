#!/usr/bin/env python3
"""Buat dist/index.html satu file: data JSON, CSS, dan JS ditanam langsung.

Dipakai untuk lingkungan yang tidak bisa memuat file terpisah (mis. Page Hark
atau dibuka langsung lewat file://). Jalankan dari root repo:

    python3 scripts/build_inline.py
"""
import base64
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "index.html").read_text(encoding="utf-8")
data = json.loads((ROOT / "data" / "ayam-goreng-34-kota-2025.json").read_text(encoding="utf-8"))

def css(m):
    return "<style>\n" + (ROOT / m.group(1)).read_text(encoding="utf-8") + "\n</style>"

def js(m):
    code = (ROOT / m.group(1)).read_text(encoding="utf-8").replace("</script", "<\\/script")
    return "<script>\n" + code + "\n</script>"

out = re.sub(r'<link rel="stylesheet" href="(vendor/[^"]+)" />', css, src)
out = re.sub(r'<script src="(vendor/[^"]+)"></script>', js, out)
def img(m):
    b64 = base64.b64encode((ROOT / m.group(1)).read_bytes()).decode()
    return 'src="data:image/jpeg;base64,' + b64 + '"'

out = re.sub(r'src="(img/[^"]+\.jpg)"', img, out)
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
marker = "    <script>\n      var DATA_URL"
assert marker in out, "penanda skrip utama tidak ditemukan"
out = out.replace(marker, "    <script>window.KOTA_DATA = " + payload + ";</script>\n" + marker, 1)

dist = ROOT / "dist"
dist.mkdir(exist_ok=True)
(dist / "index.html").write_text(out, encoding="utf-8")
print("Ditulis:", dist / "index.html", f"({len(out):,} byte)")
