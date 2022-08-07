from django.urls import path

from .views import (CreateClientView, GetUserView, UpdateClientView, RemoveClientView,
                    CreateMailingView, GetMailingView, UpdateMailingView, RemoveMailingView)

urlpatterns = [
    path('create_client/', CreateClientView.as_view()),
    path('get_client/<int:unique_id>/', GetUserView.as_view()),
    path('update_client/<int:unique_id>/', UpdateClientView.as_view()),
    path('remove_client/<int:unique_id>/', RemoveClientView.as_view()),
    path('create_mailing/', CreateMailingView.as_view()),
    path('get_mailing/<int:unique_id>/', GetMailingView.as_view()),
    path('update_mailing/<int:unique_id>/', UpdateMailingView.as_view()),
    path('remove_mailing/<int:unique_id>/', RemoveMailingView.as_view()),
]
