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

from .views import HomeExtractor, DownloadALFlapyList, DownloadALFlapyCSV, \
    CheckAlFlapyProcessByLog, CheckAlFlapyProcessByLog400, GenerateCSVAlFlapyProcessByLog400, \
    getRepositoriesCommitHashCode

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', HomeExtractor.as_view(), name='stractor'),
    path('download-al-flapy-list', DownloadALFlapyList.as_view(), name='download_al_flapy_list'),
    path('download-al-flapy-csv', DownloadALFlapyCSV.as_view(), name='download_al_flapy_csv'),
    path('check-al-flapy-process-by-log', CheckAlFlapyProcessByLog.as_view(), name='check_al_flapy_process_by_log'),
    path('check-al-flapy-process-by-log-400', CheckAlFlapyProcessByLog400.as_view(),
         name='check_al_flapy_process_by_log_400'),
    path('generate-csv-al-flapy-process-by-log-400', GenerateCSVAlFlapyProcessByLog400.as_view(),
         name='generate_csv_al_flapy_process_by_log_400'),
    path('get-repositories-commit-hash-code', getRepositoriesCommitHashCode.as_view(),
         name='get_repositories_commit_hash_code'),
]
