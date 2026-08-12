#!/usr/bin/env python3
from pathlib import Path
import sys, re

R = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
p = R/"web/index.html"
s = p.read_text(encoding="utf-8")

required = [
    "한국어 펌웨어 설치",
    "포켓몬 그림 데이터 설치",
    "기기 연결",
]
for token in required:
    if token not in s:
        raise SystemExit(f"웹 한국어 문구 누락: {token}")

# Functional elements known from the upstream installer must still exist.
# We intentionally use broad checks because exact upstream IDs can evolve.
if "<script" not in s:
    raise SystemExit("웹 설치기 script가 없습니다.")
if "navigator.serial" not in s:
    raise SystemExit("Web Serial 코드가 없습니다.")
if "sprites" not in s.lower():
    raise SystemExit("sprite 전송 코드/요소가 없습니다.")

print("✅ 웹 설치기 기능 구조 검증 통과")
