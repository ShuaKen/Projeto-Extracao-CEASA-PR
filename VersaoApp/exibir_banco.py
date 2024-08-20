import tkinter as tk
from tkinter import ttk
import sqlite3

def configurar_treeview(treeview):
    # Define as colunas
    colunas = (
        'ID', 'Data', 'Produto', 'Tipo', 'Unidade Embalagem',
        'Valor Unidade de Medidas', 'Unidade de Medidas', 'Situação Mercado',
        'Valor Mínimo', 'Valor M_C do Dia', 'Valor Máximo',
        'Valor M_C do dia Anterior', 'Valor Variação', 'Estados', 'Cidade'
    )
    
    treeview['columns'] = colunas
    
    # Configura as colunas
    for col in colunas:
        treeview.column(col, anchor=tk.W, width=120, stretch=tk.NO)  # Ajuste o width conforme necessário
        treeview.heading(col, text=col, anchor=tk.W)
    
    # Exclui o cabeçalho padrão que não é necessário
    treeview['show'] = 'headings'

def carregar_dados(treeview, filtro=""):
    # Conectar ao banco de dados
    conn = sqlite3.connect('ceasa_pr.db')
    cursor = conn.cursor()

    # Define as colunas para pesquisa
    colunas = [
        'data', 'produto', 'tipo', 'unidade_embalagem', 'valor_unidade_de_medidas', 'unidade_de_medidas', 'situacao_mercado', 'valor_min', 'valor_m_c_do_dia', 'valor_max','valor_m_c_do_dia_anterior', 'valor_variacao', 'estados_siglas', 'cidade'
    ]
    
    # Construa a consulta SQL com base nas colunas
    query = "SELECT * FROM produtos"
    parametros = ()
    if filtro:
        conditions = [f"{col} LIKE ?" for col in colunas]
        query += " WHERE " + " OR ".join(conditions)
        parametros = tuple([f"%{filtro}%" for _ in colunas])
    
    cursor.execute(query, parametros)
    registros = cursor.fetchall()

    # Limpar o Treeview antes de adicionar novos dados
    treeview.delete(*treeview.get_children())
    
    # Adiciona dados ao Treeview
    for registro in registros:
        treeview.insert('', 'end', values=registro)
    
    conn.close()

def pesquisar(treeview, entry):
    # Obtém o texto de pesquisa e carrega os dados filtrados
    texto_pesquisa = entry.get()
    carregar_dados(treeview, texto_pesquisa)

def exibir_banco():
    # Configuração da janela principal
    janela_exibir_banco = tk.Tk()
    janela_exibir_banco.title("Visualizador de Dados do SQLite")
    
    # Maximiza a janela
    janela_exibir_banco.state('zoomed')

    # Criação do frame principal com layout de grid
    frame_principal = tk.Frame(janela_exibir_banco)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Criação da barra lateral
    largura_barra_lateral = 200
    barra_lateral = tk.Frame(frame_principal, width=largura_barra_lateral, bg='lightgray', height=1)
    barra_lateral.pack(side=tk.LEFT, fill=tk.Y)

    # Adiciona o campo de pesquisa e botão à barra lateral
    campo_pesquisa = tk.Entry(barra_lateral, width=20)
    campo_pesquisa.pack(pady=10, padx=10, fill=tk.X)

    botao_pesquisar = tk.Button(barra_lateral, text="Pesquisar", command=lambda: pesquisar(treeview, campo_pesquisa))
    botao_pesquisar.pack(pady=10, padx=10)

    # Criação do frame para o Treeview
    frame_treeview = tk.Frame(frame_principal)
    frame_treeview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Criação da barra de rolagem horizontal
    barra_rolagem_horizontal = ttk.Scrollbar(frame_treeview, orient=tk.HORIZONTAL)
    barra_rolagem_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

    # Criação da barra de rolagem vertical
    barra_rolagem_vertical = ttk.Scrollbar(frame_treeview, orient=tk.VERTICAL)
    barra_rolagem_vertical.pack(side=tk.RIGHT, fill=tk.Y)

    # Criação do Treeview
    treeview = ttk.Treeview(frame_treeview, xscrollcommand=barra_rolagem_horizontal.set, yscrollcommand=barra_rolagem_vertical.set)
    configurar_treeview(treeview)

    # Configurar a barra de rolagem
    barra_rolagem_horizontal.config(command=treeview.xview)
    barra_rolagem_vertical.config(command=treeview.yview)

    # Carregar dados no Treeview inicialmente sem filtro
    carregar_dados(treeview)

    # Exibir o Treeview
    treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Ajusta a largura das colunas com base na largura da janela
    def ajustar_largura_colunas(event=None):
        largura_janela = frame_treeview.winfo_width()
        num_colunas = len(treeview['columns'])
        largura_coluna = largura_janela // num_colunas

        for col in treeview['columns']:
            treeview.column(col, width=largura_coluna)
    
    # Ajustar a largura das colunas quando a janela for redimensionada
    frame_treeview.bind("<Configure>", ajustar_largura_colunas)

    # Iniciar o loop principal
    janela_exibir_banco.mainloop()


