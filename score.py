from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
from PIL import Image
import io
from image_quality.brisque import BRISQUE

app = FastAPI()

class ImageRequest(BaseModel):
    image_url: str

@app.post("/evaluate")
def evaluate_image_quality(data: ImageRequest):
    try:
        response = requests.get(data.image_url)
        img = Image.open(io.BytesIO(response.content))
        brisque = BRISQUE()
        score = brisque.get_score(img)
        return { "score": score }
    except Exception as e:
        return { "error": str(e) }
