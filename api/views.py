import json
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import Mailing, Client, Message
from .serializers import MailingSerializer, ClientSerializer, MessageSerializer


class CreateClientView(generics.GenericAPIView):
    """Creates client if it's not exist yet"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientSerializer

    def post(self, request, *args,  **kwargs):
        data = json.loads(request.body)
        unique_id = data.get('unique_id')
        try:
            client = Client.objects.get(unique_id=unique_id)
        except Client.DoesNotExist:
            client = Client()
            client.unique_id = unique_id
            client.phone_number = data.get('phone_number')
            client.provider_code = data.get('provider_code')
            client.tag = data.get('tag')
            client.timezone = data.get('timezone')
            try:  # Validate data before save
                client.full_clean()
                client.save()
            except ValidationError:
                message = {'error': 'Incorrect data!'}
                return Response(message)
        else:  # Client already exists
            message = 'Client already exists!'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        message = {'client': ClientSerializer(
            client,
            context=self.get_serializer_context()).data,
                   'message': 'Client created successfully'}
        return Response(message)


class GetUserView(generics.GenericAPIView):
    """Returns client's data by its unique_id"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientSerializer

    def get(self, request, *args,  **kwargs):
        try:
            client = Client.objects.get(unique_id=self.kwargs['unique_id'])
        except Client.DoesNotExist:
            message = 'Client not found'
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        message = {'client': ClientSerializer(
            client,
            context=self.get_serializer_context()).data}
        return Response(message)


class UpdateClientView(generics.GenericAPIView):
    """Updates client info and return modified client data"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientSerializer

    def post(self, request, *args,  **kwargs):
        data = json.loads(request.body)
        unique_id = self.kwargs['unique_id']
        try:
            client = Client.objects.get(unique_id=unique_id)
        except Client.DoesNotExist:
            message = 'Client does not exist!'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        if data.get('phone_number'):
            client.phone_number = data.get('phone_number')
        if data.get('provider_code'):
            client.provider_code = data.get('provider_code')
        if data.get('tag'):
            client.tag = data.get('tag')
        if data.get('timezone'):
            client.timezone = data.get('timezone')

        try:  # Validate data before save
            client.full_clean()
            client.save()
        except ValidationError:
            message = {'error': 'Incorrect data!'}
            return Response(message)

        message = {'client': ClientSerializer(
            client,
            context=self.get_serializer_context()).data,
                   'message': 'User updated successfully'}
        return Response(message)


class RemoveClientView(generics.GenericAPIView):
    """Removes client from the database by its unique_id"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientSerializer

    def delete(self, request, *args,  **kwargs):
        try:
            client = Client.objects.get(unique_id=self.kwargs['unique_id'])
        except Client.DoesNotExist:
            message = 'Client not found'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        else:
            client.delete()

        message = {'client': ClientSerializer(
            client,
            context=self.get_serializer_context()).data,
                   'message': 'Client removed successfully'}
        return Response(message)


class CreateMailingView(generics.GenericAPIView):
    """Creates mailing if it's not exist yet"""
    permission_classes = [permissions.AllowAny]
    serializer_class = MailingSerializer

    def post(self, request, *args,  **kwargs):
        data = json.loads(request.body)
        unique_id = data.get('unique_id')
        try:
            mailing = Mailing.objects.get(unique_id=unique_id)
        except Mailing.DoesNotExist:
            mailing = Mailing()
            mailing.unique_id = unique_id
            mailing.datetime_start = data.get('datetime_start')
            mailing.message_text = data.get('message_text')
            mailing.filter_property = data.get('filter_property')
            mailing.datetime_end = data.get('datetime_end')
            mailing.status = data.get('status')
            mailing.save()
        else:
            message = 'Mailing already exists!'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        message = {'mailing': MailingSerializer(
            mailing,
            context=self.get_serializer_context()).data,
                   'message': 'Mailing created successfully'}
        return Response(message)


class GetMailingView(generics.GenericAPIView):
    """Returns mailing data by its unique_id"""
    permission_classes = [permissions.AllowAny]
    serializer_class = MailingSerializer

    def get(self, request, *args,  **kwargs):
        try:
            mailing = Mailing.objects.get(unique_id=self.kwargs['unique_id'])
        except Mailing.DoesNotExist:
            message = 'Mailing not found'
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        message = {'mailing': MailingSerializer(
            mailing,
            context=self.get_serializer_context()).data}
        return Response(message)


class UpdateMailingView(generics.GenericAPIView):
    """Updates mailing data and returns modified record"""
    permission_classes = [permissions.AllowAny]
    serializer_class = MailingSerializer

    def post(self, request, *args,  **kwargs):
        data = json.loads(request.body)
        unique_id = self.kwargs['unique_id']
        try:
            mailing = Mailing.objects.get(unique_id=unique_id)
        except Mailing.DoesNotExist:
            message = 'Mailing does not exist!'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        if data.get('datetime_start'):
            mailing.datetime_start = data.get('datetime_start')
        if data.get('message_text'):
            mailing.message_text = data.get('message_text')
        if data.get('filter_property'):
            mailing.filter_property = data.get('filter_property')
        if data.get('datetime_end'):
            mailing.datetime_end = data.get('datetime_end')
        if data.get('status'):
            mailing.status = data.get('status')
        mailing.save()

        message = {'mailing': MailingSerializer(
            mailing,
            context=self.get_serializer_context()).data,
                   'message': 'Mailing updated successfully'}
        return Response(message)


class RemoveMailingView(generics.GenericAPIView):
    """Removes mailing from the database"""
    permission_classes = [permissions.AllowAny]
    serializer_class = MailingSerializer

    def delete(self, request, *args,  **kwargs):
        try:
            mailing = Mailing.objects.get(unique_id=self.kwargs['unique_id'])
        except Mailing.DoesNotExist:
            message = 'Mailing not found'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        else:
            mailing.delete()

        message = {'client': MailingSerializer(
            mailing,
            context=self.get_serializer_context()).data,
                   'message': 'Mailing removed successfully'}
        return Response(message)


class GetMailingStatisticsView(generics.GenericAPIView):
    """Returns statistics of a chosen mailing"""
    permission_classes = [permissions.AllowAny]
    serializer_class = MessageSerializer

    def get(self, request, *args,  **kwargs):
        unique_id = self.kwargs['unique_id']
        mailing = Mailing.objects.get(unique_id=unique_id)

        messages = Message.objects.filter(mailing=unique_id).filter(status='sent')
        data = []
        for message in messages:
            data.append({'message': MessageSerializer(message, context=self.get_serializer_context()).data})
        return Response(data)


class GetGeneralStatisticsView(generics.GenericAPIView):
    """
    Returns overall statistics of mailings with number of messages
    grouped by they status. Response includes mailing data.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = MailingSerializer

    def get(self, request, *args,  **kwargs):
        data = []
        for mailing in Mailing.objects.all():
            record = {'mailing': MailingSerializer(mailing, context=self.get_serializer_context()).data,
                      'messages_new': Message.objects.filter(mailing=mailing, status='new').count(),
                      'messages_sent': Message.objects.filter(mailing=mailing, status='sent').count(),
                      'messages_error': Message.objects.filter(mailing=mailing, status='error').count()}
            data.append(record)

        return Response(data)
