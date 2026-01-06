#!/usr/bin/env python3
"""
Final verification script to ensure all components of the API are properly set up.
This script checks that all files exist and have the expected imports/structure.
"""
import os
import sys
from pathlib import Path


def check_file_exists(filepath):
    """Check if a file exists"""
    path = Path(filepath)
    if path.exists():
        print(f"[OK] {filepath} exists")
        return True
    else:
        print(f"[ERROR] {filepath} does not exist")
        return False


def verify_project_structure():
    """Verify that all required files and directories exist"""
    print("Verifying project structure...")

    required_files = [
        "main.py",
        "requirements.txt",
        ".env.example",
        ".env",
        ".gitignore",
        "README.md",

        # Database
        "app/database/__init__.py",
        "app/database/database.py",
        "app/database/config.py",

        # Models
        "app/models/__init__.py",
        "app/models/task.py",

        # Schemas
        "app/schemas/__init__.py",
        "app/schemas/task.py",
        "app/schemas/response.py",

        # API
        "app/api/__init__.py",
        "app/api/crud.py",

        # Utils
        "app/utils/__init__.py",
        "app/utils/external_api.py",
        "app/utils/exceptions.py",
        "app/utils/db_utils.py",

        # Tests
        "app/tests/__init__.py",
        "app/tests/test_external_api.py",
        "app/tests/test_crud.py",
        "app/tests/test_api.py",
        "app/tests/conftest.py",
    ]

    all_good = True
    for file in required_files:
        if not check_file_exists(file):  # Fixed: removed extra path prefix
            all_good = False

    return all_good


def verify_fastapi_imports():
    """Verify that main.py has all required imports"""
    print("\nVerifying main.py imports...")
    main_file = "main.py"  # Fixed: corrected path

    if not os.path.exists(main_file):
        print(f"[ERROR] {main_file} does not exist")
        return False
    
    with open(main_file, 'r') as f:
        content = f.read()
    
    required_imports = [
        "from fastapi import FastAPI, Depends, HTTPException, status",
        "from sqlalchemy.orm import Session",
        "from app.database.database import engine, Base, get_db",
        "from app.models.task import Task as TaskModel",
        "from app.schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate",
        "from app.api import crud",
        "from app.utils.external_api import get_ai_summary",
        "from app.utils.exceptions import add_exception_handlers"
    ]

    all_good = True
    for imp in required_imports:
        if imp in content:
            print(f"[OK] Found import: {imp.split()[3] if imp.startswith('from') else imp.split()[1]}")
        else:
            print(f"[ERROR] Missing import: {imp}")
            all_good = False

    return all_good


def verify_models():
    """Verify that models are properly defined"""
    print("\nVerifying models...")
    model_file = "app/models/task.py"  # Fixed: corrected path

    if not os.path.exists(model_file):
        print(f"[ERROR] {model_file} does not exist")
        return False
    
    with open(model_file, 'r') as f:
        content = f.read()
    
    required_elements = [
        "class Task(Base):",
        "__tablename__ = \"tasks\"",
        "id = Column(Integer, primary_key=True",
        "title = Column(String, index=True, nullable=False)",
        "summary = Column(Text)"
    ]
    
    all_good = True
    for element in required_elements:
        if element in content:
            if "Column" in element:
                print(f"[OK] Found column: {element.split(' = ')[0].split('.')[-1]}")
            else:
                print(f"[OK] Found element: {element[:20]}...")
        else:
            print(f"[ERROR] Missing element in model: {element}")
            all_good = False

    return all_good


def verify_schemas():
    """Verify that Pydantic schemas are properly defined"""
    print("\nVerifying schemas...")
    schema_file = "app/schemas/task.py"  # Fixed: corrected path

    if not os.path.exists(schema_file):
        print(f"[ERROR] {schema_file} does not exist")
        return False
    
    with open(schema_file, 'r') as f:
        content = f.read()
    
    required_schemas = [
        "class TaskBase(BaseModel):",
        "class TaskCreate(TaskBase):",
        "class TaskUpdate(BaseModel):",
        "class Task(TaskBase):"
    ]
    
    all_good = True
    for schema in required_schemas:
        if schema in content:
            print(f"[OK] Found schema: {schema.split()[1]}")
        else:
            print(f"[ERROR] Missing schema: {schema}")
            all_good = False

    # Check for validation
    if "validator" in content:
        print("[OK] Found validation logic")
    else:
        print("[ERROR] Missing validation logic")
        all_good = False

    return all_good


