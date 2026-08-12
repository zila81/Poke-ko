# Poke-ko v1.0.1

TamaPoke의 기존 기능과 6개 언어를 유지하면서 **한국어를 추가한 비공식 한국어판**입니다.

원본 프로젝트: `socquique/TamaPoke`  
한국어판 저장소: `zila81/Poke-ko`

웹 설치 페이지:

**https://zila81.github.io/Poke-ko/**

> 지원 하드웨어: **Waveshare ESP32-S3-Touch-AMOLED-1.75**

---

## 주요 기능

Poke-ko는 원본 TamaPoke를 별도로 설치한 뒤 패치를 덧씌우는 방식이 아닙니다.

GitHub Actions가 최신 TamaPoke 원본 소스를 가져와 한국어 기능을 적용한 후,
**한국어가 포함된 완성 펌웨어를 새로 빌드**합니다.

포함 기능:

- 원본 TamaPoke 게임 기능 유지
- 기존 6개 언어 유지
  - ES
  - EN
  - FR
  - DE
  - IT
  - PT
- 한국어 2종 추가
  - KD — DotumChe
  - KG — GulimChe
- 1세대 151마리 한국어 이름
- UTF-8 한글 출력
- 작은 AMOLED 화면에 맞춘 11 / 12 / 14px 한글 bitmap 폰트
- 웹 브라우저 원클릭 펌웨어 설치
- microSD 포켓몬 그림 데이터 설치
- 기존 TamaPoke 저장 데이터 유지 업데이트 지원

---

## 언어 선택

언어 순서는 다음과 같습니다.

```text
ES → EN → FR → DE → IT → PT → KD → KG
```

기존 원본 언어 번호는 변경하지 않습니다.

```text
ES = 0
EN = 1
FR = 2
DE = 3
IT = 4
PT = 5
KD = 6
KG = 7
```

따라서 기존 TamaPoke에서 저장되어 있던 언어 설정과의 호환성을 최대한 유지합니다.

### KD와 KG의 차이

두 모드는 번역 내용과 포켓몬 이름이 완전히 같습니다.

차이는 **한글 폰트**뿐입니다.

| 모드 | 한글 폰트 |
| --- | --- |
| KD | DotumChe |
| KG | GulimChe |

실제 AMOLED 화면에서 KD와 KG를 바로 전환하면서 가독성을 비교할 수 있도록
v1.0.1에서는 두 폰트를 모두 포함했습니다.

---

## 한글 폰트 크기

원본 TamaPoke는 Arduino_GFX 기본 폰트와 `setTextSize()`를 사용합니다.

Poke-ko에서는 원본이 지정한 글씨 크기 단계에 따라 한국어 bitmap 폰트를 자동으로 선택합니다.

| 원본 UI | 한국어 |
| --- | --- |
| `textSize(1)` 작은 글씨 | 11px |
| `textSize(2)` 일반 글씨 | 12px |
| `textSize(3+)` 큰 글씨 | 14px |

KD와 KG 모두 동일한 크기 체계를 사용합니다.

폰트 원본은 GitHub 저장소에 직접 포함하지 않고,
GitHub Actions 빌드 과정에서 Google Fonts의 Gulim/Dotum 프로젝트에서 받아
TamaPoke에서 실제 사용하는 문자만 subset으로 생성합니다.

---

## 포켓몬 이름

한국어 모드인 KD 또는 KG에서만 포켓몬 이름을 한국어로 표시합니다.

예:

```text
Bulbasaur  → 이상해씨
Charmander → 파이리
Squirtle   → 꼬부기
Pikachu    → 피카츄
Eevee      → 이브이
Mewtwo     → 뮤츠
Mew        → 뮤
```

ES/EN/FR/DE/IT/PT에서는 원본 `DEX_TBL`의 이름을 그대로 사용합니다.

즉 한국어화를 위해 원본 도감 데이터 자체를 한국어로 덮어쓰지 않습니다.

---

# 웹 설치

PC의 **Chrome 또는 Edge** 사용을 권장합니다.

설치 페이지:

**https://zila81.github.io/Poke-ko/**

