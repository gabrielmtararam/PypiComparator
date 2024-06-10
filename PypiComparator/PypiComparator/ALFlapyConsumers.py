import json
import random
from time import sleep, time
import asyncio
import git
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from asyncio import Queue

from channels.generic.websocket import AsyncWebsocketConsumer
import random
from time import sleep
from PypiComparator import settings
import requests
import os
import shutil
import subprocess
import tempfile

from bs4 import BeautifulSoup

from extractor.models import PypiSimpleIndexLinks

from extractor.models import GlobalProcessorParameters

from extractor.models import PypiProcessedLink

from extractor.models import PyPiFlapyIndexLinks
from extractor.models import ALIndexLinks

from extractor.models import ALIndexLinksAnalysis

diretorio_atual = os.path.dirname(__file__)

import csv

# arquivos que nao rodaram
#httpsgithubcomfacebookresearchpytext
#/httpsgithubcomjfkirktensorrec n sei o pq
#httpsgithubcomIronLanguagesironpython3 cmake compile

#httpsgithubcomr0x0rpywebview
#httpsgithubcomchriskiehlGooey
#httpsgithubcomMicrosoftPTVS
#httpsgithubcomajentiajenti



class CheckAlFlapyProcessHandler():
    stop_processing = False
    processing = False
    index_processor_websocket = None
    index_processor_websocket_queue = None

    @staticmethod
    async def compare_with_pypi_record(link):
        search_link = link.replace('https://', '')
        search_link = search_link.replace('http://', '')
        old_flapy_instance = await sync_to_async(PyPiFlapyIndexLinks.objects.filter)(url__icontains=search_link)
        old_flapy_instance_exists = await sync_to_async(old_flapy_instance.exists)()

        old_al_instance = await sync_to_async(ALIndexLinks.objects.filter)(url=link)
        old_al_instance_exists = await sync_to_async(old_al_instance.exists)()

        if old_al_instance_exists:
            if not old_flapy_instance_exists:
                return {'message': f"al link já cadastrado, flapy equivalente não encontrado {link}", 'level': 'error'}
            else:
                return {'message': f" al link já cadastrado, flapy equivalente encontrado {link}", 'level': 'success'}
        else:
            new_al_link = await ALIndexLinks.objects.acreate(
                url=link,
            )

            if not old_flapy_instance_exists:
                return {'message': f"al link cadastrado, flapy equivalente não encontrado {link}", 'level': "warning"}
            else:
                old_flapy_instance = await sync_to_async(old_flapy_instance.first)()

                new_al_link.flapy_link = old_flapy_instance
                await sync_to_async(new_al_link.save)()
                return {'message': f" al link cadastrado, flapy equivalente encontrado {link}", 'level': 'success'}

    @staticmethod
    async def clone_project(url_repo, output_folder):
        try:
            await sync_to_async(os.mkdir)(output_folder)
            await sync_to_async(git.Repo.clone_from)(url_repo, output_folder)
            await sync_to_async(print)("Projeto clonado com sucesso!")
        except git.GitCommandError as e:
            await sync_to_async(print)(e)

    @staticmethod
    async def run_flapy(output_folder, flapy_dir, bash_file_dir, log_file, package_folder_dir, folder_name):
        try:
            os.chdir(flapy_dir,)
            await sync_to_async(print)("\n#######iniciando bash")

            # comando_terminal = f"gnome-terminal -- bash -c '{bash_file_dir} >> {log_file} && rm -rf {package_folder_dir}; exit'"
            comando_terminal = f"touch {log_file} && " \
                               f"gnome-terminal -- bash -c '{bash_file_dir} >> {log_file} && rm -rf {package_folder_dir} && rm -rf results/example_results_{folder_name}; exit'"
            await sync_to_async(print)(comando_terminal)

            subprocess.run(comando_terminal, shell=True)
            # output = subprocess.run(["bash", bash_file_dir])

            with open(log_file, 'r') as output_file:
                saida_terminal = output_file.read()
            await sync_to_async(print)(saida_terminal)
            await sync_to_async(print)("#######fim bash\n")
            # bash_command = f"cd {flapy_dir} && ./flapy.sh run --out-dir example_results {output_folder} 1"
            #
            # await sync_to_async(print)(bash_command)
            #
            # # output = subprocess.run(bash_command, shell=True, capture_output=True, text=True, stdin=subprocess.PIPE)
            # # await sync_to_async(print)(output.stdout)
            # # await sync_to_async(print)(output.stderr)
            #
            # processo = subprocess.Popen(bash_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            #                             stdin=subprocess.PIPE)
            #
            # # Capturando a saída e os erros
            # saida, erro = processo.communicate()
            #
            # # Verificando se a execução do comando foi bem-sucedida
            #     # Exibindo a saída do comando
            #
            # await sync_to_async(print)("ccccSaída do comando:")
            #
            # await sync_to_async(print)(saida.decode())
            #
            # await sync_to_async(print)("\n zzzzErro ao executar o comando:")
            # await sync_to_async(print)(erro.decode())
            #
            # await sync_to_async(print)("#######fim bash\n")
        except Exception as e:
            await sync_to_async(print)("except")
            await sync_to_async(print)(e)

    @staticmethod
    async def create_flapy_file(output_folder, package_folder_dir, package_name):
        try:

            output_folder_exists = await sync_to_async(os.path.exists)(output_folder)
            if output_folder_exists:
                await sync_to_async(os.remove)(output_folder)

            with open(output_folder, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["PROJECT_NAME", "PROJECT_URL", "PROJECT_HASH", "PYPI_TAG", "FUNCS_TO_TRACE",
                     "TESTS_TO_RUN"])
                NUM_RUNS = 70
                # Escreva os dados da queryset no arquivo CSV
                writer.writerow([package_name, package_folder_dir, "", "", "",
                                 "", ])

            await sync_to_async(print)("csv criado com sucesso!")
        except git.GitCommandError as e:
            await sync_to_async(print)(e)

    @staticmethod
    async def create_bash_file(bash_file_dir, output_folder, folder_name, flapy_dir):
        try:
            bash_command = f" time ./flapy.sh run --out-dir ./results/example_results_{folder_name} {output_folder} 1  && " \
                           f" time ./flapy.sh parse ResultsDirCollection --path ./results/example_results_{folder_name} get_tests_overview _df to_csv --index=false"

            bash_file_dir_exists = await sync_to_async(os.path.exists)(bash_file_dir)
            if bash_file_dir_exists:
                await sync_to_async(os.remove)(bash_file_dir)

            # Escreva o conteúdo do script em um arquivo
            with open(bash_file_dir, "w") as bash_file:
                bash_file.write(bash_command)

            os.chmod(bash_file_dir, 0o755)
            await sync_to_async(print)("bash criado com sucesso!")
        except Exception as e:
            await sync_to_async(print)(e)

    @staticmethod
    async def start_processing(queue):
        await sync_to_async(print)("start processing")
        CheckAlFlapyProcessHandler.index_processor_websocket_queue = queue
        flapy_github_url = "https://github.com/gabrielmtararam/FlaPy-custom"
        base_dir = await sync_to_async(str)(settings.BASE_DIR)
        flapy_dir = base_dir + "/repositories/flapy"
        rep_dir = base_dir + "/repositories/"

        # flapy_folder_exists = await sync_to_async(os.path.exists)(flapy_dir)
        # if flapy_folder_exists:
        #     await sync_to_async(shutil.rmtree)(flapy_dir)

        max_packages = 500

        # await CheckAlFlapyProcessHandler.clone_project(flapy_github_url, flapy_dir)
        if not CheckAlFlapyProcessHandler.processing:

            bash_file_dir = flapy_dir+"/run_custom_flapy.sh"
            output_folder = flapy_dir + "/temporary_example.csv"
            log_folder = flapy_dir + "/log"

            log_folder_exists = await sync_to_async(os.path.exists)(log_folder)
            if not log_folder_exists:
                await sync_to_async(os.mkdir)(log_folder)
                # await sync_to_async(shutil.rmtree)(log_folder)
            # await sync_to_async(os.mkdir)(log_folder)


            al_query = {
                "flapy_link": None,
                "processed_by_flapy": False,
            }
            al_filtered = await sync_to_async(ALIndexLinksAnalysis.objects.filter)(**al_query)
            qtd_pacotes = await sync_to_async(al_filtered.count)()
            await sync_to_async(print)(qtd_pacotes)
            await sync_to_async(print)(base_dir)

            count = 0
            al_filtered = await sync_to_async(list)(al_filtered)
            for package in al_filtered:
                count += 1
                folder_name = package.url.replace('/', '').replace('-', '').replace('.', '').replace(':', '')
                package_folder_dir = rep_dir + folder_name + ""

                log_file = flapy_dir + "/log/"+folder_name+".txt"
                await CheckAlFlapyProcessHandler.create_bash_file(bash_file_dir, output_folder, folder_name, flapy_dir)

                print_value = f"count {package.url} package_folder_dir  {package_folder_dir}"
                await sync_to_async(print)(print_value)

                package_folder_dirr_exists = await sync_to_async(os.path.exists)(package_folder_dir)
                if package_folder_dirr_exists:
                    await sync_to_async(shutil.rmtree)(package_folder_dir)

                await CheckAlFlapyProcessHandler.clone_project(package.url, package_folder_dir + "/")

                await CheckAlFlapyProcessHandler.create_flapy_file(output_folder, package_folder_dir, folder_name)

                await CheckAlFlapyProcessHandler.run_flapy(output_folder, flapy_dir, bash_file_dir, log_file, package_folder_dir, folder_name)
                package.processed_by_flapy = True
                await sync_to_async(package.save)()
                await sync_to_async(print)(count)
                if count >= max_packages:
                    break
                sleep(30)
            await sync_to_async(print)("fim tudo")
            # os.rmdir(flapy_dir)

            # pipy_urls_file = os.path.join(settings.BASE_DIR, "extractor/extracted_files/links_awsome_python.txt")
            #
            # link_count = 0
            # with open(pipy_urls_file, newline='') as Allinks:
            #
            #     for link in Allinks:
            #         link = link.strip()
            #         if link.startswith('http'):
            #             message_data = await CheckAlFlapyProcessHandler.compare_with_pypi_record(link)
            #         else:
            #             message_data = {'message': f"link invalido {link}", 'level': 'error'}
            #         link_count += 1
            #         await queue.put(message_data)

            # print(f'Total de links no formato especificado: {link_count}')
            await queue.put({'message': f"todos os links cadastrados com sucesso ", 'level': 'error'})
            return


class CheckAlFlapyProcess(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect here")
        self.queue = Queue()
        self.stop_processing = False

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'feedback_message_value',
            'message': "started_socket_sucessefuly"
        }))

    async def process_messages(self):
        asyncio.create_task(CheckAlFlapyProcessHandler.start_processing(self.queue))
        while True:
            message = await self.queue.get()
            await self.send_feedback_message_level(message)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == "start_processing_al":
            asyncio.create_task(self.process_messages())
        elif message == "stop_processing_al":
            CheckAlFlapyProcessHandler.stop_processing = True

    async def send_feedback_message(self, message):
        await self.send(text_data=json.dumps({
            'type': 'success',
            'message': message
        }))

    async def send_feedback_message_level(self, message):
        # print("message ",message)
        await self.send(text_data=json.dumps({
            'type': message['level'],
            'message': message['message']
        }))
