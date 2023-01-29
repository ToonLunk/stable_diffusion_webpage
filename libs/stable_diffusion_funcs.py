# import the necessary libraries
from libs.requirements import *

def generate_image(prompt, fileName):
    # make sure gpus are available for torch, print result
    print(f"GPU is available: {torch.cuda.is_available()}")
    # empty the cache for better performance
    torch.cuda.empty_cache()
    try:
        # path to the Stable Diffusion model
        modelId = "D:\ML Models\stable-diffusion-2-1"
        pipeline = StableDiffusionPipeline.from_pretrained(
        modelId, torch_dtype=torch.float16)
        pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
            pipeline.scheduler.config)
        pipeline = pipeline.to("cuda")
        pipeline.enable_attention_slicing()
    except:
        print("ERROR: Exception creating pipeline")
        return False

    try:
        # generate an image
        image = pipeline(prompt).images[0]

    except:
        print("ERROR: Exception generating image")
        return False
    try:
        # if the output folder doesn't exist, create it
        if not os.path.exists("./static/img/output"):
            os.makedirs("./static/img/output")
        
        # save the image
        image.save(f"./static/img/output/{fileName}.png")

        # if the prompts folder doesn't exist, create it
        if not os.path.exists("./extras"):
            os.makedirs("./extras")

        # append the prompt to a text file under ./static/img/output named "prompts.txt"
        with open("./extras/prompts.txt", "a") as f:
            f.write(prompt)
            f.write("\n")

        return "Image generation successful"
    except:
        print("ERROR: Exception saving image to ./output")
        return False