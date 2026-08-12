#!/usr/bin/env python3
from pathlib import Path
import argparse, subprocess

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bdfconv",required=True)
    ap.add_argument("--bdf-dir",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    bd=Path(a.bdf_dir); parts=[]
    for family in ("kd","kg"):
        for px in (11,12,14):
            src=bd/f"tamapoke_{family}{px}.bdf"
            tmp=bd/f"tamapoke_{family}{px}.c"
            name=f"tamapoke_{family}{px}"
            subprocess.run([a.bdfconv,"-f","1","-n",name,"-o",str(tmp),str(src)],check=True)
            parts.append(tmp.read_text(encoding="utf-8"))
    header="#pragma once\n#include <Arduino.h>\n\n/* KD=DotumChe, KG=GulimChe; SIL OFL 1.1 */\n\n"
    Path(a.out).write_text(header+"\n\n".join(parts),encoding="utf-8")

if __name__=="__main__":
    main()
