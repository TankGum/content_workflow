from app.workers.celery_app import celery_app
from app.services.llm import LLMService
from app.services.tts import TTSService
from app.services.image import ImageService
from app.services.renderer import VideoRenderer
from app.channels.trending.collector import TrendingCollector
from app.channels.trending.ranker import TrendingRanker
from app.channels.trending.scripter import TrendingScripter
from app.models.database import SessionLocal
from app.models.video_project import VideoProject, ProjectStatus

@celery_app.task(bind=True, max_retries=3)
def run_trending_pipeline(self):
    db = SessionLocal()
    llm = LLMService()
    collector = TrendingCollector()
    ranker = TrendingRanker(llm)
    scripter = TrendingScripter(llm)
    tts = TTSService()
    image_gen = ImageService()
    renderer = VideoRenderer()
    
    try:
        # Step 1: Collect Trends
        raw_topics = collector.fetch_trends()
        
        # Step 2: Rank & Select
        best_topic_data = ranker.select_viral_topic(topics=raw_topics)
        best_topic = best_topic_data['top_topic']
        
        # Create DB project
        project = VideoProject(channel_type="trending", topic=best_topic, status=ProjectStatus.PROCESSING)
        db.add(project)
        db.commit()
        db.refresh(project)
        
        # Step 3: Generate & Review Script
        script_data = scripter.generate_script(topic=best_topic)
        improved_script = scripter.review_script(script_data=script_data)
        
        project.script = improved_script['narration']
        project.status = ProjectStatus.SCRIPT_DONE
        db.commit()
        
        # Step 4: Generate Voice & Images
        voice_path = tts.generate_voice(text=improved_script['narration'])
        
        images = []
        for prompt in improved_script['image_prompts']:
            img_path = image_gen.generate_image(prompt=prompt)
            images.append(img_path)
            
        project.status = ProjectStatus.MEDIA_DONE
        db.commit()
        
        # Step 5: Render Video
        video_path = renderer.render_short(
            audio_path=voice_path, 
            image_paths=images
        )
        
        project.video_url = video_path
        project.status = ProjectStatus.RENDER_DONE
        db.commit()
        
        # Step 6: Publish (Mock)
        # publisher.upload(...)
        project.status = ProjectStatus.PUBLISHED
        db.commit()
        
        return {"status": "success", "video_path": video_path, "project_id": project.id}
        
    except Exception as exc:
        if project:
            project.status = ProjectStatus.FAILED
            db.commit()
        db.close()
        raise self.retry(exc=exc, countdown=300)
    finally:
        db.close()
