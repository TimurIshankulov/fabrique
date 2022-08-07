from django.db import models

from .validators import phone_number_regex


class Mailing(models.Model):
    unique_id = models.IntegerField(null=False, unique=True)
    datetime_start = models.DateTimeField()
    message_text = models.TextField()
    filter_property = models.CharField(max_length=30)
    datetime_end = models.DateTimeField()


class Client(models.Model):
    unique_id = models.IntegerField(null=False, unique=True)
    phone_number = models.CharField(max_length=20, validators=[phone_number_regex])
    provider_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=20)
    timezone = models.CharField(max_length=30)


class Message(models.Model):
    unique_id = models.IntegerField(null=False, unique=True)
    datetime_sent = models.DateTimeField()
    status = models.CharField(max_length=30)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE, to_field='unique_id')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, to_field='unique_id')
