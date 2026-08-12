#!/usr/bin/env python3
from pathlib import Path
import argparse
import freetype

def collect_chars(source_text: str):
    cps = set(range(32, 127))
    for ch in source_text:
        if ord(ch) > 127 and ch not in "\r\n\t":
            cps.add(ord(ch))
    return sorted(cps)

def strike_px(s):
    y = int(round(s.y_ppem / 64.0)) if s.y_ppem > 64 else int(s.y_ppem)
    return y if y else int(s.height)

def choose_strike(face, px):
    sizes = list(face.available_sizes)
    if not sizes:
        raise SystemExit("DotumChe.ttf에 embedded bitmap strike가 없습니다.")
    matches = [(i, s) for i, s in enumerate(sizes) if strike_px(s) == px or int(s.height) == px]
    if not matches:
        print("사용 가능한 strike:", [(strike_px(s), int(s.height)) for s in sizes])
        raise SystemExit(f"{px}px strike를 찾지 못했습니다.")
    face.select_size(matches[0][0])
    print(f"선택: {px}px strike")

def row_hex(bitmap, row):
    width = int(bitmap.width)
    need = max(1, (width + 7) // 8)
    pitch = abs(int(bitmap.pitch))
    buf = bytes(bitmap.buffer)
    start = row * pitch
    data = buf[start:start+need]
    return (data if data else b"\x00").hex().upper()

def render_bdf(ttf, out, px, cps):
    face = freetype.Face(str(ttf))
    choose_strike(face, px)
    flags = freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO

    glyphs = []
    max_w = 1
    max_top = 0
    min_bottom = 0

    for cp in cps:
        try:
            face.load_char(chr(cp), flags)
        except Exception:
            continue
        g = face.glyph
        bm = g.bitmap
        w, h = int(bm.width), int(bm.rows)
        left, top = int(g.bitmap_left), int(g.bitmap_top)
        bottom = top - h
        adv = max(1, int(round(g.advance.x / 64.0)))
        rows = [row_hex(bm, r) for r in range(h)] if h else ["00"]
        max_w = max(max_w, w)
        max_top = max(max_top, top)
        min_bottom = min(min_bottom, bottom)
        glyphs.append((cp, adv, max(w,1), max(h,1), left, bottom, rows))

    lines = [
        "STARTFONT 2.1",
        f"FONT -TamaPoke-DotumChe-Medium-R-Normal--{px}-0-0-0-M-0-ISO10646-1",
        f"SIZE {px} 75 75",
        f"FONTBOUNDINGBOX {max(px,max_w)} {max(px,max_top-min_bottom)} 0 {min_bottom}",
        "STARTPROPERTIES 3",
        f"PIXEL_SIZE {px}",
        f"FONT_ASCENT {max_top}",
        f"FONT_DESCENT {abs(min_bottom)}",
        "ENDPROPERTIES",
        f"CHARS {len(glyphs)}",
    ]
    for cp, adv, w, h, left, bottom, rows in glyphs:
        lines += [
            f"STARTCHAR uni{cp:04X}",
            f"ENCODING {cp}",
            f"SWIDTH {adv*1000//px} 0",
            f"DWIDTH {adv} 0",
            f"BBX {w} {h} {left} {bottom}",
            "BITMAP",
            *rows,
            "ENDCHAR",
        ]
    lines.append("ENDFONT")
    out.write_text("\n".join(lines)+"\n", encoding="ascii")
    print(f"{out.name}: {len(glyphs)} glyph")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dotum",required=True)
    ap.add_argument("--gulim",required=True)
    ap.add_argument("--patch-source",required=True)
    ap.add_argument("--out-dir",required=True)
    a=ap.parse_args()
    cps=collect_chars(Path(a.patch_source).read_text(encoding="utf-8"))
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)
    for family, font in (("kd",Path(a.dotum)),("kg",Path(a.gulim))):
        for px in (11,12,14):
            render_bdf(font,out/f"tamapoke_{family}{px}.bdf",px,cps)

if __name__=="__main__":
    main()
