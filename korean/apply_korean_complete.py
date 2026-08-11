#!/usr/bin/env python3
from pathlib import Path
import sys, re

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
H = ROOT / "i18n.h"
C = ROOT / "i18n.cpp"
INO = ROOT / "TamaPoke.ino"
DEX = ROOT / "dex.h"
DEXDATA = ROOT / "tools" / "dex_data.py"

for p in (H, C, INO, DEX):
    if not p.exists():
        raise SystemExit(f"파일을 찾을 수 없습니다: {p}")

def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"{label}: 예상한 원본 코드를 찾지 못했습니다.")
    return text.replace(old, new, 1)

h = H.read_text(encoding="utf-8")
h = replace_once(
    h,
    "enum Lang : uint8_t { LANG_ES = 0, LANG_EN, LANG_FR, LANG_DE, LANG_IT, LANG_PT, LANG_COUNT };",
    "enum Lang : uint8_t { LANG_ES = 0, LANG_EN, LANG_FR, LANG_DE, LANG_IT, LANG_PT, LANG_KO, LANG_COUNT };",
    "i18n.h 언어 enum"
)
h = h.replace("#define LANG_DEFAULT LANG_EN", "#define LANG_DEFAULT LANG_KO", 1)
H.write_text(h, encoding="utf-8")

c = C.read_text(encoding="utf-8")
ko_strings = r'''
  // ---------------- KO ----------------
  {
    "진화 중!", "냠냠!", "좋아해요!", "배고파요!", "목욕이 필요해요!",
    "지쳤어요...", "슬퍼 보여요...", "조금 통통해요...", "색이 다른 포켓몬!!", "행복해요",
    "고마워요! 또 만나요", "도망가 버렸어요...", "안녕! 작별 인사 중...",
    "알", "전설의 알!?", "희귀한 알!", "알을 터치하세요...", "움직였어요!", "곧 부화해요!",
    "도감 %u/151",
    "%s%s Lv.%u",
    "%s을(를) 놓아줄까요?", "예", "아니요",
    "%u 타격", "힘 +%u", "신기록!", "최고: %u", "빠르게 쳐요!",
    "점수: %u", "정말 즐거워요!", "+행복",
    "시간 설정", "시", "분", "위로 밀기: 취소", "언어",
    "메달!", "최고!", "%u일 연속!",
    "연속 %u  최고 %u", "유대", "열매 ???", "빨간 열매", "파란 열매", "초록 열매",
    "%s  %lu일째", "이름 터치: 변경",
    "배틀", "공격", "방어", "속도", "체중", "힘 훈련",
    "메달 %d/%d", "터치: 뒤로",
    "이름:", "터치하면 돌아가기",
    "먹이", "행복", "에너지", "위생",
    "최고 %u",
    "성장", "Lv.%u", "%u분 후 Lv.%u", "진화", "최종 형태",
    "진화 준비 완료!", "모든 상태를 40 이상으로",
    "%u레벨 후 진화", "실수: %u",
    "소리 켬", "소리 끔",
    "진화!", "%s이(가) 할 말이 있어요...", "%s이(가) 버려졌다고 느껴요...",
    "진화할까요?", "그대로", "작별할까요?", "작별하기", "함께 있기",
    "스타팅 포켓몬 선택",
    "스프라이트 없음", "SD 카드에 넣어주세요",
  },
'''

marker = "// Nombres de medalla"
idx = c.find(marker)
if idx < 0:
    raise SystemExit("i18n.cpp: 메달 테이블 마커를 찾지 못했습니다.")
prefix = c[:idx]
suffix = c[idx:]
end = prefix.rfind("};")
if end < 0:
    raise SystemExit("i18n.cpp: STRINGS 배열 끝을 찾지 못했습니다.")
c = prefix[:end] + ko_strings + prefix[end:] + suffix

def add_row_to_array(src, array_name, row):
    start = src.find(f"static const char *const {array_name}")
    if start < 0:
        raise SystemExit(f"{array_name} 배열을 찾지 못했습니다.")
    end = src.find("};", start)
    if end < 0:
        raise SystemExit(f"{array_name} 배열 끝을 찾지 못했습니다.")
    return src[:end] + "  " + row + "\n" + src[end:]

c = add_row_to_array(c, "MED_NAME",
    '{ "Lv.10", "Lv.25", "Lv.50", "열매", "7일 연속", "최고 유대", "최종 형태", "건강" },')
c = add_row_to_array(c, "MED_LBL",
    '{ "Lv10", "Lv25", "Lv50", "열매", "7일", "유대", "최종", "건강" },')
c = add_row_to_array(c, "MED_DSC",
    '{ "레벨 10", "레벨 25", "레벨 50", "좋아하는 열매 발견", "7일 연속", "유대 최대", "최종 형태", "최상의 컨디션" },')
C.write_text(c, encoding="utf-8")

