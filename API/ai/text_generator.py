import json
from io import BytesIO
from wsgiref.util import FileWrapper
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from flask import Flask, request, jsonify, Response
from comtypes import CoInitialize
from requests_toolbelt import MultipartEncoder
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from datetime import datetime
from utilities import *
import speech_recognition
import pyttsx3
import torch
import soundfile

import requests_toolbelt

app = Flask(__name__)
project_directory = create_project_directory_path("MeetAI")
conversation_tokenizer = None
conversation_model = None
conversation_user_input = None
conversation_bot_input_ids = None
conversation_chat_history = None
conversation_started = False
conversation_step = 0


@app.route('/generate_story/', methods=['POST'])
def generate_story():
    request_data = request.get_json()
    request_seed = request_data["seed"]
    request_length = request_data["length"]
    request_model = request_data["model"]

    if request_seed == "" or request_length == "" or request_model == "":
        return jsonify({'status': 'Unable to generate story', 'story': '-'})

    if request_seed is None or request_length is None or request_model is None:
        return jsonify({'status': 'Unable to generate story', 'story': '-'})

    if int(request_length) < 50:
        return jsonify({'status': 'Unable to generate story', 'story': '-'})

    try:
        generator = pipeline('text-generation', model=request_model)
        response = generator(request_seed, do_sample=True, max_length=int(request_length), pad_token_id=50256)
        return jsonify({
            'status': 'Story generated successfully',
            'story': sanitize(response[0]['generated_text'])
        })
    except Exception as error:
        print(error)
        return jsonify({'status': 'Unable to generate story', 'story': '-'})


@app.route('/conversation/', methods=['POST'])
def conversation():
    request_data = request.get_json()
    request_input = request_data["input"]
    request_model = request_data["model"]

    if request_input is None or request_model is None or request_input == "" or request_model == "":
        return jsonify({'status': 'Unable to generate answer', 'output': '-'})

    global conversation_tokenizer
    global conversation_model
    global conversation_user_input
    global conversation_bot_input_ids
    global conversation_chat_history
    global conversation_started
    global conversation_step

    try:
        if not conversation_started:
            conversation_tokenizer = AutoTokenizer.from_pretrained(request_model, padding_side='left')
            conversation_model = AutoModelForCausalLM.from_pretrained(request_model)
            conversation_started = True

        conversation_user_input = conversation_tokenizer.encode(
            request_input + conversation_tokenizer.eos_token,
            return_tensors='pt',
            pad_to_max_length=False
        )
        conversation_bot_input_ids = torch.cat([
            conversation_chat_history,
            conversation_user_input],
            dim=-1
        ) if conversation_step > 0 else conversation_user_input
        conversation_chat_history = conversation_model.generate(
            conversation_bot_input_ids, max_length=100,
            pad_token_id=conversation_tokenizer.eos_token_id,
            no_repeat_ngram_size=4,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8
        )
        response = conversation_tokenizer.decode(
            conversation_chat_history[:, conversation_bot_input_ids.shape[-1]:][0],
            skip_special_tokens=True,
            padding_side='left'
        )
        conversation_step = conversation_step + 1
        return jsonify({'status': 'Answer generated successfully', 'output': sanitize(response)})
    except Exception as error:
        print(error)
        return jsonify({'status': 'Unable to generate answer', 'output': '-'})


@app.route('/speech_to_text/', methods=['POST'])
def speech_to_text():
    try:
        # Save uploaded file
        path = project_directory + '\\' + datetime.now().strftime("audio_%d-%m-%Y_%H-%M-%S.wav")
        with open(path, 'wb') as file:
            file.write(request.get_data(cache=False, as_text=False, parse_form_data=False))

        # Resample file
        data, samplerate = soundfile.read(path)
        soundfile.write(path, data, samplerate, subtype='PCM_16')

        # Speech recognition
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.AudioFile(path) as source:
            audio_data = recognizer.record(source)
            response = recognizer.recognize_google(audio_data)
        return jsonify({'status': 'Speech recognized successfully', 'text': response})
    except Exception as error:
        print(error)
        return jsonify({'status': 'Unable to recognize speech', 'text': '-'})


@app.route('/generate_speech/', methods=['POST'])
def generate_speech():
    request_data = request.get_json()
    request_text = request_data["text"]
    request_voice = int(request_data["voice"])
    request_rate = int(request_data["rate"])

    if request_text is None or request_voice is None or request_rate is None or request_text == "":
        return jsonify({'status': 'Unable to generate speech', 'src': '-', 'len': 0.0})

    if request_voice != 0 and request_voice != 1:
        return jsonify({'status': 'Unable to generate speech', 'src': '-', 'len': 0.0})

    try:
        CoInitialize()
        engine = pyttsx3.init()
        if not change_voice(engine, "English", request_voice):
            return jsonify({'status': 'Unable to generate speech', 'src': '-', 'len': 0.0})
        engine.setProperty('rate', request_rate)
        path = project_directory + '\\' + datetime.now().strftime("audio_%d-%m-%Y_%H-%M-%S.wav")
        engine.save_to_file(request_text, path)
        engine.runAndWait()
        return jsonify({'status': 'Speech generated successfully', 'src': path, 'len': audio_duration(path)})
    except Exception as error:
        print(error)
        return jsonify({'status': 'Unable to generate speech', 'src': '-', 'len': 0.0})



@app.route('/open_ai_conversation/', methods=['POST'])
def open_ai_conversation():
    return jsonify({
        "status": "",
        "len": 0.0,
        "src": "",
        "text": "",
        "timestamps": [{}]
    })

