from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, engine, Base
from app.models.video_project import VideoProject, TopicLibrary, ProjectStatus
from app.workers.trending_pipeline import run_trending_pipeline
from app.workers.evergreen_pipeline import run_evergreen_pipeline
from pydantic import BaseModel
from typing import List, Optional

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Video Automation System")

class TopicCreate(BaseModel):
    name: str
    category: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "AI Video Automation System is running."}

@app.post("/trigger/trending")
def trigger_trending():
    task = run_trending_pipeline.delay()
    return {"task_id": str(task.id), "status": "queued"}

@app.post("/trigger/evergreen")
def trigger_evergreen(topic_id: Optional[int] = None):
    task = run_evergreen_pipeline.delay(topic_id=topic_id)
    return {"task_id": str(task.id), "status": "queued"}

@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    return db.query(VideoProject).all()

@app.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(VideoProject).filter(VideoProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/library")
def add_to_library(topic: TopicCreate, db: Session = Depends(get_db)):
    db_topic = TopicLibrary(name=topic.name, category=topic.category)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic
