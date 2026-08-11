# Poke-ko

TamaPoke 한국어판 자동 빌드 + 초보자용 웹 설치 저장소입니다.

원본: https://github.com/socquique/TamaPoke

## 최종 설치 주소

GitHub Pages 배포 완료 후:

https://zila81.github.io/Poke-ko/

사용자는 PC Chrome/Edge에서 위 주소만 열면 됩니다.

1. `한국어판 설치하기`
2. `연결하고 그림 데이터 설치`
3. PWR 재시작

## 저장소에서 처음 한 번만

1. `Settings → Pages`
2. `Build and deployment → Source`를 **GitHub Actions**로 선택
3. `Actions` 탭
4. `한국어판 빌드 및 웹설치 배포`
5. `Run workflow`

## 자동 처리

- 원본 TamaPoke 다운로드
- 한국어 UI 적용
- 151마리 한국어 이름 적용
- U8g2 UTF-8 한글 폰트
- ESP32-S3 빌드
- 웹 설치용 BIN 생성
- 스프라이트 번들 생성
- GitHub Pages 자동 배포

## 하드웨어

Waveshare ESP32-S3-Touch-AMOLED-1.75 기준.

## 크레딧

비공식 팬 프로젝트입니다. 원본 코드/자산 라이선스는 socquique/TamaPoke를 따릅니다.
PMD SpriteCollab 스프라이트는 CC BY-NC입니다.
