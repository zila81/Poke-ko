#!/usr/bin/env python3
from pathlib import Path
import argparse
import freetype

MANDATORY = "꼬부기이상해씨피카츄먹이행복에너지위생성장메달배틀공격방어속도체중진화"

def required_codepoints(text):
    cps={ord(ch) for ch in text if ord(ch)>127 and ch not in "\r\n\t"}
    cps.update(ord(ch) for ch in MANDATORY)
    return sorted(cps)

def px_of(s):
    y=int(round(s.y_ppem/64.0)) if s.y_ppem>64 else int(s.y_ppem)
    return y or int(s.height)

def choose(face, px):
    face.select_charmap(freetype.FT_ENCODING_UNICODE)
    sizes=list(face.available_sizes)
    hits=[(i,s) for i,s in enumerate(sizes) if px_of(s)==px or int(s.height)==px]
    if not hits:
        raise SystemExit(f"{face.family_name}: {px}px strike 없음, available={[(px_of(s),int(s.height)) for s in sizes]}")
    face.select_size(hits[0][0])

def rowhex(bm,row):
    need=max(1,(int(bm.width)+7)//8); pitch=abs(int(bm.pitch))
    b=bytes(bm.buffer)[row*pitch:row*pitch+need]
    return (b or b"\x00").hex().upper()

def make(font,out,px,cps):
    face=freetype.Face(str(font)); choose(face,px)
    flags=freetype.FT_LOAD_RENDER|freetype.FT_LOAD_TARGET_MONO
    glyphs=[]; missing=[]; maxw=1; topmax=0; botmin=0
    for cp in cps:
        if face.get_char_index(cp)==0:
            missing.append(cp); continue
        face.load_char(chr(cp),flags)
        g=face.glyph; bm=g.bitmap
        w,h=int(bm.width),int(bm.rows); left,top=int(g.bitmap_left),int(g.bitmap_top); bot=top-h
        if cp>=0xAC00 and (w==0 or h==0):
            missing.append(cp); continue
        adv=max(1,int(round(g.advance.x/64.0)))
        rows=[rowhex(bm,r) for r in range(h)] if h else ["00"]
        glyphs.append((cp,adv,max(w,1),max(h,1),left,bot,rows))
        maxw=max(maxw,w); topmax=max(topmax,top); botmin=min(botmin,bot)
    if missing:
        raise SystemExit("glyph 누락: "+" ".join(f"U+{x:04X}({chr(x)})" for x in missing[:50]))
    lines=["STARTFONT 2.1",f"FONT -PokeKO-{font.stem}-{px}-ISO10646-1",f"SIZE {px} 75 75",
           f"FONTBOUNDINGBOX {max(px,maxw)} {max(px,topmax-botmin)} 0 {botmin}",
           "STARTPROPERTIES 3",f"PIXEL_SIZE {px}",f"FONT_ASCENT {topmax}",f"FONT_DESCENT {abs(botmin)}",
           "ENDPROPERTIES",f"CHARS {len(glyphs)}"]
    for cp,adv,w,h,left,bot,rows in glyphs:
        lines += [f"STARTCHAR uni{cp:04X}",f"ENCODING {cp}",f"SWIDTH {adv*1000//px} 0",f"DWIDTH {adv} 0",
                  f"BBX {w} {h} {left} {bot}","BITMAP",*rows,"ENDCHAR"]
    lines.append("ENDFONT")
    out.write_text("\n".join(lines)+"\n",encoding="ascii")
    print(f"OK {font.stem} {px}px {len(glyphs)} glyph")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--dotum",required=True); ap.add_argument("--gulim",required=True)
    ap.add_argument("--patch-source",required=True); ap.add_argument("--out-dir",required=True)
    a=ap.parse_args()
    cps=required_codepoints(Path(a.patch_source).read_text(encoding="utf-8"))
    out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)
    for fam,font in (("kd",Path(a.dotum)),("kg",Path(a.gulim))):
        for px in (11,12,14): make(font,out/f"{fam}{px}.bdf",px,cps)

if __name__=="__main__": main()
