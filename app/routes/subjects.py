from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.subject import Subject
from app.models.grade import Grade
from app.schemas.subject import SubjectResponse
from app.schemas.grade import GradeResponse

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.get("/", response_model=list[SubjectResponse])
async def get_subjects(db: Session = Depends(get_db)):
    """Get all active subjects"""
    subjects = db.query(Subject).filter(Subject.is_active == True).all()
    return subjects

@router.get("/grades", response_model=list[GradeResponse])
async def get_grades(db: Session = Depends(get_db)):
    """Get all grades"""
    grades = db.query(Grade).order_by(Grade.level).all()
    return grades