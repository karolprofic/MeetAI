from diffusers import StableDiffusionPipeline, DiffusionPipeline
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
            "compvis/stable-diffusion-v1-4",
            "runwayml/stable-diffusion-v1-5",
        ]
        self.stable_diffusion_models_xl_base = [
            "stabilityai/stable-diffusion-xl-base-1.0"
        ]
        self.stable_diffusion_models_xl_refiner = [
            "stabilityai/stable-diffusion-xl-refiner-1.0",
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

        if model in self.stable_diffusion_models_xl_base:
            return self.stable_diffusion_xl_base(model, description)

        if model in self.stable_diffusion_models_xl_refiner:
            return self.stable_diffusion_xl_refined(model, description)

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

    def stable_diffusion_xl_base(self, model, description):
        try:
            filename = datetime.now().strftime("image_%d-%m-%Y_%H-%M-%S.png")
            filepath = os.path.join(self.path, filename)
            pipe = DiffusionPipeline.from_pretrained(
                model,
                torch_dtype=torch.float16,
                use_safetensors=True,
                variant="fp16"
            )
            pipe.to("cuda")
            # pipe.enable_xformers_memory_efficient_attention()
            image = pipe(prompt=description).images[0]
            image.save(filepath)
            return {'status': 'Image generated successfully', 'filename': filename}
        except Exception as e:
            print(f"Stable Diffusion returned an error: {e}")
            return {'status': 'Unable to generated image'}

    def stable_diffusion_xl_refined(self, model, description):
        try:
            filename = datetime.now().strftime("image_%d-%m-%Y_%H-%M-%S.png")
            filepath = os.path.join(self.path, filename)

            base = DiffusionPipeline.from_pretrained(
                model,
                torch_dtype=torch.float16,
                variant="fp16",
                use_safetensors=True
            )
            base.to("cuda")
            refiner = DiffusionPipeline.from_pretrained(
                model,
                text_encoder_2=base.text_encoder_2,
                vae=base.vae,
                torch_dtype=torch.float16,
                use_safetensors=True,
                variant="fp16",
            )
            refiner.to("cuda")

            n_steps = 20
            high_noise_frac = 0.8
            image = base(
                prompt=description,
                num_inference_steps=n_steps,
                denoising_end=high_noise_frac,
                output_type="latent",
            ).images
            image = refiner(
                prompt=description,
                num_inference_steps=n_steps,
                denoising_start=high_noise_frac,
                image=image,
            ).images[0]
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
