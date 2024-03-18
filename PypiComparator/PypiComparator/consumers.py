import json
import random
from time import sleep
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from asyncio import Queue

from channels.generic.websocket import AsyncWebsocketConsumer
import random
from time import sleep
from PypiComparator import settings
import requests
import os
from bs4 import BeautifulSoup

from extractor.models import PypiSimpleIndexLinks

from extractor.models import GlobalProcessorParameters

from extractor.models import PypiProcessedLink

diretorio_atual = os.path.dirname(__file__)


class SimpleIndexProcessorHandler():
    stop_processing = False
    processing = False
    index_processor_websocket = None
    index_processor_websocket_queue = None

    @staticmethod
    async def extract_simple_index_project_link(link):
        url_base = 'https://pypi.org/project/'

        link_completo = url_base + link['href'].replace('/simple/', '')
        old_instance = await sync_to_async(PypiSimpleIndexLinks.objects.filter)(pypi_project_url=link_completo)
        old_instance = await sync_to_async(old_instance.exists)()
        if not old_instance:
            await PypiSimpleIndexLinks.objects.acreate(
                href=link['href'],
                pypi_project_url=link_completo,
                processed_message="False",
                processed=False,
                successful_processed=False,
                home_page_found=False,
            )
            return {'message': f"link cadastrado com sucesso {link_completo}", 'level': 'success'}
        else:
            return {'message': f"link já cadastrado {link_completo}", 'level': 'warning'}

    @staticmethod
    async def start_processing(queue):
        SimpleIndexProcessorHandler.index_processor_websocket_queue = queue
        if not SimpleIndexProcessorHandler.processing:
            # for i in range(15):
            #     sleeptime = random.uniform(1, 3)
            #     await asyncio.sleep(sleeptime)

            pasta_destino = os.path.join(settings.BASE_DIR, "extractor/extracted_files/simple_index_file.html")

            # Abre o arquivo HTML e conta os links
            stop = False
            print(f"start_processing folder")
            with open(pasta_destino, 'r') as html_file:
                soup = BeautifulSoup(html_file, 'html.parser')
                links = soup.find_all('a', href=True)

                # Conta os links no formato especificado
                contador_links = 0
                for link in links:
                    if link['href'].startswith('/simple/'):
                        contador_links += 1
                        message_data = await SimpleIndexProcessorHandler.extract_simple_index_project_link(link)
                        # check_pypi_homepage_link(link)
                    else:
                        message_data = {'message': f"link invalido {link['href']}", 'level': 'error'}
                    # if contador_links > 125:
                    #     break
                    await queue.put(message_data)
                    if SimpleIndexProcessorHandler.stop_processing:
                        break

                print(f'Total de links no formato especificado: {contador_links}')
            await queue.put({'message': f"todos os links cadastrados com sucesso {contador_links}", 'level': 'error'})
            return


