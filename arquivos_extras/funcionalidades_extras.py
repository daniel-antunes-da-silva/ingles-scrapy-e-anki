import pandas as pd
import requests
import re
import openpyxl
import os
import sqlite3
from tkinter import filedialog
from openpyxl.worksheet.worksheet import Worksheet


def buscador_de_frases(palavra, contador_offset):
    try:
        with sqlite3.connect(r'C:\Users\Daniel\Documents\Projetos Python\projeto_inglês\arquivos_extras\frases.db') as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
            SELECT texto
            FROM frases_fts
            WHERE texto MATCH ?
            LIMIT 10
            OFFSET ?
            ''', (palavra, contador_offset))
            resultado_frases = cursor.fetchmany(10)

            frases_encontradas = []
            for frase in resultado_frases:
                frases_encontradas.append(frase[0])
            print(frases_encontradas)
            return frases_encontradas
    except sqlite3.Error as e:
        print(e)
    except Exception as error:
        print(error)


def tradutor_de_palavras(palavras_a_traduzir: list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    palavras_traduzidas = {}
    for palavra in palavras_a_traduzir:
        url = f'https://context.reverso.net/traducao/ingles-portugues/{palavra}'
        resposta = requests.get(url, headers=headers).text
        # Expressão regular para capturar o conteúdo dentro do <span class="display-term">
        padrao_palavras = r'<span class="display-term">(.*?)</span>'
        palavras = re.findall(padrao_palavras, resposta)[:4]
        palavras_traduzidas[palavra] = palavras
    print(palavras_traduzidas)
    return palavras_traduzidas


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
    tradutor_de_palavras(['weather', 'join'])
