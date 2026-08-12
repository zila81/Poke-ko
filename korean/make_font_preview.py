#!/usr/bin/env python3
from pathlib import Path
import argparse,json

def parse(path):
    L=path.read_text(encoding="ascii").splitlines(); g={}; i=0
    while i<len(L):
        if L[i].startswith("STARTCHAR "):
            enc=None; adv=0; bbx=None; rows=[]; i+=1
            while i<len(L) and L[i]!="ENDCHAR":
                x=L[i]
                if x.startswith("ENCODING "): enc=int(x.split()[1])
                elif x.startswith("DWIDTH "): adv=int(x.split()[1])
                elif x.startswith("BBX "): bbx=list(map(int,x.split()[1:5]))
                elif x=="BITMAP":
                    i+=1
                    while i<len(L) and L[i]!="ENDCHAR": rows.append(L[i]); i+=1
                    break
                i+=1
            if enc is not None and bbx: g[str(enc)]={"advance":adv,"bbx":bbx,"rows":rows}
        i+=1
    return g

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bdf-dir",required=True); ap.add_argument("--patch-source",required=True); ap.add_argument("--out",required=True)
    a=ap.parse_args(); bd=Path(a.bdf_dir)
    text=Path(a.patch_source).read_text(encoding="utf-8")
    req=sorted({ch for ch in text if ord(ch)>127 and ch not in "\r\n\t"})
    fonts={}
    for fam,name in (("kd","DotumChe"),("kg","GulimChe")):
        for px in (11,12,14):
            glyphs=parse(bd/f"{fam}{px}.bdf")
            miss=[{"char":ch,"codepoint":f"U+{ord(ch):04X}"} for ch in req if str(ord(ch)) not in glyphs]
            fonts[f"{fam}{px}"]={"family":name,"size":px,"glyphCount":len(glyphs),"missing":miss,"glyphs":glyphs}
    data={"version":"1.0.1","requiredChars":req,"fonts":fonts,
          "samples":{"basic":["이상해씨","꼬부기","피카츄","먹이 행복","에너지 위생"],
                     "growth":["성장","Lv.1","59분 후 Lv.2","Lv.15 진화","실수 0"],
                     "battle":["배틀","공격 45","방어 48","속도 47","체중 0"],
                     "medal":["메달","레벨 10","열매 발견","최고 유대","최종 형태"]}}
    Path(a.out).write_text(json.dumps(data,ensure_ascii=False,separators=(",",":")),encoding="utf-8")

if __name__=="__main__": main()
