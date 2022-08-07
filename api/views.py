import json
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .models import Mailing, Client, Message
from .serializers import MailingSerializer, ClientSerializer, MessageSerializer


class CreateClientView(generics.GenericAPIView):
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
            client.save()
        else:
            message = 'Client already exists!'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        message = {'client': ClientSerializer(
            client,
            context=self.get_serializer_context()).data,
                   'message': 'Client created successfully'}
        return Response(message)


class GetUserView(generics.GenericAPIView):
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
        client.save()

        message = {'client': ClientSerializer(
            client,
            context=self.get_serializer_context()).data,
                   'message': 'User updated successfully'}
        return Response(message)


class RemoveClientView(generics.GenericAPIView):
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
        mailing.save()

        message = {'mailing': MailingSerializer(
            mailing,
            context=self.get_serializer_context()).data,
                   'message': 'Mailing updated successfully'}
        return Response(message)


class RemoveMailingView(generics.GenericAPIView):
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
