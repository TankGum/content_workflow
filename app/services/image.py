from openai import OpenAI
from app.core.config import settings
import requests
import os
import uuid

class ImageService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.storage_path = os.path.join(settings.LOCAL_STORAGE_PATH, "images")
        os.makedirs(self.storage_path, exist_ok=True)

    def generate_image(self, prompt, size="1024x1792"):
        # Default size is 9:16 approx for shorts
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        
        filename = f"{uuid.uuid4()}.png"
        file_path = os.path.join(self.storage_path, filename)
        
        with open(file_path, 'wb') as f:
            f.write(img_data)
            
        return file_path
