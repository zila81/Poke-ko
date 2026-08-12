#!/usr/bin/env python3
from pathlib import Path
import sys
R=Path(sys.argv[1] if len(sys.argv)>1 else "."); s=(R/"web/index.html").read_text(encoding="utf-8")
for x in ("navigator.serial","font-sim.js","ko-font-simulator","한국어 펌웨어 설치"): assert x in s,x
for f in ("font-sim.js","font-preview.json"): assert (R/"web"/f).exists(),f
print("웹/시뮬레이터 OK")
