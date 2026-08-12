#!/usr/bin/env python3
from pathlib import Path
import sys, json, re, hashlib

R = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
INDEX = R / "web/index.html"
MANIFEST = R / "web/manifest.json"

original = INDEX.read_text(encoding="utf-8")

SCRIPT_RE = re.compile(r'(<script\b[^>]*>.*?</script\s*>)', re.I | re.S)

def script_blocks(text):
    return SCRIPT_RE.findall(text)

before_scripts = script_blocks(original)

# Split while retaining script blocks. Only non-script chunks are translated.
parts = SCRIPT_RE.split(original)

# IMPORTANT:
# Replacements intentionally target visible prose/text only.
# Do not include id/class/onclick/slot/disabled or other attribute fragments.
VISIBLE_REPLACEMENTS = [
    ("A 151-Pokémon tamagotchi for the Waveshare ESP32-S3-Touch-AMOLED-1.75. "
     "Install it from your browser — no Arduino, no drivers.",
     "Waveshare ESP32-S3-Touch-AMOLED-1.75용 포켓몬 육성 게임입니다. "
     "1세대 151마리를 만나고 키울 수 있으며 Arduino IDE 없이 웹에서 바로 설치할 수 있습니다."),

    ("Your browser doesn't support Web Serial. Use", "현재 브라우저에서는 USB 연결 기능을 지원하지 않습니다."),
    ("on a computer.", "PC에서 사용해 주세요."),

    ("Flash the firmware", "한국어 펌웨어 설치"),
    ("Plug the board in via USB and press install. Pick the port and wait.",
     "TamaPoke를 USB 데이터 케이블로 PC에 연결한 뒤 설치 버튼을 누르세요. "
     "목록에서 ESP32-S3 포트를 선택하고 설치가 끝날 때까지 기다려 주세요."),
    ("Install TamaPoke", "한국어판 펌웨어 설치"),
    ("Browser not supported (use Chrome/Edge).", "PC의 Chrome 또는 Edge를 사용해 주세요."),
    ("Needs HTTPS.", "보안 연결(HTTPS)에서만 설치할 수 있습니다."),

    ("Updating to a new version?", "기존 TamaPoke를 업데이트하나요?"),
    ("Install", "설치는"),
    ("without erasing", "Erase(지우기) 없이"),
    ("to keep your Pokémon", "진행하면 기존 포켓몬 저장 데이터를 유지할 수 있습니다"),
    ("the save lives in flash and the sprites on the microSD, so a normal install keeps both.",
     "저장 데이터는 기기 Flash에 있고 포켓몬 그림은 microSD에 있으므로 일반 업데이트에서는 둘 다 유지됩니다."),
    ("Only a full", "완전한"),
    ("wipes your saved pet", "를 실행하면 저장된 포켓몬 데이터가 초기화됩니다"),
    ("the SD sprites survive even that", "microSD의 그림 데이터는 유지됩니다"),
    ("First time on a fresh board? You can erase, no problem.",
     "새 기기에 처음 설치하는 경우에는 Erase를 사용해도 됩니다."),

    ("Load the sprites onto the microSD", "포켓몬 그림 데이터 설치"),

    ("Put a microSD into the board (it formats itself).",
     "microSD 카드를 TamaPoke에 넣으세요."),
    ("Press", "먼저"),
    ("and then", "을 누른 뒤"),
    ("they download and copy over USB automatically",
     "을 누르면 그림 파일을 다운로드하여 USB로 microSD에 자동 전송합니다"),
    ("(~40 MB, a few minutes). Don't remove the card.",
     "(약 40MB, 몇 분 정도 걸릴 수 있습니다). 전송 중에는 microSD 카드를 분리하지 마세요."),

    ("Close the step-1 install tab first (only one program can use the port at a time).",
     "먼저 1번 펌웨어 설치 창을 완전히 닫아 주세요. 한 번에 한 프로그램만 USB 포트를 사용할 수 있습니다."),

    ("Connect board", "기기 연결"),
    ("Load sprites", "포켓몬 그림 데이터 설치"),

    ("Have your own", "직접 준비한"),
    ("files? pick them manually.", "파일이 있나요? 직접 선택할 수 있습니다."),
    ("Want to make your own sprites? See", "직접 포켓몬 그림을 만들고 싶나요? 저장소의"),
    ("how to generate & load them", "생성 및 설치 방법"),
    ("in the repo.", "을 참고하세요."),

    ("How to play", "설치 완료 후"),
    ("Restart the board (PWR button).", "설치가 끝나면 PWR 버튼으로 TamaPoke를 재시작하세요."),
]

