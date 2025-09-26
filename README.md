# Chirp3 화자 분리 (Speaker Diarization) 샘플

이 프로젝트는 Google Cloud의 Chirp3 모델을 사용하여 오디오 파일에서 화자를 분리하는 방법을 보여주는 Python 스크립트 예제입니다.
- [Using Chirp3](https://cloud.google.com/speech-to-text/v2/docs/chirp_3-model#using_chirp_3)

## 주요 기능

- 로컬 오디오 파일을 Google Cloud Storage(GCS)에 업로드합니다.
- Speech-to-Text V2 API와 Chirp3 모델을 사용하여 화자 분리가 포함된 음성 인식을 수행합니다.
- 인식된 텍스트를 화자별로 구분하여 출력합니다.

## 사전 준비

### 1. 라이브러리 설치

스크립트를 실행하려면 다음 Python 라이브러리가 필요합니다.

```bash
pip install google-api-core google-cloud-speech-v2 google-cloud-storage
```

### 2. Google Cloud 설정

- [Google Cloud 프로젝트](https://console.cloud.google.com/projectcreate)를 생성하고 결제를 활성화하세요.
- [Speech-to-Text API](https://console.cloud.google.com/flows/enableapi?apiid=speech.googleapis.com)를 활성화하세요.
- [Cloud Storage 버킷](https://console.cloud.google.com/storage/create-bucket)을 생성하세요.
- **API 인증 설정:** Google Cloud API를 호출하기 위해 인증을 설정해야 합니다. 다음 두 가지 방법 중 하나를 선택하세요.

  **방법 1: 서비스 계정 키 (JSON) 사용**

  1.  [서비스 계정을 생성](https://console.cloud.google.com/iam-admin/serviceaccounts/create)하고 키(JSON 파일)를 다운로드합니다. 이 서비스 계정에는 `Speech-to-Text API 관리자` 및 `스토리지 객체 생성자` 역할이 필요합니다.
  2.  다운로드한 키 파일의 경로를 환경 변수로 설정합니다. 이 환경 변수는 스크립트를 실행하는 터미널 세션에 적용됩니다.

      ```bash
      export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
      ```

  **방법 2: Application Default Credentials (ADC) 사용**

  로컬 개발 환경에서 개인 사용자 계정으로 인증하는 간편한 방법입니다.

  1.  [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)를 설치합니다.
  2.  다음 명령어를 실행하여 gcloud CLI에 로그인하고 ADC를 설정합니다. 브라우저가 열리면 Google 계정으로 로그인하여 인증을 완료하세요.

      ```bash
      gcloud auth application-default login
      ```

## 사용 방법

1.  `chirp3_diarization.py` 파일을 열고 상단의 변수들을 사용자의 환경에 맞게 수정합니다.

    ```python
    # ==============================================================================
    # ⚠️ 주의: 다음 변수들을 사용자의 환경에 맞게 수정해주세요.
    # ==============================================================================
    PROJECT_ID = "YOUR_PROJECT_ID"       # Google Cloud 프로젝트 ID
    GCS_BUCKET_NAME = "YOUR_BUCKET_NAME" # GCS 버킷 이름
    LOCAL_AUDIO_FILE = "/path/to/your/audio.wav" # 로컬 오디오 파일 경로
    LOCATION = "us" # API를 호출할 리전 (예: "us", "europe-west4")
    # ==============================================================================
    ```

2.  스크립트를 실행합니다.

    ```bash
    python chirp3_diarization.py
    ```

## 실행 결과 예시

스크립트가 성공적으로 실행되면 다음과 같은 결과가 출력됩니다.

```
Uploading /path/to/your/audio.wav to gs://YOUR_BUCKET_NAME/audio.wav...
✅ File uploaded successfully.
🚀 Initializing Speech-to-Text client...
🛰️  Sending transcription request...
🕒 Waiting for operation to complete...
✅ Transcription complete.

--- Transcription & Diarization Result ---
🗣️ Speaker-separated utterances:
  [Speaker 1]: 안녕하세요
  [Speaker 2]: 네 안녕하세요 반갑습니다
  [Speaker 1]: 오늘 날씨가 좋네요
```
*(위 결과는 예시이며, 실제 출력은 오디오 파일의 내용과 화자에 따라 달라집니다.)*
