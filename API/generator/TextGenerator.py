

class TextGenerator:
    def __init__(self, path, openAI):
        self.path = path
        self.openAI = openAI

    def generate(self, model, query):
        model = model.lower().replace(" ", "_")

        if "dummy" in model:
            return {'status': 'Text generated successfully', 'text': 'Example'}






# from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
# import torch
#
# conversation_tokenizer = None
# conversation_model = None
# conversation_user_input = None
# conversation_bot_input_ids = None
# conversation_chat_history = None
# conversation_started = False
# conversation_step = 0
# @app.route('/conversation/', methods=['POST'])
# def conversation():
#     request_data = request.get_json()
#     request_input = request_data["input"]
#     request_model = request_data["model"]
#
#     if request_input is None or request_model is None or request_input == "" or request_model == "":
#         return jsonify({'status': 'Unable to generate answer', 'output': '-'})
#
#     global conversation_tokenizer
#     global conversation_model
#     global conversation_user_input
#     global conversation_bot_input_ids
#     global conversation_chat_history
#     global conversation_started
#     global conversation_step
#
#     try:
#         if not conversation_started:
#             conversation_tokenizer = AutoTokenizer.from_pretrained(request_model, padding_side='left')
#             conversation_model = AutoModelForCausalLM.from_pretrained(request_model)
#             conversation_started = True
#
#         conversation_user_input = conversation_tokenizer.encode(
#             request_input + conversation_tokenizer.eos_token,
#             return_tensors='pt',
#             pad_to_max_length=False
#         )
#         conversation_bot_input_ids = torch.cat([
#             conversation_chat_history,
#             conversation_user_input],
#             dim=-1
#         ) if conversation_step > 0 else conversation_user_input
#         conversation_chat_history = conversation_model.generate(
#             conversation_bot_input_ids, max_length=100,
#             pad_token_id=conversation_tokenizer.eos_token_id,
#             no_repeat_ngram_size=4,
#             do_sample=True,
#             top_k=100,
#             top_p=0.7,
#             temperature=0.8
#         )
#         response = conversation_tokenizer.decode(
#             conversation_chat_history[:, conversation_bot_input_ids.shape[-1]:][0],
#             skip_special_tokens=True,
#             padding_side='left'
#         )
#         conversation_step = conversation_step + 1
#         return jsonify({'status': 'Answer generated successfully', 'output': sanitize(response)})
#     except Exception as error:
#         print(error)
#         return jsonify({'status': 'Unable to generate answer', 'output': '-'})
#
#
# def sanitize(string):
#     characters = ['\"', '\'', '\\', '\r']
#     for char in characters:
#         string = string.replace(char, " ")
#     return string
