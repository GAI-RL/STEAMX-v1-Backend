"""
Run this script to seed initial data:
python scripts/seed_data.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.subject import Subject
from app.models.grade import Grade
from app.models.subscription_plan import SubscriptionPlan

def seed_subjects():
    subjects = [
        {"name": "Physics", "icon": "⚡", "color": "#F59E0B", "is_active": True},
        {"name": "Chemistry", "icon": "🧪", "color": "#10B981", "is_active": True},
        {"name": "Mathematics", "icon": "📐", "color": "#8B5CF6", "is_active": True},
        {"name": "Biology", "icon": "🧬", "color": "#22C55E", "is_active": True},
        {"name": "Computer Science", "icon": "💻", "color": "#3B82F6", "is_active": True},
        {"name": "Python Programming", "icon": "🐍", "color": "#06B6D4", "is_active": True},
        {"name": "English", "icon": "📚", "color": "#EC4899", "is_active": True},
        {"name": "Urdu", "icon": "📖", "color": "#14B8A6", "is_active": True},
        {"name": "Pakistan Studies", "icon": "🇵🇰", "color": "#F97316", "is_active": True},
        {"name": "Islamic Studies", "icon": "🕌", "color": "#A855F7", "is_active": True},
        {"name": "Tarjuma tul Quran", "icon": "📖", "color": "#D97706", "is_active": True},
    ]
    
    db = SessionLocal()
    for subject_data in subjects:
        existing = db.query(Subject).filter(Subject.name == subject_data["name"]).first()
        if not existing:
            subject = Subject(**subject_data)
            db.add(subject)
    db.commit()
    print("✅ Subjects seeded")
    db.close()

def seed_grades():
    grades = [
        {"level": 9, "display_name": "Grade 9"},
        {"level": 10, "display_name": "Grade 10"},
        {"level": 11, "display_name": "Grade 11"},
        {"level": 12, "display_name": "Grade 12"},
    ]
    
    db = SessionLocal()
    for grade_data in grades:
        existing = db.query(Grade).filter(Grade.level == grade_data["level"]).first()
        if not existing:
            grade = Grade(**grade_data)
            db.add(grade)
    db.commit()
    print("✅ Grades seeded")
    db.close()

def seed_subscription_plans():
    plans = [
        {
            "name": "Free", 
            "slug": "free", 
            "price_monthly_pkr": 0,
            "qa_pairs_per_day": 20,
            "sessions_per_day": 5,
            "max_file_uploads": 5,
            "max_file_size_bytes": 5 * 1024 * 1024,  # 5MB
            "rag_enabled": False
        },
        {
            "name": "Pro", 
            "slug": "pro", 
            "price_monthly_pkr": 999,
            "qa_pairs_per_day": 200,
            "sessions_per_day": 50,
            "max_file_uploads": 50,
            "max_file_size_bytes": 20 * 1024 * 1024,  # 20MB
            "rag_enabled": True
        },
        {
            "name": "Enterprise", 
            "slug": "enterprise", 
            "price_monthly_pkr": 4999,
            "qa_pairs_per_day": 1000,
            "sessions_per_day": 500,
            "max_file_uploads": 500,
            "max_file_size_bytes": 100 * 1024 * 1024,  # 100MB
            "rag_enabled": True
        },
    ]
    
    db = SessionLocal()
    for plan_data in plans:
        existing = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == plan_data["slug"]).first()
        if not existing:
            plan = SubscriptionPlan(**plan_data)
            db.add(plan)
    db.commit()
    print("✅ Subscription plans seeded")
    db.close()

if __name__ == "__main__":
    print("🌱 Seeding database...")
    seed_subjects()
    seed_grades()
    seed_subscription_plans()
    print("🎉 Done!")