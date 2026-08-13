#!/usr/bin/env python3
from pathlib import Path
import sys
R=Path(sys.argv[1] if len(sys.argv)>1 else ".")
h=(R/"i18n.h").read_text(encoding="utf-8"); c=(R/"i18n.cpp").read_text(encoding="utf-8"); ino=(R/"TamaPoke.ino").read_text(encoding="utf-8")
assert "LANG_PT, LANG_KO, LANG_COUNT" in h
assert "// ---------------- KO ----------------" in c
assert "u8g2_font_unifont_t_korean2" in ino
if "tamapoke_ko_fonts.h" in ino:
    raise AssertionError("이전 KD/KG 커스텀 폰트 헤더 잔재가 남아 있습니다.")
assert '"이상해씨"' in ino and '"꼬부기"' in ino
print("기준선 OK: KO + korean2")