ino = INO.read_text(encoding="utf-8")
ino = replace_once(
    ino,
    '#include "Arduino_GFX_Library.h"',
    '#include <U8g2lib.h>\n#include "Arduino_GFX_Library.h"',
    "U8g2 include"
)
helper = r'''
static int utf8len(const char *s) {
  int n = 0;
  while (*s) {
    uint8_t c = (uint8_t)*s++;
    if ((c & 0xC0) != 0x80) n++;
  }
  return n;
}
'''
anchor = "#define CX 233  // centro de la pantalla redonda"
ino = replace_once(ino, anchor, helper + "\n" + anchor, "UTF-8 길이 helper")
ino = ino.replace("strlen(", "utf8len(")
ino = replace_once(
    ino,
    'static const char *const LANG_CODES[LANG_COUNT] = { "ES", "EN", "FR", "DE", "IT", "PT" };',
    'static const char *const LANG_CODES[LANG_COUNT] = { "ES", "EN", "FR", "DE", "IT", "PT", "KO" };',
    "언어 코드"
)
begin_line = 'if (!gfx->begin(80000000)) Serial.println("gfx->begin() fallo");'
ino = replace_once(
    ino,
    begin_line,
    begin_line + '\n  gfx->setUTF8Print(true);\n  gfx->setFont(u8g2_font_unifont_t_korean2);',
    "UTF-8 폰트 초기화"
)
INO.write_text(ino, encoding="utf-8")

KO_NAMES = ["이상해씨", "이상해풀", "이상해꽃", "파이리", "리자드", "리자몽", "꼬부기", "어니부기", "거북왕", "캐터피", "단데기", "버터플", "뿔충이", "딱충이", "독침붕", "구구", "피죤", "피죤투", "꼬렛", "레트라", "깨비참", "깨비드릴조", "아보", "아보크", "피카츄", "라이츄", "모래두지", "고지", "니드런♀", "니드리나", "니드퀸", "니드런♂", "니드리노", "니드킹", "삐삐", "픽시", "식스테일", "나인테일", "푸린", "푸크린", "주뱃", "골뱃", "뚜벅쵸", "냄새꼬", "라플레시아", "파라스", "파라섹트", "콘팡", "도나리", "디그다", "닥트리오", "나옹", "페르시온", "고라파덕", "골덕", "망키", "성원숭", "가디", "윈디", "발챙이", "슈륙챙이", "강챙이", "캐이시", "윤겔라", "후딘", "알통몬", "근육몬", "괴력몬", "모다피", "우츠동", "우츠보트", "왕눈해", "독파리", "꼬마돌", "데구리", "딱구리", "포니타", "날쌩마", "야돈", "야도란", "코일", "레어코일", "파오리", "두두", "두트리오", "쥬쥬", "쥬레곤", "질퍽이", "질뻐기", "셀러", "파르셀", "고오스", "고우스트", "팬텀", "롱스톤", "슬리프", "슬리퍼", "크랩", "킹크랩", "찌리리공", "붐볼", "아라리", "나시", "탕구리", "텅구리", "시라소몬", "홍수몬", "내루미", "또가스", "또도가스", "뿔카노", "코뿌리", "럭키", "덩쿠리", "캥카", "쏘드라", "시드라", "콘치", "왕콘치", "별가사리", "아쿠스타", "마임맨", "스라크", "루주라", "에레브", "마그마", "쁘사이저", "켄타로스", "잉어킹", "갸라도스", "라프라스", "메타몽", "이브이", "샤미드", "쥬피썬", "부스터", "폴리곤", "암나이트", "암스타", "투구", "투구푸스", "프테라", "잠만보", "프리져", "썬더", "파이어", "미뇽", "신뇽", "망나뇽", "뮤츠", "뮤"]

dex = DEX.read_text(encoding="utf-8")
lines = dex.splitlines()
changed = 0
for i, name in enumerate(KO_NAMES, start=1):
    for li, line in enumerate(lines):
        if re.search(rf'//\s*{i}\b', line):
            m = re.search(r'\{\s*"[^"]*"', line)
            if m:
                repl = re.sub(r'"[^"]*"', f'"{name}"', m.group(0), count=1)
                lines[li] = line[:m.start()] + repl + line[m.end():]
                changed += 1
                break
if changed != 151:
    raise SystemExit(f"dex.h 한국어 이름 적용 실패: {changed}/151")
DEX.write_text("\n".join(lines) + "\n", encoding="utf-8")

if DEXDATA.exists():
    d = DEXDATA.read_text(encoding="utf-8")
    dl = d.splitlines()
    changed_src = 0
    for i, name in enumerate(KO_NAMES, start=1):
        pat = re.compile(rf"^(\s*\({i},\s*'[^']+',\s*)'[^']*'(,.*)$")
        for li, line in enumerate(dl):
            m = pat.match(line)
            if m:
                safe = name.replace("\\", "\\\\").replace("'", "\\'")
                dl[li] = m.group(1) + "'" + safe + "'" + m.group(2)
                changed_src += 1
                break
    if changed_src == 151:
        DEXDATA.write_text("\n".join(dl) + "\n", encoding="utf-8")
    else:
        print(f"주의: tools/dex_data.py는 {changed_src}/151개만 수정됨. dex.h는 정상 적용됨.")

print("TamaPoke 한국어 완전 패치 적용 완료")
print("UI 한국어 + 한글 폰트 + UTF-8 정렬 + 151마리 한국어 이름")
print("필요 라이브러리: U8g2")
