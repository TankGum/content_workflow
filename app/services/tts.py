from elevenlabs.client import ElevenLabs
from app.core.config import settings
import os
import uuid

class TTSService:
    def __init__(self):
        self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        self.storage_path = os.path.join(settings.LOCAL_STORAGE_PATH, "audio")
        os.makedirs(self.storage_path, exist_ok=True)

    def generate_voice(self, text, voice="Josh"):
        # Returns path to generated audio
        audio = self.client.generate(
            text=text,
            voice=voice,
            model="eleven_multilingual_v2"
        )
        
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(self.storage_path, filename)
        
        with open(file_path, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)
        
        return file_path
