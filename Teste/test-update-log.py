import os
import re
import tabula
import sqlite3
from unidecode import unidecode
import logging

# Configuração do logging
logging.basicConfig(
    filename='processamento.log',  # Nome do arquivo de log
    level=logging.INFO,  # Nível de log (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato da mensagem
)

conn = sqlite3.connect('TESTE_BD.db')
cursor = conn.cursor()
lista_produtos_comparar = ["maracuja","radite","palmito/pupunha conserva vidro", "funcho", "cebolinha cheiro-verde","bucha","broto de feijao moyashi","broto de bambu","nabo branco","batada doce", "batata salsa mandiquinha","batata lavada","genipapo", "jatoba","jambo", "phisalis", "ciriguela", "kino/kiwano", "macadamia","noz peca", "mirtilo","mangostim", "fruta do conde", "figo da india","maça","cereja", "castanha do para", "kinkan", "grap fruit", "lima persia", "grão de bico", "feijão","amendoim com casca", "amendoim sem casca", "amendoim", "salvia", "salsinha", "salsao aipo", "manjerona", "chicória/escarola", "escarola/chicoria", "couve manteiga", "couve chinesa", "couve brocolo", "cheiro verde", "aspargo", "alho poró", "mandioquinha/batata salsa", "alecrim", "cebolao", "inhame/taia","aipim-mandioca", "aipim", "alho importado", "alho nacional", "pimenta", "caxi", "abacate breda/margarida", "abacate fucks/geada", "abacate fortuna/quintal", "abacaxi havai", "abacaxi perola", "abiu", "acerola", "ameixa estrangeira", "ameixa nacional", "amendoa", "amora", "atemoia", "avela", "banana maca", "banana nanica", "banana prata", "caju", "caqui", "carambola", "castanha estrangeira", "castanha nacional", "cereja estrangeira", "cidra", "coco verde", "cupuacu", "damasco estrangeiro", "figo", "framboesa", "goiaba", "graviola", "greap fruit", "jabuticaba", "jaca", "pera nacional", "pera importada","kiwi", "laranja", "laranja pera", "lichia", "lima da persia", "limão", "limão taiti", "mamao", "manga", "mangostao", "maracuja azedo", "maracuja doce", "marmelo", "melancia","melao","melao amarelo","morango", "nectarina","nectarina estrangeira", "nectarina nacional", "nespera", "nozes", "pêra nacional", "pêra estrangeira","pessego", "pessego nacional", "pessego estrangeiro", "physalis", "pinha", "pitaia", "quincam", "roma", "sapoti","seriguela", "tamara", "tamarindo", "tangerina cravo", "tangerina murcot", "tangerina poncam", "uva italia", "uva niagara","uva rubi", "uva thompson", "uva estrangeira", "abobora d'agua", "abobora japonesa", "abobora moranga", "abobora paulista","abobora seca", "abobrinha brasileira", "abobrinha italiana", "batata doce", "batata yakon", "alcachofra", "batata doce amarela","batata doce rosada", "berinjela comum", "berinjela conserva", "berinjela japonesa", "beterraba", "cará", "cenoura", "chuchu",   "cogumelo", "ervilha comum", "ervilha torta", "fava", "feijao corado", "gengibre", "jilo", "mandioca", "mandioquinha", "maxixe", "pepino caipira", "pepino comum", "pepino japones", "pimenta cambuci", "pimenta vermelha", "pimentao amarelo", "pimentao verde", "pimentao vermelho", "quiabo", "taquenoco", "tomate", "tomate caqui", "tomate salada", "vagem", "acelga", "agriao", "alface", "alho porro", "almeirão", "aspargos", "beterraba com folhas", "brocolis", "catalonha", "cebolinha", "cenoura com folhas", "chicoria", "coentro", "couve", "couve bruxelas", "couve flor", "endívia", "erva-doce", "escarola","espinafre", "folha de uva", "gengibre com folhas", "gobo", "hortelã", "louro", "manjericão", "milho verde", "moiashi","mostarda preta", "nabo", "orégano", "palmito", "rabanete", "repolho", "rúcula", "salsão", "alho nacional", "alho estrangeiro", "batata nacional", "canjica", "cebola nacional", "cebola mg", "cebola sc", "cebola sp", "cebola estrangeira", "coco seco", "milho pipoca nacional", "milho pipoca estrangeiro","ovos", "ovos brancos", "ovos de codorna", "ovos vermelhos","leite","mel","carne","peixe","queijo", "pinhão", "agapanto", "astromeria", "angelica", "anturio", "azaleia", "begonia", "boca de leao", "branquinha", "bromelia", "ciclamem", "copo de leite", "cravina", "crisantemo", "dalia", "dracena", "estatice", "estrelicia", "eucalipto simeria", "flor de trigo", "gerbera", "gipysofila", "girassol", "gladíolo", "goivo", "grama", "heleconia", "hortencia", "impatins", "jasmim", "kalanchoe", "lirio", "lisianthus", "mini rosa", "musgo pequeno", "orquidea", "palmeira", "petunia", "pingo de ouro", "primula","samambaia", "tango", "tuia", "violeta", "abrotea", "agulhao", "anchovas", "atum", "bacalhau seco", "badejo", "bagre", "berbigao", "betarra", "bonito", "cacao", "camarao cativeiro", "camarao 7 barbas", "cambeva", "caranguejo", "carapau", "cascote", "cavalinha", "conglio", "corvina", "curimbeta", "espada", "galo", "garoupa", "gordinho", "guaivira", "jundia", "lambari", "linguado", "lula", "mandi", "manjuba", "meca", "merluza", "mexilhao", "mistura", "namorado", "olhete", "olho de boi", "ostra", "oveva", "pacu", "palombeta","alfava", "pampo", "papa terra", "parati", "pargo", "peroa", "pescada", "piau", "pintado", "piranha", "pitangola", "polvo", "robalo", "salmao", "sardinha fresca", "savelha", "serra", "siri", "sororoca", "tainha", "tilapia", "traira", "trilha", "pescado", "truta", "tucunare", "vira", "abacate", "abacaxi", "abobora", "abobrinha","alfavaca", "alface", "alho", "banana", "batata doce", "arroz","berinjela", "beterraba", "brocolos", "cara", "cebola", "cenoura", "chuchu", "coco", "couve", "couve flor", "goiaba", "inhame", "jilo", "laranja", "limao", "maçã importada", "maca (importada)", "maca nacional", "maca nacional", "mamao", "mandioca", "mandioquinha", "manga", "maracujá", "melancia", "melão","milho", "morango", "ovo", "pepino","pêra (nacional)", "pêra importada", "pêra nacional", "pimentao", "quiabo", "repolho", "tangerina", "tomate", "uva", "vagem"
]

