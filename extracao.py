import re
import tabula
import sqlite3
banco = sqlite3.connect('CEASA.db')
#para conseguir dar comandos sql
cursor = banco.cursor()
filename = "janeiro02012023_1.pdf"
filename2 = "fevereiro08022023.pdf"
filename3 = "janeiro032011.pdf"
filename4 = "janeiro31012024.pdf" 
filename5 = "Dezembro302014.pdf"

#Lista das Siglas dos Estados e Paises que o brazil faz importação dos produtos
estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO", 'ARG', "CHN", "USA", "DEU", "JPN", "KOR", "MEX", "IND", "SAU", "CAN","ITA", "GBR", "ESP", "NLD", "BEL", "CHE", "SWE", "RUS","ZAF", "IDN", "TUR", "IRL", "POL", "THA", "SGP", "MYS", "EGY", "ARE", "CLILE", "CHL", "URU"]
#Dentro do campo "UNIDADE EMBALAGEM", tem esse capo que é a primeira opção, varia de documento para documento, exemplo os mais antigos normalmente usam nomes completos como "Caixa" 
unidades_de_embalagens = ["CX","Caixa", "UN","Unidade","Kg", "C1", "PT","Pcte", "CB", "SC", "MÇ","Maço", "BJ", "DZ","Engr", "Dúzia", "Fardo", "Quilo", "Saco"]
#Campo situação do mercado-AUS=Produto indisponível no mercado
# -FRA=Mercado fraco: Quando o preço mais comum do dia é inferior ao do dia anterior
# -FIR=Mercado firme: Quando o preço mais comum do dia é superior ao do dia anterior.
# -EST=Mercado estável: Quando o preço mais comum do dia é igual ao anterior
situacoes_de_mercado = ["AUS", "FIR","Firme", "FRA","Fraco", "EST", "Estável","Estavel"]
#Lista dos possiveis tipos de unidade de medida
medicoes = ["Kg","g", "gr","Un"]
# Lista de dias da semana em vários formatos
dias_da_semana = ["segunda-feira", "segunda","terça-feira", "terça","quarta-feira","quarta", "quinta-feira", "quinta", "sexta-feira", "sexta", "sábado","domingo"]
# Lista de meses em português
meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
cidades = ["Londrina", "Cascavel", "Foz do Iguaçu", "Maringá", "Curitiba"]
meses_r = '|'.join(meses)
#lista para achar os produtos, fica fora do for para não zerar a cada interação
lista_produtos = []
#dia da semana

cidade = data_dia_mes_ano  = ''
#Lista dos Produtos para identificar seus tipos, exemplo 'ABACATE','ABACAXI', ...




