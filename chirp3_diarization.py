import os
from google.api_core.client_options import ClientOptions
from google.cloud import speech_v2
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.cloud import storage

# ==============================================================================
# ⚠️ 주의: 다음 변수들을 사용자의 환경에 맞게 수정해주세요.
# ==============================================================================
PROJECT_ID = "YOUR_PROJECT_ID"       # Google Cloud 프로젝트 ID
GCS_BUCKET_NAME = "YOUR_BUCKET_NAME" # GCS 버킷 이름
LOCAL_AUDIO_FILE = "/path/to/your/audio.wav" # 로컬 오디오 파일 경로
LOCATION = "us" # API를 호출할 리전 (예: "us", "europe-west4")
# ==============================================================================

GCS_AUDIO_URI = f"gs://{GCS_BUCKET_NAME}/{os.path.basename(LOCAL_AUDIO_FILE)}"

def upload_to_gcs(bucket_name: str, source_file: str, destination_blob_name: str):
    """로컬 파일을 Google Cloud Storage에 업로드합니다."""
    print(f"Uploading {source_file} to gs://{bucket_name}/{destination_blob_name}...")
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file)
        print(f"✅ File uploaded successfully.")
    except Exception as e:
        print(f"❌ GCS upload failed: {e}")
        raise

def transcribe_diarize_from_example(gcs_uri: str):
    """사용자가 제공한 예시를 기반으로 화자 분리를 수행합니다."""
    print("🚀 Initializing Speech-to-Text client...")
    client = SpeechClient(
        client_options=ClientOptions(
            api_endpoint=f"{LOCATION}-speech.googleapis.com",
        )
    )

    # 예시에 따라 RecognitionConfig를 설정합니다.
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["ko-KR", "en-US"],
        model="chirp_3",
        features=cloud_speech.RecognitionFeatures(
            # 비어있는 DiarizationConfig로 화자 분리를 활성화합니다.
            diarization_config=cloud_speech.SpeakerDiarizationConfig(),
        ),
    )

    file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)

    # 기본 Recognizer를 사용하여 요청을 생성합니다.
    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{PROJECT_ID}/locations/{LOCATION}/recognizers/_",
        config=config,
        files=[file_metadata],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )

    print("🛰️  Sending transcription request...")
    operation = client.batch_recognize(request=request)
    print("🕒 Waiting for operation to complete...")
    response = operation.result(timeout=300)
    print("✅ Transcription complete.")

    print("\n--- Transcription & Diarization Result ---")
    result_for_file = response.results.get(gcs_uri)
    if not result_for_file or not result_for_file.transcript.results:
        print("No transcription results found.")
        return

    transcript_results = result_for_file.transcript.results
    
    print("🗣️ Speaker-separated utterances:")
    current_speaker = None
    current_utterance = ""
    for result in transcript_results:
        for word in result.alternatives[0].words:
            print("🗣️ Speaker-separated utterances:")
    current_speaker = None
    current_utterance = ""
    for result in transcript_results:
        for word in result.alternatives[0].words:
            if current_speaker != word.speaker_label and current_speaker is not None:
                print(f"  [Speaker {current_speaker}]: {current_utterance.strip()}")
                current_utterance = ""
            current_speaker = word.speaker_label
            current_utterance += f" {word.word}"
    if current_utterance:
        print(f"  [Speaker {current_speaker}]: {current_utterance.strip()}")

if __name__ == "__main__":
    if not os.path.exists(LOCAL_AUDIO_FILE):
        print(f"🚨 Error: Audio file not found at '{LOCAL_AUDIO_FILE}'.")
    else:
        try:
            upload_to_gcs(GCS_BUCKET_NAME, LOCAL_AUDIO_FILE, os.path.basename(LOCAL_AUDIO_FILE))
            transcribe_diarize_from_example(GCS_AUDIO_URI)
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
