from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/dream/$", consumers.DreamConsumer.as_asgi()),
]