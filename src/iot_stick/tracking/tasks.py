from celery.task import task
import requests

from django.conf import settings

base_url = 'https://maker.ifttt.com/trigger/{event}/with/key/' + settings.IFTTT_KEY


@task
def send_outgoing_webhook(module_id, state, home, radius, out):
    from .models import NotificationLog, Module
    m = Module.objects.get(module_id=module_id)
    log = NotificationLog()
    http_choice = log.HttpStatusChoice
    log.status = http_choice.RUNNING.value
    log.module = m
    log.home = home
    log.state = state
    log.save()
    event = 'hacku_outgoing' if out else 'hacku_incoming'
    res = requests.post(
        url=base_url.format(event=event),
        json={
            'value1': m.name,
            'value2': home,
            'value3': str(radius)
        },
        headers={'Content-Type': 'application/json'}
    )
    log.status_code = res.status_code
    if res.status_code in [i for i in range(200, 209)]:
        log.status = http_choice.SUCCESS.value
    else:
        log.status = http_choice.FAIL.value
    log.save()
