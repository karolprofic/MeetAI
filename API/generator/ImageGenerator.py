from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from datetime import datetime
from utilities import *
import torch


# TODO Tested Image: "CompVis/stable-diffusion-v1-4" / "stabilityai/stable-diffusion-2"
# TODO Stable Diffusion 2 dont work
# TODO Endpoint should return binary image or error
# TODO Generator method refactor and evaluate model choice

class ImageGenerator:
    def __init__(self, device, save_path):
        self.device = device
        self.save_path = save_path

    def generate(self, model, description):

        if model == "" or description == "":
            return {'status': 'Unable to generate image'}

        if "dummy" in model:
            return {'status': 'Image generated successfully', 'filename': 'example.png'}

        if "stable-diffusion-v1" in model:
            return self.stable_diffusion_1(model, description)

        if "stable-diffusion-2" in model:
            return self.stable_diffusion_2(model, description)

        if "dall-e-3" == model or "dall-e-2" == model:
            return self.open_ai(description)

    def stable_diffusion_1(self, model, description):
        try:
            filename = datetime.now().strftime("image_%d-%m-%Y_%H-%M-%S.png")
            file_path = os.path.join(self.save_path, filename)
            pipe = StableDiffusionPipeline.from_pretrained(
                model,
                torch_dtype=torch.float16,
                revision="fp16"
            )
            pipe = pipe.to(self.device)
            image = pipe(description).images[0]
            image.save(file_path)
            return {'status': 'Image generated successfully', 'filename': filename}
        except Exception as e:
            return {'status': f'An error occurred: {e}'}

    def stable_diffusion_2(self, model, description):
        try:
            filename = datetime.now().strftime("image_%d-%m-%Y_%H-%M-%S.png")
            file_path = os.path.join(self.save_path, filename)
            scheduler = EulerDiscreteScheduler.from_pretrained(model, subfolder="scheduler")
            pipe = StableDiffusionPipeline.from_pretrained(
                model,
                scheduler=scheduler,
                torch_dtype=torch.float16
            )
            pipe = pipe.to(self.device)
            image = pipe(description).images[0]
            image.save(file_path)
            return {'status': 'Image generated successfully', 'filename': filename}
        except Exception as e:
            return {'status': f'An error occurred: {e}'}

    def open_ai(self, description):
        pass
