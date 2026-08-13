#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
H = ROOT/"i18n.h"; C = ROOT/"i18n.cpp"; INO = ROOT/"TamaPoke.ino"
for p in (H,C,INO):
    if not p.exists(): raise SystemExit(f"필수 파일 없음: {p}")

KO_STRINGS = ['진화 중!', '냠냠!', '좋아해!', '배고파!', '목욕 필요!', '지쳤어...', '슬퍼...', '통통해...', '색이 달라!', '행복해', '고마워! 또 만나', '도망갔어...', '안녕! 잘 가...', '알', '전설의 알!?', '희귀한 알!', '알을 터치', '움직였어!', '곧 부화!', '도감 %u/151', '%s%s Lv.%u', '%s 놓기?', '예', '아니요', '%u 타', '힘 +%u', '신기록!', '최고 %u', '빠르게!', '점수 %u', '정말 즐거워!', '+행복', '시간 설정', '시', '분', '위로 밀기: 취소', '언어', '메달!', '최고!', '%u일 연속!', '연속 %u 최고 %u', '유대', '열매 ???', '빨강 열매', '파랑 열매', '초록 열매', '%s %lu일', '이름 터치: 변경', '배틀', '공격', '방어', '속도', '체중', '힘 훈련', '메달 %d/%d', '터치: 뒤로', '이름:', '터치: 뒤로', '먹이', '행복', '에너지', '위생', '최고 %u', '성장', 'Lv.%u', '%u분 후 Lv.%u', '진화', '최종 형태', '진화 준비!', '모든 상태 40 이상', '%u레벨 후 진화', '실수 %u', '소리 켬', '소리 끔', '진화!', '%s이(가) 할 말이 있어...', '%s이(가) 외로워해...', '진화할까?', '그대로', '작별할까?', '작별', '함께 있기', '스타팅 포켓몬 선택', '그림 없음', 'SD에 설치하세요']
KO_NAMES = ['이상해씨', '이상해풀', '이상해꽃', '파이리', '리자드', '리자몽', '꼬부기', '어니부기', '거북왕', '캐터피', '단데기', '버터플', '뿔충이', '딱충이', '독침붕', '구구', '피죤', '피죤투', '꼬렛', '레트라', '깨비참', '깨비드릴조', '아보', '아보크', '피카츄', '라이츄', '모래두지', '고지', '니드런♀', '니드리나', '니드퀸', '니드런♂', '니드리노', '니드킹', '삐삐', '픽시', '식스테일', '나인테일', '푸린', '푸크린', '주뱃', '골뱃', '뚜벅쵸', '냄새꼬', '라플레시아', '파라스', '파라섹트', '콘팡', '도나리', '디그다', '닥트리오', '나옹', '페르시온', '고라파덕', '골덕', '망키', '성원숭', '가디', '윈디', '발챙이', '슈륙챙이', '강챙이', '캐이시', '윤겔라', '후딘', '알통몬', '근육몬', '괴력몬', '모다피', '우츠동', '우츠보트', '왕눈해', '독파리', '꼬마돌', '데구리', '딱구리', '포니타', '날쌩마', '야돈', '야도란', '코일', '레어코일', '파오리', '두두', '두트리오', '쥬쥬', '쥬레곤', '질퍽이', '질뻐기', '셀러', '파르셀', '고오스', '고우스트', '팬텀', '롱스톤', '슬리프', '슬리퍼', '크랩', '킹크랩', '찌리리공', '붐볼', '아라리', '나시', '탕구리', '텅구리', '시라소몬', '홍수몬', '내루미', '또가스', '또도가스', '뿔카노', '코뿌리', '럭키', '덩쿠리', '캥카', '쏘드라', '시드라', '콘치', '왕콘치', '별가사리', '아쿠스타', '마임맨', '스라크', '루주라', '에레브', '마그마', '쁘사이저', '켄타로스', '잉어킹', '갸라도스', '라프라스', '메타몽', '이브이', '샤미드', '쥬피썬', '부스터', '폴리곤', '암나이트', '암스타', '투구', '투구푸스', '프테라', '잠만보', '프리져', '썬더', '파이어', '미뇽', '신뇽', '망나뇽', '뮤츠', '뮤']

def esc(s):
    return s.replace("\\","\\\\").replace('"','\\"')

def crow(items):
    return "{\n" + ",\n".join('  "'+esc(x)+'"' for x in items) + "\n}"

h = H.read_text(encoding="utf-8")
old = "enum Lang : uint8_t { LANG_ES = 0, LANG_EN, LANG_FR, LANG_DE, LANG_IT, LANG_PT, LANG_COUNT };"
new = "enum Lang : uint8_t { LANG_ES = 0, LANG_EN, LANG_FR, LANG_DE, LANG_IT, LANG_PT, LANG_KO, LANG_COUNT };"
if old not in h and new not in h: raise SystemExit("언어 enum 구조 불일치")
h = h.replace(old,new,1)
H.write_text(h,encoding="utf-8")

c = C.read_text(encoding="utf-8")
if "// ---------------- KO ----------------" not in c:
    marker = "// Nombres de medalla"
    mi = c.find(marker)
    if mi < 0: raise SystemExit("메달 마커 없음")
    before, after = c[:mi], c[mi:]
    end = before.rfind("};")
    if end < 0: raise SystemExit("STRINGS 끝 없음")
    ko = "\n// ---------------- KO ----------------\n" + crow(KO_STRINGS) + ",\n" + "// ---------------- KG ----------------\n" + crow(KO_STRINGS) + ",\n"
    c = before[:end] + ko + before[end:] + after

