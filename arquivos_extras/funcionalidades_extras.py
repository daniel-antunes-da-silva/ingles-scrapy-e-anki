import os
import requests
import re
import sqlite3
import openpyxl
from tkinter import filedialog
from openpyxl.worksheet.worksheet import Worksheet
from tkinter import messagebox
from openpyxl.utils.exceptions import InvalidFileException


def buscador_de_frases(palavra, contador_offset):
    try:
        with sqlite3.connect(r'..\arquivos_extras\frases.db') as conexao:
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

        try:
            self.planilha.save(caminho)
            print(f"Planilha salva com sucesso em: {caminho}")
        except FileNotFoundError:
            messagebox.showwarning(title='Ops', message='Caminho inválido ou operação cancelada.')
        except Exception as e:
            print(f"Erro ao salvar a planilha: {e}")


def adicionar_cartao(baralho, frase, significado_palavra, palavra):
    palavra_escapada = re.escape(palavra)  # Protege caracteres especiais
    # Regex para permitir espaços, e destacar a expressão ou palavra, preservando a formatação
    frase_formatada = re.sub(rf'(?<!\w)({palavra_escapada})(?!\w)', r'<b>\1</b>', frase, flags=re.IGNORECASE)

    requisicao = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": f"{baralho}",
                "modelName": "Básico",
                "fields": {
                    "Frente": f"{frase_formatada}",
                    "Verso": f"{significado_palavra}"
                },
                "audio": [{
                    "url": f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q={frase.replace(' ', '+')}",
                    "filename": f"{palavra}.mp3",
                    "fields": [
                        "Frente"
                    ]
                }],
                "options": {
                    "allowDuplicate": False
                }
                }
        }
    }
    try:
        resposta = requests.post(url='http://127.0.0.1:8765', json=requisicao)
        print(resposta.json())
    except requests.exceptions.ConnectionError:
        messagebox.showerror(title='Erro de conexão com o Anki',
                             message='Verifique se o Anki está aberto e verifique sua conexão com a internet.')
    else:
        return resposta.json()

def pegar_baralhos():
    requisicao = {
        "action": "deckNames",
        "version": 6
    }
    try:
        resposta = requests.get(url='http://127.0.0.1:8765', json=requisicao)
        print(resposta.json()['result'])
    except InvalidFileException:
        messagebox.showwarning(title='Atenção!',
                               message='Arquivo inválido ou vazio.')
    except requests.exceptions.ConnectionError:
        messagebox.showerror(title='Erro de conexão com o Anki',
                             message='Verifique se o Anki está aberto e verifique sua conexão com a internet.')
    else:
        return resposta.json()['result']


def escrever_log(campo_log, mensagem):
    campo_log.configure(state='normal')
    campo_log.insert('end', mensagem + os.linesep)
    campo_log.configure(state='disabled')


def automatizar_anki(arquivo, baralho, campo_log):
    campo_log = campo_log
    qtd_frases = 0
    try:
        workbook = openpyxl.load_workbook(arquivo)
        # talvez possa usar workbook.active aqui
        sheet = workbook['Sheet']

        for linha in sheet.iter_rows(min_row=2, min_col=1):
            frase = linha[0].value
            palavra = linha[1].value
            traducao = linha[2].value
            traducao_palavra = f'{palavra} = {traducao}'

            resultado_requisicao = adicionar_cartao(baralho=baralho, frase=frase, significado_palavra=traducao_palavra, palavra=palavra)
            if 'duplicate' in resultado_requisicao['error']:
                escrever_log(campo_log=campo_log, mensagem=f'Frase referente a "{palavra}" não inserida por estar duplicada.')
                continue
            elif resultado_requisicao['error'] is not None:
                continue

            qtd_frases += 1
    except Exception as e:
        print(f'Aconteceu algum erro na automação Anki. Erro: {e}')
    finally:
        escrever_log(campo_log=campo_log,
                     mensagem=f'A sua automação terminou. Foram adicionadas {qtd_frases} frases!')



if __name__ == '__main__':
    pegar_baralhos()
