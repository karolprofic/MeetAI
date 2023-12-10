from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from datetime import datetime
from utilities import *
import torch


# TODO Tested Image: "CompVis/stable-diffusion-v1-4" / "stabilityai/stable-diffusion-2"
# TODO Stable Diffusion 2 dont work
# TODO Endpoint should return binary image or error
# TODO Generator method refactor and evaluate model choice
# TODO Code refactor and check input

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
            return self.openai_dalle(description)

    def stable_diffusion(self, model, description):
        try:
            filename = datetime.now().strftime("image_%d-%m-%Y_%H-%M-%S.png")
            file_path = os.path.join(self.path, filename)
            pipe = StableDiffusionPipeline.from_pretrained(
                model,
                torch_dtype=torch.float16,
                revision="fp16"
            )
            pipe = pipe.to("cuda")
            image = pipe(description).images[0]
            image.save(file_path)
            return {'status': 'Image generated successfully', 'filename': filename}
        except Exception as e:
            return {'status': f'An error occurred: {e}'}

    def openai_dalle(self, description):
        pass
