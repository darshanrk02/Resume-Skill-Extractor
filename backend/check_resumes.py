import sqlite3
import os
from pathlib import Path

def check_database():
    db_path = Path(__file__).parent / 'resume_extractor.db'
    print(f"Checking database at: {db_path}")
    
    if not db_path.exists():
        print("Database file not found!")
        return
        
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("\nTables in database:")
        for table in tables:
            print(f"- {table[0]}")
            
        # Check if resumes table exists
        if 'resumes' in [t[0] for t in tables]:
            # Count resumes
            cursor.execute("SELECT COUNT(*) FROM resumes")
            count = cursor.fetchone()[0]
            print(f"\nFound {count} resume(s) in the database")
            
            # Show first 5 resumes
            if count > 0:
                print("\nSample resume data:")
                cursor.execute("SELECT * FROM resumes LIMIT 5")
                for row in cursor.fetchall():
                    print(row)
        else:
            print("\nNo 'resumes' table found in the database")
            
    except Exception as e:
        print(f"\nError accessing database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_database()
