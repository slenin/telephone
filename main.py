import requests
from PIL import Image
import base64
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

hyperbolic_key = os.getenv("HYPEBOLIC_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")


def generate_image_with_image(prompt, image_base64):
    url = "https://api.hyperbolic.xyz/v1/image/generation"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hyperbolic_key}"
    }
    data = {
        "model_name": "SDXL1.0-base",
        "prompt": prompt,
        "steps": 30,
        "cfg_scale": 5,
        "enable_refiner": False,
        "height": 1024,
        "width": 1024,
        "enable_reference": True,
        "image": image_base64,
        "strength": 0.8,
        "backend": "auto"
    }
    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    return data["images"][0]["image"]


def generate_image(prompt):
    url = "https://api.hyperbolic.xyz/v1/image/generation"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hyperbolic_key}"
    }
    data = {
        "model_name": "FLUX.1-dev",
        "prompt": prompt,
        "steps": 30,
        "cfg_scale": 5,
        "enable_refiner": False,
        "height": 1024,
        "width": 1024,
        "backend": "auto"
    }
    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    return data["images"][0]["image"]


def show_image(image_base64):
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))
    image.show()


def caption_image(image_base64):
    client = OpenAI(api_key=openai_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Generate a descriptive caption for the attached image.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                        },
                    ],
                }
            ]
        )
        caption = response.choices[0].message.content
        return caption
    except Exception as e:
        print("Error during captioning:", e)
        return None


def func1():
    prompt1 = "A beautiful sunrise."
    reference_image = generate_image(prompt1)
    show_image(reference_image)
    prompt2 = "Put two cats in the image"
    final_image = generate_image_with_image(prompt2, reference_image)
    show_image(final_image)


def func2():
    caption = "Two cats riding a motorbike."
    for i in range(5):
        image_base64 = generate_image(caption)
        show_image(image_base64)
        caption = caption_image(image_base64)
        print(caption)
        caption = caption + " Produce an image that is exactly opposite of this description."
        print("-----")


func1()
