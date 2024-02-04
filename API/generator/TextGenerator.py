from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


class TextGenerator:
    def __init__(self, path, openAI):
        self.path = path
        self.openAI = openAI
        self.openai_messages = [{
            "role": "system",
            "content": "You are a AI companion in video game. "
                       "Answer player questions in a friendly way. "
                       "Avoid answers in which you say you are AI. "
                       "Try to keep your answers short"
        }]
        # Supported models
        self.openai_models = [
            "gpt-3.5-turbo",
            "gpt-4_turbo",
            "gpt-4",
        ]
        self.microsoft_models = [
            "microsoft/dialogpt-large",
            "microsoft/dialogpt-medium",
            "microsoft/dialogpt-small",
        ]
        self.blenderbot_models = [
            "facebook/blenderbot-400m-distill",
            "facebook/blenderbot-1b-distill",
            "facebook/blenderbot-3b",
        ]
        # DialoGPT
        self.dialo_ai_tokenizer = None
        self.dialo_ai_model = None
        self.dialo_ai_user_input = None
        self.dialo_ai_bot_input_ids = None
        self.dialo_ai_chat_history = None
        self.dialo_ai_started = False
        self.dialo_ai_step = 0
        # Blenderbot
        self.blenderbot_model = None
        self.blenderbot_chat = None

    def generate(self, model, query):
        model = model.lower().replace(" ", "_")

        if model == "dummy":
            return {'status': 'Text generated successfully', 'text': 'Example'}

        if model in self.microsoft_models:
            return self.microsoft_dialo(model, query)

        if model in self.blenderbot_models:
            return self.facebook_blenderbot(model, query)

        if model in self.openai_models:
            return self.openai_gpt(model, query)

        return {'status': 'Unable to find model'}

    def microsoft_dialo(self, model, query):
        try:
            if not self.dialo_ai_started:
                self.dialo_ai_tokenizer = AutoTokenizer.from_pretrained(model, padding_side='left')
                self.dialo_ai_model = AutoModelForCausalLM.from_pretrained(model)
                self.dialo_ai_started = True

            self.dialo_ai_user_input = self.dialo_ai_tokenizer.encode(
                query + self.dialo_ai_tokenizer.eos_token,
                return_tensors='pt',
                pad_to_max_length=False
            )
            self.dialo_ai_bot_input_ids = torch.cat([
                self.dialo_ai_chat_history,
                self.dialo_ai_user_input],
                dim=-1
            ) if self.dialo_ai_step > 0 else self.dialo_ai_user_input
            self.dialo_ai_chat_history = self.dialo_ai_model.generate(
                self.dialo_ai_bot_input_ids, max_length=100,
                pad_token_id=self.dialo_ai_tokenizer.eos_token_id,
                no_repeat_ngram_size=4,
                do_sample=True,
                top_k=100,
                top_p=0.7,
                temperature=0.8
            )
            response = self.dialo_ai_tokenizer.decode(
                self.dialo_ai_chat_history[:, self.dialo_ai_bot_input_ids.shape[-1]:][0],
                skip_special_tokens=True,
                padding_side='left'
            )
            self.dialo_ai_step = self.dialo_ai_step + 1
            return {'status': 'Text generated successfully', 'text': self.sanitize(response)}
        except Exception as e:
            print(f"Dialo returned an error: {e}")
            return {'status': 'Unable to generate text'}

    def openai_gpt(self, model, query):
        self.openai_messages.append({"role": "user", "content": query})

        try:
            response = self.openAI.chat.completions.create(
                model=model,
                messages=self.openai_messages
            )
        except Exception as e:
            print(f"OpenAI API returned an error: {e}")
            return {'status': 'Unable to generate text'}

        response_content = response.choices[0].message.content
        self.openai_messages.append({"role": "assistant", "content": response_content})

        return {'status': 'Text generated successfully', 'text': response_content}

    def facebook_blenderbot(self, model, query):
        if self.blenderbot_model != model:
            self.blenderbot_model = model
            self.blenderbot_chat = pipeline("text2text-generation", model=model)
        try:
            response = self.blenderbot_chat(query)
            return {'status': 'Text generated successfully', 'text': response[0]['generated_text']}
        except Exception as e:
            print(f"OpenAI API returned an error: {e}")
            return {'status': 'Unable to generate text'}

    @staticmethod
    def sanitize(string):
        characters = ['\"', '\'', '\\', '\r']
        for char in characters:
            string = string.replace(char, " ")
        return string
