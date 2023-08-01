from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from flask import jsonify
from datetime import datetime
from utilities import *
import torch


# TODO Tested Image: "CompVis/stable-diffusion-v1-4" / "stabilityai/stable-diffusion-2"
# TODO Stable Diffusion 2 dont work
# TODO 0 - success / 1 - error / 2 - empty / 3 - not recognized

class ImageGenerator:
    def __init__(self, device, save_path):
        self.device = device
        self.save_path = save_path

    def generate(self, model, description):

        if model == "" or description == "":
            return jsonify({'status': 2, 'description': 'Unable to generate image', 'file_name': ''})

        if "stable-diffusion-v1" in model:
            return self.stable_diffusion_1(model, description)

        if "stable-diffusion-2" in model:
            return self.stable_diffusion_2(model, description)

        if "open-ai" in model:
            return self.open_ai(description)

        return jsonify({'status': 3, 'description': 'The model was not recognized', 'file_name': ''})

    def stable_diffusion_1(self, model, description):
        try:
            file_name = datetime.now().strftime("image_%d-%m-%Y_%H-%M-%S.png")
            file_path = os.path.join(self.save_path, file_name)
            pipe = StableDiffusionPipeline.from_pretrained(
                model,
                torch_dtype=torch.float16,
                revision="fp16"
            )
            pipe = pipe.to(self.device)
            image = pipe(description).images[0]
            image.save(file_path)
            return jsonify({'status': 0, 'description': 'Image generated successfully', 'file_name': file_name})
        except Exception as e:
            return jsonify({'status': 1, 'description': f'An error occurred: {e}', 'file_name': ''})

    def stable_diffusion_2(self, model, description):
        try:
            file_name = datetime.now().strftime("image_%d-%m-%Y_%H-%M-%S.png")
            file_path = os.path.join(self.save_path, file_name)
            scheduler = EulerDiscreteScheduler.from_pretrained(model, subfolder="scheduler")
            pipe = StableDiffusionPipeline.from_pretrained(
                model,
                scheduler=scheduler,
                torch_dtype=torch.float16
            )
            pipe = pipe.to(self.device)
            image = pipe(description).images[0]
            image.save(file_path)
            return jsonify({'status': 0, 'description': 'Image generated successfully', 'file_name': file_name})
        except Exception as e:
            return jsonify({'status': 1, 'description': f'An error occurred: {e}', 'file_name': ''})

    def open_ai(self, description):
        pass