import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.subject import Subject

db = SessionLocal()
bad_subject = db.query(Subject).filter(Subject.name == "Tarjuma-e-Quran").first()
if bad_subject:
    db.delete(bad_subject)
    db.commit()
    print("Deleted duplicate")
db.close()
