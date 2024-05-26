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

import os
import shutil
import subprocess
from time import sleep
import git

diretorio_atual = os.path.dirname(__file__)


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
                        if ' passed in ' in single_line:
                            has_passed_test = True
                            runnable_packages_count += 1
                            print(f"{single_line.strip()} {package.url}")
                            package.can_run_flapy = True
                            package.save()
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



class CheckAlFlapyProcessByLog400(APIView):
    """View for the Structure list management."""


    @staticmethod
    def create_flapy_file(output_folder, package_folder_dir, package_name):
        try:

            output_folder_exists = os.path.exists(output_folder)
            if output_folder_exists:
                os.remove(output_folder)

            with open(output_folder, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["PROJECT_NAME", "PROJECT_URL", "PROJECT_HASH", "PYPI_TAG", "FUNCS_TO_TRACE",
                     "TESTS_TO_RUN"])
                NUM_RUNS = 2
                # Escreva os dados da queryset no arquivo CSV
                writer.writerow([package_name, package_folder_dir, "", "", "",
                                 "", ])

            print("csv criado com sucesso!")

        except git.GitCommandError as e:
            print(e)
    @staticmethod
    def run_flapy(output_folder, flapy_dir, bash_file_dir, log_file, package_folder_dir, folder_name):
        try:
            os.chdir(flapy_dir, )
            print("\n#######iniciando bash")

            # comando_terminal = f"gnome-terminal -- bash -c '{bash_file_dir} >> {log_file} && rm -rf {package_folder_dir}; exit'"
            comando_terminal = f"gnome-terminal -- bash -c '{bash_file_dir} >> {log_file} && rm -rf {package_folder_dir} && rm -rf results/example_results_{folder_name}; exit'"
            print(comando_terminal)

            subprocess.run(comando_terminal, shell=True)
            # output = subprocess.run(["bash", bash_file_dir])

            with open(log_file, 'r') as output_file:
                saida_terminal = output_file.read()
            print(saida_terminal)
            print("#######fim bash\n")
          
        except Exception as e:
            print("except")
            print(e)
    @staticmethod
    def clone_project(url_repo, output_folder):
        try:
            os.mkdir(output_folder)
            git.Repo.clone_from(url_repo, output_folder)
            print("Projeto clonado com sucesso!")
        except git.GitCommandError as e:
            print(e)
    @staticmethod
    def create_bash_file(bash_file_dir, output_folder, folder_name):
        try:
            bash_command = f"./flapy.sh run --out-dir results/example_results_{folder_name} --plus-random-runs {output_folder} 20  && " \
                           f"./flapy.sh parse ResultsDirCollection --path results/example_results_{folder_name} get_tests_overview _df to_csv --index=false"

            bash_file_dir_exists = os.path.exists(bash_file_dir)
            if bash_file_dir_exists:
                os.remove(bash_file_dir)

            # Escreva o conteúdo do script em um arquivo
            with open(bash_file_dir, "w") as bash_file:
                bash_file.write(bash_command)

            os.chmod(bash_file_dir, 0o755)
            print("bash criado com sucesso!")
        except Exception as e:
            print(e)

    @staticmethod
    def start_processing():
        print("start processing")
        flapy_github_url = "https://github.com/se2p/FlaPy"
        base_dir = str(settings.BASE_DIR)
        flapy_dir = base_dir + "/repositories/flapy"
        rep_dir = base_dir + "/repositories2/"

        rep_dir_exists = os.path.exists(rep_dir)
        if not rep_dir_exists:
            os.mkdir(rep_dir)

        max_packages = 30

        #  CheckAlFlapyProcessByLog400.clone_project(flapy_github_url, flapy_dir)

        bash_file_dir = flapy_dir + "/run_custom_flapy_2.sh"
        output_folder = flapy_dir + "/temporary_example_2.csv"
        log_folder = flapy_dir + "/log2"

        log_folder_exists = os.path.exists(log_folder)
        if not log_folder_exists:
            os.mkdir(log_folder)
            # shutil.rmtree)(log_folder)
        # os.mkdir)(log_folder)

        al_query = {
            "flapy_link": None,
            "processed_by_flapy": True,
            "can_run_flapy": True,
            "processed_by_flapy_400": False,
        }
        al_filtered = ALIndexLinksAnalysis.objects.filter(**al_query)
        qtd_pacotes = al_filtered.count()
        print(qtd_pacotes)
        print(base_dir)

        count = 0
        al_filtered = list(al_filtered)
        for package in al_filtered:
            count += 1
            folder_name = package.url.replace('/', '').replace('-', '').replace('.', '').replace(':', '')
            package_folder_dir = rep_dir + folder_name + ""

            log_file = flapy_dir + "/log2/" + folder_name + ".txt"
            CheckAlFlapyProcessByLog400.create_bash_file(bash_file_dir, output_folder, folder_name)

            print_value = f"count {package.url} package_folder_dir  {package_folder_dir}"
            print(print_value)

            package_folder_dirr_exists = os.path.exists(package_folder_dir)
            if package_folder_dirr_exists:
                shutil.rmtree(package_folder_dir)

            CheckAlFlapyProcessByLog400.clone_project(package.url, package_folder_dir + "/")

            CheckAlFlapyProcessByLog400.create_flapy_file(output_folder, package_folder_dir, folder_name)

            CheckAlFlapyProcessByLog400.run_flapy(output_folder, flapy_dir, bash_file_dir, log_file, package_folder_dir,
                                                  folder_name)

            package.processed_by_flapy_400 = True
            package.save()
            print(count)
            if count >= max_packages:
                break
            sleep(60*20)
            print("fim tudo")
        return

    def get(self, request, *args, **kwargs):
        """List structures get method."""
        print("requisitou")
        CheckAlFlapyProcessByLog400.start_processing()
        print("requisitou fim")

        # al_query = {
        #     "flapy_link": None,
        #     "processed_by_flapy": True,
        #     "can_run_flapy": True,
        # }
        # al_filtered = ALIndexLinksAnalysis.objects.filter(** al_query)
        # runnable_packages_count = 0
        #
        # for package in al_filtered:
        #     folder_name = package.url.replace('/', '').replace('-', '').replace('.', '').replace(':', '')
        #     base_dir = str(settings.BASE_DIR)
        #     flapy_dir = base_dir + "/repositories/flapy"
        #     log_file = flapy_dir + "/log/" + folder_name + ".txt"
        #     log_file_exists =os.path.exists(log_file)
        #     csv_log = ""
        #     load_csv = False
        #     has_passed_test = False
        #     find_csv_start = False
        #     find_done = False
        #     if log_file_exists:
        #         with open(log_file, 'r') as log_file_instance:
        #             for single_line in log_file_instance:
        #                 # if '=========' in single_line:
        #                 if ' passed in ' in single_line:
        #                     has_passed_test = True
        #                     runnable_packages_count += 1
        #                     print(f"{single_line.strip()} {package.url}")
        #                     package.can_run_flapy = True
        #                     package.save()
        #                 if find_done:
        #                     if single_line.startswith(','):
        #                         # print(f"{single_line.strip()} {package.url}")
        #                         # runnable_packages_count+=1
        #                         load_csv = True
        #                     find_done = False
        #                 if 'Done' in single_line:
        #                     find_done = True
        #                     # print(f"{single_line.strip()} {package.url}")
        #                 if load_csv and has_passed_test:
        #                     csv_log += single_line
        #             # if load_csv and has_passed_test:
        #             #     print(f"csv_log \n {csv_log} {package.url} \n")
        # print(f"runnable_packages_count {runnable_packages_count}")
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