class SimpleIndexUrlProcessorHandler():
    stop_processing = False
    processing = False
    index_processor_websocket = None
    index_processor_websocket_queue = None

    @staticmethod
    async def process_links(project_link):

        response_link = requests.get(project_link)

        if response_link.status_code == 200:
            soup_link = BeautifulSoup(response_link.content, 'html.parser')

            # Verifica se a página contém o ícone 'fas fa-home'
            icone = soup_link.find('i', class_='fas fa-home')
            if icone:
                link_homepage = icone.find_parent('a', href=True)
                return {'message': f"link processado com sucesso {str(link_homepage['href'])}", 'level': 'success'},False,link_homepage['href']
            return {'message': f"home page não encontrada  {project_link}", 'level': 'error'},True,None
        else:
            return {'message': f"link do projeto não encontrado  {project_link}", 'level': 'error'},False,None

        # url_base = 'https://pypi.org/project/'
        #
        # link_completo = url_base + link['href'].replace('/simple/', '')
        # old_instance = await sync_to_async(PypiSimpleIndexLinks.objects.filter)(pypi_project_url=link_completo)
        # old_instance = await sync_to_async(old_instance.exists)()
        # if not old_instance:
        #     await PypiSimpleIndexLinks.objects.acreate(
        #         href=link['href'],
        #         pypi_project_url=link_completo,
        #         processed_message="False",
        #         processed=False,
        #         successful_processed=False,
        #         home_page_found=False,
        #     )

    @staticmethod
    @sync_to_async
    def get_links():
        first_global_paramenter = GlobalProcessorParameters.objects.all().first()
        n = first_global_paramenter.total_links_to_process_per_chunck

        simple_index_records = PypiSimpleIndexLinks.objects.filter(processed=False)
        simple_index_records = simple_index_records.order_by('-id')
        simple_index_records = simple_index_records[:n]
        return list(simple_index_records)

    @staticmethod
    @sync_to_async
    def create_processed_link(simple_index_link, link_homepage ):
        first_global_paramenter = PypiProcessedLink.objects.filter(simple_index=simple_index_link)
        if not first_global_paramenter.exists():
             PypiProcessedLink.objects.create(
                simple_index=simple_index_link,
                homepage_link=link_homepage,
            )

    @staticmethod
    async def start_processing(queue):
        SimpleIndexUrlProcessorHandler.index_processor_websocket_queue = queue
        if not SimpleIndexUrlProcessorHandler.processing:

            # old_instance = await sync_to_async(PypiSimpleIndexLinks.objects.filter)(pypi_project_url=link_completo)
            # old_instance = await sync_to_async(old_instance.exists)()

            # simple_index_records = await sync_to_async(simple_index_records)
            # print("simple_index_records ", simple_index_records)
            link_homepage = None
            simple_index_records = await SimpleIndexUrlProcessorHandler.get_links()
            contador_links = 0
            for simple_index_link in simple_index_records:
                if simple_index_link.pypi_project_url:
                    contador_links += 1
                    message_data,home_page_not_found,link_homepage = await SimpleIndexUrlProcessorHandler.process_links(
                        simple_index_link.pypi_project_url)
                    print("message_data ", message_data)
                    simple_index_link.home_page_found = not home_page_not_found
                    # check_pypi_homepage_link(link)
                else:
                    message_data = {'message': f"Url do projeto não encontrada {simple_index_link.href}",
                                    'level': 'error'}

                if message_data['level'] == 'error':
                    simple_index_link.processed_message = message_data['message']
                    simple_index_link.successful_processed = False
                elif message_data['level'] == 'success':
                    simple_index_link.processed_message = message_data['message']
                    simple_index_link.successful_processed = True
                    await SimpleIndexUrlProcessorHandler.create_processed_link(
                        simple_index_link, link_homepage)

                # if contador_links > 125:
                #     break
                simple_index_link.processed = True
                await sync_to_async(simple_index_link.save)()
                await queue.put(message_data)
                if SimpleIndexUrlProcessorHandler.stop_processing:
                    break

                print(f'Total de links processados, com o url do projeto: {contador_links}')
            await queue.put({'message': f"Total de links processados com sucesso {contador_links}", 'level': 'error'})
            return


class SimpleIndexUrlExtractorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.queue = Queue()
        self.stop_processing = False

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'feedback_message_value',
            'message': "started_socket_sucessefuly"
        }))

    async def process_messages(self):
        asyncio.create_task(SimpleIndexUrlProcessorHandler.start_processing(self.queue))
        while True:
            message = await self.queue.get()
            await self.send_feedback_message_level(message)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == "start_processing_simple_index_url":
            asyncio.create_task(self.process_messages())
        elif message == "stop_processing_simple_index_url":
            SimpleIndexUrlProcessorHandler.stop_processing = True

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


class SimpleIndexExtractorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.queue = Queue()
        self.stop_processing = False

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'feedback_message_value',
            'message': "started_socket_sucessefuly_xx"
        }))

    async def process_messages(self):
        asyncio.create_task(SimpleIndexProcessorHandler.start_processing(self.queue))
        while True:
            message = await self.queue.get()
            await self.send_feedback_message_level(message)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == "start_processing_simple_index":
            asyncio.create_task(self.process_messages())
        elif message == "stop_processing_simple_index":
            SimpleIndexProcessorHandler.stop_processing = True

    async def send_feedback_message(self, message):
        await self.send(text_data=json.dumps({
            'type': 'success',
            'message': message
        }))

    async def send_feedback_message_level(self, message):
        await self.send(text_data=json.dumps({
            'type': message['level'],
            'message': message['message']
        }))
