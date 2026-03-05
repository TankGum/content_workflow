from app.workers.celery_app import celery_app
from app.services.llm import LLMService
from app.services.tts import TTSService
from app.services.image import ImageService
from app.services.renderer import VideoRenderer
from app.channels.evergreen.research import EvergreenResearch
from app.channels.evergreen.factcheck import EvergreenFactCheck
from app.channels.trending.scripter import TrendingScripter # Reusable scripter or custom one
from app.models.database import SessionLocal
from app.models.video_project import VideoProject, ProjectStatus, TopicLibrary

@celery_app.task(bind=True, max_retries=2)
def run_evergreen_pipeline(self, topic_id=None):
    db = SessionLocal()
    llm = LLMService()
    research_agent = EvergreenResearch(llm)
    factcheck_agent = EvergreenFactCheck(llm)
    scripter = TrendingScripter(llm) # Reusing for brevity
    tts = TTSService()
    image_gen = ImageService()
    renderer = VideoRenderer()
    
    try:
        # Step 1: Select Topic
        if not topic_id:
            topic_obj = db.query(TopicLibrary).filter(TopicLibrary.used == False).first()
            if not topic_obj:
                return {"status": "error", "message": "No unused topics in library."}
            topic = topic_obj.name
        else:
            topic_obj = db.query(TopicLibrary).filter(TopicLibrary.id == topic_id).first()
            topic = topic_obj.name
            
        project = VideoProject(channel_type="evergreen", topic=topic, status=ProjectStatus.PROCESSING)
        db.add(project)
        db.commit()
        db.refresh(project)
        
        # Step 2: Deep Research
        research_data = research_agent.gather_facts(topic=topic)
        
        # Step 3: Generate Script
        script_data = scripter.generate_script(topic=f"{topic}. Facts: {research_data}")
        
        # Step 4: Fact-Check (Critical)
        is_accurate_data = factcheck_agent.verify(script=script_data, source_data=research_data)
        
        if not is_accurate_data['accurate']:
            # Retry or fix
            script_data['narration'] = is_accurate_data['corrected_script'] or script_data['narration']
            
        project.script = script_data['narration']
        project.fact_check_passed = True
        db.commit()
        
        # Step 5: Media & Render
        voice_path = tts.generate_voice(text=script_data['narration'])
        
        images = []
        for prompt in script_data['image_prompts']:
            img_path = image_gen.generate_image(prompt=prompt)
            images.append(img_path)
            
        video_path = renderer.render_short(audio_path=voice_path, image_paths=images)
        
        project.video_url = video_path
        project.status = ProjectStatus.PUBLISHED
        db.commit()
        
        # Mark topic as used
        topic_obj.used = True
        db.commit()
        
        return {"status": "success", "video_path": video_path, "project_id": project.id}
        
    except Exception as exc:
        if project:
            project.status = ProjectStatus.FAILED
            db.commit()
        db.close()
        raise self.retry(exc=exc, countdown=600)
    finally:
        db.close()
