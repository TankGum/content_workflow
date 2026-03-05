from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import os
import uuid
from app.core.config import settings

class VideoRenderer:
    def __init__(self):
        self.storage_path = os.path.join(settings.LOCAL_STORAGE_PATH, "videos")
        os.makedirs(self.storage_path, exist_ok=True)

    def render_short(self, audio_path, image_paths, subtitles=None):
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Calculate duration per image
        num_images = len(image_paths)
        if num_images == 0:
            raise ValueError("At least one image is required for rendering.")
            
        img_duration = duration / num_images
        
        clips = []
        for img_path in image_paths:
            clip = ImageClip(img_path).set_duration(img_duration)
            # Standard Short (9:16) format 1080x1920
            clip = clip.resize(width=1080).margin(bottom=0, top=0, opacity=0).set_position(("center", "center"))
            clips.append(clip)
            
        video = concatenate_videoclips(clips, method="compose")
        video = video.set_audio(audio)
        
        # Output path
        filename = f"short_{uuid.uuid4()}.mp4"
        output_path = os.path.join(self.storage_path, filename)
        
        # Render
        video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        
        return output_path
