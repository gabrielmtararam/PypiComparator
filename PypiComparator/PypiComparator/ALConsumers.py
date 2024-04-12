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

from extractor.models import PyPiFlapyIndexLinks
from extractor.models import ALIndexLinks

diretorio_atual = os.path.dirname(__file__)

import csv


class ALComparerHandler():
    stop_processing = False
    processing = False
    index_processor_websocket = None
    index_processor_websocket_queue = None

    @staticmethod
    async def compare_with_pypi_record(link):
        search_link= link.replace('https://', '')
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
    async def start_processing(queue):
        ALComparerHandler.index_processor_websocket_queue = queue
        if not ALComparerHandler.processing:
            pipy_urls_file = os.path.join(settings.BASE_DIR, "extractor/extracted_files/links_awsome_python.txt")

            link_count = 0
            with open(pipy_urls_file, newline='') as Allinks:

                for link in Allinks:
                    link = link.strip()
                    if link.startswith('http'):
                        message_data = await ALComparerHandler.compare_with_pypi_record(link)
                    else:
                        message_data = {'message': f"link invalido {link}", 'level': 'error'}
                    link_count += 1
                    await queue.put(message_data)


                print(f'Total de links no formato especificado: {link_count}')
            await queue.put({'message': f"todos os links cadastrados com sucesso {link_count}", 'level': 'error'})
            return


class ALUrlComparerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.queue = Queue()
        self.stop_processing = False

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'feedback_message_value',
            'message': "started_socket_sucessefuly"
        }))

    async def process_messages(self):
        asyncio.create_task(ALComparerHandler.start_processing(self.queue))
        while True:
            message = await self.queue.get()
            await self.send_feedback_message_level(message)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == "start_processing_al":
            asyncio.create_task(self.process_messages())
        elif message == "stop_processing_al":
            ALComparerHandler.stop_processing = True

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


class ALComparerSimilarHandler():
    stop_processing = False
    processing = False
    index_processor_websocket = None
    index_processor_websocket_queue = None

    @staticmethod
    async def compare_with_similar_pypi_record(link):

        search_link= link.replace('https://github.com', '')
        search_link = search_link.replace('http://github.com', '')

        search_link = search_link.split('/')

        search_link_last_world = search_link[-1]

        old_flapy_instance = await sync_to_async(PyPiFlapyIndexLinks.objects.filter)(url__icontains=search_link_last_world)
        old_flapy_instance_exists = await sync_to_async(old_flapy_instance.exists)()

        old_al_instance = await sync_to_async(ALIndexLinks.objects.filter)(url=link)
        old_al_instance_exists = await sync_to_async(old_al_instance.exists)()

        if old_al_instance_exists:
            if not old_flapy_instance_exists:
                return {'message': f"al link já cadastrado, flapy equivalente não encontrado {link} palavra {search_link_last_world}", 'level': 'error'}
            else:
                old_flapy_instance = await sync_to_async(old_flapy_instance.first)()
                old_al_instance = await sync_to_async(old_al_instance.first)()
                al_attr_compare = True

                old_al_instance_flapy_link = await sync_to_async(lambda: old_al_instance.flapy_link)()
                if old_al_instance_flapy_link:
                    al_attr_compare = old_al_instance_flapy_link.pk != old_flapy_instance.pk

                if al_attr_compare:
                    old_al_instance.similar_flapy_link = old_flapy_instance
                    await sync_to_async(old_al_instance.save)()
                else:
                    return {
                        'message': f" al link flay link igual ao similar{link}  palavra {search_link_last_world}",
                        'level': 'warning'}
                return {'message': f" al link já cadastrado, flapy equivalente encontrado {link}  palavra {search_link_last_world}", 'level': 'success'}
        else:
            return {'message': f" al link ainda não cadastrado {link}  palavra {search_link_last_world}", 'level': 'error'}

    @staticmethod
    async def start_processing(queue):
        ALComparerSimilarHandler.index_processor_websocket_queue = queue
        if not ALComparerSimilarHandler.processing:
            pipy_urls_file = os.path.join(settings.BASE_DIR, "extractor/extracted_files/links_awsome_python.txt")

            link_count = 0
            with open(pipy_urls_file, newline='') as Allinks:

                for link in Allinks:
                    link = link.strip()
                    if link.startswith('http'):
                        message_data = await ALComparerSimilarHandler.compare_with_similar_pypi_record(link)
                    else:
                        message_data = {'message': f"link invalido {link}", 'level': 'error'}
                    link_count += 1
                    await queue.put(message_data)

                print(f'Total de links no formato especificado: {link_count}')
            await queue.put({'message': f"todos os links cadastrados com sucesso {link_count}", 'level': 'error'})
            return


class ALUrlComparerSimilarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.queue = Queue()
        self.stop_processing = False

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'feedback_message_value',
            'message': "started_socket_sucessefuly"
        }))

    async def process_messages(self):
        asyncio.create_task(ALComparerSimilarHandler.start_processing(self.queue))
        while True:
            message = await self.queue.get()
            await self.send_feedback_message_level(message)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == "start_processing_al":
            asyncio.create_task(self.process_messages())
        elif message == "stop_processing_al":
            ALComparerSimilarHandler.stop_processing = True

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

