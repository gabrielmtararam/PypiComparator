from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', consumers.SimpleIndexExtractorConsumer.as_asgi()),
    re_path(r'ws/process-urls/', consumers.SimpleIndexUrlExtractorConsumer.as_asgi())
]
# https://www.youtube.com/watch?v=cw8-KFVXpTE