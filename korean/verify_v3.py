#!/usr/bin/env python3
from pathlib import Path
import sys
R=Path(sys.argv[1] if len(sys.argv)>1 else ".")
h=(R/"i18n.h").read_text(encoding="utf-8")
c=(R/"i18n.cpp").read_text(encoding="utf-8")
ino=(R/"TamaPoke.ino").read_text(encoding="utf-8")
assert "LANG_ES = 0, LANG_EN, LANG_FR, LANG_DE, LANG_IT, LANG_PT, LANG_KO, LANG_COUNT" in h
assert "// ---------------- KO ----------------" in c
for x in ["KO_POKE_NAMES[152]","localizedPokeName","u8g2_font_unifont_t_korean2","applyLanguageFont"]:
    assert x in ino, x
assert '"이상해씨"' in ino and '"뮤"' in ino
print("✅ v3 정적 검증 통과")
