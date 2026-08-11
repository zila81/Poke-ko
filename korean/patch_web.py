#!/usr/bin/env python3
from pathlib import Path
import sys,json
R=Path(sys.argv[1] if len(sys.argv)>1 else ".")
p=R/"web/index.html"; s=p.read_text(encoding="utf-8")
for a,b in [
('<html lang="en">','<html lang="ko">'),
('<h1>🐢 TamaPoke</h1>','<h1>🐢 TamaPoke 한국어판</h1>'),
('⚡ Install TamaPoke','⚡ 한국어판 설치'),
('🔌 Connect board','🔌 기기 연결'),
('⬇️ Load sprites','⬇️ 그림 데이터 설치'),
('Flash the firmware','한국어 펌웨어 설치'),
('Load the sprites onto the microSD','포켓몬 그림 데이터 설치'),
('How to play','설치 완료 후')
]: s=s.replace(a,b)
p.write_text(s,encoding="utf-8")
m=R/"web/manifest.json"; d=json.loads(m.read_text(encoding="utf-8"))
d["name"]="TamaPoke 한국어판"; v=str(d.get("version","1.4"))
if not v.endswith("-ko3"): d["version"]=v+"-ko3"
m.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("✅ 웹 설치기 표시 한국어화")
