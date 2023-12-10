import tkinter as tk
from tkinter import messagebox
import pickle
from datetime import datetime

class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha
        self.itens_comprados = []

    def salvar_callback(self):
        with open(f"{self.nome}_itens.pkl", "wb") as file:
            pickle.dump(self.itens_comprados, file)

    def __str__(self):
        return f'Usuário: {self.nome}'

class ItemDeCompra:
    def __init__(self, nome, preco, data_compra, local_compra, compra, renda):
        self.nome = nome
        self.preco = preco
        self.data_compra = data_compra
        self.local_compra = local_compra
        self.compra = compra
        self.renda = renda

    def __str__(self):
        tipo = "Compra" if self.compra else "Renda"
        return f'{self.nome} - R$ {self.preco:.2f} - {self.data_compra.strftime("%Y-%m-%d")} - {self.local_compra} - {tipo}'

class TelaLogin:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Controle de Finanças")

        self.carregar_usuarios()

        frame_usuario = tk.Frame(janela)
        frame_usuario.pack(anchor='center', pady=(0, 0))

        self.label_usuario = tk.Label(frame_usuario, text="  Usuário:")
        self.label_usuario.grid(row=0, column=0, sticky='e', padx=(0, 0))

        self.campoUsuario = tk.Entry(frame_usuario, width=30)
        self.campoUsuario.grid(row=0, column=1, sticky='w')

        frame_senha = tk.Frame(janela)
        frame_senha.pack(anchor='center', pady=(0, 0))

        self.label_senha = tk.Label(frame_senha, text="   Senha:")
        self.label_senha.grid(row=0, column=0, sticky='e', padx=(0, 5))

        self.campoSenha = tk.Entry(frame_senha, show="*", width=30)
        self.campoSenha.grid(row=0, column=1, sticky='w')

        frame_botoes = tk.Frame(janela)
        frame_botoes.pack(pady=(0, 0))

        self.botao_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=self.abrir_tela_cadastro, width=10)
        self.botao_cadastrar.grid(row=0, column=0, padx=(5, 2), pady=(0, 0))

        self.botao_entrar = tk.Button(frame_botoes, text="Entrar", command=self.verificar_login, width=10)
        self.botao_entrar.grid(row=0, column=1, padx=(2, 5), pady=(0, 0))

        self.janela.geometry("300x70")

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
        usuario_existente = False
        for usuario in self.usuarios:
            if usuario.nome == self.campoUsuario.get() and usuario.senha == self.campoSenha.get():
                usuario_existente = True
                break

        if usuario_existente:
            self.abrir_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário não encontrado")

    def abrir_tela_cadastro(self):
        tela_cadastro = TelaCadastro(self.janela, self.usuarios, self.salvar_usuarios)
        self.janela.wait_window(tela_cadastro.root)

    def abrir_tela_principal(self):
        usuario_correspondente = None
        for usuario in self.usuarios:
            if usuario.nome == self.campoUsuario.get() and usuario.senha == self.campoSenha.get():
                usuario_correspondente = usuario
                break

        if usuario_correspondente:
            usuario_correspondente.itens_comprados.clear()  # Limpa a lista ao entrar na tela principal
            self.janela.destroy()
            janela_principal = tk.Tk()
            tela_principal = TelaPrincipal(janela_principal, usuario_correspondente)
            janela_principal.mainloop()



class TelaCadastro:
    def __init__(self, root, usuarios, salvar_callback):
        self.root = tk.Toplevel(root)
        self.usuarios = usuarios
        self.salvar_callback = salvar_callback

        self.root.title("Cadastro de Usuário")

        # Rótulo principal
        self.labelCadastroDeUsuario = tk.Label(self.root, text="Cadastro de Usuário")
        self.labelCadastroDeUsuario.pack()

        # Frame principal
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(anchor='center', pady=0)

        # Frame para o campo Usuário
        frame_usuario = tk.Frame(frame_principal)
        frame_usuario.pack(pady=(0, 0))

        # Rótulo "Usuário" no frame à esquerda
        label_usuario = tk.Label(frame_usuario, text="                 Usuário:")
        label_usuario.grid(row=0, column=0, sticky='e', padx=(0, 5))

        # Campo de preenchimento no frame à direita
        self.entry_usuario = tk.Entry(frame_usuario, width=30)
        self.entry_usuario.grid(row=0, column=1, sticky='w')

        # Frame para o campo Senha
        frame_senha = tk.Frame(frame_principal)
        frame_senha.pack(pady=(0, 0))

        # Rótulo "Senha" no frame à esquerda
        label_senha = tk.Label(frame_senha, text="                   Senha:")
        label_senha.grid(row=0, column=0, sticky='e', padx=(0, 5))

        # Campo de preenchimento no frame à direita
        self.entry_senha = tk.Entry(frame_senha, show="*", width=30)
        self.entry_senha.grid(row=0, column=1, sticky='w')

        # Frame para o campo Confirmar Senha
        frame_confirmar_senha = tk.Frame(frame_principal)
        frame_confirmar_senha.pack(pady=(0, 0))

        # Rótulo "Confirmar Senha" no frame à esquerda
        label_confirmar_senha = tk.Label(frame_confirmar_senha, text="Confirmar Senha:")
        label_confirmar_senha.grid(row=0, column=0, sticky='e', padx=(0, 5))

        # Campo de preenchimento no frame à direita
        self.entry_confirmar_senha = tk.Entry(frame_confirmar_senha, show="*", width=30)
        self.entry_confirmar_senha.grid(row=0, column=1, sticky='w')

        # Botão para salvar o cadastro
        botao_salvar = tk.Button(frame_principal, text="Salvar", command=self.salvar_cadastro, width=7, height=1)
        botao_salvar.pack()

        # Define o tamanho inicial da janela de cadastro
        self.root.geometry("290x112")

    def salvar_cadastro(self):
        novo_usuario = Usuario(self.entry_usuario.get(), self.entry_senha.get())
        self.usuarios.append(novo_usuario)
        self.salvar_callback()
        self.root.destroy()

