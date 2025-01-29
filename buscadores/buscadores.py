import pandas as pd
import requests
import re

def buscador_de_frases(palavra):
    # Carregar apenas a terceira coluna
    df = pd.read_csv('C:\\Users\\Daniel\\Documents\\Projetos Python\\projeto_inglês\\buscadores\\eng_sentences.tsv', sep="\t", names=['frase'], usecols=[2], dtype=str)

    # Filtrar frases que contêm a palavra desejada (ignorando maiúsculas/minúsculas)
    resultado = df[df['frase'].str.contains(f' {palavra} ', case=False, na=False)]

    lista_frases = resultado.sample(10)['frase'].tolist()

    # Exibir algumas frases encontradas
    print(lista_frases)

    return lista_frases


def buscador_de_traducoes():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    url = 'https://context.reverso.net/traducao/ingles-portugues/weather'

    resposta = requests.get(url, headers=headers).text

    # Expressão regular para capturar o conteúdo dentro do <span class="display-term">
    padrao_palavras = r'<span class="display-term">(.*?)</span>'
    palavras = re.findall(padrao_palavras, resposta)

    return palavras


