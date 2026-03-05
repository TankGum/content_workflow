from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.models.database import Base
import enum

class ChannelType(str, enum.Enum):
    TRENDING = "trending"
    EVERGREEN = "evergreen"

class ProjectStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SCRIPT_DONE = "script_done"
    MEDIA_DONE = "media_done"
    RENDER_DONE = "render_done"
    PUBLISHED = "published"
    FAILED = "failed"

class VideoProject(Base):
    __tablename__ = "video_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_type = Column(String) # 'trending' or 'evergreen'
    topic = Column(String)
    script = Column(Text)
    status = Column(String, default=ProjectStatus.PENDING)
    video_url = Column(String, nullable=True)
    fact_check_passed = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TopicLibrary(Base):
    __tablename__ = "topic_library"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    category = Column(String) # 'history', 'space', 'science'
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
