from threading import Thread
from customtkinter import *
from arquivos_extras.funcionalidades_extras import buscador_de_frases, tradutor_de_palavras, GerenciadorPlanilha
from arquivos_extras.anki_automation import automatizar_anki


class JanelaIngles(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        set_appearance_mode('dark')

        self.geometry('650x450')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(padx=20, pady=20)
        self.title('Escolher funcionalidade')

        self.frame_inicial = FrameEscolhaInicial(master=self, janela_principal=self, fg_color='transparent')
        self.frame_inicial.grid(row=0, column=0, sticky='nsew')

        self.frame_traducao = FrameTraducao(master=self, janela_principal=self)
        self.frame_traducao.grid(row=0, column=0, sticky='nsew')

        self.frame_anki = FrameAnki(master=self, janela_principal=self)
        self.frame_anki.grid(row=0, column=0, sticky='nsew')
        self.frame_inicial.tkraise()

    def exibir_frame_traducao(self):
        self.frame_traducao.tkraise()

    def exibir_frame_anki(self):
        self.frame_anki.tkraise()

    def exibir_frame_inicial(self):
        self.frame_inicial.tkraise()


class FrameEscolhaInicial(CTkFrame):
    def __init__(self, master, janela_principal, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.janela_principal = janela_principal
        self.grid_anchor('center')

        self.btn_iniciar_janela_buscas = CTkButton(self, text='Iniciar janela de buscas', width=200,
                                                   command=janela_principal.exibir_frame_traducao)
        self.btn_iniciar_janela_buscas.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.btn_iniciar_automacao = CTkButton(self, text='Iniciar automação Anki', width=200,
                                               command=janela_principal.exibir_frame_anki)
        self.btn_iniciar_automacao.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')


class FrameAnki(CTkFrame):
    def __init__(self, janela_principal, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.janela_principal = janela_principal
        self.grid_anchor('center')

        self.fonte_titulo = CTkFont(weight='bold', size=18)
        self.fonte_padrao = CTkFont(size=15)
        texto_titulo = 'Para iniciar a automação do Anki sem erros, é importante seguir esses passos:'
        texto = '''
1º - Escolha o arquivo arquivo que contêm as frases, palavras e traduções, no formato correto.
2º - Abra o Anki e deixe selecionado o baralho (deck) que deseja inserir as frases e traduções.
3º - Clique em iniciar e clique na janela do Anki para mantê-la selecionada'''
        CTkLabel(self, text=texto_titulo, font=self.fonte_titulo, justify='left', wraplength=600).grid(
            row=0, column=0, padx=10, columnspan=2)
        CTkLabel(self, text=texto, justify='left', wraplength=550).grid(
            row=1, column=0, padx=10, pady=(0, 20), columnspan=2)
        self.campo_arquivo = CTkEntry(self, placeholder_text='Caminho do arquivo', width=330)
        self.campo_arquivo.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.botao_selecionar = CTkButton(self, text='Selecionar arquivo', command=self.selecionar_arquivo)
        self.botao_selecionar.grid(row=2, column=1, padx=10, pady=10)
        self.botao_iniciar = CTkButton(self, text='Iniciar', command=self.iniciar_thread_anki)
        self.botao_iniciar.grid(row=3, column=0, padx=10, pady=20, sticky='ew')
        self.botao_voltar = CTkButton(self, text='< Voltar', command=self.janela_principal.exibir_frame_inicial)
        self.botao_voltar.grid(row=3, column=1, padx=10, pady=20)

    def selecionar_arquivo(self):
        self.caminho_arquivo = filedialog.askopenfilename(
            title='Selecionar arquivo',
            filetypes=[('Arquivo de planilha', '*.xlsx')]
        )
        if self.caminho_arquivo:
            self.campo_arquivo.insert(0, self.caminho_arquivo)

    def iniciar_thread_anki(self):
        def iniciar_automacao_anki():
            self.botao_iniciar.configure(state='disabled')
            automatizar_anki(self.caminho_arquivo)
            self.botao_iniciar.configure(state='normal')

        thread_anki = Thread(target=iniciar_automacao_anki, daemon=True)
        thread_anki.start()


class FrameTraducao(CTkFrame):
    def __init__(self, janela_principal, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.janela_principal = janela_principal
        self.fonte_titulo = CTkFont(weight='bold', size=18)
        self.fonte_padrao = CTkFont(size=15)
        self.palavras_formatadas = None
        self.grid_anchor('center')

        self.texto_palavras = CTkLabel(self, text='Digite palavras em inglês, separadas por vírgula.', font=self.fonte_titulo)
        self.texto_palavras.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w', columnspan=2)
        self.texto_exemplo = CTkLabel(self, text='Ex: window, table, wall', font=self.fonte_padrao)
        self.texto_exemplo.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='w', columnspan=2)

        self.campo_palavras = CTkEntry(self, placeholder_text='Digite...', height=34, font=self.fonte_padrao)
        self.campo_palavras.grid(row=2, column=0, padx=10, pady=10, sticky='ew', columnspan=2)

        self.texto_informativo = CTkLabel(self, text='')
        self.texto_informativo.grid(row=3, column=0, padx=10, columnspan=2)

        self.botao_avancar = CTkButton(self, text='Avançar', command=self.iniciar_thread_avancar)
        self.botao_avancar.grid(row=4, column=0, padx=10, pady=10, sticky='ew')
        self.botao_voltar = CTkButton(self, text='< Voltar', command=self.janela_principal.exibir_frame_inicial)
        self.botao_voltar.grid(row=4, column=1, padx=10, pady=10)

    def avancar_etapa(self):
        self.botao_avancar.configure(state='disabled')
        self.texto_informativo.configure(text='')

        # Manipulação de strings
        palavras_digitadas = self.campo_palavras.get().replace(' ', '').split(',')
        # List comprehension - Nesse caso, serve para adicionar cada palavra que não
        # for um espaço vazio dentro da lista self.palavras_formatadas.
        self.palavras_formatadas = []
        for palavra in palavras_digitadas:
            # Essa verificação é feita para garantir que a palavra tenha um valor e que seja
            # alfa (apenas letras) ou que tenha hífen.
            # Uma opção mais segura seria usar regex, mas acredito que não tenha problema.
            if palavra != '' and (palavra.isalpha() or "-" in palavra or "'" in palavra):
                self.palavras_formatadas.append(palavra)
        print(f'Palavras formatadas após o loop = {self.palavras_formatadas}')
        if not self.palavras_formatadas:
            self.texto_informativo.configure(text='Corrija as palavras digitadas.', text_color='yellow')
        else:
            try:
                JanelaExibicaoFrases(self.palavras_formatadas)
            except:
                self.texto_informativo.configure(
                    text=f'Ocorreu algum erro durante a busca. Tente novamente!',
                    wraplength=300)

        self.botao_avancar.configure(state='normal')

    def iniciar_thread_avancar(self):
        if self.campo_palavras.get() != '':
            thread = Thread(target=self.avancar_etapa, daemon=True)
            thread.start()
        else:
            self.texto_informativo.configure(text='Insira ao menos uma palavra', text_color='yellow')


class JanelaExibicaoFrases(CTkToplevel):
    def __init__(self, palavras, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tentativa de usar um Popup personalizado, mas as tentativas de centralizar não funcionaram muito bem.
        # janela_carregamento = PopupCarregamento(self)

        self.palavras_formatadas = palavras
        print(f'Palavras formatadas dentro da classe: {palavras}')

        self.geometry('600x800')
        self.state('zoomed')
        self.title('Frases')
        self.configure(padx=20, pady=20)
        self.grid_anchor('center')
        self.grab_set()
        self.focus_force()

        self.contador = 0

        self.texto_frases = CTkLabel(self, text='Exemplos de frases')
        self.texto_frases.grid(row=0, column=0, padx=10, pady=10)
        self.gerenciador_abas = CTkTabview(self)
        self.gerenciador_abas.grid(row=1, column=0, padx=10, pady=10)

        self.gerenciador_abas.configure(width=200)

        self.botao_salvar = CTkButton(self, text='Salvar dados', state='disabled', command=self.salvar_dados)
        self.botao_salvar.grid(row=2, column=0, padx=10, pady=20)

        # Cria uma variável StringVar para armazenar a frase selecionada pelo usuário.
        # Essa variável será compartilhada entre todos os radiobuttons da aba atual.
        self.var_frases = {}

        # Chamando a função que cria as abas e radiobuttons
        self.criar_abas_e_radiobuttons(palavras)

    def formatar_frases_para_exibicao(self, frases):
        # Nesse trecho de código, estou formatando as frases apenas para EXIBIÇÃO.
        # Ou seja, para que elas não sejam exibidas de modo muito GRANDE.
        # Essa exibição faz quebras de linhas
        frases_formatadas = []
        for frase in frases:
            if frase.count(' ') >= 15:
                frase = frase.split(' ')
                frase_copia = ''

                for indice, trecho_da_frase in enumerate(frase, start=0):
                    if indice % 15 == 0 and indice != 0:
                        frase_copia += os.linesep
                    frase_copia += trecho_da_frase + ' '
                frases_formatadas.append(frase_copia.strip())
            else:
                frases_formatadas.append(frase)
        return frases_formatadas

    def criar_abas_e_radiobuttons(self, palavras):
        for i, palavra in enumerate(palavras, start=3):
            frases_a_exibir = buscador_de_frases(palavra, self.contador)
            if not frases_a_exibir:
                CTkLabel(self, text=f'Palavra "{palavra}" não encontrada. Verifique a grafia.',
                         text_color='yellow').grid(row=i, column=0, padx=5, pady=5)
                continue

            self.aba_palavra = self.gerenciador_abas.add(palavra)
            self.aba_palavra.grid_columnconfigure(0, weight=1)

            # Mapeia a palavra à sua StringVar, ou seja, associa cada palavra à sua StringVar
            # para armazenar a frase selecionada pelo usuário.
            self.var_frases[palavra] = StringVar()

            # Dentro da aba específica da palavra atual do loop, adiciona um radiobutton para cada frase encontrada.
            for indice, frase in enumerate(frases_a_exibir, start=2):
                # Apenas exibe a frase formatada, mas não será o valor associado a ela, e sim a frase sem formatação (sem quebra de linha).
                frase_formatada = self.formatar_frases_para_exibicao([frase])[0]
                CTkRadioButton(self.aba_palavra, text=frase_formatada, variable=self.var_frases[palavra], value=frase,
                               command=self.verificar_selecao).grid(
                    row=indice, column=0, padx=10, pady=10, sticky='w')
            botao_gerar = CTkButton(self.aba_palavra, text='Gerar mais', command=self.gerar_frases)
            botao_gerar.grid(row=12, column=0, padx=10, pady=10)

    def gerar_frases(self):
        palavra = self.gerenciador_abas.get()
        aba_atual = self.gerenciador_abas.tab(palavra)
        self.contador += 10

        novas_frases = buscador_de_frases(palavra, self.contador)

        if not novas_frases:
            return

        # Remove os radiobuttons existentes
        for widget in aba_atual.winfo_children():
            if isinstance(widget, CTkRadioButton):
                widget.destroy()

        # Recria os radiobuttons com as novas frases
        for indice, frase in enumerate(novas_frases, start=2):
            # Apenas exibe a frase formatada, mas não será o valor associado a ela, e sim a frase sem formatação (sem quebra de linha).
            frase_formatada = self.formatar_frases_para_exibicao([frase])[0]
            CTkRadioButton(aba_atual, text=frase_formatada, variable=self.var_frases[palavra],
                           value=frase, command=self.verificar_selecao).grid(
                row=indice, column=0, padx=10, pady=10, sticky='w')

    def verificar_selecao(self):
        valores_selecionados = []
        for valor in self.var_frases.values():
            valores_selecionados.append(valor.get())
        if all(valores_selecionados):
            self.botao_salvar.configure(state='normal')

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