def append_row(src, name, vals):
    pos = src.find(f"static const char *const {name}[LANG_COUNT]")
    if pos < 0: raise SystemExit(f"{name} 없음")
    end = src.find("};",pos)
    if end < 0: raise SystemExit(f"{name} 끝 없음")
    block = src[pos:end]
    marker = "유대 최대" if name=="MED_DSC" else ("최고 유대" if name=="MED_NAME" else '"유대"')
    if marker in block: return src
    return src[:end] + crow(vals) + ",\n" + src[end:]

c = append_row(c,"MED_NAME",["Lv.10","Lv.25","Lv.50","열매","7일 연속","최고 유대","최종 형태","건강"])
c = append_row(c,"MED_LBL",["Lv10","Lv25","Lv50","열매","7일","유대","최종","건강"])
c = append_row(c,"MED_DSC",["레벨 10","레벨 25","레벨 50","열매 발견","7일 연속","유대 최대","최종 형태","최상 상태"])
C.write_text(c,encoding="utf-8")

ino = INO.read_text(encoding="utf-8")

if "#include <U8g2lib.h>" not in ino:
    needle='#include "Arduino_GFX_Library.h"'
    if needle not in ino: raise SystemExit("Arduino_GFX include 없음")
    ino=ino.replace(needle,'#include <U8g2lib.h>\n#include \"tamapoke_ko_fonts.h\"\n'+needle,1)

if "KO_POKE_NAMES[152]" not in ino:
    anchor="#define CX 233"
    p=ino.find(anchor)
    if p<0: raise SystemExit("CX 없음")
    names=[""]+KO_NAMES
    table="static const char *const KO_POKE_NAMES[152] = {\n"+",\n".join('  "'+esc(x)+'"' for x in names)+"\n};\n\n"
    helper = '''static const char *localizedPokeName(int16_t dex) {
  if (dex >= 1 && dex <= 151 && gLang == LANG_KO) return KO_POKE_NAMES[dex];
  if (dex >= 0 && dex <= DEX_COUNT) return DEX_TBL[dex].name;
  return "?";
}

static int uiTextLen(const char *s) {
  int n = 0;
  while (*s) {
    unsigned char c = (unsigned char)*s++;
    if ((c & 0xC0) != 0x80) n++;
  }
  return n;
}

static void applyLanguageFont() {
  gfx->setUTF8Print(true);
  if (gLang == LANG_KO) gfx->setFont(u8g2_font_unifont_t_korean2);
  else gfx->setFont((const GFXfont *)nullptr);
}

'''
    ino=ino[:p]+table+helper+ino[p:]

ino=ino.replace("strlen(","uiTextLen(")

for a,b in [
('{ "ES", "EN", "FR", "DE", "IT", "PT" }','{ "ES", "EN", "FR", "DE", "IT", "PT", "KO" }'),
('{"ES","EN","FR","DE","IT","PT"}','{"ES","EN","FR","DE","IT","PT","KO"}')
]:
    ino=ino.replace(a,b)

begin='if (!gfx->begin(80000000)) Serial.println("gfx->begin() fallo");'
if begin not in ino: raise SystemExit("gfx begin 없음")
if "applyLanguageFont();" not in ino[ino.find(begin):ino.find(begin)+250]:
    ino=ino.replace(begin,begin+"\n  applyLanguageFont();",1)
if "void render() {\n  applyLanguageFont();" not in ino:
    ino=ino.replace("void render() {","void render() {\n  applyLanguageFont();",1)

repls=[
("gfx->print(de.name);","gfx->print(localizedPokeName(d));"),
("drawHeader(d.name, d.accent, msg);","drawHeader(localizedPokeName(pet.speciesId), d.accent, msg);"),
("const char *base = pet.nick[0] ? pet.nick : d.name;","const char *base = pet.nick[0] ? pet.nick : localizedPokeName(pet.speciesId);"),
("T(S_RELEASE_FMT), DEX_TBL[pet.speciesId].name","T(S_RELEASE_FMT), localizedPokeName(pet.speciesId)")
]
for a,b in repls: ino=ino.replace(a,b)
ino=re.sub(r'gfx->print\(DEX_TBL\[([A-Za-z_][A-Za-z0-9_]*)\]\.name\);',r'gfx->print(localizedPokeName(\1));',ino)
ino=ino.replace("char name[28];","char name[64];").replace("char q[28];","char q[96];")
ino=re.sub(r'#define FW_VERSION "([^"]+)"',lambda m:'#define FW_VERSION "1.0.1"',ino,count=1)
ino=ino.replace('#include "tamapoke_ko_fonts.h"\\n','')
ino=ino.replace('#include "tamapoke_ko_fonts.h"','')
INO.write_text(ino,encoding="utf-8")

# 언어 코드 배열이 다른 루트 파일에 있으면 보정
for fp in list(ROOT.glob("*.cpp"))+list(ROOT.glob("*.h")):
    if fp in (C,H): continue
    s=fp.read_text(encoding="utf-8")
    ns=s.replace('{ "ES", "EN", "FR", "DE", "IT", "PT" }','{ "ES", "EN", "FR", "DE", "IT", "PT", "KO" }')
    if ns!=s: fp.write_text(ns,encoding="utf-8")

print("✅ v3 패치 적용 완료")
