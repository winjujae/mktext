import os
import textwrap
from faster_whisper import WhisperModel

VALID_EXTENSIONS = ('.mp3', '.mp4', '.m4a', '.wav', '.webm', '.ogg', '.flac')

def transcribe_audio(input_filename):
    download_dir = "./download"
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    input_path = os.path.join(download_dir, input_filename)
    if not os.path.isfile(input_path):
        print(f"❌ 파일이 존재하지 않습니다: {input_path}")
        return

    if not input_filename.lower().endswith(VALID_EXTENSIONS):
        print(f"❗ 지원하지 않는 파일 형식입니다. 지원되는 확장자: {', '.join(VALID_EXTENSIONS)}")
        return

    # ---- 모델 로드 (순정 설정에 가깝게) ----
    model_size = "small"  # 필요시 "base"/"medium"/"large-v3"
    model = WhisperModel(
        model_size,
        device="cpu",          # GPU면 "cuda"
        compute_type="int8",   # CPU에서 가볍게
        num_workers=2
    )

    print(f"🔊 {input_filename} 파일을 전사 중...")

    try:
        # == 최소 옵션만 사용 ==
        segments, info = model.transcribe(
            input_path,
            language="ko",
            # 반복 완화에 꼭 필요한 2개만:
            condition_on_previous_text=False,   # 문맥 누적 반복 방지 (공식 파라미터)
            temperature=(0.0, 0.2, 0.4),        # 내장 온도 폴백 (공식 지원)
            # 나머지는 전부 기본값(빔서치/필터/VAD 등)
        )
    except Exception as e:
        print(f"⚠️ 전사 중 오류 발생: {e}")
        return

    # === 줄바꿈 처리 (세그먼트 기반) ===
    MAX_COL = 100
    wrapper = textwrap.TextWrapper(width=MAX_COL, break_long_words=True, break_on_hyphens=False)

    lines = []
    for seg in segments:
        text = (seg.text or "").strip()
        if text:
            lines.append(wrapper.fill(text))

    output_text = "\n".join(lines) if lines else ""

    base_filename = os.path.splitext(input_filename)[0]
    output_path = os.path.join(output_dir, f"{base_filename}.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_text + "\n")

    print(f"✅ 전사 완료! 결과가 저장되었습니다: {output_path}")

if __name__ == "__main__":
    while True:
        user_input = input("\n변환할 오디오/비디오 파일 이름을 입력하세요 (예: sample.mp3): ")
        input_path = os.path.join("./download", user_input)

        if not os.path.isfile(input_path):
            print("❌ 해당 파일이 ./download 폴더에 존재하지 않습니다.")
            continue

        if not user_input.lower().endswith(VALID_EXTENSIONS):
            print(f"❗ 지원하지 않는 확장자입니다. 지원 형식: {', '.join(VALID_EXTENSIONS)}")
            continue

        transcribe_audio(user_input)
        break
