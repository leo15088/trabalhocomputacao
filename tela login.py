import tkinter as tk
from tkinter import messagebox
import pickle
from datetime import datetime
import trabalhoFinal

class TelaLogin:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Controle de Finanças")

        # Rótulo principal
        self.labelControleDeFinancas = tk.Label(janela, text="Controle de Finanças")
        self.labelControleDeFinancas.pack()

        # Carrega os usuários ao iniciar
        self.carregar_usuarios()

        # Frame para o campo Usuário
        frame_usuario = tk.Frame(janela)
        frame_usuario.pack(anchor='center', pady=(0, 0))

        # Rótulo "Usuário" no frame à esquerda
        self.label_usuario = tk.Label(frame_usuario, text="  Usuário:")
        self.label_usuario.grid(row=0, column=0, sticky='e', padx=(0, 0))

        # Campo de preenchimento no frame à direita
        self.campoUsuario = tk.Entry(frame_usuario, width=30)
        self.campoUsuario.grid(row=0, column=1, sticky='w')

        # Frame para o campo Senha
        frame_senha = tk.Frame(janela)
        frame_senha.pack(anchor='center', pady=(0, 0))

        # Rótulo "Senha" no frame à esquerda
        self.label_senha = tk.Label(frame_senha, text="   Senha:")
        self.label_senha.grid(row=0, column=0, sticky='e', padx=(0, 5))

        # Campo de preenchimento no frame à direita
        self.campoSenha = tk.Entry(frame_senha, show="*", width=30)
        self.campoSenha.grid(row=0, column=1, sticky='w')

        # Frame para os botões
        frame_botoes = tk.Frame(janela)
        frame_botoes.pack(pady=(0, 0))

        # Botão para Cadastrar
        self.botao_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=self.abrir_tela_cadastro, width=10)
        self.botao_cadastrar.grid(row=0, column=0, padx=(5, 2), pady=(0, 0))

        # Botão para Entrar
        self.botao_entrar = tk.Button(frame_botoes, text="Entrar", command=self.verificar_login, width=10)
        self.botao_entrar.grid(row=0, column=1, padx=(2, 5), pady=(0, 0))

        # Define o tamanho inicial da janela
        self.janela.geometry("300x90")

    def carregar_usuarios(self):
        try:
            with open("usuarios.pkl", "rb") as file:
                self.usuarios = pickle.load(file)
        except FileNotFoundError:
            self.usuarios = []

    def salvar_usuarios(self):
        with open("usuarios.pkl", "wb") as file:
            pickle.dump(self.usuarios, file)

    def verificar_login(self):
        # Lógica para verificar se o usuário existe
        usuario_existente = False
        for usuario in self.usuarios:
            if usuario.get_nome() == self.campoUsuario.get() and usuario.get_senha() == self.campoSenha.get():
                usuario_existente = True
                break

        if usuario_existente:
            self.abrir_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário não encontrado")

    def abrir_tela_cadastro(self):
        self.janela.withdraw()  # Esconde a janela de login
        tela_cadastro = TelaCadastro(self.janela, self.usuarios, self.salvar_usuarios)
        self.janela.deiconify()  # Torna a janela de login visível novamente

    def abrir_tela_principal(self):
        tela_principal = TelaPrincipal(self.janela, self.usuarios[0])  # Assumindo que há apenas um usuário

class TelaCadastro:
    def __init__(self, root, usuarios, salvar_callback):
        self.root = root
        self.usuarios = usuarios
        self.salvar_callback = salvar_callback

        self.root.title("Cadastro")

        # Rótulo "Nome"
        self.label_nome = tk.Label(root, text="Nome:")
        self.label_nome.pack()

        # Campo de preenchimento para o nome
        self.entry_nome = tk.Entry(root, width=15)
        self.entry_nome.pack()

        # Rótulo "Senha"
        self.label_senha = tk.Label(root, text="Senha:")
        self.label_senha.pack()

        # Campo de preenchimento para a senha
        self.entry_senha = tk.Entry(root, show="*", width=15)
        self.entry_senha.pack()

        # Botão para salvar o cadastro
        self.botao_salvar = tk.Button(root, text="Salvar", command=self.salvar_cadastro)
        self.botao_salvar.pack()

        # Define o tamanho inicial da janela de cadastro
        self.root.geometry("300x200")

    def salvar_cadastro(self):
        novo_usuario = Usuario(self.entry_nome.get(), self.entry_senha.get())
        self.usuarios.append(novo_usuario)
        self.salvar_callback()
        self.root.destroy()

