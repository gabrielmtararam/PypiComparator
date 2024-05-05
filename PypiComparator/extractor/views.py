import os

from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render, reverse
from rest_framework.views import APIView
from extractor.models import GlobalProcessorParameters
import csv
from django.http import HttpResponse
from django.db.models import Q
from extractor.models import ALIndexLinks

from extractor.models import ALIndexLinksAnalysis
from PypiComparator import settings

class HomeExtractor(APIView):
    """View for the Structure list management."""

    def get(self, request, *args, **kwargs):
        """List structures get method."""
        first_global_paramenter = GlobalProcessorParameters.objects.all().first()
        context = {
            'global_parameters': None,
        }
        if first_global_paramenter:
            context['global_parameters'] = first_global_paramenter
        print(f"context ",context)
        return render(request, "extractor_home_page.html", context)


class DownloadALFlapyList(APIView):
    """View for the Structure list management."""

    def get(self, request, *args, **kwargs):
        """List structures get method."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="dados.csv"'

        writer = csv.writer(response)



        queryset = ALIndexLinks.objects.filter(
            flapy_link=None,
            similar_flapy_link=None
        )
        queryset = queryset.filter(Q(is_a_project=True) | Q(is_a_project__isnull=True))

        # Escreva os cabeçalhos CSV
        writer.writerow(
            ["url", "é um projeto","Descrição"])  # Substitua campo1, campo2, ... pelos nomes dos campos que deseja exportar

        # Escreva os dados da queryset no arquivo CSV
        for objeto in queryset:
            writer.writerow([objeto.url, objeto.is_a_project, objeto.short_description])  # Substitua campo1, campo2, ... pelos nomes dos campos correspondentes do objeto

        return response

class DownloadALFlapyCSV(APIView):
    """View for the Structure list management."""

    def get(self, request, *args, **kwargs):
        """List structures get method."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="dados.csv"'

        writer = csv.writer(response)



        queryset = ALIndexLinks.objects.filter(
            flapy_link=None,
            similar_flapy_link=None
        )
        queryset = queryset.filter(Q(is_a_project=True) | Q(is_a_project__isnull=True))

        # Escreva os cabeçalhos CSV
        #PROJECT_NAME,PROJECT_URL,PROJECT_HASH,PYPI_TAG,FUNCS_TO_TRACE,TESTS_TO_RUN
        # localshop,https://github.com/jmcarp/robobrowser,,,,
        writer.writerow(
            ["PROJECT_NAME", "PROJECT_URL","PROJECT_HASH","PYPI_TAG","FUNCS_TO_TRACE","TESTS_TO_RUN"])  # Substitua campo1, campo2, ... pelos nomes dos campos que deseja exportar
        NUM_RUNS = 2
        # Escreva os dados da queryset no arquivo CSV
        for objeto in queryset:
            #               PROJECT_NAME    ,PROJECT_URL,PROJECT_HASH,PYPI_TAG,FUNCS_TO_TRACE,TESTS_TO_RUN
            writer.writerow([objeto.url[-18:-1], objeto.url, "", "", "",
                             "", ])

        return response


class CheckAlFlapyProcessByLog(APIView):
    """View for the Structure list management."""

    def get(self, request, *args, **kwargs):
        """List structures get method."""
        print("requisitou")

        al_query = {
            "flapy_link": None,
            "processed_by_flapy": True,
        }
        al_filtered = ALIndexLinksAnalysis.objects.filter(** al_query)
        runnable_packages_count = 0

        for package in al_filtered:
            folder_name = package.url.replace('/', '').replace('-', '').replace('.', '').replace(':', '')
            base_dir = str(settings.BASE_DIR)
            flapy_dir = base_dir + "/repositories/flapy"
            log_file = flapy_dir + "/log/" + folder_name + ".txt"
            log_file_exists =os.path.exists(log_file)
            csv_log = ""
            load_csv = False
            has_passed_test = False
            find_csv_start = False
            find_done = False
            if log_file_exists:
                with open(log_file, 'r') as log_file_instance:
                    for single_line in log_file_instance:
                        # if '=========' in single_line:
                        if ' passed ' in single_line:
                            has_passed_test = True
                            runnable_packages_count += 1
                            print(f"{single_line.strip()} {package.url}")
                        if find_done:
                            if single_line.startswith(','):
                                # print(f"{single_line.strip()} {package.url}")
                                # runnable_packages_count+=1
                                load_csv = True
                            find_done = False
                        if 'Done' in single_line:
                            find_done = True
                            # print(f"{single_line.strip()} {package.url}")
                        if load_csv and has_passed_test:
                            csv_log += single_line
                    # if load_csv and has_passed_test:
                    #     print(f"csv_log \n {csv_log} {package.url} \n")
        print(f"runnable_packages_count {runnable_packages_count}")
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="dados.csv"'

        # writer = csv.writer(response)
        #
        #
        #
        # queryset = ALIndexLinks.objects.filter(
        #     flapy_link=None,
        #     similar_flapy_link=None
        # )
        # queryset = queryset.filter(Q(is_a_project=True) | Q(is_a_project__isnull=True))
        #
        # # Escreva os cabeçalhos CSV
        # #PROJECT_NAME,PROJECT_URL,PROJECT_HASH,PYPI_TAG,FUNCS_TO_TRACE,TESTS_TO_RUN
        # # localshop,https://github.com/jmcarp/robobrowser,,,,
        # writer.writerow(
        #     ["PROJECT_NAME", "PROJECT_URL","PROJECT_HASH","PYPI_TAG","FUNCS_TO_TRACE","TESTS_TO_RUN"])  # Substitua campo1, campo2, ... pelos nomes dos campos que deseja exportar
        # NUM_RUNS = 2
        # # Escreva os dados da queryset no arquivo CSV
        # for objeto in queryset:
        #     #               PROJECT_NAME    ,PROJECT_URL,PROJECT_HASH,PYPI_TAG,FUNCS_TO_TRACE,TESTS_TO_RUN
        #     writer.writerow([objeto.url[-18:-1], objeto.url, "", "", "",
        #                      "", ])

        return HttpResponse()


class SimpleIndexExtractor(APIView):
    """View for the Structure list management."""

    def get(self, request, *args, **kwargs):
        """List structures get method."""
        first_global_paramenter = GlobalProcessorParameters.objects.all().first()
        context = {
            'global_parameters': None
        }
        if first_global_paramenter:
            context['global_parameters'] = first_global_paramenter
        print(f"context ",context)
        return render(request, "extractor_home_page.html", context)