## 기존 오리지널 TamaPoke 사용자

이미 TamaPoke가 설치되어 있고 microSD의 포켓몬 그림이 정상적으로 표시된다면:

1. 웹 설치 페이지를 엽니다.
2. **한국어 펌웨어 설치**를 실행합니다.
3. 기존 저장 데이터를 유지하려면 **Erase(지우기)를 선택하지 않습니다.**
4. 설치 완료 후 기기를 재시작합니다.
5. 설정에서 `KD` 또는 `KG`를 선택합니다.

기존 microSD 그림 데이터가 정상이라면 **2번 그림 데이터 설치는 생략할 수 있습니다.**

## 새 기기 / 새 microSD 사용자

1. microSD 카드를 TamaPoke에 넣습니다.
2. 웹페이지에서 한국어 펌웨어를 설치합니다.
3. 펌웨어 설치 창을 완전히 닫습니다.
4. TamaPoke를 재시작합니다.
5. 웹페이지의 **기기 연결**을 누릅니다.
6. ESP32-S3 USB Serial 포트를 선택합니다.
7. **포켓몬 그림 데이터 설치**를 실행합니다.
8. 전송 완료 후 PWR 버튼으로 재시작합니다.

그림 데이터 전송 중에는 USB 케이블이나 microSD 카드를 분리하지 마세요.

---

## Erase 주의사항

기존 TamaPoke의 포켓몬 저장 데이터를 유지하려면 펌웨어 업데이트 시
**Erase를 선택하지 마세요.**

일반적인 펌웨어 업데이트는 기존 저장 데이터와 microSD 그림을 유지하는 것을 목표로 합니다.

완전히 초기화하고 처음부터 시작하려는 경우에만 Erase를 사용하세요.

---

# 펌웨어와 microSD 데이터의 차이

TamaPoke는 프로그램과 포켓몬 그림을 서로 다른 곳에 저장합니다.

```text
ESP32-S3 Flash
├── TamaPoke 프로그램
├── 한국어 UI
├── 한국어 폰트
├── 도감/게임 로직
└── 저장 데이터

microSD
└── 포켓몬 스프라이트 / 애니메이션
```

따라서 이미 정상적인 microSD를 사용 중이라면 한국어 펌웨어 업데이트 때
스프라이트를 매번 다시 설치할 필요가 없습니다.

---

# 자동 빌드 구조

GitHub Actions는 다음 순서로 동작합니다.

```text
최신 socquique/TamaPoke 다운로드
        ↓
원본 무수정 컴파일
        ↓
KD / KG 한국어 기능 적용
        ↓
DotumChe / GulimChe
11px / 12px / 14px subset 생성
        ↓
한국어판 컴파일
        ↓
원본 build_web.sh 실행
        ↓
웹 설치용 펌웨어 + sprites.pak 생성
        ↓
GitHub Pages 배포
```

원본을 먼저 컴파일하기 때문에 실패 위치를 쉽게 구분할 수 있습니다.

- 원본 빌드 실패 → 원본 또는 빌드 환경 문제
- 한국어 패치 단계 실패 → Poke-ko 패치와 최신 원본의 구조 차이
- 한국어판 컴파일 실패 → 한글/폰트 관련 코드 문제
- 웹 패키징 실패 → 웹 설치 파일 생성 문제

---

# 원본 웹 설치 기능 보존

Poke-ko의 중요한 원칙 중 하나는 **원본 웹 설치 기능을 변경하지 않는 것**입니다.

웹페이지 한국어화 과정에서:

- ESP Web Tools 펌웨어 설치
- Web Serial 연결
- 포트 선택
- `sprites.pak` 다운로드
- microSD 파일 전송
- 버튼 이벤트
- JavaScript 통신 코드

를 원본과 동일하게 유지합니다.

`korean/patch_web.py`는 원본 `web/index.html`의 `<script>...</script>` 블록을
수정하지 않도록 설계되어 있습니다.

한국어화 전후 JavaScript 블록을 byte-for-byte 비교하며,
스크립트가 변경되면 GitHub Actions 빌드를 실패시키도록 검증합니다.

