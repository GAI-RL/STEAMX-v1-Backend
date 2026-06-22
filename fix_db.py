import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.database import engine

def try_add_col(col_name):
    with engine.connect() as conn:
        with conn.begin():
            try:
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} VARCHAR;"))
                print(f"Added {col_name} column")
            except Exception as e:
                print(f"{col_name} already exists or error")

if __name__ == "__main__":
    try_add_col("school_name")
    try_add_col("province")
