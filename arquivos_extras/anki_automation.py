import pyautogui as pg
import pygetwindow
import pyperclip
import openpyxl
from time import sleep
from tkinter import messagebox
from arquivos_extras.funcionalidades_extras import adicionar_cartao


def automatizar_anki(arquivo, baralho):
    workbook = openpyxl.load_workbook(arquivo)
    # talvez possa usar workbook.active aqui
    sheet = workbook['Sheet']

    messagebox.showinfo(
        title='Atenção!',
        message='Verifique se o Anki está em execução antes de prosseguir')

    qtd_frases = 0
    for linha in sheet.iter_rows(min_row=2, min_col=1):
        frase = linha[0].value
        palavra = linha[1].value
        traducao = linha[2].value
        traducao_palavra = f'{palavra} = {traducao}'

        adicionar_cartao(baralho=baralho, frase=frase, significado_palavra=traducao_palavra, palavra=palavra)

        qtd_frases += 1
    messagebox.showinfo(title='Finalizado!', message=f'A sua automação terminou. Foram adicionadas {qtd_frases} frases!')



