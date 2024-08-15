import pyautogui as pg
from time import sleep
import pyperclip
import openpyxl
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def write_message(msg):
    pyperclip.copy(msg)
    sleep(0.5)
    pg.hotkey('ctrl', 'v')


Tk().withdraw()
arquivo = askopenfilename()
workbook = openpyxl.load_workbook(arquivo)
# talvez possa usar workbook.active aqui
sheet = workbook['Sheet']

pg.alert(text='Por favor, lembre-se de habilitar o editor HTML por padrão na parte da frente. Feche esta mensagem e clique na janela do Anki para mantê-la selecionada.', title='Aviso', button='Ok')

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
    sleep(0.5)
    # selecionar frase
    pg.hotkey('ctrl', 'a')
    sleep(0.5)
    # abrir extensão do áudio
    pg.hotkey('ctrl', 't')
    sleep(1)
    # Colocar áudio
    pg.hotkey('ctrl', 'enter')
    sleep(1)
    # Pular para a linha de baixo
    pg.press('tab')
    sleep(1)
    write_message(traducao_palavra)
    sleep(0.5)
    pg.hotkey('ctrl', 'enter')
    qtd_frases += 1
pg.alert(f'A sua automação terminou. Foram adicionadas {qtd_frases} frases!')
sleep(2)
pg.hotkey('alt', 'f4')