#Lista das Siglas dos Estados e Paises que o brazil faz importação dos produtos
estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO", 'ARG', "CHN", "USA", "DEU", "JPN", "KOR", "MEX", "IND", "SAU", "CAN","ITA", "GBR", "ESP", "NLD", "BEL", "CHE", "SWE", "RUS","ZAF", "IDN", "TUR", "IRL", "POL", "THA", "SGP", "MYS", "EGY", "ARE", "CLILE", "CHL", "URU"]
#Dentro do campo "UNIDADE EMBALAGEM", tem esse capo que é a primeira opção, varia de documento para documento, exemplo os mais antigos normalmente usam nomes completos como "Caixa" 
unidades_de_embalagens = ["cx","caixa", "un", "unidade", "kg", "c1", "pt","pcte", "cb", "sc ", "mç", "mc","maço" ,"maco", "bj", "dz","engr","duzia", "dúzia", "fardo", "quilo", "saco", "eg ", "bandeija", "balde", "pc ", "bandeja "]
#Campo situação do mercado-AUS=Produto indisponível no mercado
# -FRA=Mercado fraco: Quando o preço mais comum do dia é inferior ao do dia anterior
# -FIR=Mercado firme: Quando o preço mais comum do dia é superior ao do dia anterior.
# -EST=Mercado estável: Quando o preço mais comum do dia é igual ao anterior
situacoes_de_mercado = ["aus", "fir","firme", "fra", "fraco", "est", "estável", "estavel"]
# Lista de dias da semana em vários formatos
dias_da_semana = ["segunda-feira", "segunda","terça-feira", "terça","quarta-feira","quarta", "quinta-feira", "quinta", "sexta-feira", "sexta", "sábado","domingo"]
# Lista de meses em português
meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
cidades = ["Londrina", "Cascavel", "Foz do Iguaçu", "Foz do Iguacu", "Maringá","Maringa", "Curitiba"]
meses_r = '|'.join(meses)
#lista para achar os produtos, fica fora do for para não zerar a cada interação
lista_produtos = []

