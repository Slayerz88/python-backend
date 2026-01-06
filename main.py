from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import asyncio

from app.database.database import engine, Base, get_db
from app.models.task import Task as TaskModel
from app.schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate
from app.schemas.response import SuccessResponse, ErrorResponse
from app.api import crud
from app.utils.external_api import get_ai_summary
from app.utils.exceptions import add_exception_handlers

app = FastAPI(
    title="AI-Powered Task Summarizer API",
    description="A REST API that manages tasks and uses an external AI service to summarize them",
    version="1.0.0"
)

# Add exception handlers
add_exception_handlers(app)

# Create database tables function (to be called separately)
def create_db_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Task Summarizer API"}


@app.post("/tasks/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task. If the task is marked as important, 
    it will trigger an AI summary generation.
    """
    try:
        db_task = crud.create_task(db=db, task=task)
        
        # If the task is important, generate a summary using the external API
        if db_task.is_important:
            summary = asyncio.run(get_ai_summary(db_task.title, db_task.description))
            db_task.summary = summary
            db.commit()
            db.refresh(db_task)
        
        return db_task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@app.get("/tasks/{task_id}", response_model=TaskSchema)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a specific task by ID.
    """
    try:
        db_task = crud.get_task(db=db, task_id=task_id)
        if db_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving task: {str(e)}"
        )


@app.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a specific task by ID. If the task becomes important, 
    it will trigger an AI summary generation.
    """
    try:
        db_task = crud.update_task(db=db, task_id=task_id, task=task)
        if db_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # If the task is now important and doesn't have a summary, generate one
        if db_task.is_important and not db_task.summary:
            summary = asyncio.run(get_ai_summary(db_task.title, db_task.description))
            db_task.summary = summary
            db.commit()
            db.refresh(db_task)
        
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@app.delete("/tasks/{task_id}", response_model=SuccessResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific task by ID.
    """
    try:
        success = crud.delete_task(db=db, task_id=task_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return SuccessResponse(
            success=True,
            message="Task deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )


@app.get("/tasks/", response_model=List[TaskSchema])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of tasks with pagination.
    """
    try:
        tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )