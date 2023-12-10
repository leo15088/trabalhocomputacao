# Parte responsável pela importação dos módulos
import sys
import os

# Obtém o diretório da pasta
diretorio_do_arquivo = os.path.dirname(os.path.abspath(__file__))

# Adiciona o diretório ao path para importar módulos de lá
sys.path.append(diretorio_do_arquivo)

# Muda o diretório de trabalho para o local do script
os.chdir(os.path.join(diretorio_do_arquivo, 'View'))

# Executa o script TelaLogin.py como um programa separado
os.system('python view4.py')