class TelaPrincipal:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title(f"Tela Principal - Usuário: {self.usuario.get_nome()}")
        self.itens_comprados = []  

        # Rótulo para o total gasto
        self.label_total_gasto = tk.Label(root, text="Total Gasto: R$ 0.00")
        self.label_total_gasto.pack()

        # Lista de itens comprados
        self.listbox_itens = tk.Listbox(root, selectmode=tk.SINGLE)
        self.listbox_itens.pack(side=tk.LEFT, fill=tk.BOTH)

        # Barra de rolagem para a lista de itens
        self.scrollbar = tk.Scrollbar(root, command=self.listbox_itens.yview)
        self.listbox_itens.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botões
        self.botao_cadastrar_item = tk.Button(root, text="Cadastrar Item", command=self.abrir_tela_cadastro_item)
        self.botao_cadastrar_item.pack()

        self.botao_limpar = tk.Button(root, text="Limpar", command=self.limpar_itens)
        self.botao_limpar.pack()

        self.botao_gerar_relatorio = tk.Button(root, text="Gerar Relatório", command=self.gerar_relatorio)
        self.botao_gerar_relatorio.pack()

    def abrir_tela_cadastro_item(self):
        tela_cadastro_item = TelaCadastroItem(self.root, self.itens_comprados, self.atualizar_total_gasto)

    def limpar_itens(self):
        self.itens_comprados.clear()
        self.atualizar_total_gasto()

    def gerar_relatorio(self):
        try:
            with open(f"relatorio_{self.usuario.get_nome()}.txt", "w") as file:
                total_gasto = 0
                for item in self.itens_comprados:
                    file.write(str(item) + "\n")
                    total_gasto += item.get_preco()
                file.write(f"\nTotal Gasto: R$ {total_gasto:.2f}")

            messagebox.showinfo("Relatório Gerado", "Relatório gerado com sucesso!")
        except IOError:
            messagebox.showerror("Erro", "Erro ao operar com o arquivo")

    def atualizar_total_gasto(self):
        total_gasto = sum(item.get_preco() for item in self.itens_comprados)
        self.label_total_gasto.config(text=f"Total Gasto: R$ {total_gasto:.2f}")

class TelaCadastroItem:
    def __init__(self, root, itens_comprados, callback_atualizar_total):
        self.root = root
        self.itens_comprados = itens_comprados
        self.callback_atualizar_total = callback_atualizar_total

        self.root.title("Cadastro de Item")

        # Rótulo "Nome"
        self.label_nome = tk.Label(root, text="Nome:")
        self.label_nome.pack()

        # Campo de preenchimento para o nome
        self.entry_nome = tk.Entry(root, width=15)
        self.entry_nome.pack()

        # Rótulo "Preço"
        self.label_preco = tk.Label(root, text="Preço:")
        self.label_preco.pack()

        # Campo de preenchimento para o preço
        self.entry_preco = tk.Entry(root, width=15)
        self.entry_preco.pack()

        # Botão para salvar o cadastro do item
        self.botao_salvar = tk.Button(root, text="Salvar", command=self.salvar_cadastro_item)
        self.botao_salvar.pack()

    def salvar_cadastro_item(self):
        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())

        novo_item = ItemDeCompra(nome, preco, datetime.now(), "Local Padrão")
        self.itens_comprados.append(novo_item)
        self.callback_atualizar_total()
        self.root.destroy()

# Exemplo de uso
janelaPrincipal = tk.Tk()
tela_login = TelaLogin(janelaPrincipal)
janelaPrincipal.mainloop()
