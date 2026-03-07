<div align="center">

# 🚭 Please No Smoking

**금연 추적 데스크톱 앱 — 오늘 하루도 피우지 않았습니다.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.7%2B-41CD52?style=flat-square&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![Tests](https://img.shields.io/badge/tests-29%20passed-brightgreen?style=flat-square&logo=pytest&logoColor=white)](https://pytest.org)
[![Ruff](https://img.shields.io/badge/lint-Ruff-D7FF64?style=flat-square)](https://docs.astral.sh/ruff/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Release](https://img.shields.io/github/v/release/shinjh0380/please-no-smoking?style=flat-square&logo=github)](https://github.com/shinjh0380/please-no-smoking/releases/latest)

</div>

---

## 소개
<div align="center">
  <img src="docs/images/nosmoking.jpg" width="480" />
  <p><em>금연: 가만 있어도 성공하는 세상에서 가장 쉬운 도전.</em></p>
</div>

**Please No Smoking** 은 금연을 시작한 날짜를 기록하고, 항상 화면에 떠 있는 오버레이 창으로 금연 n일차를 보여주는 가벼운 데스크톱 앱입니다.

- "금연 시작" 버튼 한 번으로 오버레이 창 실행
- 검은 배경에 흰 글씨로 금연 경과 일수를 크게 표시
- 항상 최상위(Always on Top) 창으로 유지
- **시스템 트레이** 상주: 태스크바에 노출 없이 트레이 아이콘으로 앱 관리
- 설치 없이 실행 파일 하나로 사용할 수 있습니다

---

## 기능

| 기능 | 설명 |
|------|------|
| 금연 시작일 선택 | 달력 팝업으로 날짜 입력, 미래 날짜 입력 차단 |
| 흡연량 설정 | 하루 흡연량(개비), 갑당 가격, 갑당 개비 수 |
| 금연 n일차 오버레이 | "금연 시작" 클릭 시 검은 배경/흰 글씨 오버레이 창 표시 |
| 오버레이 위치·크기 저장 | 창 위치와 크기를 자동 저장, 재실행 시 복원 |
| 시스템 트레이 | 트레이 아이콘 우클릭: 설정, 오버레이 토글, 종료 / 더블클릭: 오버레이 표시·숨기기 |
| 설정 복귀 | 오버레이 창에서 우클릭 → 설정으로 돌아가기 / 종료 |
| 데이터 저장 / 자동 시작 | 마지막 입력값을 자동 저장, 재실행 시 복원 |
| 절약 금액 / 개비 표시 | 오버레이에 절약한 금액(원)과 안 피운 개비 수 실시간 표시 |
| 작업 표시줄 아이콘 | AppUserModelID 설정으로 작업 표시줄에 앱 커스텀 아이콘 표시 |
| 오버레이 작업 표시줄 숨김 | 오버레이 창은 작업 표시줄 버튼 목록에 노출되지 않음 |

---

## 다운로드 및 실행 (Windows)

> Python 설치 없이 바로 실행할 수 있는 빌드 패키지를 제공합니다.

### 1단계 — 다운로드

[**최신 릴리즈 페이지**](https://github.com/shinjh0380/please-no-smoking/releases/latest)에서 `please-no-smoking-vX.X.X-windows-x64.zip`을 다운받습니다.

또는 직접 링크:

```
https://github.com/shinjh0380/please-no-smoking/releases/download/v0.6.0/please-no-smoking-v0.6.0-windows-x64.zip
```

### 2단계 — 압축 해제

다운받은 zip 파일을 원하는 폴더에 압축 해제합니다.

```
please-no-smoking/
├── please-no-smoking.exe   ← 이 파일을 실행하세요
├── _internal/              (런타임 라이브러리, 삭제 금지)
└── ...
```

### 3단계 — 실행

`please-no-smoking.exe`를 더블클릭하면 앱이 실행됩니다.

> **Windows Defender 경고가 뜨는 경우:** "추가 정보" → "실행"을 클릭하면 됩니다.
> (코드서명 인증서가 없어 발생하는 경고이며, 악성 코드가 아닙니다.)

---

## 소스에서 직접 실행 (개발자용)

### 요구 사항

- Python 3.11 이상
- [uv](https://docs.astral.sh/uv/) 패키지 매니저

### 빠른 시작

```bash
# 저장소 클론
git clone https://github.com/shinjh0380/please-no-smoking.git
cd please-no-smoking

# 의존성 설치
uv sync

# 앱 실행
uv run python -m app.main
```

---

## 개발 환경 설정

```bash
# 개발 의존성 포함 설치
uv sync --all-groups

# 테스트 실행
uv run pytest

# 테스트 + 커버리지
uv run pytest --cov=app --cov-report=term-missing

# Lint
uv run ruff check app/ tests/

# Format
uv run ruff format app/ tests/

# 타입 체크
uv run mypy app/
```

---

## 배포 (패키징)

[PyInstaller](https://pyinstaller.org)를 사용해 단일 디렉터리 실행 파일로 패키징합니다.

```bash
# onedir 빌드 (권장)
uv run pyinstaller --onedir --windowed app/main.py --name please-no-smoking

# 빌드 결과물 위치
dist/please-no-smoking/please-no-smoking.exe  # Windows
dist/please-no-smoking/please-no-smoking       # macOS / Linux
```

---

## 프로젝트 구조

```
please-no-smoking/
├── app/
│   ├── __init__.py
│   ├── main.py               # 앱 진입점
│   ├── models.py             # SmokingInput, SmokingStats 데이터 클래스
│   ├── tray.py               # TrayManager, 트레이 아이콘 생성
│   ├── window.py             # PySide6 메인 윈도우
│   └── services/
│       ├── __init__.py
│       ├── quit_tracker.py   # 핵심 계산 로직 (validate_input, calculate_stats)
│       └── persistence.py    # 입력값 저장/복원 (JSON)
├── tests/
│   ├── test_quit_tracker.py  # 도메인 로직 단위 테스트
│   ├── test_window.py        # pytest-qt 위젯 테스트
│   └── test_persistence.py   # 저장/복원 단위 테스트
├── pyproject.toml
└── uv.lock
```

---

## 아키텍처

비즈니스 로직과 UI를 명확하게 분리합니다.

```
app/main.py            (진입점)
  setQuitOnLastWindowClosed(False)
  TrayManager 생성 / overlay_created 시그널 연결
       │
       ▼
app/tray.py            (트레이 레이어)
  TrayManager        ← QSystemTrayIcon 관리, 컨텍스트 메뉴, 더블클릭 토글
  create_tray_icon() → QPainter로 금연 심볼 QIcon 생성
       │
       ▼
app/window.py          (UI 레이어)
  MainWindow         ← overlay_created Signal 발행, closeEvent → hide
  OverlayWindow      ← Qt.Tool 플래그로 태스크바 숨김
       │
       │  SmokingInput 생성 / 저장
       ▼
app/services/quit_tracker.py  (도메인 레이어)
  validate_input()   ← ValueError 발생 시 window가 오류 메시지 표시
  calculate_stats()  → SmokingStats 반환
       │
       ▼
app/models.py          (데이터 모델)
  @dataclass SmokingInput
  @dataclass SmokingStats

app/services/persistence.py   (영속성 레이어)
  save_input()       ← SmokingInput을 JSON으로 저장
  load_input()       → 저장된 SmokingInput 복원 (없으면 None)
  save_geometry()    ← 오버레이 창 위치·크기를 JSON으로 저장
  load_geometry()    → 저장된 geometry 복원 (없으면 None)
```

- `quit_tracker.py`는 Qt에 의존하지 않아 단독 단위 테스트가 가능합니다
- `calculate_stats(today=...)` 파라미터로 테스트 시 날짜를 주입할 수 있습니다

---

## 테스트

```
tests/test_quit_tracker.py   8개 케이스
  - 10일 경과 정상 계산
  - 당일 시작 (경과 0일)
  - 미래 날짜 → ValueError
  - 흡연량 0 이하 → ValueError
  - 음수 흡연량 → ValueError
  - 가격 0 이하 → ValueError
  - 갑당 개비 수 0 이하 → ValueError
  - 유효 입력 반환 확인

tests/test_window.py         4개 케이스
  - 윈도우 정상 생성
  - "금연 시작" 클릭 후 오버레이 창 표시 및 경과일 확인
  - 미래 날짜 입력 시 오류 메시지 표시
  - 상태 메시지 초기값 확인

tests/test_persistence.py    8개 케이스
  - 저장 후 복원 (happy path)
  - 파일 없을 때 None 반환
  - 손상된 JSON 처리
  - 저장 경로 격리 (tmp_path 사용)
  - geometry 저장 후 복원 (happy path)
  - geometry 파일 없을 때 None 반환
  - 손상된 geometry JSON 처리
  - geometry 저장 경로 격리 (tmp_path 사용)

tests/test_tray.py           8개 케이스
  - 트레이 아이콘 생성 확인
  - TrayManager 생성 확인
  - 컨텍스트 메뉴 항목(설정, 오버레이 토글, 종료) 확인
  - 설정 창 표시 동작
  - 오버레이 표시/숨기기 토글
  - overlay=None 시 토글 안전 처리
  - update_overlay() 참조 갱신
  - CI headless 시 자동 skip

tests/test_packaging.py      1개 케이스
  - spec 파일 console=False 검증 (콘솔창 회귀 방지)
```

```bash
uv run pytest -v
```

---

## 기술 스택

| 역할 | 기술 |
|------|------|
| GUI 프레임워크 | [PySide6](https://doc.qt.io/qtforpython/) (Qt 6) |
| 패키지 관리 | [uv](https://docs.astral.sh/uv/) |
| 테스트 | [pytest](https://pytest.org) + [pytest-qt](https://pytest-qt.readthedocs.io) |
| Lint / Format | [Ruff](https://docs.astral.sh/ruff/) |
| 타입 체크 | [mypy](https://mypy-lang.org/) |
| 패키징 | [PyInstaller](https://pyinstaller.org) |

---

## 기여하기

1. 이 저장소를 Fork합니다
2. 기능 브랜치를 만듭니다 (`git checkout -b feat/my-feature`)
3. 변경 사항을 커밋합니다 (`git commit -m 'feat: 새 기능 추가'`)
4. 브랜치에 Push합니다 (`git push origin feat/my-feature`)
5. Pull Request를 열어주세요

버그 리포트나 기능 제안은 [Issues](https://github.com/shinjh0380/please-no-smoking/issues)에 올려주세요.

---

## 라이선스

[MIT License](LICENSE) © 2026 shinjh0380
