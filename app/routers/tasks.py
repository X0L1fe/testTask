from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.crud import create_task, get_tasks, get_task_by_id, update_task, delete_task
from app.dependencies import get_db, get_current_user

router = APIRouter()

# Создание задачи
@router.post("/", response_model=TaskResponse)
async def create_new_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return await create_task(db=db, task=task, user_id=current_user)

# Получение всех задач с фильтрацией по статусу
@router.get("/", response_model=List[TaskResponse])
async def read_tasks(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    return await get_tasks(db=db, status=status)

# Получение задачи по ID
@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task_by_id(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

# Обновление задачи по ID
@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    existing_task = await get_task_by_id(db=db, task_id=task_id)
    if not existing_task or existing_task.user_id != current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await update_task(db=db, task_id=task_id, task=task)
    return await get_task_by_id(db=db, task_id=task_id)

# Удаление задачи по ID
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_route(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    task = await get_task_by_id(db=db, task_id=task_id)
    if not task or task.user_id != current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await delete_task(db=db, task_id=task_id)