@app.route('/fake_request/', methods=['GET'])
def fake_request():
    return jsonify({
        "status": "OK",
        "len": 68.22648526077097,
        "src": "C:\\Users\\Karol\\MeetAI\\audio_31-07-2023_23-54-47.wav",
        "text": "Sure, I'd recommend the movie 'Inception' directed by Christopher Nolan. It's a mind-bending, action-packed sci-fi thriller that will keep you on the edge of your seat from start to finish. The film follows Dom Cobb, played by Leonardo DiCaprio, a skilled thief who enters people's dreams to steal their secrets. However, this time, he's given a unique task - not to steal an idea, but to plant one in someone's mind. As he delves into the subconscious of his target, the line between reality and dreams blurs, leading to a series of stunning visual sequences and intense psychological drama. What makes 'Inception' so captivating is its thought-provoking exploration of human emotions and the power of the mind. The intricate plot weaves layers upon layers of complexity, leaving you questioning what is real and what is merely a construct of the subconscious. The outstanding ensemble cast, including Joseph Gordon-Levitt, Tom Hardy, and Ellen Page, delivers exceptional performances that add depth to the characters and heighten the overall cinematic experience.",
        "timestamps": [{"conf": 1, "end": 0.6, "start": 0.09, "word": "sure"},
                       {"conf": 1, "end": 1.11, "start": 0.93, "word": "i'd"},
                       {"conf": 1, "end": 1.59, "start": 1.11, "word": "recommend"},
                       {"conf": 1, "end": 1.68, "start": 1.59, "word": "the"},
                       {"conf": 1, "end": 2.04, "start": 1.68, "word": "movie"},
                       {"conf": 1, "end": 2.58, "start": 2.04, "word": "inception"},
                       {"conf": 1, "end": 3.09, "start": 2.58, "word": "directed"},
                       {"conf": 1, "end": 3.24, "start": 3.09, "word": "by"},
                       {"conf": 1, "end": 3.81, "start": 3.24, "word": "christopher"},
                       {"conf": 1, "end": 4.26, "start": 3.81, "word": "nolan"},
                       {"conf": 1, "end": 5.28, "start": 5.07, "word": "it's"},
                       {"conf": 1, "end": 5.34, "start": 5.28, "word": "a"},
                       {"conf": 1, "end": 5.64, "start": 5.34, "word": "mind"},
                       {"conf": 1, "end": 6.09, "start": 5.64, "word": "bending"},
                       {"conf": 1, "end": 6.81, "start": 6.42, "word": "action"},
                       {"conf": 1, "end": 7.14, "start": 6.81, "word": "packed"},
                       {"conf": 1, "end": 7.65, "start": 7.14, "word": "sci-fi"},
                       {"conf": 1, "end": 8.04, "start": 7.65, "word": "thriller"},
                       {"conf": 1, "end": 8.19, "start": 8.04, "word": "that"},
                       {"conf": 1, "end": 8.34, "start": 8.19, "word": "will"},
                       {"conf": 1, "end": 8.61, "start": 8.34, "word": "keep"},
                       {"conf": 1, "end": 8.79, "start": 8.61, "word": "you"},
                       {"conf": 1, "end": 8.91, "start": 8.79, "word": "on"},
                       {"conf": 1, "end": 9.09, "start": 8.91, "word": "the"},
                       {"conf": 1, "end": 9.3, "start": 9.09, "word": "edge"},
                       {"conf": 1, "end": 9.42, "start": 9.3, "word": "of"},
                       {"conf": 1, "end": 9.63, "start": 9.42, "word": "your"},
                       {"conf": 1, "end": 9.93, "start": 9.63, "word": "seat"},
                       {"conf": 1, "end": 10.17, "start": 9.93, "word": "from"},
                       {"conf": 1, "end": 10.5, "start": 10.17, "word": "start"},
                       {"conf": 1, "end": 10.62, "start": 10.5, "word": "to"},
                       {"conf": 1, "end": 11.16, "start": 10.62, "word": "finish"},
                       {"conf": 1, "end": 12.06, "start": 11.91, "word": "the"},
                       {"conf": 1, "end": 12.39, "start": 12.06, "word": "film"},
                       {"conf": 1, "end": 12.84, "start": 12.39, "word": "follows"},
                       {"conf": 1, "end": 13.2, "start": 12.84, "word": "deal"},
                       {"conf": 1, "end": 13.35, "start": 13.2, "word": "m"},
                       {"conf": 1, "end": 13.8, "start": 13.35, "word": "cobb"},
                       {"conf": 1, "end": 14.46, "start": 14.1, "word": "played"},
                       {"conf": 1, "end": 14.61, "start": 14.46, "word": "by"},
                       {"conf": 1, "end": 15.18, "start": 14.61, "word": "leonardo"},
                       {"conf": 1, "end": 15.93, "start": 15.18, "word": "dicaprio"},
                       {"conf": 1, "end": 16.38, "start": 16.29, "word": "a"},
                       {"conf": 1, "end": 16.71, "start": 16.38, "word": "skilled"},
                       {"conf": 1, "end": 17.01, "start": 16.71, "word": "thief"},
                       {"conf": 1, "end": 17.16, "start": 17.01, "word": "who"},
                       {"conf": 1, "end": 17.52, "start": 17.16, "word": "enters"},
                       {"conf": 1, "end": 17.94, "start": 17.52, "word": "people's"},
                       {"conf": 1, "end": 18.33, "start": 17.94, "word": "dreams"},
                       {"conf": 1, "end": 18.45, "start": 18.33, "word": "to"},
                       {"conf": 1, "end": 18.75, "start": 18.45, "word": "steal"},
                       {"conf": 1, "end": 18.93, "start": 18.75, "word": "their"},
                       {"conf": 1, "end": 19.62, "start": 18.93, "word": "secrets"},
                       {"conf": 1, "end": 21.03, "start": 20.43, "word": "however"},
                       {"conf": 1, "end": 21.6, "start": 21.36, "word": "this"},
                       {"conf": 1, "end": 22.02, "start": 21.6, "word": "time"},
                       {"conf": 0.700509, "end": 22.65, "start": 22.32, "word": "he's"},
                       {"conf": 1, "end": 22.95, "start": 22.65, "word": "given"},
                       {"conf": 1, "end": 23.01, "start": 22.95, "word": "a"},
                       {"conf": 1, "end": 23.37, "start": 23.01, "word": "unique"},
                       {"conf": 1, "end": 23.91, "start": 23.37, "word": "task"},
                       {"conf": 1, "end": 24.54, "start": 24.21, "word": "not"},
                       {"conf": 1, "end": 24.63, "start": 24.54, "word": "to"},
                       {"conf": 1, "end": 24.93, "start": 24.63, "word": "steal"},
                       {"conf": 1, "end": 25.05, "start": 24.93, "word": "an"},
                       {"conf": 1, "end": 25.56, "start": 25.05, "word": "idea"},
                       {"conf": 1, "end": 26.1, "start": 25.89, "word": "but"},
                       {"conf": 1, "end": 26.19, "start": 26.1, "word": "to"},
                       {"conf": 1, "end": 26.55, "start": 26.19, "word": "plant"},
                       {"conf": 1, "end": 26.79, "start": 26.55, "word": "one"},
                       {"conf": 1, "end": 26.91, "start": 26.79, "word": "in"},
                       {"conf": 1, "end": 27.42, "start": 26.91, "word": "someone's"},
                       {"conf": 1, "end": 27.9, "start": 27.42, "word": "mind"},
                       {"conf": 1, "end": 28.89, "start": 28.71, "word": "as"},
                       {"conf": 1, "end": 29.04, "start": 28.89, "word": "he"},
                       {"conf": 1, "end": 29.43, "start": 29.04, "word": "delves"},
                       {"conf": 1, "end": 29.64, "start": 29.43, "word": "into"},
                       {"conf": 1, "end": 29.73, "start": 29.64, "word": "the"},
                       {"conf": 0.950254, "end": 30.51, "start": 29.73, "word": "subconscious"},
                       {"conf": 1, "end": 30.6, "start": 30.51, "word": "of"},
                       {"conf": 1, "end": 30.78, "start": 30.6, "word": "his"},
                       {"conf": 1, "end": 31.26, "start": 30.78, "word": "target"},
                       {"conf": 1, "end": 31.74, "start": 31.59, "word": "the"},
                       {"conf": 1, "end": 32.04, "start": 31.74, "word": "line"},
                       {"conf": 1, "end": 32.4, "start": 32.04, "word": "between"},
                       {"conf": 1, "end": 32.94, "start": 32.4, "word": "reality"},
                       {"conf": 1, "end": 33.06, "start": 32.94, "word": "and"},
                       {"conf": 1, "end": 33.45, "start": 33.06, "word": "dreams"},
                       {"conf": 1, "end": 33.99, "start": 33.45, "word": "blurs"},
                       {"conf": 1, "end": 34.65, "start": 34.29, "word": "leading"},
                       {"conf": 1, "end": 34.8, "start": 34.65, "word": "to"},
                       {"conf": 1, "end": 34.83, "start": 34.8, "word": "a"},
                       {"conf": 1, "end": 35.28, "start": 34.83, "word": "series"},
                       {"conf": 1, "end": 35.43, "start": 35.28, "word": "of"},
                       {"conf": 1, "end": 35.79, "start": 35.43, "word": "stunning"},
                       {"conf": 1, "end": 36.21, "start": 35.79, "word": "visual"},
                       {"conf": 1, "end": 36.84, "start": 36.21, "word": "sequences"},
                       {"conf": 0.400708, "end": 36.99, "start": 36.84, "word": "and"},
                       {"conf": 1, "end": 37.41, "start": 36.99, "word": "intense"},
                       {"conf": 1, "end": 38.13, "start": 37.41, "word": "psychological"},
                       {"conf": 1, "end": 38.61, "start": 38.13, "word": "drama"},
                       {"conf": 1, "end": 39.63, "start": 39.39, "word": "what"},
                       {"conf": 1, "end": 39.9, "start": 39.63, "word": "makes"},
                       {"conf": 0.811456, "end": 40.02, "start": 39.9, "word": "him"},
                       {"conf": 0.969282, "end": 40.32, "start": 40.05, "word": "sept"},
                       {"conf": 0.551458, "end": 40.464998, "start": 40.32, "word": "even"},
                       {"conf": 1, "end": 40.71, "start": 40.464998, "word": "so"},
                       {"conf": 1, "end": 41.37, "start": 40.71, "word": "captivating"},
                       {"conf": 0.997096, "end": 41.55, "start": 41.37, "word": "is"},
                       {"conf": 1, "end": 41.7, "start": 41.55, "word": "it's"},
                       {"conf": 1, "end": 42, "start": 41.7, "word": "thought"},
                       {"conf": 1, "end": 42.48, "start": 42, "word": "provoking"},
                       {"conf": 1, "end": 43.23, "start": 42.48, "word": "exploration"},
                       {"conf": 1, "end": 43.35, "start": 43.23, "word": "of"},
                       {"conf": 1, "end": 43.68, "start": 43.35, "word": "human"},
                       {"conf": 1, "end": 44.22, "start": 43.68, "word": "emotions"},
                       {"conf": 0.500809, "end": 44.34, "start": 44.22, "word": "in"},
                       {"conf": 1, "end": 44.43, "start": 44.34, "word": "the"},
                       {"conf": 1, "end": 44.82, "start": 44.43, "word": "power"},
                       {"conf": 1, "end": 44.94, "start": 44.82, "word": "of"},
                       {"conf": 1, "end": 45.03, "start": 44.94, "word": "the"},
                       {"conf": 1, "end": 45.48, "start": 45.03, "word": "mind"},
                       {"conf": 1, "end": 46.47, "start": 46.26, "word": "the"},
                       {"conf": 1, "end": 46.89, "start": 46.47, "word": "intricate"},
                       {"conf": 1, "end": 47.22, "start": 46.89, "word": "plot"},
                       {"conf": 1, "end": 47.52, "start": 47.22, "word": "weaves"},
                       {"conf": 1, "end": 47.94, "start": 47.52, "word": "layers"},
                       {"conf": 1, "end": 48.27, "start": 47.94, "word": "upon"},
                       {"conf": 1, "end": 48.66, "start": 48.27, "word": "layers"},
                       {"conf": 1, "end": 48.78, "start": 48.66, "word": "of"},
                       {"conf": 1, "end": 49.59, "start": 48.78, "word": "complexity"},
                       {"conf": 1, "end": 50.28, "start": 49.89, "word": "leaving"},
                       {"conf": 1, "end": 50.43, "start": 50.28, "word": "you"},
                       {"conf": 1, "end": 51, "start": 50.43, "word": "questioning"},
                       {"conf": 1, "end": 51.18, "start": 51, "word": "what"},
                       {"conf": 1, "end": 51.3, "start": 51.18, "word": "is"},
                       {"conf": 1, "end": 51.57, "start": 51.3, "word": "real"},
                       {"conf": 1, "end": 51.72, "start": 51.57, "word": "and"},
                       {"conf": 1, "end": 51.9, "start": 51.72, "word": "what"},
                       {"conf": 1, "end": 51.99, "start": 51.9, "word": "is"},
                       {"conf": 1, "end": 52.38, "start": 51.99, "word": "merely"},
                       {"conf": 1, "end": 52.44, "start": 52.38, "word": "a"},
                       {"conf": 1, "end": 53.07, "start": 52.44, "word": "construct"},
                       {"conf": 1, "end": 53.16, "start": 53.07, "word": "of"},
                       {"conf": 1, "end": 53.25, "start": 53.16, "word": "the"},
                       {"conf": 1, "end": 54.18, "start": 53.25, "word": "subconscious"},
                       {"conf": 1, "end": 55.17, "start": 54.96, "word": "the"},
                       {"conf": 1, "end": 55.83, "start": 55.17, "word": "outstanding"},
                       {"conf": 1, "end": 56.4, "start": 55.83, "word": "ensemble"},
                       {"conf": 1, "end": 56.94, "start": 56.4, "word": "cast"},
                       {"conf": 1, "end": 57.84, "start": 57.27, "word": "including"},
                       {"conf": 1, "end": 58.29, "start": 57.84, "word": "joseph"},
                       {"conf": 1, "end": 58.62, "start": 58.29, "word": "gordon"},
                       {"conf": 1, "end": 59.04, "start": 58.62, "word": "levitt"},
                       {"conf": 1, "end": 59.67, "start": 59.37, "word": "tom"},
                       {"conf": 1, "end": 60.15, "start": 59.67, "word": "hardy"},
                       {"conf": 0.794126, "end": 60.63, "start": 60.51, "word": "and"},
                       {"conf": 1, "end": 60.93, "start": 60.63, "word": "ellen"},
                       {"conf": 1, "end": 61.44, "start": 60.93, "word": "page"},
                       {"conf": 1, "end": 62.25, "start": 61.74, "word": "delivers"},
                       {"conf": 1, "end": 62.82, "start": 62.25, "word": "exceptional"},
                       {"conf": 1, "end": 63.57, "start": 62.82, "word": "performances"},
                       {"conf": 1, "end": 63.75, "start": 63.57, "word": "that"},
                       {"conf": 1, "end": 63.93, "start": 63.75, "word": "add"},
                       {"conf": 1, "end": 64.26, "start": 63.93, "word": "depth"},
                       {"conf": 1, "end": 64.38, "start": 64.26, "word": "to"},
                       {"conf": 1, "end": 64.47, "start": 64.38, "word": "the"},
                       {"conf": 1, "end": 65.07, "start": 64.47, "word": "characters"},
                       {"conf": 0.745531, "end": 65.19, "start": 65.07, "word": "and"},
                       {"conf": 0.602282, "end": 65.52, "start": 65.19, "word": "heighten"},
                       {"conf": 1, "end": 65.67, "start": 65.52, "word": "the"},
                       {"conf": 1, "end": 66.15, "start": 65.67, "word": "overall"},
                       {"conf": 1, "end": 66.69, "start": 66.15, "word": "cinematic"},
                       {"conf": 1, "end": 67.5, "start": 66.69, "word": "experience"}]
    })

