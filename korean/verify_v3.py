#!/usr/bin/env python3
from pathlib import Path
import sys
R=Path(sys.argv[1] if len(sys.argv)>1 else ".")
h=(R/"i18n.h").read_text(encoding="utf-8")
c=(R/"i18n.cpp").read_text(encoding="utf-8")
ino=(R/"TamaPoke.ino").read_text(encoding="utf-8")
fh=(R/"tamapoke_ko_fonts.h").read_text(encoding="utf-8")
assert "LANG_ES = 0, LANG_EN, LANG_FR, LANG_DE, LANG_IT, LANG_PT, LANG_KD, LANG_KG, LANG_COUNT" in h
assert "// ---------------- KD ----------------" in c
assert "// ---------------- KG ----------------" in c
assert '"이상해씨"' in ino and '"뮤"' in ino
for x in ("tamapoke_kd11","tamapoke_kd12","tamapoke_kd14","tamapoke_kg11","tamapoke_kg12","tamapoke_kg14"):
    assert x in fh, x
assert "LANG_KD" in ino and "LANG_KG" in ino
print("✅ Poke-ko v1.0.1 KD/KG 구조 검증 통과")
