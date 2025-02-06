from tkinter import filedialog
import pandas as pd
import requests
import re
import openpyxl
import os
from openpyxl.worksheet.worksheet import Worksheet

def buscador_de_frases(palavra):
    try:
        # Carregar apenas a terceira coluna
        df = pd.read_csv('C:\\Users\\Daniel\\Documents\\Projetos Python\\projeto_inglês\\buscadores\\eng_sentences.tsv', sep="\t", names=['frase'], usecols=[2], dtype=str)
    except FileNotFoundError:
        return None
    try:
        # Filtrar frases que contêm a palavra desejada (ignorando maiúsculas/minúsculas)
        resultado = df[df['frase'].str.contains(f' {palavra} ', case=False, na=False)]

        lista_frases = resultado.sample(10)['frase'].tolist()

        # Exibir algumas frases encontradas
        print(lista_frases)

        return lista_frases
    except Exception as e:
        return None


def tradutor_de_palavras(palavra_a_traduzir):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    url = f'https://context.reverso.net/traducao/ingles-portugues/{palavra_a_traduzir}'
    resposta = requests.get(url, headers=headers).text
    # Expressão regular para capturar o conteúdo dentro do <span class="display-term">
    padrao_palavras = r'<span class="display-term">(.*?)</span>'
    palavras = re.findall(padrao_palavras, resposta)[:4]

    return palavras


class GerenciadorPlanilha:
    def __init__(self):
        self.planilha = openpyxl.Workbook()
        self.sheet: Worksheet = self.planilha['Sheet']
        self.sheet.append(['Frase', 'Palavra', 'Tradução'])

    def adicionar_dados(self, frase, palavra, significados):
        self.sheet.append([frase, palavra, significados])

    def salvar_planilha(self):
        caminho = filedialog.asksaveasfilename(
            title='Escolha o local para salvar',
            filetypes=[('Arquivo de planilha', '*.xlsx')],
            defaultextension='.xlsx',
            confirmoverwrite=True
        )
        self.planilha.save(caminho)

        if caminho:
            try:
                self.planilha.save(caminho)
                print(f"Planilha salva com sucesso em: {caminho}")
            except Exception as e:
                print(f"Erro ao salvar a planilha: {e}")
        else:
            print("Salvamento cancelado pelo usuário.")


if __name__ == '__main__':
    palavras = ['weather', 'pineapple', 'keyboard', 'clip']

    for palavra in palavras:
        print(tradutor_de_palavras(palavra))