# Apply replacements only to non-script chunks.
for i in range(0, len(parts), 2):
    chunk = parts[i]
    for old, new in VISIBLE_REPLACEMENTS:
        chunk = chunk.replace(old, new)
    parts[i] = chunk

patched = "".join(parts)

# Add Korean help notes without altering existing element tags.
# Injection occurs immediately after closing h2 tag in non-script HTML only.
# Existing buttons and JavaScript references remain untouched.
if "기존 오리지널 TamaPoke 사용자" not in patched:
    marker = re.search(
        r'(<h2[^>]*>\s*<span[^>]*>\s*1\s*</span>\s*한국어 펌웨어 설치\s*</h2>)',
        patched, re.I
    )
    if marker:
        help1 = (
            marker.group(1) +
            '<div class="note"><b>💡 기존 오리지널 TamaPoke 사용자</b><br>'
            'microSD의 포켓몬 그림이 정상적으로 보였다면 <b>1번 펌웨어 설치만 하면 됩니다.</b> '
            '기존 저장 데이터를 유지하려면 <b>Erase(지우기)를 선택하지 마세요.</b></div>'
        )
        patched = patched[:marker.start()] + help1 + patched[marker.end():]

if "2번은 언제 필요한가요?" not in patched:
    marker = re.search(
        r'(<h2[^>]*>\s*<span[^>]*>\s*2\s*</span>\s*포켓몬 그림 데이터 설치\s*</h2>)',
        patched, re.I
    )
    if marker:
        help2 = (
            marker.group(1) +
            '<div class="note"><b>📌 2번은 언제 필요한가요?</b><br>'
            '새 기기, 새 microSD 카드 또는 포켓몬 그림이 보이지 않는 경우에 진행하세요. '
            '기존 microSD에서 그림이 정상적으로 보이면 <b>2번은 생략할 수 있습니다.</b></div>'
        )
        patched = patched[:marker.start()] + help2 + patched[marker.end():]

after_scripts = script_blocks(patched)

# Critical regression guard: script count and every script block must remain byte-identical.
if len(before_scripts) != len(after_scripts):
    raise SystemExit(
        f"❌ 웹 기능 보호 실패: script 블록 수 변경 {len(before_scripts)} -> {len(after_scripts)}"
    )

for idx, (a, b) in enumerate(zip(before_scripts, after_scripts), start=1):
    if a != b:
        ha = hashlib.sha256(a.encode("utf-8")).hexdigest()
        hb = hashlib.sha256(b.encode("utf-8")).hexdigest()
        raise SystemExit(
            f"❌ 웹 기능 보호 실패: script #{idx} 변경됨\n원본={ha}\n패치={hb}"
        )

INDEX.write_text(patched, encoding="utf-8")

m = json.loads(MANIFEST.read_text(encoding="utf-8"))
m["name"] = "TamaPoke 한국어판"
m["version"] = "1.0.1"
MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"✅ Poke-ko v1.0.1 웹 한국어화 완료")
print(f"✅ JavaScript {len(before_scripts)}개 블록 byte-for-byte 동일 확인")
print("✅ 버튼 ID/이벤트/Serial 전송 코드는 원본 유지")
