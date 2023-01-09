from utilities import resample_file
import speech_recognition


class SpeechToText:
    def __init__(self, path, openAI):
        self.path = path
        self.openAI = openAI
        # Supported models
        self.google_models = ["google", "google_stt", "google_cloud_stt"]
        self.openai_models = ["openai", "openai_whisper", "openai_cloud_whisper", "openai_cloud_stt"]

    def generate(self, model, filename):
        model = model.lower().replace(" ", "_")
        path = self.path + filename
        resample_file(path, path)

        if model == "dummy":
            return {'status': 'Speech recognized successfully', 'text': 'example'}

        if model in self.google_models:
            return self.google_cloud_stt(path)

        if model in self.openai_models:
            return self.openai_cloud_stt(path)

        return {'status': 'Unable to find model'}

    @staticmethod
    def google_cloud_stt(filepath):
        try:
            recognizer = speech_recognition.Recognizer()
            with speech_recognition.AudioFile(filepath) as source:
                audio_data = recognizer.record(source)
                response = recognizer.recognize_google(audio_data)
            return {'status': 'Speech recognized successfully', 'text': response}
        except Exception as e:
            print(f"Google API returned an error: {e}")
            return {'status': 'Unable to recognize speech'}

    def openai_cloud_stt(self, filepath):
        try:
            audio_file = open(filepath, "rb")
            transcript = self.openAI.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        except Exception as e:
            print(f"OpenAI API returned an error: {e}")
            return {'status': 'Unable to recognize speech'}

        return {'status': 'Speech recognized successfully', 'text': transcript}
