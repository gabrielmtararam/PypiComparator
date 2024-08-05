from django.urls import re_path 
from . import consumers, ALConsumers,ALFlapyConsumers

websocket_urlpatterns = [
    re_path(r'ws/process-al-urls/', consumers.ALUrlExtractorConsumer.as_asgi()),
    re_path(r'ws/compare-al-urls/', ALConsumers.ALUrlComparerConsumer.as_asgi()),
    re_path(r'ws/compare-similar-al-urls/', ALConsumers.ALUrlComparerSimilarConsumer.as_asgi()),
    re_path(r'ws/check-al-flapy-process/', ALFlapyConsumers.CheckAlFlapyProcess.as_asgi())
]
