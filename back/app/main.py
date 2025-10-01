from fastapi import FastAPI
from routers.api.event import event_router
from routers.api.user import user_router
from routers.api.picturesque import picturesque_router
from utils.sender import email_sender
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from datetime import date
from database.database import engine
from routers.crud import broadcast as cast_crud


app = FastAPI()

app.include_router(event_router)
app.include_router(picturesque_router)
app.include_router(user_router)

def check_memorial_dates():
    """Ежедневная проверка памятных дат"""
    with Session(engine) as db:
        today = date.today()
        memorial_dates = cast_crud.get_memorial_dates_by_date(db, today)
        users = cast_crud.get_active_users(db)
        
        for memorial_date in memorial_dates:
            # Запускаем асинхронную отправку
            import asyncio
            asyncio.create_task(
                email_sender.send_memorial_date_notification(memorial_date, users)
            )

# Настройка планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(
    check_memorial_dates,
    CronTrigger(hour=9, minute=0),  # Каждый день в 9:00
    id="daily_memorial_check"
)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()