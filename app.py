from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
# import torch

# #generating an image
# from diffusers import StableDiffusionPipeline

# device = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"Using device: {device}")
# pipe = StableDiffusionPipeline.from_pretrained(

#     # "runwayml/stable-diffusion-v1-5", # SD 1.5 uses CLIP ViT-L as its text encoder, which caps at 77 tokens and treats the prompt more as a bag of weighted concepts than as a sentence. So it responds to comma-separated tags, not natural language, and front-loaded terms carry more weight.

#     # "Lykon/dreamshaper-8",   # community fine-tune of SD 1.5 by Lykon,

#     "stabilityai/sd-turbo", # It's Stable Diffusion 2.1, it requires num_inference_steps=1, guidance_scale=0.0
#     torch_dtype=torch.float16,
#     ).to(device)


# prompt = (
#     "abstract geometric composition, layered overlapping squares and thin lines, "
#     "grid drifting out of alignment, three-color palette of black red and cream, "
#     "flat vector shapes, risograph print, screenprint texture, Bauhaus poster, "
#     "high contrast, clean"
# )
# negative_prompt = (
#     "blurry, lowres, watermark, text, deformed faces, extra limbs, "
#     "bad anatomy, extra fingers, cartoon, illustration, oversaturated"
# ) # This is what the model steers away from.


# image = pipe(
#     prompt,
#     negative_prompt=negative_prompt,
#     generator=torch.Generator(device).manual_seed(11001), # change the seed!
#     num_inference_steps=1, guidance_scale=0.0
# ).images[0]

# image



load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            response = openai.responses.create(
                model="gpt-4.1",  
                input=[{"role": "developer", "content": "You are a psychedelic AI that speaks in Oulipian constraints. Address me as bro, or something similar. Your responses are short, surreal, and witty. Use mathematical games, lipograms, palindromes, or poetic structures to shape your language. Avoid predictable phrasing. Let logic slip through the cracks like liquid geometry."}, 
                          {"role": "user", "content": prompt}],
                          temperature=1.2,
                          max_output_tokens=50
            )
            result = response.output_text
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing