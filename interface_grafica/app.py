from customtkinter import *
from translator import run_spider, ReversoContextScraperSpider
import json
from tkinter import messagebox
from threading import Thread


class JanelaIngles(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.palavras_formatadas = None
        self.geometry('500x500')
        self.title('Tradutor')
        self.configure(padx=20, pady=20)
        self.grid_anchor('center')

        set_appearance_mode('dark')

        self.texto_palavras = CTkLabel(self, text='Digite palavras em inglês separadas por vírgula')
        self.texto_palavras.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.campo_palavras = CTkEntry(self, placeholder_text='Digite...', width=300)
        self.campo_palavras.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.botao_traduzir = CTkButton(self, text='Traduzir palavras', command=self.traduzir)
        self.botao_traduzir.grid(row=2, column=0, padx=10, pady=10)

    def traduzir(self):
        self.botao_traduzir.configure(state='disabled')
        self.palavras_digitadas = self.campo_palavras.get().split(',')
        self.palavras_formatadas = [palavra.strip() for palavra in self.palavras_digitadas]
        print(self.palavras_formatadas)


app = JanelaIngles()

app.mainloop()
