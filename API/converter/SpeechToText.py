import speech_recognition


# TODO Resample file

class SpeechToText:
    def __init__(self, path, openAI):
        self.path = path
        self.openAI = openAI

    def generate(self, model, filename):
        model = model.lower().replace(" ", "_")
        path = self.path + filename

        if model in "google_cloud_stt":
            return self.google_cloud_stt(path)

        if model in "openai_whisper_cloud_stt":
            return self.openai_cloud_stt(path)

        return {'status': 'Unable to find model', 'text': '-'}

    @staticmethod
    def google_cloud_stt(filepath):
        try:
            recognizer = speech_recognition.Recognizer()
            with speech_recognition.AudioFile(filepath) as source:
                audio_data = recognizer.record(source)
                response = recognizer.recognize_google(audio_data)
                print(response)
            return {'status': 'Speech recognized successfully', 'text': response}
        except Exception as error:
            print(error)
            return {'status': 'Unable to recognize speech', 'text': '-'}

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
            return {'status': 'Unable to recognize speech', 'text': '-'}

        return {'status': 'Speech recognized successfully', 'text': transcript}