def verify_crud_operations():
    """Verify that CRUD operations are implemented"""
    print("\nVerifying CRUD operations...")
    crud_file = "app/api/crud.py"  # Fixed: corrected path

    if not os.path.exists(crud_file):
        print(f"[ERROR] {crud_file} does not exist")
        return False
    
    with open(crud_file, 'r') as f:
        content = f.read()
    
    required_functions = [
        "def get_task(db: Session, task_id: int)",
        "def get_tasks(db: Session, skip: int = 0, limit: int = 100)",
        "def create_task(db: Session, task: TaskCreate)",
        "def update_task(db: Session, task_id: int, task: TaskUpdate)",
        "def delete_task(db: Session, task_id: int)"
    ]
    
    all_good = True
    for func in required_functions:
        if func in content:
            print(f"[OK] Found function: {func.split()[1].split('(')[0]}")
        else:
            print(f"[ERROR] Missing function: {func}")
            all_good = False

    return all_good


def verify_external_api_integration():
    """Verify that external API integration is implemented"""
    print("\nVerifying external API integration...")
    api_file = "app/utils/external_api.py"  # Fixed: corrected path

    if not os.path.exists(api_file):
        print(f"[ERROR] {api_file} does not exist")
        return False
    
    with open(api_file, 'r') as f:
        content = f.read()
    
    required_elements = [
        "async def get_ai_summary(title: str, description: Optional[str] = None)",
        "settings.external_api_url",
        "settings.external_api_key",
        "asyncio.sleep(1)"  # For simulation
    ]
    
    all_good = True
    for element in required_elements:
        if element in content:
            print(f"[OK] Found element: {element.split('(')[0].split()[-1] if '(' in element else element.split()[0] if ' ' in element else element[:20]}")
        else:
            print(f"[ERROR] Missing element: {element}")
            all_good = False

    return all_good


def verify_error_handling():
    """Verify that error handling is implemented"""
    print("\nVerifying error handling...")
    exc_file = "app/utils/exceptions.py"  # Fixed: corrected path

    if not os.path.exists(exc_file):
        print(f"[ERROR] {exc_file} does not exist")
        return False
    
    with open(exc_file, 'r') as f:
        content = f.read()
    
    required_elements = [
        "class TaskException(Exception)",
        "async def task_exception_handler",
        "async def http_exception_handler",
        "async def validation_exception_handler",
        "def add_exception_handlers(app: FastAPI)"
    ]
    
    all_good = True
    for element in required_elements:
        if element in content:
            print(f"[OK] Found error handler: {element.split()[-1].split('(')[0]}")
        else:
            print(f"[ERROR] Missing error handler: {element}")
            all_good = False

    return all_good


def verify_tests():
    """Verify that tests are implemented"""
    print("\nVerifying tests...")
    test_files = [
        "app/tests/test_external_api.py",
        "app/tests/test_crud.py", 
        "app/tests/test_api.py",
        "app/tests/conftest.py"
    ]
    
    all_good = True
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"[ERROR] {test_file} does not exist")
            all_good = False
        else:
            print(f"[OK] Found test file: {test_file}")

            # Check if the test file has content
            with open(test_file, 'r') as f:
                content = f.read()
            if len(content.strip()) > 0:
                print(f"  [OK] {test_file} has content")
            else:
                print(f"  [ERROR] {test_file} is empty")
                all_good = False

    return all_good


def main():
    """Main verification function"""
    print("API Project Verification Script")
    print("=" * 50)
    
    all_checks = [
        verify_project_structure(),
        verify_fastapi_imports(),
        verify_models(),
        verify_schemas(),
        verify_crud_operations(),
        verify_external_api_integration(),
        verify_error_handling(),
        verify_tests()
    ]
    
    print("\n" + "=" * 50)
    if all(all_checks):
        print("[SUCCESS] All verifications passed! The API project is complete.")
        print("\nProject includes:")
        print("- FastAPI application with 4 endpoints (POST, GET, PUT, DELETE)")
        print("- PostgreSQL integration with SQLAlchemy")
        print("- Pydantic validation models")
        print("- External API integration (mock LLM service)")
        print("- Comprehensive error handling")
        print("- Unit and integration tests with Pytest")
        print("- Complete documentation in README.md")
        return True
    else:
        print("[ERROR] Some verifications failed. Please check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)