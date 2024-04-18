from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "diary_api.settings")

app = Celery("diary_api")

app.config_from_object("django.conf:settings")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from api.tasks import delete_old_diaries

    sender.add_periodic_task(10.0 * 60.0, delete_old_diaries.s())
