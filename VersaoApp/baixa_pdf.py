import urllib.request
from bs4 import BeautifulSoup
import wget
import os
import re
from urllib.parse import unquote
import fitz  # PyMuPDF
import pikepdf

def convert_to_pdfa(input_path, output_path):
    try:
        # Abrir o PDF com PyMuPDF
        doc = fitz.open(input_path)
        
        # Adicionar metadados mínimos exigidos pelo PDF/A usando PyMuPDF
        doc.set_metadata({
            'title': 'PDF/A Document',
            'author': 'Generated by PyMuPDF and PikePDF',
            'creator': 'PyMuPDF',
            'producer': 'PyMuPDF'
        })

        # Salvar o PDF com as configurações necessárias para PDF/A usando PyMuPDF
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()
        
        # Reabrir o PDF e usar pikepdf para realizar ajustes adicionais para conformidade PDF/A
        with pikepdf.open(output_path) as pdf:
            # Configurar para PDF/A-2b
            pdf.save(output_path, options="pdfa-2b")
        
        # Verificar se o arquivo PDF/A é válido
        if is_pdfa_valid(output_path):
            print(f'Converted {input_path} to PDF/A and saved as {output_path}')
        else:
            print(f'Failed to convert {input_path} to PDF/A. The output file {output_path} is not a valid PDF/A file.')
    except Exception as e:
        pass

def is_pdfa_valid(file_path):
    try:
        # Verificar se o arquivo é um PDF/A válido
        with pikepdf.open(file_path) as pdf:
            if pdf.is_pdfa:
                return True
            else:
                return False
    except Exception as e:
        #print(f'An error occurred while checking PDF/A conformance: {e}')
        return False

def baixar_arquivo(url, endereco):
    try:
        wget.download(url, endereco)
        print(f"Download concluído: {endereco}")
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")


def processa_urls():
    meses = ["janeiro", "fevereiro", "março","marco", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    numeros_meses = {
        "janeiro": "01", "fevereiro": "02", "março": "03", "marco": "03", "abril": "04",
        "maio": "05", "junho": "06", "julho": "07", "agosto": "08", "setembro": "09",
        "outubro": "10", "novembro": "11", "dezembro": "12"
    }
    cidades = ["Londrina", "Cascavel", "Foz do Iguaçu", "Foz do Iguacu", "Maringá","Maringa","Curitiba"]

    url_base_ceasa = ["https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2010-Novembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2010-Dezembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Janeiro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Fevereiro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Marco","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Abril","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Maio","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Junho","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Julho","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Agosto","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Setembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Outubro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Novembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2011-Dezembro","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2012","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2013","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2014","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2015", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2016", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2017","https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2018", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2019", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2020", "https://www.ceasa.pr.gov.br/Pagina/Informacoes-de-Precos-Diarios-Unidade-Ceasa-Londrina-2021","https://www.ceasa.pr.gov.br/Pagina/Cotacao-Diaria-de-Precos-2022", "https://www.ceasa.pr.gov.br/Pagina/Cotacao-Diaria-de-Precos-2023", "https://www.ceasa.pr.gov.br/Pagina/Cotacao-Diaria-de-Precos-2024"]
    
    BAIXADOS = 'C:/Users/joshu/OneDrive/Documentos/projeto-extracao-CEASA-PR/versaoFinal/baixados'
    # Cria a pasta se ela não existir
    os.makedirs(BAIXADOS, exist_ok=True)

    for url_base in url_base_ceasa:
        page = urllib.request.urlopen(url_base)
        soup = BeautifulSoup(page, 'html5lib')
        find_a = soup.find_all('a')
        lista_url = []

        for link in find_a:
            obter = link.get('href')
            formato_nome_arquivo =''
            if obter:
                regex_url = re.findall(r"https://.*\.pdf", obter)
                #print("regex_url",regex_url)
                regex_url_2021 = re.findall(r"/sites/ceasa/arquivos_restritos/files/.*\.pdf", obter)
                #print("regex_url_2021",regex_url_2021)
                if regex_url:
                    lista_url.append(regex_url[0])
                elif regex_url_2021:
                    url_com_https = f"https://www.ceasa.pr.gov.br{obter}"
                    lista_url.append(url_com_https)

        
        for i in lista_url:
            url = unquote(i)

            regex_meses = re.findall(r'\b(' + '|'.join(meses) + r')(\d+)', url, re.IGNORECASE)
            
            if regex_meses :
                
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
                formato_nome_arquivo = f"convert{ano}-{mes_numero}-{dia}"       
            elif 'cotacao' in i:
                
                #print('urrrs',url, type(url))
                #alguns casos de 2021 possuem https://www.ceasa.pr.gov.br 2X
                regex_https_duplo = novo_texto = re.sub(r"https://www\.ceasa\.pr\.gov\.br(http://www\.ceasa\.pr\.gov\.br.*)", r"\1", url)
                #print("essa é a url",url)
                if novo_texto:
                    url = novo_texto
                    #print('nosas', url)
                regex_url_data = re.search(r"cotacaolda(\d{2})(\d{2})(\d{4})\.pdf$", url)
                #print("bora",regex_url_data)
                if regex_url_data:
                    dia = regex_url_data.group(1)
                    mes_numero = regex_url_data.group(2)
                    ano = regex_url_data.group(3)    
                formato_nome_arquivo = f"convert{ano}-{mes_numero}-{dia}"    
            else:
                continue    
            
            nome_arquivo = os.path.join(BAIXADOS, f'{formato_nome_arquivo}.pdf')
            nome_arquivo_verifica = nome_arquivo.replace('convert','')
                  
            if not os.path.exists(nome_arquivo_verifica):
                baixar_arquivo(url, nome_arquivo)
            else:
                print(f'Arquivo já baixado: {nome_arquivo}')
            #conversão para PDF/A
            if os.path.exists(nome_arquivo) and 'convert' in nome_arquivo:
                input_path = nome_arquivo
                output_path = nome_arquivo.replace('convert', '')
                convert_to_pdfa(input_path, output_path)
                os.remove(nome_arquivo)
