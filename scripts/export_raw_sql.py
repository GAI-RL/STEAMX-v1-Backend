import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
from sqlalchemy import text
from app.database import SessionLocal

def export_with_raw_sql(query, filename, headers):
    """Export using raw SQL connection (bypasses ORM models)"""
    db = SessionLocal()
    
    # Get raw connection and execute with text()
    conn = db.connection()
    result = conn.execute(text(query))
    rows = result.fetchall()
    
    filepath = f"backups/{filename}"
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
    
    print(f"✅ Exported {len(rows)} records to {filepath}")
    db.close()

if __name__ == "__main__":
    os.makedirs("backups", exist_ok=True)
    
    print("\n📤 EXPORTING WITH RAW SQL (using old schema)")
    print("=" * 50)
    
    # Export chat_messages (old schema)
    export_with_raw_sql(
        "SELECT id, session_id, role, content, timestamp FROM chat_messages",
        "chat_messages.csv",
        ['id', 'session_id', 'role', 'content', 'timestamp']
    )
    
    # Export chat_sessions
    export_with_raw_sql(
        "SELECT id, user_id, title, created_at, updated_at FROM chat_sessions",
        "chat_sessions.csv",
        ['id', 'user_id', 'title', 'created_at', 'updated_at']
    )
    
    # Export users
    export_with_raw_sql(
        "SELECT id, email, full_name, created_at, subscription_tier, is_verified FROM users",
        "users.csv",
        ['id', 'email', 'full_name', 'created_at', 'subscription_tier', 'is_verified']
    )
    
    # Export feedbacks
    export_with_raw_sql(
        "SELECT id, user_id, message, rating, created_at FROM feedbacks",
        "feedbacks.csv",
        ['id', 'user_id', 'message', 'rating', 'created_at']
    )
    
    print("\n" + "=" * 50)
    print("🎉 EXPORT COMPLETE! Check the 'backups' folder.")