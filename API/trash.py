#####################################################################
# MAIN
#####################################################################
@app.route('/experiment/', methods=['POST'])
def experiment():
    try:
        requests_toolbelt.MultipartDecoder

        request_json = json.loads(request.values.get('json'))
        input_type = request_json["InputType"]
        input_content = request_json["InputContent"]

        if input_type == "Microphone":
            # TODO: Audio to text
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save(uploaded_file.filename)
            else:
                return jsonify({'status': 'file error'})
            # TODO: Implementation
            return jsonify({'status': 'succ'})

        if input_type == "Keyboard":
            if input_content == "":
                return jsonify({'status': 'content empty'})
            # TODO: Implementation
            return jsonify({'status': 'succ'})

        return jsonify({'status': 'unable to parse input_type'})

    except:
        return jsonify({'status': 'python script throw exception '})



#################################################################
# TEXT GENERATOR
#################################################################
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

