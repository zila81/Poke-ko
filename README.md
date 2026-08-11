# Poke-ko v3

기존 TamaPoke 6개 언어를 그대로 유지하고 한국어(KO)를 7번째로 추가합니다.

배포 성공 후 설치 주소:
https://zila81.github.io/Poke-ko/

핵심:
- ES=0, EN=1, FR=2, DE=3, IT=4, PT=5 유지
- KO=6 추가
- 기존 NVS 언어값 호환
- 영어 UI 유지
- 원본 DEX 영문 이름 유지
- KO일 때만 151마리 한국어 이름 표시
- 한국어에서 U8g2 UTF-8 Korean font 사용
- 원본 웹 설치기 동작 유지
- Actions에서 원본 무수정 빌드 → v3 빌드 → 원본 build_web.sh 순서로 검증

실기 확인 항목:
1. 설정에서 7개 언어 순환
2. EN에서 영어 UI/영문 포켓몬 이름
3. KO에서 한국어 UI/한국어 포켓몬 이름
4. 도감/스타팅/메인/해제창에서 한글 잘림 확인