data = tabula.read_pdf(filename5, multiple_tables=True, pages="all", stream=True, guess=False, encoding='latin-1')
if data:
    for pag_num, df in enumerate(data, start=2):
        selected_data = df.values.tolist() #seleciona linhas
        if len(selected_data) >= 1 :
            for i in selected_data:
                produto = tipo_produto = unidade_embalagem = unidade_de_medidas = situacao_mercado = estados_siglas= ''
                valor_unidade_de_medidas = min = m_c_do_dia = max = m_c_dia_anterior = var = total_valores = 0
                #identifica o tipo do 1º indice da  lista
                tipo = type(i[0])
                #Seleção da lista
                find_unidade=str(i)
                #para saber qual linha está sendo obtida
                #print('>>>>', find_unidade)
            #Parte dos Regexs
                regex_cidades = re.findall(r'\b(' + '|'.join(cidades) + r')\b', find_unidade, re.IGNORECASE)
                #identifica as datas 
                regex_datas = re.findall(r'(?i)\b(?:segunda|terça|quarta|quinta|sexta|sábado|domingo)-feira,\s\d{1,2}\sde\s(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\sde\s\d{4}\b', find_unidade, re.IGNORECASE)
                #identifica quando o produto ou variedade tiver mais de uma palavra
                regex_tipo_mais_de_uma_palavra = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[a-zA-Z]+)*\b', find_unidade)
                #para identificar as Siglas da PROCEDENCIA, como estados e países
                regex_estados_siglas = re.findall(r'\b(' + '|'.join(estados) + r')\b', find_unidade, re.IGNORECASE)
                #para identificar SITUACAO MERCADO
                regex_sitacao_mercado = re.findall(r'\b(' + '|'.join(situacoes_de_mercado) + r')\b', find_unidade, re.IGNORECASE)
                #para identificar o tipo da UNIDADE EMBALAGEM
                regex_unidade_embalagem_tipo = re.search(r'\b(' + '|'.join(unidades_de_embalagens) + r')\d*\b', find_unidade, re.IGNORECASE)
                #para identificar o valor da medida(UNIDADE EMBALAGEM)
                regex_valor_unidade_medidas = re.findall(r'(\d+[.,]?\d*)\s*(?=Kg|g|un|Dz|gr)', find_unidade, re.IGNORECASE)
                regex_valor_unidade_medidas_duas = re.findall(r'(\d[\d,.]*\s+a\s+\d[\d,.]*)', find_unidade, re.IGNORECASE)
                #para identificar o tipo da medida(UNIDADE EMBALAGEM)ex: KG
                regex_tipos_de_unidade_de_medidas = re.findall(r'\b(' + '|'.join(medicoes) + r')\b', find_unidade, re.IGNORECASE) 
                #para identificar os preços(MIN/ M_C DO DIA/ MAX M>C/ DIA ANTERIOR/ VAR %)
                regex_preco= re.findall(r'-?\d{1,3}(?:\.\d{3})*(?:,\d{2})'
            , find_unidade)
                
               
                #print(type(i[2]),'type', i[2])
                #print('+Valor bruto :',find_unidade, 'tamanho: ', len(i),'tipo', type([i]),'listaa: ', i)

                if 'FONTE:' in find_unidade or 'PRODUTOS AUSENTES' in find_unidade:
                    break
                if regex_cidades:
                    cidade = regex_cidades[-1]
                    
                if regex_datas:
                    dia_da_semana = regex_datas
                    dia_da_semana = ''.join(dia_da_semana)
                
                if tipo is float:
                    continue
                if tipo is float or 'PRODUTO' in find_unidade or 'Outras' in find_unidade or 'FRUTAS' in find_unidade:
                    continue
                
                if tipo is str and i[0].isupper(): #encontra str com letras maiusculas
                    
                    produto = i[0]
                    lista_produtos.append(produto)
                    #para entender qual o PRODUTO está sendo usado
                    #print('>>>PRD', produto)       
                    if len(i) >= 2:
                        tipo_produto = i[1]
                        result = 'Produto: ', produto, 'tipo: ', tipo_produto  
                if tipo is str and i[0].istitle() or regex_tipo_mais_de_uma_palavra:
                    tipo_produto = i[0]
                    tipo_produto_corrigida = tipo_produto#.encode('cp1252', errors='replace').decode('cp1252', 'replace').replace('?', '-')
                    #para só aparecer se tiver algum item na lista de produtos
                    result = 'Produto: ', produto, 'tipo: ', tipo_produto  
                    #print('Entrou')
                    if lista_produtos:
                        produto = lista_produtos[-1]
                #identifica tipo da embalagem(UNIDADE EMBALAGEM) ex:CX
                if regex_unidade_embalagem_tipo:
                    unidade_embalagem = regex_unidade_embalagem_tipo
                    #Caso tenha duas ocorrencias ex: 2 SC ele obtem apenas o 1º
                    unidade_embalagem= unidade_embalagem.group(1)
                else:
                    unidade_embalagem = 'não possui Unidade'
                #identifica o Tipo da unidade de medida (UNIDADE EMBALAGEM) ex Kg
                if regex_tipos_de_unidade_de_medidas:
                    unidade_de_medidas  = regex_tipos_de_unidade_de_medidas
                    unidade_de_medidas = unidade_de_medidas[-1]
                #identifica o valor da unidade de medida ex 1,5
                if regex_valor_unidade_medidas:
                    valor_unidade_de_medidas = regex_valor_unidade_medidas
                    valor_unidade_de_medidas = float(valor_unidade_de_medidas[0].replace(',', '.'))
                elif regex_valor_unidade_medidas_duas:
                    valor_unidade_de_medidas = regex_valor_unidade_medidas_duas
                    valor_unidade_de_medidas = [float(parte) for parte in valor_unidade_de_medidas[0].split(' a ')]
                    valor_unidade_de_medidas = valor_unidade_de_medidas[-1]
                #Identifica SITUAÇAO MERCADO
                if regex_sitacao_mercado:
                    situacao_mercado = regex_sitacao_mercado
                    #para obter o primeiro caso. Se tiver mais de um caso
                    situacao_mercado = situacao_mercado[0]
                #Encontra campos que tem ',' significando que possuem preço ou porcentagem
                if ',' in find_unidade:
                    #verifcia se tem valores
                    if len(regex_preco) == 0:
                        total_valores = 0
                    #identfica o MIN
                    elif len(regex_preco) == 1:
                        min = regex_preco[0]
                        total_valores = min
                    #identifica o MIN e M_C DO DIA
                    elif len(regex_preco) == 2:
                        min = regex_preco[0]
                        m_c_do_dia = regex_preco[1]
                        total_valores = min, m_c_do_dia
                    #identifica o MIN, M_C DO DIA e MAX
                    elif len(regex_preco) == 3:
                        min = regex_preco[0]
                        m_c_do_dia = regex_preco[1]
                        max = regex_preco[2]
                        total_valores = min, m_c_do_dia, max
                    #identifica o MIN, M_C DO DIA, MAX e M.C/DIA ANTERIOR
                    elif len(regex_preco) == 4:
                        min = regex_preco[0]
                        m_c_do_dia = regex_preco[1]
                        max = regex_preco[2]
                        m_c_dia_anterior = regex_preco[3]
                        total_valores = min, m_c_do_dia, max, m_c_dia_anterior
                    #identifica o MIN, M_C DO DIA, MAX, M.C/DIA ANTERIOR e VAR %
                    elif len(regex_preco) == 5:
                        min = regex_preco[0]
                        m_c_do_dia = regex_preco[1]
                        max = regex_preco[2]
                        m_c_dia_anterior = regex_preco[3]  
                        var = regex_preco[4]
                        total_valores = min, m_c_do_dia, max, m_c_dia_anterior, var
                    #Identifica quais SIGLAS tem (PROCENDENCIA)
                    if regex_estados_siglas:
                        estados_siglas = regex_estados_siglas
                        estados_siglas = ', '.join(estados_siglas)
                #caso saia fora do padrão buscado ele prosseguir   
                else:
                    continue
                #para ver dados obtidos de forma organizada
                result = '+++','Cidade: ', cidade,'dia da semana: ', dia_da_semana, type(dia_da_semana),'produto:', produto, type(produto) , 'tipo: ', tipo_produto, type(tipo_produto), 'unidade Emb: ',unidade_embalagem, type(unidade_embalagem),"Valor unidade de medida: ", valor_unidade_de_medidas, type(valor_unidade_de_medidas) ,"Unidade de medidas:", unidade_de_medidas, type(unidade_de_medidas), 'Situacao Mercado:',situacao_mercado, type(situacao_mercado), 'min: ', min, type(min), 'mc do dia: ', m_c_dia_anterior, type(m_c_dia_anterior), 'max: ', max, type(max), 'var: ', var, type(var), 'Procedencia: ', estados_siglas, type(estados_siglas)
                if find_unidade[0] and unidade_embalagem != 'não possui Unidade' and regex_sitacao_mercado:
                    #print('test')
                    print(result)
                    #aqui é para adicionar no banco de dados
                    #cursor.execute("INSERT INTO Produtos (data, produto, tipo, unidade_embalagem, valor_unidade_de_medidas, unidade_de_medidas, situacao_mercado, valor_min, valor_m_c_do_dia, valor_max, valor_variacao, estados_siglas) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(dia_da_semana, produto, tipo_produto, unidade_embalagem, valor_unidade_de_medidas, unidade_de_medidas, situacao_mercado, min, m_c_dia_anterior, max, var, estados_siglas))
                    #banco.commit()
                    #print('Foi!!!')

                    
    else:
        print('Nenhuma Pag a mais')