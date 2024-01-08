from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# TODO Finish implementation of TextGenerator
# TODO Text generation Microsoft
# TODO Text generation Facebook (LLAMA)
# TODO Text generation OpenAI
# TODO Code refactor and check input


class TextGenerator:
    def __init__(self, path, openAI):
        self.path = path
        self.openAI = openAI
        self.openai_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
        # Supported models
        self.openai_models = [
            "gpt-3.5-turbo",
            "gpt-4_turbo",
            "gpt-4",
        ]
        self.microsoft_models = [
            "microsoft/DialoGPT-large",
            "microsoft/DialoGPT-medium",
            "microsoft/DialoGPT-small",
        ]
        self.facebook_models = [

        ]
        # DialoGPT
        self.dialo_ai_tokenizer = None
        self.dialo_ai_model = None
        self.dialo_ai_user_input = None
        self.dialo_ai_bot_input_ids = None
        self.dialo_ai_chat_history = None
        self.dialo_ai_started = False
        self.dialo_ai_step = 0

    def generate(self, model, query):
        model = model.lower().replace(" ", "_")

        if model == "dummy":
            return {'status': 'Text generated successfully', 'text': 'Example'}

        if model in self.microsoft_models:
            return self.microsoft_dialo(model, query)

        if model in self.facebook_models:
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

    def facebook_blenderbot(self, model, query):
        pass

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

    @staticmethod
    def sanitize(string):
        characters = ['\"', '\'', '\\', '\r']
        for char in characters:
            string = string.replace(char, " ")
        return string
