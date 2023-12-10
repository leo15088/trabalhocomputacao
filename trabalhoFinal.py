import tkinter as tk
from tkinter import messagebox
import pickle
import datetime

class Usuario:
    '''esta classe representa um usuario'''
    def __init__(self, nome, senha,itensComprados,listaDeRendas):
        if any(c.isdigit() for c in nome):
            raise ValueError("O nome não pode conter números.")
        self.__nome = nome
        self.__senha = senha
        self.__itensComprados = []  # Lista de objetos ItemDeCompra
        self.__listaDeRendas = []  # Lista de objetos Renda
# Métodos acessadores (getters/setters) para atributos privados
    def get_nome(self):
        return self.__nome

    def set_nome(self, novoNome):
        if any(c.isdigit() for c in novoNome):
            raise ValueError("O nome não pode conter números.")
        self.__nome = novoNome

    def get_senha(self):
        return self.__senha

    def set_senha(self, novaSenha):
        self.__senha = novaSenha

    def get_itensComprados(self):
        return self.__itensComprados

    def set_itensComprados(self, novoItem):
        self.__itensComprados.append(novoItem)

    def get_listaDeRendas(self):
        return self.__listaDeRendas

    def set_listaDeRendas(self, novaLista):
        self.__listaDeRendas = novaLista
#Esse método retorna as informações da classe
    def __str__(self):
        return f'Usuário: {self.__nome}'

    
class ItemDeCompra:
    '''Esta classe representa os itens de compra'''
    def __init__(self, nome,preco,local):
        if any(c.isdigit() for c in nome):
            raise ValueError("O nome não pode conter números.")
        self.__nome = nome
        if not isinstance(preco, (float, int)):
            raise ValueError("O preço só pode conter números.")
        self.__preco = preco
        self.dataCompra=datetime.datetime.now()
        if any(c.isdigit() for c in local):
            raise ValueError("O local só pode ser string")
        self.local=local

    # Métodos acessadores (getters/setters) para atributos privados
    def get_nome(self):
        return self.__nome

    def set_nome(self, novoNome):
        if any(c.isdigit() for c in novoNome):
            raise ValueError("O nome não pode conter números.")
        self.__nome = novoNome

    def get_preco(self):
        return self.__preco

    def set_preco(self, novoPreco):
        if not isinstance(preco, (float, int)):
            raise ValueError("O preço só pode conter números.")
        self.__preco = novoPreco

#Esse método retorna as informações da classe

    def __str__(self):
        return f'itemDeCompra: {self.__nome}\n {self.__preco}\n{self.dataCompra}\n {self.local}'

class Renda:
    '''Esta classe representa a renda'''
    def __init__(self, nome, valor, fonte):
        if any(c.isdigit() for c in nome):
            raise ValueError("O nome não pode conter números.")
        self.__nome = nome
        if not isinstance(valor, (float, int)):
            raise ValueError("O valor só pode conter números.")
        self.__valor = valor
        self.dataDeRecebimento = datetime.datetime.now()
        if any(c.isdigit() for c in fonte):
            raise ValueError("A fonte só pode ser string")
        self.fonte = fonte

    # Métodos acessadores (getters/setters) para atributos privados
    def get_nome(self):
        return self.__nome

    def set_nome(self, novoNome):
        if any(c.isdigit() for c in novoNome):
            raise ValueError("O nome não pode conter números.")
        self.__nome = novoNome

    def get_valor(self):
        return self.__valor

    def set_valor(self, novoValor):
        if not isinstance(novoValor, (float, int)):
            raise ValueError("O valor só pode conter números.")
        self.__valor = novoValor

    # Este método retorna as informações da classe
    def __str__(self):
        return f'A renda: {self.__nome}\n valor:{self.__valor}\n fonte:{self.fonte}\n{self.dataDeRecebimento}'

try:
    Renda1 = Renda('fdfe', 11.0, 'ityl')
    print(Renda1)
except ValueError as e:
    print(e)
    
