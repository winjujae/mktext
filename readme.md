# mktext — Faster-Whisper로 음성 녹음 전사문 추출하기
`download/`에 넣은 오디오/영상 파일을 `output/`에 한글 자막 텍스트(.txt)로 변환
(faster-whisper + VAD, 줄바꿈 100자 기준)

---

## 폴더 구조
```bash
mktext/
├─ download/ # 입력 파일(예: 회의.m4a, 강의.mp3 등)
├─ output/ # 변환 결과(.txt)
├─ mktext.py # 실행 스크립트
└─ requirements.txt
```

## 의존성
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 시스템에 ffmpeg가 없으면 설치
- macOS: brew install ffmpeg 
- Ubuntu: sudo apt-get update && sudo apt-get install -y ffmpeg
- Windows: winget이나 choco로 설치하거나 바이너리 추가

### 사용법
1. 변환 파일 이동 download/
2. python mktext.py
3. download/"파일명"
4. 결과 : output/"파일명".txt

