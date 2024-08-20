import threading
from interface import draw_running_state, draw_done_state, atualizar_status
from baixa_pdf import processa_urls
from extrai_pdf import extrai_arq

def executa_processar_urls():
    def task():
        draw_running_state()
        atualizar_status("Baixando Arquivos...")
        processa_urls()
        atualizar_status("Arquivos Baixados!")
        draw_done_state()
    
    threading.Thread(target=task).start()  # Executa a tarefa em uma nova thread

def executa_extrai_arq():
    def task():
        draw_running_state()
        atualizar_status("Atualizando Banco de Dados...")
        extrai_arq()
        atualizar_status("Extração Concluída!")
        draw_done_state()
    
    threading.Thread(target=task).start()  # Executa a tarefa em uma nova thread
