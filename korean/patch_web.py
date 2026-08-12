#!/usr/bin/env python3
from pathlib import Path
import sys,json,re
R=Path(sys.argv[1] if len(sys.argv)>1 else ".")
P=R/"web/index.html"; M=R/"web/manifest.json"
src=P.read_text(encoding="utf-8")
SR=re.compile(r'(<script\\b[^>]*>.*?</script\\s*>)',re.I|re.S)
before=SR.findall(src); parts=SR.split(src)
pairs=[("Flash the firmware","한국어 펌웨어 설치"),("Install TamaPoke","한국어판 펌웨어 설치"),
("Load the sprites onto the microSD","포켓몬 그림 데이터 설치"),("Connect board","기기 연결"),
("Load sprites","포켓몬 그림 데이터 설치"),("How to play","설치 완료 후")]
for i in range(0,len(parts),2):
    for a,b in pairs: parts[i]=parts[i].replace(a,b)
out="".join(parts)
sim='''<section class="card" id="ko-font-simulator">
<h2>한글 폰트 시뮬레이터</h2>
<p>펌웨어 적용 전에 KD(DotumChe) / KG(GulimChe)의 TTF→BDF 변환 결과 bitmap을 픽셀 그대로 확인합니다.</p>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin:10px 0">
<label>폰트 <select id="koFamily"><option value="kd">KD · DotumChe</option><option value="kg">KG · GulimChe</option></select></label>
<label>크기 <select id="koSize"><option>11</option><option selected>12</option><option>14</option></select> px</label>
<label>화면 <select id="koPreset"><option value="basic">기본</option><option value="growth">성장</option><option value="battle">배틀</option><option value="medal">메달</option></select></label>
<label>확대 <input id="koScale" type="range" min="2" max="5" value="3"></label>
</div>
<div id="koCoverage" style="font-weight:700;margin:8px 0">폰트 데이터 확인 중...</div>
<div id="koMissing" style="font-size:.85rem;word-break:break-all;margin-bottom:8px"></div>
<canvas id="koFontCanvas" width="520" height="360" style="max-width:100%;background:#050505;border-radius:12px;border:1px solid #444"></canvas>
<p style="font-size:.85rem">이 미리보기는 브라우저 TTF가 아니라 생성된 BDF bitmap을 그립니다. 최종 실기 U8g2 검증은 별도로 필요합니다.</p>
</section>'''
if 'id="ko-font-simulator"' not in out:
    out=out.replace("</main>",sim+"\\n</main>",1) if "</main>" in out else out.replace("</body>",sim+"\\n</body>",1)
if 'src="font-sim.js"' not in out: out=out.replace("</body>",'<script src="font-sim.js"></script>\\n</body>',1)
after=SR.findall(out); pos=0
for n,orig in enumerate(before,1):
    while pos<len(after) and after[pos]!=orig: pos+=1
    if pos>=len(after): raise SystemExit(f"원본 script #{n} 변경/누락")
    pos+=1
P.write_text(out,encoding="utf-8")
d=json.loads(M.read_text(encoding="utf-8"));d["name"]="TamaPoke 한국어판";d["version"]="1.0.1"
M.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
print("원본 JS 보존 + 폰트 시뮬레이터 추가")
