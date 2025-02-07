import pyautogui as pg
from time import sleep
from tkinter import messagebox
import pygetwindow
import pyperclip
import openpyxl


def automatizar_anki(arquivo):
    def write_message(msg):
        pyperclip.copy(msg)
        sleep(0.7)
        pg.hotkey('ctrl', 'v')

    workbook = openpyxl.load_workbook(arquivo)
    # talvez possa usar workbook.active aqui
    sheet = workbook['Sheet']

    # pg.alert(text='Por favor, lembre-se de habilitar o editor HTML por padrão na parte da frente. Feche esta mensagem e clique na janela do Anki para mantê-la selecionada.', title='Aviso', button='Ok')

    titulos = pygetwindow.getAllTitles()
    titulo_anki = ''
    for titulo in titulos:
        if 'Anki' in titulo:
            titulo_anki = titulo

    janela_anki = pygetwindow.getWindowsWithTitle(titulo_anki)[0]

    if janela_anki.isMaximized:
        janela_anki.activate()
    elif janela_anki.isMinimized:
        janela_anki.restore()
    else:
        messagebox.showinfo(
            title='Atenção!',
            message='Verifique se o Anki está em execução e com a janela SELECIONADA antes de prosseguir')

    sleep(3)
    pg.press('a')

    qtd_frases = 0
    for linha in sheet.iter_rows(min_row=2, min_col=1):
        frase = linha[0].value.lower()
        palavra = linha[1].value
        traducao = linha[2].value
        traducao_palavra = f'{palavra} = {traducao}'

        frase = frase.split(palavra.lower())
        if frase[0] == '':
            frase_formatada = f'<b>{palavra.capitalize()}</b>' + frase[1]
        else:
            frase_formatada = frase[0].capitalize() + f'<b>{palavra}</b>' + frase[1]

        sleep(0.3)
        write_message(frase_formatada)
        sleep(0.6)
        # selecionar frase
        pg.hotkey('ctrl', 'a')
        sleep(0.6)
        # abrir extensão do áudio
        pg.hotkey('ctrl', 't')
        sleep(1.2)
        # Colocar áudio
        pg.hotkey('ctrl', 'enter')
        sleep(1.2)
        # Pular para a linha de baixo
        pg.press('tab')
        sleep(1.2)
        write_message(traducao_palavra)
        sleep(0.6)
        pg.hotkey('ctrl', 'enter')
        qtd_frases += 1
    messagebox.showinfo(title='Finalizado!', message=f'A sua automação terminou. Foram adicionadas {qtd_frases} frases!')



