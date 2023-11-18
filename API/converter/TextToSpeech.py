import contextlib
import wave
from comtypes import CoInitialize
from datetime import datetime
import soundfile


class TextToSpeech:
    def __init__(self, path, pyttsx, openAI):
        self.path = path
        self.pyttsx = pyttsx
        self.openAI = openAI
        self.pyttsx_voices = self.pyttsx_find_voices()
        self.openai_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    def get_voices(self):
        return {
            'windows': self.pyttsx_voices,
            'openai': self.openai_voices
        }

    def generate(self, model, voice, text):
        model = model.lower().replace(" ", "_")

        if model in "dummy_tts":
            return {'status': 'Speech generated successfully', 'filename': 'example.wav', 'len': 0.2}

        if model in "windows_tts" and voice in self.pyttsx_voices:
            return self.pyttsx_tts(text, voice)

        if model in "openai_tts" and voice in self.openai_voices:
            return self.openai_tts(text, voice)

        return {'status': 'Unable to find model or voice name'}

    def openai_tts(self, text, voice):
        try:
            response = self.openAI.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
        except Exception as e:
            print(f"OpenAI API returned an error: {e}")
            return {'status': 'Unable to generate speech'}

        path_wav = self.create_path()
        path_flac = path_wav.replace(".wav", ".flac")
        filename = path_wav.replace(self.path, "")
        response.stream_to_file(path_flac)
        self.convert_flac_to_wav(path_flac, path_wav)
        return {'status': 'Speech generated successfully', 'filename': filename, 'len': self.file_duration(path_wav)}

    def pyttsx_find_voices(self):
        voices = []
        for voice in self.pyttsx.getProperty('voices'):
            name = voice.name.split()[1].lower()
            voices.append(name)
        return voices

    def pyttsx_change_voice(self, name):
        for voice in self.pyttsx.getProperty('voices'):
            if name in voice.name.lower():
                self.pyttsx.setProperty('voice', voice.id)
                break

    def pyttsx_tts(self, text, voice):
        try:
            CoInitialize()
            self.pyttsx_change_voice(voice)
            path = self.create_path()
            filename = path.replace(self.path, "")
            self.pyttsx.save_to_file(text, path)
            self.pyttsx.runAndWait()
            return {'status': 'Speech generated successfully', 'filename': filename, 'len': self.file_duration(path)}
        except Exception as error:
            print(error)
            return {'status': 'Unable to generate speech'}

    def create_path(self):
        return self.path + datetime.now().strftime("audio_%d-%m-%Y_%H-%M-%S.wav")

    @staticmethod
    def file_duration(src):
        with contextlib.closing(wave.open(src, 'r')) as file:
            frames = file.getnframes()
            rate = file.getframerate()
            duration = frames / float(rate)
            return duration

    @staticmethod
    def convert_flac_to_wav(flac_file, wav_file):
        audio, sr = soundfile.read(flac_file)
        soundfile.write(wav_file, audio, sr, 'PCM_16')