#dia da semana
ano_obtido = 0


def listar_arquivos_em_pasta(caminho_pasta):
    try:
        # Verificar se o caminho especificado é uma pasta
        if not os.path.isdir(caminho_pasta):
            raise ValueError(f'O caminho {caminho_pasta} não é uma pasta válida.')

        # Listar todos os arquivos na pasta
        arquivos = os.listdir(caminho_pasta)

        # Retornar a lista de arquivos
        return arquivos

    except ValueError as ve:
        logging.error(f'Erro: {ve}')
        return []  # Retorna uma lista vazia se houver um erro de caminho
    except Exception as e:
        logging.error(f'Ocorreu um erro inesperado: {e}')
        return []  # Retorna uma lista vazia se houver um erro inesperado

# Exemplo de uso
if __name__ == "__main__":
    caminho_da_pasta = 'C:/Users/joshu/OneDrive/Documentos/projeto-extracao-CEASA-PR/testeNovo/arquivos'  # caminho da pasta que está os arquivos
    
    # Chamando a função para obter a lista de arquivos
    lista_de_arquivos = listar_arquivos_em_pasta(caminho_da_pasta)
    
    # Imprimindo os arquivos encontrados
    print(f'Arquivos na pasta {caminho_da_pasta}:')
    contador = 0
    for arquivo in lista_de_arquivos:
        logging.info(f'Iniciando o processamento do arquivo: {arquivo}')
        filename = f'{caminho_da_pasta}/{arquivo}'
        logging.info(f'Nome do arquivo completo: {filename}')
        #arquivo/data que será verificada no BD
        arquivo_verifica = str(arquivo).replace('.pdf','')
        #Comando de verificação, soma a quantidade de datas e retorna um valor
        cursor.execute('SELECT COUNT(*) FROM Produtos WHERE data = ?', (arquivo_verifica,))
        #resultado da soma
        resultado = cursor.fetchone()[0]
        #caso a data não exista no banco de dados executa o arquivo
        if resultado == 0:
            #Lista dos Produtos para identificar seus tipos, exemplo 'ABACATE','ABACAXI', ...
            data = tabula.read_pdf(filename, multiple_tables=True, pages="all", stream=True, guess=False, encoding='Ansi')
            #data numerica do arquivo
            data_numerica = str(arquivo).replace('.pdf', '')
            regex_ano_data = re.findall(r'^\d{4}', data_numerica)
            ano_obtido = int(regex_ano_data[0])
            produtos_ausentes = 0
            if data:
                for pag_num, df in enumerate(data, start=2):
                    selected_data = df.values.tolist() #seleciona linhas
                    #print('selecionar: ',selected_data)
                    if len(selected_data) >= 1 :
                        for i in selected_data:
                            print('-'*50)
                            print("Arquivo: ",data_numerica)
                            produto = tipo_produto = unidade_embalagem = unidade_de_medidas = situacao_mercado = estados_siglas= ''
                            valor_unidade_de_medidas = min = m_c_do_dia = max = m_c_dia_anterior = var = total_valores = 0

                            #Seleção da lista e transfomar em string
                            find_unidade = str(i).lower().replace('[','').replace("'","").replace(']','').replace('(','').replace(')','')
                            #obtenção da primeira palavra do i 
                            find_comeco = find_unidade.split()[0].replace('[', '').replace("'", "").replace(']','').replace(',','') 

                            # print('find_aa', find_unidade)            
                            print('Original: ', i )
                        
                            if 'produtos ausentes' in find_unidade.lower():
                                produtos_ausentes += 1
                                logging.warning('Produtos ausentes encontrados. Ignorando a linha.')
                                break
                            if produtos_ausentes >= 1:
                                continue
                            if any(keyword in find_unidade.lower() for keyword in ['produto', 'centrais', 'mercado', 'fonte', 'c o t a', '#ref!', '[nan', 'legenda', 'coleta', 'data', 'embalagem', 'm_c', 'pesquisa', 'endere', 'preco', 'obs:', 'fir -', 'fra -', 'est -', 'aus -', 'cep:', 'situa', 'produto indispon', 'telefone']):
                                logging.warning(f'{find_unidade} foi encontrado. Ignorando a linha.')
                                continue
                            
                            
                            regex_cidades = re.findall(r'\b(' + '|'.join(cidades) + r')\b', find_unidade, re.IGNORECASE)
                            #print('regex_cidades',regex_cidades)
                            #identifica as datas 
                            regex_datas = re.findall(r'(?i)\b(?:segunda|terça|quarta|quinta|sexta|sábado|domingo)-feira,\s\d{1,2}\sde\s(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\sde\s\d{4}\b', find_unidade, re.IGNORECASE)
                            regex_tipo_mais_de_uma_palavra = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[a-zA-Z]+)*\b', find_unidade)
                            #print('antes FONTE:', find_unidade)
                            
                            if regex_cidades:
                                cidade = regex_cidades[-1]
                            #print('REGEX_CIDADES:', find_unidade)

                            #encontra elementos antes da unidade ex:cx, un...
                            regex_antes_unidade = re.findall(r'^(.*?)\s*(?:{})'.format('|'.join(re.escape(p) for p in unidades_de_embalagens)), find_unidade, re.IGNORECASE)
                            #comparação do find com a lista de produtos comparar
                            regex_produtos_comparar = re.findall(r'\b(' + '|'.join(lista_produtos_comparar) + r')\b', unidecode(find_unidade), re.IGNORECASE)
                            
                            produto = regex_produtos_comparar
                            produto = str(produto).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace(",","")
                            #print('>>>PRODUTO', produto, 'len()', len(produto))
                            #caso exista alguma coisa na regex
                            if len(produto) > 1 :
                                lista_produtos.append(produto)
                            if lista_produtos:
                                produto = str(lista_produtos[-1])
                                if 'cereja' in produto and 'tomate' in lista_produtos[-2] :
                                    produto = lista_produtos[-2]
                            #para obter o tipo do produto                        
                            tipo_produto = regex_antes_unidade
                            tipo_produto = str(tipo_produto).replace("['",'').replace("']","")
                            #print(f'Produto é: {produto}>>>> Tipo: {tipo_produto}')
                            
                            #para identificar as Siglas da PROCEDENCIA, como estados e países
                            regex_estados_siglas = re.findall(r'\b(' + '|'.join(estados) + r')\b', find_unidade, re.IGNORECASE)
                                        
                            #para identificar SITUACAO MERCADO
                            regex_sitacao_mercado = re.findall(r'\b(' + '|'.join(situacoes_de_mercado) + r')\b', find_unidade, re.IGNORECASE)
                            #print('regexzfa', regex_estados_siglas, type(regex_estados_siglas), len(regex_sitacao_mercado))
                            #para identificar o tipo da UNIDADE EMBALAGEM
                            regex_unidade_embalagem_tipo = re.search(r'\b(' + '|'.join(unidades_de_embalagens) + r')\d*\b', find_unidade, re.IGNORECASE)
                            
                            #para identificar o valor da medida(UNIDADE EMBALAGEM)
                            regex_valor_unidade_medidas = re.findall(r'(\d+[.,]?\d*)\s*(?=Kg|g|un|Dz|gr)', find_unidade, re.IGNORECASE)
                            
                            regex_valor_unidade_medidas_duas = re.findall(r'(\d[\d,.]*\s+a\s+\d[\d,.]*)', find_unidade, re.IGNORECASE)
                    
                            #para identificar o tipo da medida(UNIDADE EMBALAGEM)ex: KG
                            regex_tipos_de_unidade_de_medidas = re.findall(r'\b(\d*\.?\d+)\s*(kg|g|gr|kilo)\b', find_unidade, re.IGNORECASE) 
                            
                            #para identificar os preços(MIN/ M_C DO DIA/ MAX M>C/ DIA ANTERIOR/ VAR %)
                            regex_preco= re.findall(r'\b\d+,\d{2}\b', find_unidade)
                            #print('regex_prego', regex_preco, 'Length',len(regex_preco))
                            if len(regex_sitacao_mercado) == 0 :
                                situacao_mercado = 'Não definida'
                                #print('situacaoaa', situacao_mercado)
                            if len(regex_preco) == 0:
                                min = m_c_do_dia = max = m_c_dia_anterior = 0.00
                            if len(regex_estados_siglas) == 0:
                                estados_siglas = 'Sem procedencia'
                                #print('regex_estados_siglas',regex_estados_siglas)
                            #identifica tipo da embalagem(UNIDADE EMBALAGEM) ex:CX
                            if regex_unidade_embalagem_tipo:
                                unidade_embalagem = regex_unidade_embalagem_tipo
                                #Caso tenha duas ocorrencias ex: 2 SC ele obtem apenas o 1º
                                unidade_embalagem= unidade_embalagem.group(1)
                            else:
                                unidade_embalagem = 'não possui Unidade'
                                logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}, não possui Unidade de Embalagem')
                            #identifica o Tipo da unidade de medida (UNIDADE EMBALAGEM) ex Kg
                            if regex_tipos_de_unidade_de_medidas:
                                unidade_de_medidas  = regex_tipos_de_unidade_de_medidas
                                #print("unidade_de_medidas",unidade_de_medidas)
                                unidade_de_medidas = unidade_de_medidas[-1][-1]
                                
                            #identifica o valor da unidade de medida ex 1,5
                            if regex_valor_unidade_medidas:
                                valor_unidade_de_medidas = regex_valor_unidade_medidas
                                #print("valor uni",valor_unidade_de_medidas)
                                valor_unidade_de_medidas = float(valor_unidade_de_medidas[-1].replace(',', '.'))
                            elif regex_valor_unidade_medidas_duas:
                                valor_unidade_de_medidas = regex_valor_unidade_medidas_duas
                                #print("valor_unidade_de_medidas:",valor_unidade_de_medidas)
                                valor_unidade_de_medidas = [float(parte) for parte in valor_unidade_de_medidas[0].split(' a ')]
                                valor_unidade_de_medidas = valor_unidade_de_medidas[-1]
                            else:
                                logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Não foi informado o tipo de unidade de medida.')
                            #Identifica SITUAÇAO MERCADO
                            if regex_sitacao_mercado:
                                situacao_mercado = regex_sitacao_mercado
                                #para obter o primeiro caso. Se tiver mais de um caso
                                situacao_mercado = situacao_mercado[0]
                            else:
                                situacao_mercado = 'não definida'
                                logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Não foi Informado a situação mercado.')
                            #Encontra campos que tem ',' significando que possuem preço ou porcentagem
                            if ',' in find_unidade:
                                #verifcia se tem valores
                                if len(regex_preco) == 0:
                                    total_valores = 0
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Não foi Informado os valores min, m_c_do_dia, max e var.')
                                    #print('total_valores:', total_valores)
                                #identfica o MIN
                                elif len(regex_preco) == 1:
                                    min = regex_preco[0]
                                    total_valores = min
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Não foi Informado os valores m_c_do_dia, max e var.')
                                #identifica o MIN e M_C DO DIA
                                elif len(regex_preco) == 2:
                                    min = regex_preco[0]
                                    m_c_do_dia = regex_preco[1]
                                    total_valores = min, m_c_do_dia
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Não foi Informado os valores max e var.')
                                #identifica o MIN, M_C DO DIA e MAX
                                elif len(regex_preco) == 3:
                                    min = regex_preco[0]
                                    m_c_do_dia = regex_preco[1]
                                    max = regex_preco[2]
                                    total_valores = min, m_c_do_dia, max
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Não foi Informado o valor var.')
                                #identifica o MIN, M_C DO DIA, MAX e M.C/DIA ANTERIOR
                                elif len(regex_preco) == 4:
                                    min = regex_preco[0]
                                    m_c_do_dia = regex_preco[1]
                                    max = regex_preco[2]
                                    m_c_dia_anterior = regex_preco[3]
                                    total_valores = min, m_c_do_dia, max, m_c_dia_anterior
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Todos os valores foram identificados.')
                                #identifica o MIN, M_C DO DIA, MAX, M.C/DIA ANTERIOR e VAR %
                                elif len(regex_preco) == 5:
                                    min = regex_preco[0]
                                    m_c_do_dia = regex_preco[1]
                                    max = regex_preco[2]
                                    m_c_dia_anterior = regex_preco[3]  
                                    var = regex_preco[4]
                                    total_valores = min, m_c_do_dia, max, m_c_dia_anterior, var
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Todos os valores foram identificados.')
                                if situacao_mercado:
                                    if len(regex_preco) == 6:
                                        min = regex_preco[0]
                                        m_c_do_dia = regex_preco[1]
                                        max = regex_preco[2]
                                        m_c_dia_anterior = regex_preco[3]  
                                        var = regex_preco[4] 
                                elif '2012' in data_numerica :  
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Arquivos do ano de 2012 com padrão de valores diferentes.')
                                    if len(regex_preco) == 6:
                                        min = regex_preco[1]
                                        m_c_do_dia = regex_preco[2]
                                        max = regex_preco[3]
                                        m_c_dia_anterior = regex_preco[4]  
                                        var = regex_preco[5]     
                                        logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Todos os valores foram identificados.')
                                    elif len(regex_preco) == 7:
                                        situacao_mercado = situacao_mercado
                                        min = regex_preco[1]
                                        m_c_do_dia = regex_preco[2]
                                        max = regex_preco[3]
                                        m_c_dia_anterior = regex_preco[4]  
                                        var = regex_preco[5]
                                        situacao_mercado = regex_preco[6]
                                        total_valores = min, m_c_do_dia, max, m_c_dia_anterior, var
                                        logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Todos os valores foram identificados.')
                                else:
                                    min = m_c_do_dia = max = m_c_dia_anterior = var = 0.00
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Não foi Informado os valores min, m_c_do_dia, max e var')
                                #Identifica quais SIGLAS tem (PROCENDENCIA)
                                if regex_estados_siglas:
                                    estados_siglas = regex_estados_siglas
                                    estados_siglas = ', '.join(estados_siglas)
                                #caso o campo sigla esteja 0,00 ocorre quando não se possui procedencia 
                                if str(i[-1]) == '0,00':
                                    estados_siglas = 'não informado'
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Procedencia não foi informada.')
                                else:
                                    logging.info(f'No Arquivo {arquivo}, no produto {produto} e tipo  {tipo_produto}. Procedencia não foi informada.')
                            #     #caso saia fora do padrão buscado ele prosseguir   
                            # else:                    
                            #     continue
                            
                            
                            produto = produto.upper()
                            tipo_produto = unidecode(tipo_produto).replace('"','').replace(',','')
                            
                            unidade_embalagem.lower()
                            str(situacao_mercado).upper()
                            estados_siglas.upper()
                            #para testes
                            #print(f"{produto}{tipo_produto}{unidade_embalagem}{valor_unidade_de_medidas}{unidade_de_medidas}{situacao_mercado}{min}{m_c_do_dia}{max}{m_c_dia_anterior}{estados_siglas}")
                            result = '+++','produto:', produto, type(produto) , 'tipo: ', tipo_produto, type(tipo_produto), 'unidade Emb: ',unidade_embalagem, type(unidade_embalagem),"Valor unidade de medida: ", valor_unidade_de_medidas, type(valor_unidade_de_medidas) ,"Unidade de medidas:", unidade_de_medidas, type(unidade_de_medidas), 'Situacao Mercado:',situacao_mercado, type(situacao_mercado), 'min: ', min, type(min), 'mc do dia: ', m_c_do_dia, type(m_c_do_dia), 'max: ', max, type(max),'M_C do dia Anterior: ', m_c_dia_anterior, type(m_c_dia_anterior), 'var: ', var, type(var),  'Procedencia: ', estados_siglas, type(estados_siglas),'Data: ', data_numerica
                            #print(f'valor fora: {result}')
                            if tipo_produto != '[]': 
                                print(result)
                                cursor.execute("INSERT INTO Produtos (data, produto, tipo, unidade_embalagem, valor_unidade_de_medidas, unidade_de_medidas, situacao_mercado, valor_min, valor_m_c_do_dia, valor_max, valor_variacao, estados_siglas, cidade) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)",(data_numerica, produto, tipo_produto, unidade_embalagem,valor_unidade_de_medidas, unidade_de_medidas, situacao_mercado, min, m_c_dia_anterior, max, var, estados_siglas,'LONDRINA'))
                        conn.commit()       
        else:
            logging.info(f'O arquivo {filename}, já foi adicionado!')
