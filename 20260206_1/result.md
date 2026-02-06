# 변경 결과 요약 (result.md)

## 변경 내용

### Step 1: HTML 파일 수정 (src → data-src 변환)

| 파일명 | 변환 수 | 변환 상세 |
|--------|---------|-----------|
| new_sapphire_index.html | 1 | `<iframe src="{{map_embed}}">` → `<iframe src="" data-src="{{map_embed}}">` |
| new_sapphire_about.html | 0 | img/iframe 태그에 `{{...}}` placeholder src 없음 |
| new_sapphire_joint.html | 0 | img/iframe 태그에 `{{...}}` placeholder src 없음 |
| new_sapphire_spine.html | 0 | img/iframe 태그에 `{{...}}` placeholder src 없음 |
| new_sapphire_sports.html | 0 | img/iframe 태그에 `{{...}}` placeholder src 없음 |

**참고:** 대부분의 `<img>` 태그는 정적 경로(`sapphire_assets/...`)를 사용합니다. `{{...}}` placeholder를 `src` 속성에 포함한 태그는 `sapphire_index.html`의 `<iframe src="{{map_embed}}">` 1건뿐입니다.

### Step 2: sapphire_main.js 수정 (config loader section, 1~33행만 수정)

`replaceInNode` 함수에 다음 로직을 추가했습니다:

1. 기존 텍스트 노드 치환 (변경 없음)
2. 기존 속성값 치환 (변경 없음)
3. **신규**: 속성값 치환 후, `data-src` 속성이 있고 `src`가 비어 있으면 치환된 `data-src` 값을 `src`에 복사

추가된 코드:
```javascript
// data-src → src: 빈 src에 치환된 data-src 값 적용
if (node.hasAttribute('data-src') && !node.getAttribute('src')) {
  node.setAttribute('src', node.getAttribute('data-src'));
}
```

34행 이후 코드는 수정하지 않았습니다.

## 한국어 텍스트 보존 검증

| 파일명 | 검증 결과 |
|--------|-----------|
| new_sapphire_index.html | 9/9 한국어 키워드 확인 |
| new_sapphire_about.html | 9/9 한국어 키워드 확인 |
| new_sapphire_joint.html | 9/9 한국어 키워드 확인 |
| new_sapphire_spine.html | 9/9 한국어 키워드 확인 |
| new_sapphire_sports.html | 9/9 한국어 키워드 확인 |
| new_sapphire_main.js | 3/3 한국어 키워드 확인 |

**검증 방법:** 각 파일에서 한국어 키워드(병원소개, 관절센터, 척추센터, 스포츠, 재활, 의료진, 시설안내, 진료센터, 연락처)의 존재 여부를 확인했습니다. 모든 한국어 텍스트가 정상적으로 보존되었습니다.

## 최종 산출물

1. `new_sapphire_index.html` - iframe의 src → data-src 변환 (1건)
2. `new_sapphire_about.html` - 변환 대상 없음 (원본 복사)
3. `new_sapphire_joint.html` - 변환 대상 없음 (원본 복사)
4. `new_sapphire_spine.html` - 변환 대상 없음 (원본 복사)
5. `new_sapphire_sports.html` - 변환 대상 없음 (원본 복사)
6. `new_sapphire_main.js` - replaceInNode에 data-src → src 복사 로직 추가
7. `result.md` - 본 문서
