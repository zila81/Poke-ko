#!/usr/bin/env python3
from pathlib import Path
import sys
R=Path(sys.argv[1] if len(sys.argv)>1 else ".")
h=(R/"i18n.h").read_text(encoding="utf-8"); c=(R/"i18n.cpp").read_text(encoding="utf-8"); ino=(R/"TamaPoke.ino").read_text(encoding="utf-8")
assert "LANG_PT, LANG_KO, LANG_COUNT" in h
assert "// ---------------- KO ----------------" in c
assert "u8g2_font_unifont_t_korean2" in ino
assert "tamapoke_ko_fonts.h" not in ino
assert '"이상해씨"' in ino and '"꼬부기"' in ino
print("기준선 OK: KO + korean2")
