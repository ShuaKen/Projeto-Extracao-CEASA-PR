from tkinter import Tk, Label, Button, Canvas
from tkinter import ttk  # Para widgets modernos

# Variáveis globais
texto_extracao = None
status_canvas = None
janela = None

def atualizar_status(mensagem):
    global texto_extracao
    texto_extracao.config(text=mensagem)
    janela.update()  # Atualiza a interface gráfica

def draw_running_state():
    # Limpa o Canvas e desenha um círculo azul
    status_canvas.delete("all")
    status_canvas.create_oval(5, 5, 25, 25, fill="blue")

def draw_done_state():
    # Limpa o Canvas e desenha um 'v' verde
    status_canvas.delete("all")
    status_canvas.create_text(15, 15, text="✓", font=("Arial", 20), fill="green")

def configurar_interface(executa_processar_urls, executa_extrai_arq, exibir_banco):
    global texto_extracao, status_canvas, janela

    janela = Tk()
    janela.title("Extração dos Documentos")
    janela.geometry("400x400")
    janela.configure(bg="#f0f0f0")  # Cor de fundo da janela

    # Frame principal
    frame_principal = ttk.Frame(janela, padding="20")
    frame_principal.place(relx=0.5, rely=0.5, anchor="center")

    # Configuração dos widgets
    text_orientacao = ttk.Label(frame_principal, text="Escolha uma opção:", font=("Arial", 14))
    text_orientacao.grid(column=0, row=0, columnspan=2, pady=10, sticky="n")

    btn_adicionar_atualizar_documentos = ttk.Button(
        frame_principal, text="Adicionar/Atualizar Documentos", command=executa_processar_urls
    )
    btn_adicionar_atualizar_documentos.grid(column=0, row=1, columnspan=2, pady=5, padx=5, sticky="ew")

    btn_extrai_documentos = ttk.Button(
        frame_principal, text="Extrair Documentos", command=executa_extrai_arq
    )
    btn_extrai_documentos.grid(column=0, row=2, columnspan=2, pady=5, padx=5, sticky="ew")

    # Label para mostrar o status
    texto_extracao = ttk.Label(frame_principal, text="Status...", anchor="w", font=("Arial", 12))
    texto_extracao.grid(column=0, row=3, columnspan=1, pady=10, sticky="e")

    # Adiciona o Canvas para o status
    status_canvas = Canvas(frame_principal, width=30, height=30, bg="#f0f0f0", highlightthickness=0)
    status_canvas.grid(column=1, row=3, pady=10, sticky="w")

    # Inicialmente, desenha o estado "Pronto"
    status_canvas.create_oval(5, 5, 25, 25, fill="grey")

    btn_exibir_dados = ttk.Button(frame_principal, text="Exibir Dados", command=exibir_banco)
    btn_exibir_dados.grid(column=0, row=4, columnspan=2, pady=10, padx=10, sticky="ew")

    # Configuração do layout
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_rowconfigure(0, weight=0)
    frame_principal.grid_rowconfigure(1, weight=0)
    frame_principal.grid_rowconfigure(2, weight=0)
    frame_principal.grid_rowconfigure(3, weight=0)
    frame_principal.grid_rowconfigure(4, weight=0)

    janela.mainloop()
