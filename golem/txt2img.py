from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
import argparse
import sys

def initialize_pipeline(offline: bool):
    model_id = "stabilityai/stable-diffusion-2-1-base"

    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler", local_files_only=offline)
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float32, local_files_only=offline)
    pipe = pipe.to("cpu")

    print("successfully initialized pipeline")
    return pipe

if "--load" in sys.argv:
    initialize_pipeline(False)
    exit(0)
    


parser = argparse.ArgumentParser(prog="txt2img.py", description="generates an image from a text prompt using stable diffusion")
parser.add_argument("--offline", action='store_true')
parser.add_argument("prompt")
parser.add_argument("output_path")

args = parser.parse_args()

pipe = initialize_pipeline(args.offline)

prompt = args.prompt
path = args.output_path

print("running prompt:",prompt)
print("saving to:", path)

image = pipe(prompt).images[0]
image.save(path)