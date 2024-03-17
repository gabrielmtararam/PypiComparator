import random
from time import sleep

import requests
import os
from bs4 import BeautifulSoup
diretorio_atual = os.path.dirname(__file__)


def download_pypi_simple_index():
    # URL da página que será baixada
    url = 'https://pypi.org/simple/'

    # Obtém o diretório atual do script

    # Pasta onde o arquivo HTML será salvo (dentro do diretório atual)
    pasta_destino = os.path.join(diretorio_atual, 'pypi_files')

    # Verifica se a pasta de destino existe, senão cria
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Nome do arquivo onde a página HTML será salva
    nome_arquivo = os.path.join(pasta_destino, 'pagina.html')

    # Faz o download da página HTML
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Salva o conteúdo da página HTML no arquivo
        with open(nome_arquivo, 'wb') as file:
            file.write(response.content)
        print(f'Página HTML baixada com sucesso em {nome_arquivo}')
    else:
        print(f'Erro ao baixar a página HTML: {response.status_code}')

# download_pypi_simple_index()


def check_pypi_homepage_link(link):
    sleeptime = random.uniform(2, 5)
    sleep(sleeptime)
    url_base = 'https://pypi.org/project/'

    link_completo = url_base + link['href'].replace('/simple/', '')
    # print(f'Analisando link: {link_completo}')

    # Faz a requisição para o link completo
    response_link = requests.get(link_completo)

    if response_link.status_code == 200:
        soup_link = BeautifulSoup(response_link.content, 'html.parser')

        # Verifica se a página contém o ícone 'fas fa-home'
        icone = soup_link.find('i', class_='fas fa-home')
        if icone:
            link_homepage = icone.find_parent('a', href=True)
            print(f"icones {link_homepage['href']}  url original {link['href']}")
    else:
        print(f'Erro ao acessar o link: {link_completo}, Status code: {response_link.status_code}')


def count_pypi_packages_links():
        # Salva o conteúdo da página HTML no arquivo
        pasta_destino = os.path.join(diretorio_atual, 'pypi_files/pagina.html')


        # Abre o arquivo HTML e conta os links
        with open(pasta_destino, 'r') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            links = soup.find_all('a', href=True)

            # Conta os links no formato especificado
            contador_links = 0
            for link in links:
                if link['href'].startswith('/simple/'):
                    contador_links += 1
                    check_pypi_homepage_link(link)
                if contador_links >25:
                    return

            print(f'Total de links no formato especificado: {contador_links}')
count_pypi_packages_links()