---

# 저장소 구조

```text
Poke-ko/
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── korean/
│   ├── patch_v3.py
│   ├── patch_web.py
│   ├── verify_v3.py
│   ├── verify_web.py
│   ├── build_dotum_bdf.py
│   └── make_u8g2_fonts.py
│
└── README.md
```

Poke-ko 저장소에는 원본 TamaPoke 전체 소스를 복사해 넣지 않습니다.

GitHub Actions가 빌드할 때 최신 원본을 자동으로 가져옵니다.

---

# 개발 / 업데이트

저장소 파일을 수정해 `main` 브랜치에 Commit하면 GitHub Actions가 자동으로 실행됩니다.

수동 실행도 가능합니다.

```text
GitHub
→ Poke-ko
→ Actions
→ Poke-ko build workflow
→ Run workflow
```

빌드와 Pages 배포가 성공하면 기존 웹 설치 주소가 새 버전으로 갱신됩니다.

---

# 실기 테스트 체크리스트

v1.0.1에서 확인할 항목:

- [ ] 부팅 정상
- [ ] 기존 저장 데이터 유지
- [ ] ES / EN / FR / DE / IT / PT 정상
- [ ] KD 선택 가능
- [ ] KG 선택 가능
- [ ] KD 한국어 UI 정상
- [ ] KG 한국어 UI 정상
- [ ] KD 151마리 한국어 이름 정상
- [ ] KG 151마리 한국어 이름 정상
- [ ] 11px 작은 라벨 가독성
- [ ] 12px 일반 UI 가독성
- [ ] 14px 큰 제목/포켓몬 이름 가독성
- [ ] 메인 화면 정렬
- [ ] 성장 화면 정렬
- [ ] 메달 화면 정렬
- [ ] 배틀 화면 정렬
- [ ] 설정 화면 정렬
- [ ] 웹 펌웨어 설치 정상
- [ ] Web Serial 기기 연결 정상
- [ ] microSD 그림 데이터 설치 정상

---

# 버전

현재 Poke-ko 버전:

**v1.0.1**

v1.0.1은 KD(DotumChe)와 KG(GulimChe)를 동시에 포함해 실제 기기에서 폰트를 비교하기 위한
첫 공식 테스트 버전입니다.

---

# 크레딧 및 라이선스

Poke-ko는 비공식 팬 프로젝트입니다.

- TamaPoke 원본 프로젝트: socquique/TamaPoke
- 한국어판: zila81/Poke-ko
- DotumChe / GulimChe: Google Fonts Gulim/Dotum project — SIL Open Font License 1.1
- U8g2: olikraus/u8g2
- Arduino_GFX: moononournation/Arduino_GFX
- 포켓몬 스프라이트 관련 크레딧과 라이선스는 원본 TamaPoke 프로젝트의 안내를 따릅니다.

Pokémon 및 관련 명칭/캐릭터의 권리는 각 권리자에게 있습니다.
Poke-ko는 Pokémon Company, Nintendo, Game Freak, Creatures와 공식적인 관련이 없습니다.


---

# 한글 폰트 시뮬레이터

현재 실제 펌웨어는 실기에서 한글 출력이 확인된 `u8g2_font_unifont_t_korean2`를 사용합니다.

DotumChe/GulimChe 11/12/14px은 바로 펌웨어에 적용하지 않고 웹 설치 페이지에서 먼저 검증합니다.

GitHub Actions는 Unicode charmap을 명시적으로 선택하고 필수 한글 codepoint의 glyph index와 bitmap 존재 여부를 검사합니다. 누락이 있으면 빌드를 실패시킵니다.

그 다음 TTF→BDF 변환 결과를 `font-preview.json`으로 만들어 웹 Canvas에서 픽셀 그대로 표시합니다.

테스트 조합:
- KD DotumChe: 11 / 12 / 14px
- KG GulimChe: 11 / 12 / 14px

시뮬레이터는 브라우저의 TTF 렌더링을 사용하지 않습니다. 생성된 BDF bitmap 자체를 표시합니다.
