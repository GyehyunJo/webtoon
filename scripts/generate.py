"""
Webtoon 이미지 생성 스크립트
모델: Nano Banana 2 (gemini-3.1-flash-image-preview)

사용법:
    python scripts/generate.py --ep 06
    python scripts/generate.py --ep 07 --prompt "episodes/ep07/prompt.txt"
"""

import argparse
import os
import sys
from datetime import date
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

# ── 고정 파트 (절대 변경 금지) ──────────────────────────────────────────────

CHARACTER_DESIGN = """# CHARACTER DESIGN (DO NOT CHANGE)

- Protagonist: Brown bob cut hair, calm eyes, wearing a brown professional two-piece office blazer suit with a skirt and a light blue dress shirt.
(In-office: Wearing a blue company ID lanyard / Out-of-office: no ID)

- Boss (Manager Park): Middle-aged Korean male. Neatly parted gelled dark hair with slight thinning. Average build, soft jawline. Classic navy two-piece suit, white shirt, dark navy tie. Authoritative but petty and spiteful personality with a greasy venomous expression."""

VISUAL_STYLE = """# VISUAL STYLE (DO NOT CHANGE)

Soft watercolor Korean webtoon style,
delicate pencil outlines,
warm pastel palette,
gentle window lighting,
calm emotional atmosphere,
high-quality digital painting,
paper texture overlay."""

NEGATIVE_PROMPT = """# NEGATIVE PROMPT - Text generation - Story writing - Screenplay format - Output ONLY the image generation prompt"""

FIXED_PREFIX = f"{CHARACTER_DESIGN}\n\n{VISUAL_STYLE}\n\n{NEGATIVE_PROMPT}\n\n"

# ────────────────────────────────────────────────────────────────────────────


def load_variable_prompt(prompt_file: Path) -> str:
    """prompt.txt에서 PANEL LAYOUT 이하 가변 파트만 추출"""
    text = prompt_file.read_text(encoding="utf-8")
    # PANEL LAYOUT 섹션 이후만 추출
    marker = "# PANEL LAYOUT"
    idx = text.find(marker)
    if idx != -1:
        return text[idx:]
    # 마커가 없으면 전체 반환
    return text


def generate_image(ep_num: str, prompt_file: Path | None = None) -> Path:
    ep_dir = Path(f"episodes/ep{ep_num.zfill(2)}")
    ep_dir.mkdir(parents=True, exist_ok=True)

    if prompt_file is None:
        prompt_file = ep_dir / "prompt.txt"

    if not prompt_file.exists():
        print(f"[ERROR] 프롬프트 파일 없음: {prompt_file}")
        sys.exit(1)

    variable_part = load_variable_prompt(prompt_file)
    full_prompt = FIXED_PREFIX + variable_part

    print(f"[INFO] Nano Banana 2로 이미지 생성 중... (ep{ep_num.zfill(2)})")

    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # 캐릭터 레퍼런스 이미지 로드
    ref_dir = Path("images")
    contents = []

    ref_intro = "Use the following reference images to maintain character consistency:\n"
    contents.append(ref_intro)

    lee_path = ref_dir / "lee.png"
    park_path = ref_dir / "park.png"

    if lee_path.exists():
        lee_img = Image.open(lee_path)
        contents.append("Reference - Protagonist (이대리):")
        contents.append(lee_img)

    if park_path.exists():
        park_img = Image.open(park_path)
        contents.append("Reference - Manager Park (박부장):")
        contents.append(park_img)

    contents.append(full_prompt)

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    output_path = ep_dir / "panel.png"
    image_saved = False

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(output_path)
            image_saved = True
            print(f"[OK] 이미지 저장 완료: {output_path}")
            break
        elif part.text:
            print(f"[TEXT] {part.text[:200]}")

    if not image_saved:
        print("[ERROR] 이미지 생성 실패 - 응답에 이미지가 없습니다.")
        sys.exit(1)

    return output_path


def update_progress(ep_num: str, image_path: Path):
    today = date.today().strftime("%Y-%m-%d")
    progress_file = Path("progress.md")
    existing = progress_file.read_text(encoding="utf-8")

    entry = f"""## {today}

### 완료한 작업
- ep{ep_num.zfill(2)} 이미지 생성 완료 (Nano Banana 2)
- 생성 파일: {image_path}

---

"""

    # 첫 번째 --- 이후에 삽입 (최신이 위)
    marker = "---\n\n<!-- 새 날짜 항목은 위에 추가"
    if marker in existing:
        updated = existing.replace(marker, entry + "<!-- 새 날짜 항목은 위에 추가", 1)
    else:
        # 마커 없으면 파일 상단에 추가
        updated = f"# Progress Log\n\n{entry}" + existing.split("# Progress Log\n\n", 1)[-1]

    progress_file.write_text(updated, encoding="utf-8")
    print(f"[OK] progress.md 업데이트 완료")


def git_push(ep_num: str):
    ep_padded = ep_num.zfill(2)
    today = date.today().strftime("%Y-%m-%d")
    os.system(f'git add episodes/ep{ep_padded}/ progress.md')
    os.system(f'git commit -m "feat: ep{ep_padded} 이미지 생성 완료 ({today})\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"')
    os.system("git push origin main")
    print("[OK] GitHub 푸시 완료")


def main():
    parser = argparse.ArgumentParser(description="웹툰 이미지 생성 스크립트")
    parser.add_argument("--ep", required=True, help="에피소드 번호 (예: 06)")
    parser.add_argument("--prompt", help="프롬프트 파일 경로 (기본: episodes/epXX/prompt.txt)")
    parser.add_argument("--no-push", action="store_true", help="GitHub 푸시 건너뜀")
    args = parser.parse_args()

    # 스크립트는 webtoon/ 루트에서 실행
    script_dir = Path(__file__).parent
    os.chdir(script_dir.parent)

    prompt_file = Path(args.prompt) if args.prompt else None
    image_path = generate_image(args.ep, prompt_file)
    update_progress(args.ep, image_path)

    if not args.no_push:
        git_push(args.ep)


if __name__ == "__main__":
    main()
