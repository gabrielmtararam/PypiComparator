from bs4 import BeautifulSoup
import requests
count = 0
links_list = []
def percorrer_links(elemento,arquivo_saida):
    links = elemento.find_all("a", href=True)
    global count, links_list
    for link in links:
        url = link["href"]

        if not url.startswith("#") and (not url in links_list) and url.startswith("https://github.com/"):
            print(f"Link: {link}")
            arquivo_saida.write(f"{url}\n")
            count += 1
            links_list.append(url)
            percorrer_links(link, arquivo_saida)


caminho_arquivo = "/home/gabrieltararam/PycharmProjects/awsomeHtmlProcess/awesome_readme_html_clean.html"

with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
    conteudo_html = arquivo.read()

soup = BeautifulSoup(conteudo_html, "html.parser")

div_readme = soup.find("div", {"id": "readme"})
listas =  div_readme.find_all("ul")
if div_readme:
    # conteudo_div = div_readme.get_text()
    # print(conteudo_div)
    with open("lista_links.txt", "w", encoding="utf-8") as arquivo_saida:
        for lista in listas:
            percorrer_links(lista, arquivo_saida)
    print("total ",count)
else:
    print("não encontrad")

#
# def obter_lista_pacotes():
#     url = 'https://pypi.org/pypi/pypi/last/json'
#     resposta = requests.get(url)
#
#     if resposta.status_code == 200:
#         dados = resposta.json()
#         pacotes = list(dados['releases'].keys())
#         return pacotes
#     else:
#         print(f'Falha ao obter a lista de pacotes. Código de status: {resposta.status_code}')
#         return None
#
#
# def salvar_lista_em_arquivo(lista, nome_arquivo='lista_pacotes.txt'):
#     with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
#         for pacote in lista:
#             arquivo.write(f'{pacote}\n')
#
#
# def get_pypi_data():
#     lista_pacotes = obter_lista_pacotes()
#
#     # Salva a lista de pacotes em um arquivo de texto
#     if lista_pacotes:
#         salvar_lista_em_arquivo(lista_pacotes)
#         print("Lista de pacotes salva no arquivo lista_pacotes.txt.")
#     else:
#         print("Não foi possível obter a lista de pacotes.")
#
# get_pypi_data()