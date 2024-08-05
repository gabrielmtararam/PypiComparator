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





class ALProcessorHandler():
    stop_processing = False
    processing = False
    index_processor_websocket = None
    index_processor_websocket_queue = None

    @staticmethod
    async def create_pypi_record(link, name):

        old_instance = await sync_to_async(PyPiFlapyIndexLinks.objects.filter)(url=link)
        old_instance = await sync_to_async(old_instance.exists)()
        if not old_instance:
            await PyPiFlapyIndexLinks.objects.acreate(
                url=link,
                name=name,
            )
            return {'message': f"Url registered successfullyo {link}", 'level': 'success'}
        else:
            return {'message': f"Url already registered {link}", 'level': 'warning'}

    @staticmethod
    async def start_processing(queue):
        ALProcessorHandler.index_processor_websocket_queue = queue
        if not ALProcessorHandler.processing:
            pipy_urls_file = os.path.join(settings.BASE_DIR, "extractor/extracted_files/flapy_projects.csv")

            with open(pipy_urls_file, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                link_count = 0
                for row in csv_reader:
                    name, link, _ = row
                    if link.startswith('http'):
                        message_data = await ALProcessorHandler.create_pypi_record(link, name)
                    else:
                        message_data = {'message': f"invalid url {link}", 'level': 'error'}
                    link_count += 1
                    await queue.put(message_data)

                    if ALProcessorHandler.stop_processing:
                        break

            await queue.put({'message': f"Links registered successfully {link_count}", 'level': 'error'})
            return


class ALUrlExtractorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.queue = Queue()
        self.stop_processing = False

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'feedback_message_value',
            'message': "started_socket_sucessefuly"
        }))

    async def process_messages(self):
        asyncio.create_task(ALProcessorHandler.start_processing(self.queue))
        while True:
            message = await self.queue.get()
            await self.send_feedback_message_level(message)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == "start_processing_al":
            asyncio.create_task(self.process_messages())
        elif message == "stop_processing_al":
            ALProcessorHandler.stop_processing = True

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

