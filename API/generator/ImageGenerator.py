from diffusers import StableDiffusionPipeline
from datetime import datetime
from utilities import *
import requests
import torch


class ImageGenerator:
    def __init__(self, path, openAI):
        self.path = path
        self.openAI = openAI
        # Supported models
        self.stable_diffusion_models = [
            "CompVis/stable-diffusion-v1-4",
            "runwayml/stable-diffusion-v1-5",
        ]
        self.openai_models = [
            "dall-e-2",
            "dall-e-3"
        ]

    def generate(self, model, description):
        model = model.lower().replace(" ", "_")

        if model == "dummy":
            return {'status': 'Image generated successfully', 'filename': 'example.png'}

        if model in self.stable_diffusion_models:
            return self.stable_diffusion(model, description)

        if model in self.openai_models:
            return self.openai_dall_e(model, description)

        return {'status': 'Unable to find model'}

    def stable_diffusion(self, model, description):
        try:
            filename = datetime.now().strftime("image_%d-%m-%Y_%H-%M-%S.png")
            filepath = os.path.join(self.path, filename)
            pipe = StableDiffusionPipeline.from_pretrained(
                model,
                torch_dtype=torch.float16,
                revision="fp16"
            )
            pipe = pipe.to("cuda")
            image = pipe(description).images[0]
            image.save(filepath)
            return {'status': 'Image generated successfully', 'filename': filename}
        except Exception as e:
            print(f"Stable Diffusion returned an error: {e}")
            return {'status': 'Unable to generated image'}

    def openai_dall_e(self, model, description):
        try:
            response = self.openAI.images.generate(
                model=model,
                prompt=description,
                size="1024x1024",
                quality="standard",
                n=1,
            )
        except Exception as e:
            print(f"Dall-e API returned an error: {e}")
            return {'status': 'Unable to generated image'}

        response = requests.get(response.data[0].url)
        filename = datetime.now().strftime("image_%d-%m-%Y_%H-%M-%S.png")
        filepath = os.path.join(self.path, filename)

        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
        else:
            return {'status': 'Unable to save generated image'}

        return {'status': 'Image generated successfully', 'filename': filename}
