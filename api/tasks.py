import pytz

import requests
from fabrique.celery import app
from django.utils import timezone

from .models import Mailing, Client, Message
from fabrique.config import BEARER_TOKEN

utc = pytz.UTC


@app.task
def send_message(client_unique_id, mailing_unique_id):
    """
    Task creates message instance and tries to send it to mailing service.
    :param client_unique_id: client's unique id, recipient of the message
    :param mailing_unique_id: mailing's unique id, within which we perform mailing
    """
    mailing = Mailing.objects.get(unique_id=mailing_unique_id)
    client = Client.objects.get(unique_id=client_unique_id)

    message = Message()
    message.datetime_sent = None
    message.status = 'new'
    message.mailing = mailing
    message.client = client
    message.save()
    message.unique_id = message.id

    url = 'https://probe.fbrq.cloud/v1/send/'
    headers = {'Authorization': BEARER_TOKEN}
    body = {'id': message.unique_id,
            'phone': message.client.phone_number,
            'text': message.mailing.message_text}
    try:
        response = requests.post(url + str(message.unique_id), headers=headers, json=body)
    except Exception:
        message.status = 'error'
    else:
        if response.status_code == 200:
            message.datetime_sent = timezone.now()
            message.status = 'sent'
        else:
            message.status = 'error'
    finally:
        message.save()


@app.task
def beat_handle_mailings():
    """
    Beat task to handle active mailings.
    Does nothing, if mailing.datetime_start in a future, but mailing will be handled
    when the time will come. Sending messages only if current moment is between
    mailing.datetime_start and mailing.datetime_end.
    Filters by mailing's filter and value designated as 'parameter:value', e.g.
    'tag:test' or 'provider_code:999'.
    """
    for mailing in Mailing.objects.filter(status='new'):
        now = timezone.now()
        if now < mailing.datetime_start:
            return
        mailing.status = 'in_progress'
        mailing.save()

        filter_mailing = mailing.filter_property.split(':')[0]
        filter_value = mailing.filter_property.split(':')[1]
        client_list = []
        if filter_mailing == 'tag':
            client_list = Client.objects.filter(tag=filter_value)
        elif filter_mailing == 'provider_code':
            client_list = Client.objects.filter(provider_code=filter_value)
        for client in client_list:
            if mailing.datetime_start < now < mailing.datetime_end:
                send_message.delay(client.unique_id, mailing.unique_id)
            else:
                break
        mailing.status = 'completed'
        mailing.save()
