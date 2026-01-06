#!/usr/bin/env python3
"""
Test script to verify database initialization works with SQLite for testing purposes.
"""
import os
import tempfile
from sqlalchemy import create_engine
from app.database.database import Base
from app.database.config import settings


def test_db_creation():
    """Test database table creation with SQLite"""
    # Create a temporary SQLite database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        temp_db_path = temp_db.name
    
    try:
        # Temporarily change the database URL to use SQLite
        original_url = settings.database_url
        settings.database_url = f"sqlite:///{temp_db_path}"
        
        # Import the engine with the new SQLite URL
        from app.database.database import engine
        engine.dispose()  # Close any existing connections
        
        # Create a new engine for SQLite
        sqlite_engine = create_engine(settings.database_url)
        
        # Import and create tables
        from app.models.task import Task
        Base.metadata.create_all(bind=sqlite_engine)
        
        print("[SUCCESS] Database tables created successfully with SQLite")
        
        # Clean up
        os.unlink(temp_db_path)
        return True
        
    except Exception as e:
        print(f"[ERROR] Database creation failed: {str(e)}")
        return False
    finally:
        # Restore original database URL
        settings.database_url = original_url


if __name__ == "__main__":
    success = test_db_creation()
    if success:
        print("[SUCCESS] Database initialization test completed successfully")
    else:
        print("[ERROR] Database initialization test failed")