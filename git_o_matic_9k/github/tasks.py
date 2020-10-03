import random

from celery import shared_task
from django.db.models import F

from .models import *


@celery_app.task(bind=True)
def test_task():
    n = random.randint(0, 10)
    print(f'haha {n}')
    return n