class TelaPrincipal:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title(f"Controle de Finanças")
        self.itens_comprados = self.carregar_itens_usuario()

        # Frame para o total gasto
        self.frame_total = tk.Frame(root)
        self.frame_total.pack(expand=True, fill=tk.BOTH)

        # Rótulo para o total gasto
        self.label_total_gasto = tk.Label(self.frame_total, text="Total: R$ 0.00")
        self.label_total_gasto.pack(anchor=tk.CENTER)

        # Lista de itens comprados
        self.frame_lista_itens = tk.Frame(root)
        self.frame_lista_itens.pack(expand=True, fill=tk.BOTH)

        self.listbox_itens = tk.Listbox(self.frame_lista_itens, selectmode=tk.SINGLE)
        self.listbox_itens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de rolagem para a lista de itens
        self.scrollbar = tk.Scrollbar(self.frame_lista_itens, command=self.listbox_itens.yview)
        self.listbox_itens.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botão Cadastrar Item à esquerda no frame dos botões
        self.frame_botoes = tk.Frame(root)
        self.frame_botoes.pack(side=tk.BOTTOM)

        self.botao_cadastrar_item = tk.Button(self.frame_botoes, text="Cadastrar Item", command=self.abrir_tela_cadastro_item)
        self.botao_cadastrar_item.pack(side=tk.LEFT)

        # Botões Limpar e Gerar Relatório à direita no frame dos botões
        self.botao_limpar = tk.Button(self.frame_botoes, text="Limpar", command=self.limpar_itens)
        self.botao_limpar.pack(side=tk.RIGHT)

        self.botao_gerar_relatorio = tk.Button(self.frame_botoes, text="Gerar Relatório", command=self.gerar_relatorio)
        self.botao_gerar_relatorio.pack(side=tk.RIGHT)

        # Define o tamanho inicial da janela de cadastro
        self.root.geometry("300x210")

        # Atualiza a lista de itens e o total gasto
        self.atualizar_lista_itens()
        self.atualizar_total_gasto()

    def abrir_tela_cadastro_item(self):
        tela_cadastro_item = TelaCadastroItem(
            self.root,
            self.usuario,
            self.itens_comprados,
            self.atualizar_lista_itens,
            self.atualizar_total_gasto,
            self.atualizar_usuario
        )
        tela_cadastro_item.wait_window()

    def limpar_itens(self):
        self.itens_comprados.clear()
        self.atualizar_lista_itens()
        self.atualizar_total_gasto()
        self.usuario.itens_comprados = self.itens_comprados  # Atualiza a lista do usuário
        self.usuario.salvar_callback()  # Salva as alterações no arquivo


    def gerar_relatorio(self):
        try:
            # Usar o nome do usuário como parte do caminho do arquivo
            nome_arquivo = f"relatorio_{self.usuario.nome}.txt"
            with open(nome_arquivo, "w") as file:
                total_gasto = 0
                for item in self.itens_comprados:
                    file.write(str(item) + "\n")
                    total_gasto += item.preco
                file.write(f"\nTotal Gasto: R$ {total_gasto:.2f}")

            messagebox.showinfo("Relatório Gerado", "Relatório gerado com sucesso!")
        except IOError:
            messagebox.showerror("Erro", "Erro ao operar com o arquivo")

    def atualizar_lista_itens(self):
        self.listbox_itens.delete(0, tk.END)
        for item in self.itens_comprados:
            self.listbox_itens.insert(tk.END, str(item))

    def atualizar_total_gasto(self):
        total_gasto = sum(item.preco for item in self.itens_comprados)
        self.label_total_gasto.config(text=f"Total Gasto: R$ {total_gasto:.2f}")

    def carregar_itens_usuario(self):
        try:
            with open(f"{self.usuario.nome}_itens.pkl", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

    def atualizar_usuario(self):
        self.usuario.itens_comprados = self.itens_comprados
        self.usuario.salvar_callback()

class TelaCadastroItem(tk.Toplevel):
    def __init__(self, root, usuario, itens_comprados, callback_atualizar_lista, callback_atualizar_total, callback_atualizar_usuario):
        tk.Toplevel.__init__(self, root)
        self.usuario = usuario
        self.itens_comprados = itens_comprados
        self.callback_atualizar_lista = callback_atualizar_lista
        self.callback_atualizar_total = callback_atualizar_total
        self.callback_atualizar_usuario = callback_atualizar_usuario

        self.title("Cadastro de Item")

        # Definir o tamanho da janela
        self.geometry("290x245")

        # Criar um frame principal
        frame_principal = tk.Frame(self)
        frame_principal.pack()

        # Rótulo principal
        self.labelCadastroDeItem = tk.Label(frame_principal, text="Cadastro de Item")
        self.labelCadastroDeItem.pack()

        # Frame para o campo Nome
        frame_nome = tk.Frame(frame_principal)
        frame_nome.pack(pady=5)

        # Rótulo "Nome" no frame à esquerda
        self.label_nome = tk.Label(frame_nome, text="    Nome do item:")
        self.label_nome.grid(row=0, column=0, sticky='e', padx=(0, 5))

        # Campo de preenchimento para o nome no frame à direita
        self.entry_nome = tk.Entry(frame_nome, width=30)
        self.entry_nome.grid(row=0, column=1, sticky='w')

        # Frame para o campo Preço
        frame_preco = tk.Frame(frame_principal)
        frame_preco.pack(pady=5)

        # Rótulo "Preço" no frame à esquerda
        self.label_preco = tk.Label(frame_preco, text="                    Preço:")
        self.label_preco.grid(row=0, column=0, sticky='e', padx=(0, 5))

        # Campo de preenchimento para o preço no frame à direita
        self.entry_preco = tk.Entry(frame_preco, width=30)
        self.entry_preco.grid(row=0, column=1, sticky='w')

        # Frame para o campo Local de Compra
        frame_local_compra = tk.Frame(frame_principal)
        frame_local_compra.pack(pady=5)

        # Rótulo "Local de Compra" no frame à esquerda
        self.label_local_compra = tk.Label(frame_local_compra, text="Local de Compra:")
        self.label_local_compra.grid(row=0, column=0, sticky='e', padx=(0, 5))

        # Campo de preenchimento para o local de compra no frame à direita
        self.entry_local_compra = tk.Entry(frame_local_compra, width=30)
        self.entry_local_compra.grid(row=0, column=1, sticky='w')

        # Frame para o campo Data
        frame_data = tk.Frame(frame_principal)
        frame_data.pack(pady=5)

        # Rótulo "Data" no frame à esquerda
        self.label_data = tk.Label(frame_data, text="                      Data:")
        self.label_data.grid(row=0, column=0, sticky='e', padx=(0, 5))

        # Campo de preenchimento para a data no frame à direita
        self.entry_data = tk.Entry(frame_data, width=30)
        self.entry_data.grid(row=0, column=1, sticky='w')
        self.entry_data.bind('<KeyRelease>', self.formatar_data)
   
        # Botão para salvar o cadastro do item abaixo do campo "Data"
        self.botao_salvar = tk.Button(frame_principal, text="Salvar", command=self.salvar_cadastro_item, width=7, height=1)
        self.botao_salvar.pack(pady=5, side=tk.TOP)

        # Frame para os checkbuttons abaixo do botão "Salvar"
        frame_checkbuttons = tk.Frame(frame_principal)
        frame_checkbuttons.pack(pady=5, anchor='w')

        # Checkbutton para indicar se é uma Compra
        self.var_compra = tk.BooleanVar()
        checkbutton_compra = tk.Checkbutton(frame_checkbuttons, text="Compra", variable=self.var_compra, anchor='w')
        checkbutton_compra.grid(row=0, column=0, sticky='w')

        # Checkbutton para indicar se é uma Renda
        self.var_renda = tk.BooleanVar()
        checkbutton_renda = tk.Checkbutton(frame_checkbuttons, text="Renda", variable=self.var_renda, anchor='w')
        checkbutton_renda.grid(row=1, column=0, sticky='w')

        # Função para formatar a data enquanto o usuário digita
    def formatar_data(self, event):
        data = self.entry_data.get()
        if len(data) == 2 and data[1] != '-':
            self.entry_data.insert(2, '-')
        elif len(data) == 5 and data[4] != '-':
            self.entry_data.insert(5, '-')

    def salvar_cadastro_item(self):
        nome = self.entry_nome.get()
        preco = float(self.entry_preco.get())
        local_compra = self.entry_local_compra.get()
        data = self.entry_data.get()
        compra = self.var_compra.get()
        renda = self.var_renda.get()

        try:
            data_formatada = datetime.strptime(data, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use o formato DD-MM-AAAA.")
            return

        novo_item = ItemDeCompra(nome, preco, data_formatada, local_compra, compra, renda)
        self.itens_comprados.append(novo_item)
        self.callback_atualizar_lista()
        self.callback_atualizar_total()
        self.callback_atualizar_usuario()
        self.destroy()

# Exemplo de uso
if __name__ == "__main__":
    janela_principal = tk.Tk()
    tela_login = TelaLogin(janela_principal)
    janela_principal.mainloop()
