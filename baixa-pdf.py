import urllib.request
from bs4 import BeautifulSoup
import wget
import os
import re
from urllib.parse import unquote

def baixar_arquivo(url, endereco):
    try:
        wget.download(url, endereco)
        print(f"Download concluído: {endereco}")
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

meses = ["janeiro", "fevereiro", "março","marco", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
numeros_meses = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "marco": "03", "abril": "04",
    "maio": "05", "junho": "06", "julho": "07", "agosto": "08", "setembro": "09",
    "outubro": "10", "novembro": "11", "dezembro": "12"
}
cidades = ["Londrina", "Cascavel", "Foz do Iguaçu", "Foz do Iguacu", "Maringá","Maringa","Curitiba"]

url_base_ceasa = ["https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2010-Novembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2010-Dezembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Janeiro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Fevereiro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Marco","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Abril","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Maio","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Junho","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Julho","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Agosto","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Setembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Outubro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Novembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Dezembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2012","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2013","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2014","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2015", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2016", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2017","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2018", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2019", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2020", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2021","https://www.ceasa.pr.gov.br/Pagina/Cotacao-Diaria-de-Precos-2022", "https://www.ceasa.pr.gov.br/Pagina/Cotacao-Diaria-de-Precos-2023", "https://www.ceasa.pr.gov.br/Pagina/Cotacao-Diaria-de-Precos-2024"]

BAIXADOS = 'baixados'
os.makedirs(BAIXADOS, exist_ok=True)

for url_base in url_base_ceasa:
    page = urllib.request.urlopen(url_base)
    soup = BeautifulSoup(page, 'html5lib')
    find_a = soup.find_all('a')
    lista_url = []

    for link in find_a:
        obter = link.get('href')
        
        if obter:
            regex_url = re.findall(r"https://.*\.pdf", obter)
            regex_url_2021 = re.findall("/sites/ceasa/arquivos_restritos/files/.*\.pdf", obter)
            
            if regex_url:
                lista_url.append(regex_url[0])
            elif regex_url_2021:
                url_com_https = f"https://www.ceasa.pr.gov.br{obter}"
                lista_url.append(url_com_https)

    for i in lista_url:
        regex_meses = re.findall(r'\b(' + '|'.join(meses) + r')(\d+)', i, re.IGNORECASE)
        
        if regex_meses:
            url = unquote(i)
            mes = regex_meses
            mes_nome = regex_meses[0][0].lower()
            mes_numero = numeros_meses.get(mes_nome)
            qtd_numeros_data = regex_meses[-1][1]
            tam_data_numeros = len(qtd_numeros_data)

             # Formato do arquivo: MêsDDMMYYYY ou MêsDDMMAAAA
            if tam_data_numeros in [6, 8, 10]:
                dia = qtd_numeros_data[:2]
                ano = qtd_numeros_data[-4:]  # Pega os últimos 4 dígitos como ano
                
                if tam_data_numeros == 6:
                    # MêsDDMMYY (ano é YY, ex: 01-01-17)
                    ano = '20' + ano[-2:]  # Para converter YY em YYYY
                elif tam_data_numeros == 8:
                    # MêsDDMMYYYY (ano é YYYY, ex: 01-01-2017)
                    pass  # Ano já está correto
                elif tam_data_numeros == 10:
                    # Lógica para formatos específicos, se necessário
                    pass  # Ajuste conforme o formato que você precisa

                formato_nome_arquivo = f"{ano}-{mes_numero}-{dia}"
                
                nome_arquivo = os.path.join(BAIXADOS, f'{formato_nome_arquivo}.pdf')       
                if not os.path.exists(nome_arquivo):
                    baixar_arquivo(url, nome_arquivo)
                else:
                    print(f'Arquivo já baixado: {nome_arquivo}')