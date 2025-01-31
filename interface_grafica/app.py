from customtkinter import *
from buscadores.funcionalidades_extras import buscador_de_frases
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
        self.texto_informativo = CTkLabel(self, text='')
        self.texto_informativo.grid(row=2, column=0, padx=10)
        self.botao_traduzir = CTkButton(self, text='Traduzir palavras', command=self.avancar)
        self.botao_traduzir.grid(row=3, column=0, padx=10, pady=10)

    def avancar(self):
        def avancar_etapa():
            self.botao_traduzir.configure(state='disabled')
            self.texto_informativo.configure(text='')

            palavras_digitadas = self.campo_palavras.get().split(',')
            palavras_formatadas = [palavra.strip() for palavra in palavras_digitadas]
            print(palavras_formatadas)
            JanelaExibicaoFrases(palavras=palavras_formatadas)

            self.botao_traduzir.configure(state='normal')

        if self.campo_palavras.get() != '':
            thread = Thread(target=avancar_etapa, daemon=True)
            thread.start()
        else:
            self.texto_informativo.configure(text='Insira ao menos uma palavra', text_color='yellow')


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

        # Busca as frases referentes a cada palavra, e adiciona uma aba para cada palavra
        for palavra in palavras:
            aba_palavra = self.gerenciador_abas.add(palavra)
            frases_a_exibir = buscador_de_frases(palavra)

            # Dentro da aba específica da palavra atual do loop, adiciona um radiobutton para cada frase encontrada.
            for indice, frase in enumerate(frases_a_exibir, start=2):
                CTkRadioButton(aba_palavra, text=frase).grid(row=indice, column=0, padx=10, pady=10, sticky='w')

        self.botao_salvar = CTkButton(self, text='Salvar dados', command=self.salvar_dados)
        self.botao_salvar.grid(row=2, column=0, padx=10, pady=20)

    def salvar_dados(self):
        pass


app = JanelaIngles()

app.mainloop()
