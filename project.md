# Webtoon Project

## 프로젝트 개요

- 장르: 직장인 일상 웹툰 (Korean office life webtoon)
- 스타일: Soft watercolor Korean webtoon style
- 이미지 생성 모델: 나노바나나 최신 모델
- 패널 구성: 3패널 (Top-Left / Top-Right / Bottom-Center)
- GitHub 레포: webtoon
- 작업 폴더: C:\Users\cgh56\Desktop\pocsoccer\webtoon

## 캐릭터 레퍼런스 이미지

이미지 생성 시 아래 레퍼런스 이미지를 Gemini API에 함께 전달하여 캐릭터 일관성 유지.

| 캐릭터 | 파일 |
|--------|------|
| 이 대리 (주인공) | `images/lee.png` |
| 박 부장 | `images/park.png` |

> generate.py가 자동으로 두 이미지를 프롬프트와 함께 API에 전달함.

## 고정 캐릭터 디자인 (CHARACTER DESIGN - DO NOT CHANGE)

### 주인공 (Protagonist)
- 갈색 단발머리, 차분한 눈빛
- 갈색 정장 투피스 (블레이저 + 스커트) + 하늘색 드레스 셔츠
- 사내: 파란색 사원증 목걸이 착용 / 사외: 사원증 없음

### 박 팀장 (Manager Park)
- 중년 한국 남성
- 단정하게 빗어 넘긴 젤 바른 검은 머리 (약간 숱이 적음)
- 평균 체형, 부드러운 턱선
- 클래식 네이비 투피스 정장, 흰 셔츠, 네이비 타이
- 권위적이지만 옹졸하고 앙심을 품는 성격, 음흉한 표정

## 고정 비주얼 스타일 (VISUAL STYLE - DO NOT CHANGE)

```
Soft watercolor Korean webtoon style,
delicate pencil outlines,
warm pastel palette,
gentle window lighting,
calm emotional atmosphere,
high-quality digital painting,
paper texture overlay.
```

## 고정 네거티브 프롬프트 (NEGATIVE PROMPT - DO NOT CHANGE)

```
Text generation, Story writing, Screenplay format
Output ONLY the image generation prompt
```

## 프롬프트 구조

### 고정 파트 (매 이미지 동일)
- CHARACTER DESIGN 섹션
- VISUAL STYLE 섹션
- NEGATIVE PROMPT 섹션

### 가변 파트 (에피소드마다 변경)
- Panel Layout (Top-Left → Top-Right → Bottom-Center)
- Panel 1, 2, 3 내용 (대사, 장면 묘사, 나레이션, SFX 등)
- 페이지 번호

## 폴더 구조

```
webtoon/
├── project.md          # 프로젝트 유의점 및 설정 (자동 업데이트)
├── progress.md         # 일일 진행 상황 (자동 업데이트)
├── episodes/           # 에피소드별 폴더
│   ├── ep01/
│   │   ├── prompt.txt  # 사용한 프롬프트
│   │   └── panel.png   # 생성된 이미지
│   └── ...
└── scripts/            # 자동화 스크립트
```

## 유의사항

1. CHARACTER DESIGN과 VISUAL STYLE은 절대 변경하지 않는다.
2. 패널 레이아웃과 대사는 에피소드마다 새로 작성한다.
3. 생성된 이미지와 프롬프트는 episodes/ 폴더에 에피소드별로 저장한다.
4. 매일 GitHub webtoon 레포에 커밋 & 푸시한다.
5. progress.md에 당일 작업 내용을 기록한다.

## GitHub 설정

- 레포 이름: webtoon
- 브랜치: main
- 커밋 주기: 에피소드 완성 시 또는 매일 1회
