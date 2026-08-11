#!/usr/bin/env python3
from pathlib import Path
import sys, json

R = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
p = R / "web/index.html"
s = p.read_text(encoding="utf-8")

pairs = [
    ('<html lang="en">', '<html lang="ko">'),
    ('<h1>🐢 TamaPoke</h1>', '<h1>🐢 TamaPoke 한국어판</h1>'),

    ('A 151-Pokémon tamagotchi for the Waveshare ESP32-S3-Touch-AMOLED-1.75. '
     'Install it from your browser — no Arduino, no drivers.',
     'Waveshare ESP32-S3-Touch-AMOLED-1.75용 1세대 151마리 포켓몬 다마고치입니다. '
     'Arduino IDE나 복잡한 개발 도구 없이 웹에서 바로 설치할 수 있습니다.'),

    ("⚠️ Your browser doesn't support Web Serial. Use <b>Chrome</b> or <b>Edge</b> on a computer.",
     "⚠️ 현재 브라우저에서는 USB 설치를 지원하지 않습니다. "
     "PC의 <b>Chrome</b> 또는 <b>Edge</b>에서 접속해 주세요."),

    ('Flash the firmware', '한국어 펌웨어 설치'),

    ('Plug the board in via USB and press install. Pick the port and wait.',
     'TamaPoke를 USB 데이터 케이블로 PC에 연결한 뒤 아래 설치 버튼을 누르세요. '
     '장치 목록에서 ESP32-S3 포트를 선택하고 설치가 끝날 때까지 기다려 주세요.'),

    ('⚡ Install TamaPoke', '⚡ 한국어판 설치하기'),
    ('Browser not supported (use Chrome/Edge).', 'PC의 Chrome 또는 Edge가 필요합니다.'),
    ('Needs HTTPS.', '보안 연결(HTTPS)에서만 설치할 수 있습니다.'),

    ('🔄 <b>Updating to a new version?</b> Install <u>without erasing</u> to keep your Pokémon — '
     'the save lives in flash and the sprites on the microSD, so a normal install keeps both. '
     'Only a full <b>Erase</b> wipes your saved pet (the SD sprites survive even that). '
     'First time on a fresh board? You can erase, no problem.',
     '🔄 <b>기존 TamaPoke를 업데이트하나요?</b> 저장된 포켓몬을 유지하려면 '
     '<u>Erase(지우기)를 선택하지 않고</u> 설치하세요. 일반 설치는 저장 데이터와 microSD의 '
     '포켓몬 그림을 유지합니다. <b>Erase</b>를 선택하면 기기에 저장된 포켓몬 데이터가 초기화됩니다. '
     '처음 설치하는 새 기기라면 Erase를 사용해도 괜찮습니다.'),

    ('Load the sprites onto the microSD', '포켓몬 그림 데이터 설치'),

    ('Put a microSD into the board (it formats itself). Press <b>Connect board</b> and then <b>Load sprites</b>.',
     'microSD 카드를 TamaPoke에 넣으세요. 아래에서 <b>기기 연결</b>을 누른 다음 '
     '<b>포켓몬 그림 데이터 설치</b>를 누르면 필요한 그림 파일을 자동으로 전송합니다.'),

    ('🔌 Connect board', '🔌 기기 연결'),
    ('⬇️ Load sprites', '⬇️ 포켓몬 그림 데이터 설치'),
    ('Connected. Press "Load sprites".', '기기 연결 완료. 이제 "포켓몬 그림 데이터 설치"를 누르세요.'),
    ('Downloading sprite bundle (~58 MB)...', '포켓몬 그림 데이터(~58MB)를 다운로드하는 중입니다...'),
    ('Downloading bundle...', '그림 데이터를 다운로드하는 중...'),
    ('Sending files...', 'microSD로 그림 파일을 전송하는 중...'),
    ('Done!', '설치 완료!'),
    ('Failed:', '오류:'),

    ('How to play', '설치 완료 후'),
    ('Restart the board (PWR button).', '설치가 끝나면 PWR 버튼으로 TamaPoke를 재시작하세요.'),
]

for old, new in pairs:
    s = s.replace(old, new)

# 원문의 표현이 버전별로 약간 달라도 사용자에게 꼭 필요한 안내는 단계 아래에 삽입한다.
step1 = '<h2><span class="num">1</span>한국어 펌웨어 설치</h2>'
notice1 = (
    '<div class="note"><b>💾 저장 데이터 안내</b><br>'
    '기존 TamaPoke의 포켓몬을 유지하려면 설치 과정에서 <b>Erase(지우기)를 선택하지 마세요.</b> '
    '처음 설치하는 새 기기라면 초기화해도 괜찮습니다.</div>'
)
if step1 in s and notice1 not in s:
    s = s.replace(step1, step1 + "\n" + notice1, 1)

step2 = '<h2><span class="num">2</span>포켓몬 그림 데이터 설치</h2>'
notice2 = (
    '<div class="note"><b>💾 microSD 카드가 필요합니다.</b><br>'
    '펌웨어 설치가 끝난 뒤 설치 창을 닫고 진행하세요. '
    '그림 데이터 전송 중에는 USB 케이블이나 microSD 카드를 분리하지 마세요.</div>'
)
if step2 in s and notice2 not in s:
    s = s.replace(step2, step2 + "\n" + notice2, 1)

# 남아 있는 대표 영어 상태 메시지를 추가 보정.
extra = {
    "Connect the board first.": "먼저 기기를 연결하세요.",
    "Connection failed": "기기 연결에 실패했습니다.",
    "Transfer failed": "파일 전송에 실패했습니다.",
    "Restart the board": "기기를 재시작하세요",
    "files": "개 파일",
}
for old, new in extra.items():
    s = s.replace(old, new)

p.write_text(s, encoding="utf-8")

m = R / "web/manifest.json"
d = json.loads(m.read_text(encoding="utf-8"))
d["name"] = "TamaPoke 한국어판"
v = str(d.get("version", "1.4"))
# 기존 -ko3 등이 있으면 중복 suffix 방지
base = v.split("-ko")[0]
d["version"] = base + "-ko3.2"
m.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("✅ v3.2 웹 설치기 전체 한국어 안내 적용 완료")
