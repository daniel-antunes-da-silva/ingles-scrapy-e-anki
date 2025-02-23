from threading import Thread
from customtkinter import *
from arquivos_extras.funcionalidades_extras import buscador_de_frases, tradutor_de_palavras, GerenciadorPlanilha, pegar_baralhos
from arquivos_extras.funcionalidades_extras import automatizar_anki
from tkinter import messagebox
from PIL import Image


class JanelaIngles(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        set_appearance_mode('dark')
        set_default_color_theme(r'arquivos_extras\tema.json')

        self.geometry('600x400')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(padx=30, pady=30)
        self.iconbitmap(r'imagens\icone_programa.ico')

        self.title('Escolher funcionalidade')

        self.frame_inicial = FrameEscolhaInicial(master=self, janela_principal=self)
        self.frame_inicial.grid(row=0, column=0, sticky='nsew')

        self.frame_traducao = FrameTraducao(master=self, janela_principal=self)
        self.frame_traducao.grid(row=0, column=0, sticky='nsew')

        self.frame_anki = FrameAnki(master=self, janela_principal=self)
        self.frame_anki.grid(row=0, column=0, sticky='nsew')
        self.frame_inicial.tkraise()

    def exibir_frame_traducao(self):
        self.frame_traducao.tkraise()
        self.geometry('600x330')
        self.title('Pesquisar palavras')

    def exibir_frame_anki(self):
        self.frame_anki.tkraise()
        self.geometry('650x600')
        self.title('Automação Anki')

    def exibir_frame_inicial(self):
        self.frame_inicial.tkraise()
        self.geometry('600x400')
        self.title('Escolher funcionalidade')


class FrameEscolhaInicial(CTkFrame):
    def __init__(self, master, janela_principal, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.janela_principal = janela_principal
        self.grid_anchor('center')

        imagem_busca = CTkImage(dark_image=Image.open(r'imagens/imagem_busca.png'), size=(200, 200))
        imagem_automacao_anki = CTkImage(dark_image=Image.open(r'imagens/imagem_automacao_anki.png'),
                                         size=(200, 200))

        self.btn_iniciar_janela_buscas = CTkButton(self, text='', image=imagem_busca, fg_color='transparent',
                                                   command=janela_principal.exibir_frame_traducao)
        self.btn_iniciar_janela_buscas.grid(row=1, column=0, padx=40, pady=10, sticky='nsew')
        self.btn_iniciar_automacao = CTkButton(self, text='', image=imagem_automacao_anki, fg_color='transparent',
                                               command=janela_principal.exibir_frame_anki)
        self.btn_iniciar_automacao.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')


class FrameAnki(CTkFrame):
    def __init__(self, janela_principal, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.fonte_titulo = CTkFont(weight='bold', size=20)
        self.configuracoes_titulo = {
            'font': self.fonte_titulo,
            'text_color': '#51EDFF',
            'height': 60
        }

        self.janela_principal = janela_principal
        self.grid_anchor('center')

        texto_titulo = 'Instruções para utilizar a automação do Anki'
        texto = ('1º - Abra o Anki (caso contrário, não irá funcionar).\n'
                 '2º - Escolha o arquivo arquivo (.xlsx) que contêm as frases, palavras e traduções.\n'
                 '3º - Clique em iniciar e aguarde a finalização.')
        CTkLabel(self, text=texto_titulo, justify='left', wraplength=600, **self.configuracoes_titulo).grid(
            row=0, column=0, padx=10, columnspan=2, sticky='w')
        CTkLabel(self, text=texto, justify='left', wraplength=550).grid(
            row=1, column=0, padx=10, pady=(0, 20), columnspan=2)
        self.campo_arquivo = CTkEntry(self, placeholder_text='Caminho do arquivo', width=330, height=38)
        self.campo_arquivo.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.botao_selecionar = CTkButton(self, text='Selecionar arquivo', command=self.selecionar_arquivo, height=34)
        self.botao_selecionar.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        self.botao_iniciar = CTkButton(self, text='Iniciar', command=self.abrir_janela_deck, height=34,
                                       width=200, font=CTkFont(weight='bold'))
        self.botao_iniciar.grid(row=3, column=0, padx=10, pady=20, sticky='ew')
        self.botao_voltar = CTkButton(self, text='< Voltar', command=self.janela_principal.exibir_frame_inicial, height=34)
        self.botao_voltar.grid(row=3, column=1, padx=10, pady=20, sticky='ew')
        CTkLabel(self, text='Log da automação', font=('Roboto', 16, 'bold'),
                 corner_radius=10).grid(row=4, column=0, pady=(5, 0), columnspan=2, sticky='w')
        self.campo_log = CTkTextbox(self, height=200, state='disabled')
        self.campo_log.grid(row=5, column=0, padx=10, pady=(0, 5), columnspan=2, sticky='nsew')
        self.campo_log.configure()

    def abrir_janela_deck(self):
        if not self.campo_arquivo.get():
            messagebox.showwarning(title='Atenção!',
                                   message='Nenhum arquivo foi inserido.')
            return
        JanelaEscolhaBaralho(self)

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(
            title='Selecionar arquivo',
            filetypes=[('Arquivo de planilha', '*.xlsx')],
            initialfile='Planilha Anki',
            defaultextension='.xlsx'
        )
        if caminho_arquivo:
            self.campo_arquivo.delete(0, 'end')
            self.campo_arquivo.insert(0, caminho_arquivo)

    def iniciar_thread_anki(self, baralho):
        def iniciar_automacao_anki():
            self.botao_iniciar.configure(state='disabled')
            arquivo = self.campo_arquivo.get()
            automatizar_anki(arquivo=arquivo, baralho=baralho, campo_log=self.campo_log)
            self.botao_iniciar.configure(state='normal')

        thread_anki = Thread(target=iniciar_automacao_anki, daemon=True)
        thread_anki.start()


class FrameTraducao(CTkFrame):
    def __init__(self, janela_principal, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.janela_principal = janela_principal
        self.fonte_titulo = CTkFont(weight='bold', size=20)
        self.configuracoes_titulo = {
            'font': self.fonte_titulo,
            'text_color': '#51EDFF'
        }

        self.palavras_formatadas = None
        self.grid_anchor('center')

        self.texto_palavras = CTkLabel(self, text='Digite palavras em inglês, separadas por vírgula.', **self.configuracoes_titulo)
        self.texto_palavras.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w', columnspan=2)
        self.texto_exemplo = CTkLabel(self, text='Ex: window, table, wall')
        self.texto_exemplo.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='w', columnspan=2)

        self.campo_palavras = CTkEntry(self, placeholder_text='Digite...', height=38)
        self.campo_palavras.grid(row=2, column=0, padx=10, pady=10, sticky='ew', columnspan=2)

        self.texto_informativo = CTkLabel(self, text='')
        self.texto_informativo.grid(row=3, column=0, padx=10, columnspan=2)

        self.botao_avancar = CTkButton(self, text='Avançar', height=34, command=self.iniciar_thread_avancar)
        self.botao_avancar.grid(row=4, column=0, padx=10, pady=10, sticky='ew')
        self.botao_voltar = CTkButton(self, text='< Voltar', height=34, command=self.janela_principal.exibir_frame_inicial)
        self.botao_voltar.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

    def avancar_etapa(self):
        self.botao_avancar.configure(state='disabled')
        self.texto_informativo.configure(text='')

        # Manipulação de strings
        palavras_digitadas = self.campo_palavras.get().split(',')
        # List comprehension - Nesse caso, serve para adicionar cada palavra que não
        # for um espaço vazio dentro da lista self.palavras_formatadas.
        self.palavras_formatadas = []
        for palavra in palavras_digitadas:
            palavra = palavra.strip()
            # Essa verificação é feita para garantir que a palavra tenha um valor e que seja
            # alfa (apenas letras) ou que tenha hífen.
            # Uma opção mais segura seria usar regex, mas acredito que não tenha problema.
            if palavra != '' and (palavra.isalpha() or "-" in palavra or "'" in palavra or ' ' in palavra):
                self.palavras_formatadas.append(palavra)
        print(f'Palavras formatadas após o loop = {self.palavras_formatadas}')
        if not self.palavras_formatadas:
            self.texto_informativo.configure(text='Corrija as palavras digitadas.', text_color='yellow')
        else:
            JanelaExibicaoFrases(self.palavras_formatadas)

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

        self.fonte_titulo = CTkFont(weight='bold', size=20)
        self.configuracoes_titulo = {
            'font': self.fonte_titulo,
            'text_color': '#51EDFF'
        }

        self.palavras_formatadas = palavras
        print(f'Palavras formatadas dentro da classe: {palavras}')

        self.geometry('600x800')
        self.state('zoomed')
        self.title('Frases')
        self.configure(padx=20, pady=20)
        self.grid_anchor('center')
        self.grab_set()
        self.focus_force()

        self.texto_frases = CTkLabel(self, text='Exemplos de frases', **self.configuracoes_titulo)
        self.texto_frases.grid(row=0, column=0, padx=10, pady=10)
        self.gerenciador_abas = CTkTabview(self, fg_color='gray13')
        self.gerenciador_abas.grid(row=1, column=0, padx=10, pady=10)
        self.gerenciador_abas._segmented_button.configure(font=("Arial", 18, "bold"))

        self.botao_salvar = CTkButton(self, text='Salvar dados', state='disabled', command=self.salvar_dados)
        self.botao_salvar.grid(row=2, column=0, padx=10, pady=20)

        # Cria uma variável StringVar para armazenar a frase selecionada pelo usuário.
        # Essa variável será compartilhada entre todos os radiobuttons da aba atual.
        self.var_frases = {}

        self.contador = {}

        # Iniciando Thread que traduz as palavras digitadas
        thread_traducao = Thread(target=self.traduzir_palavras, daemon=True)
        thread_traducao.start()

        # Chamando a função que cria as abas e radiobuttons
        self.criar_abas_e_radiobuttons(palavras)

    def formatar_frases_para_exibicao(self, frases):
        # Nesse trecho de código, estou formatando as frases apenas para EXIBIÇÃO.
        # Ou seja, para que elas não sejam exibidas de modo muito GRANDE.
        # Essa exibição faz quebras de linhas
        frases_formatadas = []
        for frase in frases:
            if frase.count(' ') >= 25:
                frase = frase.split(' ')
                frase_copia = ''

                for indice, trecho_da_frase in enumerate(frase, start=0):
                    if indice % 25 == 0 and indice != 0:
                        frase_copia += os.linesep
                    frase_copia += trecho_da_frase + ' '
                frases_formatadas.append(frase_copia.strip())
            else:
                frases_formatadas.append(frase)
        return frases_formatadas

    def criar_abas_e_radiobuttons(self, palavras):
        for i, palavra in enumerate(palavras, start=3):
            self.contador[palavra] = 0
            print(f'Contador de {palavra} criar as abas e radiobuttons: {self.contador[palavra]}')
            frases_a_exibir = buscador_de_frases(palavra, self.contador[palavra])
            if not frases_a_exibir:
                CTkLabel(self, text=f'Palavra "{palavra}" não encontrada. Verifique a grafia.',
                         text_color='yellow').grid(row=i, column=0, padx=5, pady=10)
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
                    row=indice, column=0, padx=10, pady=15, sticky='w')
            botao_gerar = CTkButton(self.aba_palavra, text='Gerar mais', command=self.gerar_frases)
            botao_gerar.grid(row=12, column=0, padx=10, pady=10)

    def gerar_frases(self):
        palavra = self.gerenciador_abas.get()
        aba_atual = self.gerenciador_abas.tab(palavra)

        if self.contador[palavra] is not None:
            self.contador[palavra] += 10
        else:
            messagebox.showinfo(title='Poxa :(',
                                message=f'Não há mais frases para "{palavra}".')
            return

        print(f'Contador de {palavra} ao gerar mais frases: {self.contador[palavra]}')
        novas_frases = buscador_de_frases(palavra, self.contador[palavra])

        if not novas_frases:
            self.contador[palavra] = None
            messagebox.showinfo(title='Poxa :(',
                                message=f'Não há mais frases para "{palavra}".')
            return

        # Remove os radiobuttons existentes
        for widget in aba_atual.winfo_children():
            if isinstance(widget, CTkRadioButton):
                widget.destroy()

        # Recria os radiobuttons com as novas frases
        for indice, frase in enumerate(novas_frases, start=2):
            # Apenas exibe a frase formatada, mas não será o valor associado a ela,
            # e sim a frase sem formatação (sem quebra de linha).
            frase_formatada = self.formatar_frases_para_exibicao([frase])[0]
            CTkRadioButton(aba_atual, text=frase_formatada, variable=self.var_frases[palavra],
                           value=frase, command=self.verificar_selecao).grid(
                row=indice, column=0, padx=10, pady=15, sticky='w')

    def verificar_selecao(self):
        valores_selecionados = []
        for valor in self.var_frases.values():
            valores_selecionados.append(valor.get())
        if all(valores_selecionados):
            self.botao_salvar.configure(state='normal')

    def traduzir_palavras(self):
        self.significados_palavra = tradutor_de_palavras(self.palavras_formatadas)

    def salvar_dados(self):
        try:
            planilha = GerenciadorPlanilha()
            for palavra, var_frase in self.var_frases.items():
                significados = self.significados_palavra[palavra]
                significados = ', '.join(significados)
                frase_selecionada = var_frase.get()
                planilha.adicionar_dados(frase_selecionada, palavra, significados)
                print(f'Frase selecionada para "{palavra}": {frase_selecionada}')

            planilha.salvar_planilha()
        except AttributeError:
            messagebox.showwarning(title='Aguarde!',
                                   message='A tradução ainda está em andamento. Aguarde a finalização!')


class JanelaEscolhaBaralho(CTkToplevel):
    def __init__(self, frame, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.withdraw()
        self.frame_anki = frame
        self.title('Escolha o Deck')
        self.geometry('350x300')
        self.configure(padx=20, pady=20)
        self.grid_anchor('center')
        self.focus_force()
        self.grab_set()

        self.fonte_titulo = CTkFont(weight='bold', size=20)
        self.configuracoes_titulo = {
            'font': self.fonte_titulo,
            'text_color': '#51EDFF'
        }

        CTkLabel(self, text='Selecione o deck desejado: ',
                 **self.configuracoes_titulo).grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.variavel_deck = StringVar()
        baralhos = pegar_baralhos()
        if baralhos:
            self.deiconify()
            for indice, baralho in enumerate(baralhos, start=1):
                CTkRadioButton(self, text=baralho, command=self.iniciar_automacao_e_fechar_janela,
                               variable=self.variavel_deck, value=baralho).grid(row=indice, column=0, padx=10, pady=5, sticky='w')
        else:
            self.destroy()

    def iniciar_automacao_e_fechar_janela(self):
        self.destroy()
        self.frame_anki.iniciar_thread_anki(self.pegar_baralho_selecionado())

    def pegar_baralho_selecionado(self):
        baralho_selecionado = self.variavel_deck.get()
        return baralho_selecionado


app = JanelaIngles()

app.mainloop()
