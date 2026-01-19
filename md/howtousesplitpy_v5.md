# 스프라이트 분할 스크립트 v5.1 사용 가이드

## GitHub 구조

```
PARK-JUHWAN/claude/
├── ingredient/
│   ├── batch1/
│   │   ├── prompt.txt    ← GPT 프롬프트 (아이템 목록)
│   │   ├── origin.png    ← GPT 결과 (라벨 있음)
│   │   └── renew.png     ← 투명배경 버전 (라벨 제거)
│   ├── batch2/
│   │   └── ...
│   └── batch3/
│       └── ...
├── assets/
│   ├── bed_1_32x32.png         ← 결과물 (누적)
│   ├── bed_2_64x32.png
│   ├── chair_1_32x32.png
│   └── sprite_index.json       ← JSON 1개 (누적)
└── md/
    ├── split_sprites_v5.py     ← 이 스크립트
    └── howtousesplitpy_v5.md   ← 이 문서
```

---

## 1. 설치

```bash
pip install pillow opencv-python numpy easyocr --break-system-packages
```

---

## 2. 입력 파일 준비

### batch 폴더 생성

```
ingredient/batch1/
├── prompt.txt    # 아이템 목록
├── origin.png    # GPT 이미지 (라벨 포함)
└── renew.png     # 투명배경 (라벨 제거)
```

### prompt.txt 형식

```
1. Hospital bed
2. IV pole
3. Wheelchair
4. Medical cart
5. Bedside table
```

또는

```
- Hospital bed
- IV pole
- Wheelchair
```

### origin.png
- GPT가 생성한 원본 이미지
- 라벨(텍스트)이 포함된 상태
- OCR로 라벨 위치 인식용

### renew.png
- 투명 배경 버전
- 라벨 제거된 상태
- 실제 분할 대상

---

## 3. 실행

### 기본 실행

```bash
cd claude

python md/split_sprites_v5.py \
    --prompt ingredient/batch1/prompt.txt \
    --origin ingredient/batch1/origin.png \
    --renew ingredient/batch1/renew.png \
    --output assets/
```

### GitHub 자동 push

```bash
python md/split_sprites_v5.py \
    --prompt ingredient/batch1/prompt.txt \
    --origin ingredient/batch1/origin.png \
    --renew ingredient/batch1/renew.png \
    --output assets/ \
    --push
```

---

## 4. batch 작업 흐름

```bash
# batch1 작업
python md/split_sprites_v5.py \
    --prompt ingredient/batch1/prompt.txt \
    --origin ingredient/batch1/origin.png \
    --renew ingredient/batch1/renew.png \
    --output assets/ \
    --push

# batch2 작업 (자동 누적)
python md/split_sprites_v5.py \
    --prompt ingredient/batch2/prompt.txt \
    --origin ingredient/batch2/origin.png \
    --renew ingredient/batch2/renew.png \
    --output assets/ \
    --push

# batch3 작업 (자동 누적)
python md/split_sprites_v5.py \
    --prompt ingredient/batch3/prompt.txt \
    --origin ingredient/batch3/origin.png \
    --renew ingredient/batch3/renew.png \
    --output assets/ \
    --push
```

**핵심:** `sprite_index.json`이 자동 누적됨

---

## 5. 출력물

### PNG 파일명 규칙

```
{name}_{number}_{width}x{height}.png

예시:
bed_1_32x32.png
bed_2_64x32.png
ivpole_1_32x64.png
wheelchair_1_64x32.png
```

### sprite_index.json 구조

```json
{
  "_meta": {
    "sources": [
      {
        "batch": "batch1",
        "prompt": "prompt.txt",
        "origin": "origin.png",
        "renew": "renew.png",
        "sprites": 45,
        "date": "2026-01-17"
      },
      {
        "batch": "batch2",
        "sprites": 38,
        "date": "2026-01-18"
      }
    ],
    "total_sprites": 83,
    "last_updated": "2026-01-18 14:30:00"
  },
  "counts": {
    "bed": 5,
    "chair": 3,
    "ivpole": 2
  },
  "files": [
    "bed_1_32x32.png",
    "bed_2_64x32.png",
    "chair_1_32x32.png"
  ]
}
```

---

## 6. 캔버스 크기 규칙

| 원본 비율 | 캔버스 |
|----------|--------|
| 가로 긴 (≥2.5) | 96x32 |
| 가로 긴 (1.5~2.5) | 64x32 |
| 정사각형 (0.67~1.5) | 32x32 |
| 세로 긴 (0.4~0.67) | 32x64 |
| 세로 긴 (<0.4) | 32x96 |

---

## 7. 파일명 정규화 규칙

| 원본 | 정규화 |
|------|--------|
| Hospital bed | hospitalbed |
| IV pole | ivpole |
| Wheelchairs | wheelchair |
| Medical cart | medicalcart |

- 소문자 변환
- 공백/특수문자 제거
- 복수형 's' 제거 (ss, us, is 제외)

---

## 8. 옵션 요약

| 옵션 | 필수 | 설명 |
|------|------|------|
| `--prompt` | ✅ | prompt.txt 경로 |
| `--origin` | ✅ | origin.png 경로 (OCR용) |
| `--renew` | ✅ | renew.png 경로 (분할용) |
| `--output` | ✅ | 출력 폴더 (assets/) |
| `--push` | ❌ | GitHub 자동 push |

---

## 9. 문제 해결

### OCR 안 됨
```
⚠️ OCR 엔진 없음 - prompt 순서 사용
```
→ `pip install easyocr` 실행

### Git push 실패
```
⚠️ Git push 실패
```
→ `git config` 확인, 인증 설정

### 스프라이트 누락
- renew.png 투명배경 확인
- 작은 아이템이 필터링됐을 수 있음 (최소 8x8px)

---

## 10. 전체 워크플로우

```
┌─────────────────────────────────────────────┐
│ 1. GPT에 스티커시트 프롬프트 입력            │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 2. GPT 결과 이미지 저장                      │
│    → origin.png (라벨 포함)                  │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 3. 투명배경 + 라벨제거 버전 생성             │
│    → renew.png                              │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 4. ingredient/batchN/ 폴더에 저장            │
│    - prompt.txt                             │
│    - origin.png                             │
│    - renew.png                              │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 5. 스크립트 실행                             │
│    python md/split_sprites_v5.py ... --push │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 6. assets/ 폴더에 PNG + JSON 생성            │
│    → GitHub 자동 push                        │
└─────────────────────────────────────────────┘
```

---

## 버전 히스토리

| 버전 | 날짜 | 변경사항 |
|------|------|----------|
| v5.0 | 2026-01-17 | OCR + 3파일 입력 방식 |
| v5.1 | 2026-01-17 | ZIP 제거, --push 추가, GitHub 구조 최적화 |
