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
                       {"conf": 1, "end": 1.59, "start": 1.11, "word": "recommend"}]
    })

