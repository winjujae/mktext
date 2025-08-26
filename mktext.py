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

    # ---- 모델 로드 (하드웨어에 맞게 조정) ----
    # GPU: device="cuda", compute_type="float16"
    # CPU: device="cpu", compute_type="int8_float16" (또는 "int8")
    model_size = "small"  # 필요 시 "base" / "medium" / "large-v3"
    model = WhisperModel(
        model_size,
        device="cpu",              # CPU면 "cpu"
        compute_type="int8",     # CPU면 "int8_float16" 권장
        num_workers=2               # 오디오 디코딩 워커
    )

    print(f"🔊 {input_filename} 파일을 전사 중... (faster-whisper)")

    try:
        segments, info = model.transcribe(
            input_path,
            beam_size=1,             # 빠르게: 그리디
            best_of=1,
            vad_filter=True,         # 무음 구간 필터
            vad_parameters={"min_silence_duration_ms": 500},
            language="ko",           # 알면 지정(모르면 None)
            temperature=0.0,
            condition_on_previous_text=False,
            word_timestamps=False
        )
    except Exception as e:
        print(f"⚠️ 전사 중 오류 발생: {e}")
        return

    # === 줄바꿈 처리 (세그먼트 기반) ===
    MAX_COL = 100
    wrapper = textwrap.TextWrapper(width=MAX_COL, break_long_words=True, break_on_hyphens=False)

    lines = []
    for seg in segments:
        # seg.text는 앞에 공백이 포함될 수 있으니 strip
        lines.append(wrapper.fill(seg.text.strip()))

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
