from customtkinter import *
from buscadores.funcionalidades_extras import buscador_de_frases, tradutor_de_palavras, GerenciadorPlanilha
from threading import Thread


class JanelaIngles(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        set_appearance_mode('dark')

        self.geometry('500x350')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(padx=20, pady=20)
        self.title('Escolher funcionalidade')

        self.frame_traducao = FrameTraducao(master=self)
        self.frame_traducao.grid(row=0, column=0, sticky='nsew')

        self.frame_inicial = FrameEscolhaInicial(master=self, janela_principal=self, fg_color='transparent')
        self.frame_inicial.grid(row=0, column=0, sticky='nsew')

    def exibir_frame_traducao(self):
        self.frame_traducao.tkraise()


class FrameEscolhaInicial(CTkFrame):
    def __init__(self, master, janela_principal, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.janela_principal = janela_principal
        self.grid_anchor('center')

        self.btn_iniciar_janela_buscas = CTkButton(self, text='Iniciar janela de buscas', width=200, command=janela_principal.exibir_frame_traducao)
        self.btn_iniciar_janela_buscas.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.btn_iniciar_automacao = CTkButton(self, text='Iniciar automação Anki', width=200)
        self.btn_iniciar_automacao.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')


class FrameTraducao(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.palavras_formatadas = None
        self.grid_anchor('center')

        set_appearance_mode('dark')

        self.texto_palavras = CTkLabel(self, text='Digite palavras em inglês separadas por vírgula')
        self.texto_palavras.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.campo_palavras = CTkEntry(self, placeholder_text='Digite...', width=300)
        self.campo_palavras.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.texto_informativo = CTkLabel(self, text='')
        self.texto_informativo.grid(row=2, column=0, padx=10)
        self.botao_traduzir = CTkButton(self, text='Avançar', command=self.iniciar_thread_avancar)
        self.botao_traduzir.grid(row=3, column=0, padx=10, pady=10)

    def avancar_etapa(self):
        self.botao_traduzir.configure(state='disabled')
        self.texto_informativo.configure(text='')
        palavras_digitadas = self.campo_palavras.get().split(',')
        self.palavras_formatadas = [palavra.strip() for palavra in palavras_digitadas]

        JanelaExibicaoFrases(self.palavras_formatadas)

        self.botao_traduzir.configure(state='normal')

    def iniciar_thread_avancar(self):
        if self.campo_palavras.get() != '':
            thread = Thread(target=self.avancar_etapa, daemon=True)
            thread.start()
        else:
            self.texto_informativo.configure(text='Insira ao menos uma palavra', text_color='yellow')


class JanelaExibicaoFrases(CTkToplevel):
    def __init__(self, palavras, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.palavras_formatadas = palavras
        print(f'Palavras formatadas: {palavras}')

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

        self.botao_salvar = CTkButton(self, text='Salvar dados', command=self.salvar_dados)
        self.botao_salvar.grid(row=2, column=0, padx=10, pady=20)

        # Cria uma variável StringVar para armazenar a frase selecionada pelo usuário.
        # Essa variável será compartilhada entre todos os radiobuttons da aba atual.
        self.var_frases = {}

        # Chamando a função que cria as abas e radiobuttons
        self.criar_abas_e_radiobuttons(palavras)


    def criar_abas_e_radiobuttons(self, palavras):
        for palavra in palavras:
            aba_palavra = self.gerenciador_abas.add(palavra)
            frases_a_exibir = buscador_de_frases(palavra)

            var_frase = StringVar()
            # Mapeia a palavra à sua StringVar, ou seja, associa cada palavra à sua StringVar
            # para armazenar a frase selecionada pelo usuário.
            self.var_frases[palavra] = var_frase
            # Dentro da aba específica da palavra atual do loop, adiciona um radiobutton para cada frase encontrada.
            for indice, frase in enumerate(frases_a_exibir, start=2):
                CTkRadioButton(aba_palavra, text=frase, variable=var_frase, value=frase).grid(
                    row=indice, column=0, padx=10, pady=10, sticky='w')

    def salvar_dados(self):
        planilha = GerenciadorPlanilha()

        for palavra, var_frase in self.var_frases.items():
            significados_palavra = tradutor_de_palavras(palavra)
            significados_palavra = ', '.join(significados_palavra)
            frase_selecionada = var_frase.get()
            planilha.adicionar_dados(frase_selecionada, palavra, significados_palavra)
            print(f'Frase selecionada para "{palavra}": {frase_selecionada}')

        planilha.salvar_planilha()


app = JanelaIngles()

app.mainloop()
