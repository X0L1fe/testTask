from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

# Создание новой задачи
async def create_task(db: AsyncSession, task: TaskCreate, user_id: int):
    new_task = Task(**task.dict(), user_id=user_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

# Получение всех задач с возможностью фильтрации по статусу
async def get_tasks(db: AsyncSession, status: str = None):
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    result = await db.execute(query)
    return result.scalars().all()

# Получение задачи по ID
async def get_task_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()

# Обновление задачи по ID
async def update_task(db: AsyncSession, task_id: int, task: TaskUpdate):
    query = (
        update(Task)
        .where(Task.id == task_id)
        .values(**task.dict(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()

# Удаление задачи по ID
async def delete_task(db: AsyncSession, task_id: int):
    query = delete(Task).where(Task.id == task_id)
    await db.execute(query)
    await db.commit()
