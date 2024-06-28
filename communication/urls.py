from django.urls import path

from . import views
from .views import global_chat, private_chat, fetch_private_messages

urlpatterns = [
    path('global_chat/', global_chat, name='global_chat'),
    path('private_chat/<int:user_id>/', private_chat, name='private_chat'),
    path('fetch_private_messages/<int:user_id>/', fetch_private_messages, name='fetch_private_messages'),
]

