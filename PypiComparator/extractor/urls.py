"""
URL configuration for PypiComparator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from .views import HomeExtractor, SimpleIndexExtractor, DownloadALFlapyList, DownloadALFlapyCSV,CheckAlFlapyProcessByLog

from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('', HomeExtractor.as_view(), name='stractor'),
    path('extract-urls-from-simple-index', SimpleIndexExtractor.as_view(), name='extract_urls_from_simple_index'),
    path('download-al-flapy-list', DownloadALFlapyList.as_view(), name='download_al_flapy_list'),
    path('download-al-flapy-csv', DownloadALFlapyCSV.as_view(), name='download_al_flapy_csv'),
    path('check-al-flapy-process-by-log', CheckAlFlapyProcessByLog.as_view(), name='check_al_flapy_process_by_log'),
]