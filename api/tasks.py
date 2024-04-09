from celery import shared_task
from datetime import datetime
from .models import Diary


@shared_task
def delete_old_diaries():
    today = datetime.now().date()
    diaries = Diary.objects.filter(expiration__lte=today)
    for diary in diaries:
        diary.delete()
