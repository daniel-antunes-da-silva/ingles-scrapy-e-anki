from customtkinter import *
from buscadores.buscadores import buscador_de_frases
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
        self.botao_traduzir = CTkButton(self, text='Traduzir palavras', command=self.avancar)
        self.botao_traduzir.grid(row=2, column=0, padx=10, pady=10)

    def avancar(self):
        def avancar_etapa():
            self.botao_traduzir.configure(state='disabled')
            palavras_digitadas = self.campo_palavras.get().split(',')
            palavras_formatadas = [palavra.strip() for palavra in palavras_digitadas]
            print(palavras_formatadas)
            JanelaExibicaoFrases(palavras=palavras_formatadas)
            self.botao_traduzir.configure(state='normal')

        thread = Thread(target=avancar_etapa, daemon=True)
        thread.start()


class JanelaExibicaoFrases(CTkToplevel):
    def __init__(self, palavras, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('600x800')
        self.state('zoomed')
        self.title('Frases')
        self.configure(padx=20, pady=20)
        self.grid_anchor('center')
        self.grab_set()

        self.texto_frases = CTkLabel(self, text='Exemplos de frases')
        self.texto_frases.grid(row=0, column=0, padx=10, pady=10)

        self.gerenciador_abas = CTkTabview(self)
        self.gerenciador_abas.grid(row=1, column=0, padx=10, pady=10)

        for palavra in palavras:
            aba_palavra = self.gerenciador_abas.add(palavra)
            frases = buscador_de_frases(palavra)

            for indice, frase in enumerate(frases, start=2):
                CTkRadioButton(aba_palavra, text=frase).grid(row=indice, column=0, padx=10, pady=10, sticky='w')


app = JanelaIngles()

app.mainloop()
