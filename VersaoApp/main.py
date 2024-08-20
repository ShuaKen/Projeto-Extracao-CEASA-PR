from tkinter import Tk
from interface import configurar_interface
from tarefas import executa_processar_urls, executa_extrai_arq
from exibir_banco import exibir_banco

def main():
    configurar_interface(executa_processar_urls, executa_extrai_arq, exibir_banco)

if __name__ == "__main__":
    main()
