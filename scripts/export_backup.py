import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
from datetime import datetime
from app.database import SessionLocal
from app.models.chat_messages import ChatMessage
from app.models.chat_sessions import ChatSession
from app.models.user import User
from app.models.feedback import Feedback

# Create backups folder
os.makedirs("backups", exist_ok=True)

def export_table(model, filename, columns):
    """Export any table to CSV"""
    db = SessionLocal()
    records = db.query(model).all()
    
    if not records:
        print(f"⚠️ No records found for {model.__tablename__}")
        db.close()
        return 0
    
    filepath = f"backups/{filename}"
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        
        for record in records:
            row = [getattr(record, col, None) for col in columns]
            writer.writerow(row)
    
    print(f"✅ Exported {len(records)} records to {filepath}")
    db.close()
    return len(records)

if __name__ == "__main__":
    print("\n📤 STARTING DATA EXPORT")
    print("=" * 40)
    
    # Export chat_messages
    export_table(
        ChatMessage, 
        "chat_messages.csv",
        ['id', 'session_id', 'role', 'content', 'timestamp']
    )
    
    # Export chat_sessions
    export_table(
        ChatSession,
        "chat_sessions.csv", 
        ['id', 'user_id', 'title', 'created_at', 'updated_at']
    )
    
    # Export users
    export_table(
        User,
        "users.csv",
        ['id', 'email', 'full_name', 'created_at', 'subscription_tier', 'is_verified']
    )
    
    # Export feedbacks
    export_table(
        Feedback,
        "feedbacks.csv",
        ['id', 'user_id', 'message', 'rating', 'created_at']
    )
    
    print("\n" + "=" * 40)
    print("🎉 EXPORT COMPLETE! Check the 'backups' folder.")