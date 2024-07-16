import os
import re
import tabula
import sqlite3
from unidecode import unidecode
conn = sqlite3.connect('ceasa.db')
cursor = conn.cursor()
lista_produtos_comparar = ["AMEIXA", "LIMA PERSIA", 'GRAO DE BICO', "feijao", 'AMENDOIM', 'SALVIA', 'SALSINHA', 'SALSAO (AIPO)', 'MANJERONA', 'ESCAROLA/CHICORIA', 'COUVE MANTEIGA', 'COUVE CHINESA', 'COUVE BROCOLO', 'CHEIRO VERDE', 'ASPARGO', 'ALHO PORO', 'MANDIOQUINHA/BATATA SALSA','ALECRIM', 'CEBOLAO', "INHAME-TAIA",'AIPIM-MANDIOCA', 'ALHO IMPORTADO', 'ALHO NACIONAL', "PIMENTA","CAXI","Abacate Breda/Margarida", "Abacate Fucks/Geada", "Abacate Fortuna/Quintal", "Abacaxi Havai", "Abacaxi Perola","Abiu", "Acerola", "Ameixa Estrangeira", "Ameixa Nacional", "Amendoa", "Amora", "Atemoia", "Avela", "Banana Maca",
"Banana Nanica", "Banana Prata", "Caju", "Caqui", "Carambola", "Castanha Estrangeira", "Castanha Nacional","Cereja Estrangeira", "Cidra", "Coco Verde", "Cupuacu", "Damasco Estrangeiro", "Figo", "Framboesa", "Goiaba","Graviola", "Greap Fruit", "Jabuticaba", "Jaca", "Kiwi", "Laranja","Laranja Pera", "Lichia", "Lima da Persia", "LIMAO", "Limao Taiti", "Mamao", "Manga", "Mangostao", "Maracuja Azedo", "Maracuja Doce", "Marmelo", "Melancia", "Melao Amarelo","Mexerica", "Morango", "Nectarina Estrangeira", "Nectarina Nacional", "Nespera", "Nozes", "Pera Nacional", "Pera Estrangeira", "Pessego", "Pessego Nacional", "Pessego Estrangeiro", "Physalis", "Pinha", "Pitaia", "Quincam", "Roma", "Sapoti", "Seriguela", "Tamara", "Tamarindo", "Tangerina Cravo", "Tangerina Murcot", "Tangerina Poncam", "Uva Italia","Uva Niagara", "Uva Rubi", "Uva Thompson", "Uva Estrangeira", "Abobora D'Agua", "Abobora Japonesa", "Abobora Moranga","Abobora Paulista", "Abobora Seca", "Abobrinha Brasileira", "Abobrinha Italiana","Batata Doce",'BATATA YAKON', "Alcachofra", "Batata Doce Amarela", "Batata Doce Rosada", "Berinjela Comum", "Berinjela Conserva", "Berinjela Japonesa", "Beterraba", "Cara", "Cenoura",
"Chuchu", "Cogumelo", "Ervilha Comum", "Ervilha Torta", "Fava", "Feijao Corado", "Gengibre", "Inhame", "Jilo", "Mandioca", "Mandioquinha", "Maxixe", "Pepino Caipira", "Pepino Comum", "Pepino Japones", "Pimenta Cambuci",
"Pimenta Vermelha", "Pimentao Amarelo", "Pimentao Verde", "Pimentao Vermelho", "Quiabo", "Taquenoco", "Tomate","Tomate Caqui", "Tomate Salada", "Vagem", "Acelga", "Agriao", "Alface", "Alho Porro", "Almeirao", "Aspargos",
"Beterraba com Folhas", "Brocolis", "Catalonha", "Cebolinha", "Cenoura com Folhas", "Chicoria", "Coentro", "Couve","Couve Bruxelas", "Couve Flor", "Endivias", "Erva-Doce", "Escarola", "Espinafre", "Folha de Uva", "Gengibre com Folhas","Gobo", "Hortela", "Louro", "Manjericao", "Milho Verde", "Moiashi", "Mostarda", "Nabo", "Oregano", "Palmito", "Rabanete","Repolho", "Rucula", "Salsa", "Salsao", "Alho Nacional", "Alho Estrangeiro", "Amendoim com Casca", "Amendoim sem Casca","Batata Nacional", "Canjica", "Cebola Nacional", "Cebola MG", "Cebola SC", "Cebola SP", "Cebola Estrangeira", "Coco Seco","Milho Pipoca Nacional", "Milho Pipoca Estrangeiro", "Ovos Brancos", "Ovos de Codorna", "Ovos Vermelhos", "Pinhao",
"Agapanto", "Astromeria", "Angelica", "Anturio", "Azaleia", "Begonia", "Boca de Leao", "Branquinha", "Bromelia", "Ciclamem","Copo de Leite", "Cravina", "Crisantemo", "Dalia", "Dracena", "Estatice", "Estrelicia", "Eucalipto Simeria",
"Flor de Trigo", "Gerbera", "Gipysofila", "Girassol", "Gladíolo", "Goivo", "Grama", "Heleconia", "Hortencia", "Impatins","Jasmim", "Kalanchoe", "Lirio", "Lisianthus", "Mini Rosa", "Musgo Pequeno", "Orquidea", "Palmeira", "Petunia","Pingo de Ouro", "Primula", "Samambaia", "Tango", "Tuia", "Violeta", "Abrotea", "Agulhao", "Anchovas", "Atum","Bacalhau Seco", "Badejo", "Bagre", "Berbigao", "Betarra", "Bonito", "Cacao", "Camarao Cativeiro", "Camarao 7 Barbas","Cambeva", "Caranguejo", "Carapau", "Cascote", "Cavalinha", "Conglio", "Corvina", "Curimbeta", "Dourado", "Espada", "Galo","Garoupa", "Gordinho", "Guaivira", "Jundia", "Lambari", "Linguado", "Lula", "Mandi", "Manjuba", "Meca", "Merluza", "Mexilhao", "Mistura", "Namorado", "Olhete", "Olho de Boi", "Ostra", "Oveva", "Pacu", "Palombeta", "Pampo", "Papa Terra", "Parati", "Pargo", "Peroa", "Pescada", "Piau", "Pintado", "Piranha", "Pitangola", "Polvo", "Robalo", "Salmao", "Sardinha Fresca", "Savelha", "Serra", "Siri", "Sororoca", "Tainha", "Tilapia", "Traira", "Trilha", "Pescado", "Truta", "Tucunare", "Vira", 'ABACATE', 'ABACAXI', 'ABOBORA', 'ABOBRINHA', 'ALFACE', 'ALHO', 'BANANA', 'BATATA', 'BATATADOCE', 'BERINJELA', 'BETERRABA', 'BROCOLOS', 'CARA', 'CEBOLA', 'CENOURA', 'CHUCHU', 'COCO', 'COUVE', 'COUVE FLOR', 'GOIABA', 'INHAME', 'JILO', 'LARANJA', 'LIMAO', 'MACA IMPORTADA', 'MAMAO', 'MANDIOCA', 'MANDIOQUINHA', 'MANGA', 'MARACUJA', 'MELANCIA', 'MELAO', 'MILHO', 'MORANGO', 'OVO', 'PEPINO', 'PERA IMPORTADA', 'PERA NACIONAL', 'PIMENTAO', 'QUIABO', 'REPOLHO', 'TANGERINA', 'TOMATE', 'UVA', 'VAGEM']


#Lista das Siglas dos Estados e Paises que o brazil faz importação dos produtos
estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO", 'ARG', "CHN", "USA", "DEU", "JPN", "KOR", "MEX", "IND", "SAU", "CAN","ITA", "GBR", "ESP", "NLD", "BEL", "CHE", "SWE", "RUS","ZAF", "IDN", "TUR", "IRL", "POL", "THA", "SGP", "MYS", "EGY", "ARE", "CLILE", "CHL", "URU"]
#Dentro do campo "UNIDADE EMBALAGEM", tem esse capo que é a primeira opção, varia de documento para documento, exemplo os mais antigos normalmente usam nomes completos como "Caixa" 
unidades_de_embalagens = ["cx","CX","caixa","Caixa", "UN","Unidade","Kg","kg", "C1", "PT", "pt","Pcte", "CB", "SC", "MÇ", "mç", "mc" ,"Maço","maco", "Maco", "BJ", "bj", "DZ", "dz","Engr", "Dúzia", "Fardo", "Quilo", "Saco", "eg"]
#Campo situação do mercado-AUS=Produto indisponível no mercado
# -FRA=Mercado fraco: Quando o preço mais comum do dia é inferior ao do dia anterior
# -FIR=Mercado firme: Quando o preço mais comum do dia é superior ao do dia anterior.
# -EST=Mercado estável: Quando o preço mais comum do dia é igual ao anterior
situacoes_de_mercado = ["AUS", "FIR","Firme", "firme", "FRA","Fraco", "fraco", "EST", "Estável","Estavel", "estavel"]
# Lista de dias da semana em vários formatos
dias_da_semana = ["segunda-feira", "segunda","terça-feira", "terça","quarta-feira","quarta", "quinta-feira", "quinta", "sexta-feira", "sexta", "sábado","domingo"]
# Lista de meses em português
meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
cidades = ["Londrina", "Cascavel", "Foz do Iguaçu", "foz do iguacu", "Maringá","maringa", "Curitiba"]
meses_r = '|'.join(meses)
#lista para achar os produtos, fica fora do for para não zerar a cada interação
lista_produtos = []

#dia da semana
ano_obtido = 0
cidade = dia_da_semana  = ''

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
        print(f'Erro: {ve}')
        return []  # Retorna uma lista vazia se houver um erro de caminho
    except Exception as e:
        print(f'Ocorreu um erro inesperado: {e}')
        return []  # Retorna uma lista vazia se houver um erro inesperado

# Exemplo de uso
if __name__ == "__main__":
    caminho_da_pasta = 'C:/Users/joshu/OneDrive/Documentos/extracaoPdfTcc/baixados'  # caminho da pasta que está os arquivos
    
    # Chamando a função para obter a lista de arquivos
    lista_de_arquivos = listar_arquivos_em_pasta(caminho_da_pasta)
    
    # Imprimindo os arquivos encontrados
    print(f'Arquivos na pasta {caminho_da_pasta}:')
    contador = 0
    for arquivo in lista_de_arquivos:
        print('Arquivo executando: ',arquivo)
        filename = f'{caminho_da_pasta}/{arquivo}'
        print('nome arquivo: ', filename)
        
        #Lista dos Produtos para identificar seus tipos, exemplo 'ABACATE','ABACAXI', ...
        data = tabula.read_pdf(filename, multiple_tables=True, pages="all", stream=True, guess=False, encoding='latin-1')
        if data:
            for pag_num, df in enumerate(data, start=2):
                selected_data = df.values.tolist() #seleciona linhas
                #print('selecionar: ',selected_data)
                if len(selected_data) >= 1 :
                    for i in selected_data:
                        print('-'*50)
                        produto = tipo_produto = unidade_embalagem = unidade_de_medidas = situacao_mercado = estados_siglas= ''
                        valor_unidade_de_medidas = min = m_c_do_dia = max = m_c_dia_anterior = var = total_valores = 0
                        #identifica o tipo do 1º indice da  lista
                        tipo = type(i[0])
                        #Seleção da lista
                        find_unidade=str(i)
                        
                        
                        print('ai papai', find_unidade)
                        #print('pasou find', find_unidade)
                        # if find_unidade_nan:
                        #     find_unidade = find_unidade_nan
                        #     print('if FIND_UNIDADE_NAN', find_unidade) 
                        regex_cidades = re.findall(r'\b(' + '|'.join(cidades) + r')\b', find_unidade, re.IGNORECASE)
                        #print('regex_cidades',regex_cidades)
                        #identifica as datas 
                        regex_datas = re.findall(r'(?i)\b(?:segunda|terça|quarta|quinta|sexta|sábado|domingo)-feira,\s\d{1,2}\sde\s(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\sde\s\d{4}\b', find_unidade, re.IGNORECASE)
                        regex_tipo_mais_de_uma_palavra = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[a-zA-Z]+)*\b', find_unidade)
                        #print('antes FONTE:', find_unidade)
                        if 'FONTE:' in find_unidade or 'PRODUTOS AUSENTES' in find_unidade:
                            break
                        if regex_cidades:
                            cidade = regex_cidades[-1]
                        #print('REGEX_CIDADES:', find_unidade)
                        if regex_datas:
                            dia_da_semana = regex_datas
                            dia_da_semana = ''.join(dia_da_semana)
                            regex_ano = re.findall(r'\d{4}', dia_da_semana)
                            ano_obtido = regex_ano[-1]
                            ano_obtido = int(ano_obtido)
                            print('anoaa',regex_ano, 'confere', ano_obtido)
                    
                        #print('REGEX_DATAS:', find_unidade)
                        # if tipo is float:
                        #     continue
                        #print('FLOAT', find_unidade)
                        if 'Produto' in find_unidade or 'Centrais' in find_unidade or 'Mercado' in find_unidade:
                            continue
                        
                        if ano_obtido <= 2023:
                                                
                            if tipo is str and i[0].isupper(): #encontra str com letras maiusculas
                                produto = i[0]
                                lista_produtos.append(produto)
                                #print('>>>PRD', produto)       
                                if len(i) >= 2:
                                    tipo_produto = i[1]
                                    result = 'Produto: ', produto, 'tipo: ', tipo_produto  
                            if tipo is str and i[0].istitle() or regex_tipo_mais_de_uma_palavra:
                                tipo_produto = i[0]
                                
                                result = 'Produto: ', produto, 'tipo: ', tipo_produto  
                                #print('Entrou')
                                if lista_produtos:
                                    produto = lista_produtos[-1]
                            #print('abaixo if continue', find_unidade)
                            #caso o tipo_produto acima obtenha mais do que o necessario(ocorre em docs do ano de 2010)
                            if str(tipo_produto).count(" ") >= 4:
                                print('correção: ')
                                #para encontrar tipos, que vem antes de unidades de embalagem(cx, un...)    
                                regex_antes_unidade = re.findall(r'^(.*?)\s*(?:{})'.format('|'.join(re.escape(p) for p in unidades_de_embalagens)), find_unidade, re.IGNORECASE) 
                                if regex_antes_unidade:
                                    find_antes = regex_antes_unidade
                                    tipo_produto = str(find_antes).replace("[", "").replace('"','').replace(',','').replace(']','').replace("'","")
                        #caso especificos para obter produtos e tipos que ocorrem após o ano de 2024
                        elif ano_obtido >= 2024: 
                            
                            #verifica valores antes da unidade embalagem(cx...)
                            find_nan_inicio = find_unidade.replace('[','').replace(']','').replace("'",'').split(',')
                        #print('tests',find_nan_inicio)
                        #print(">>>>>>>>>", find_unidade)
                            #caso lista comece com nan
                            if lista_produtos:
                                #se o primeiro elemento da listar for nan, vali ser substituido pelo indice -1 da lista de
                                if 'nan' in find_nan_inicio[0]:
                                    find_unidade = find_unidade.replace('nan', f"'{lista_produtos[-1]}'", 1)
                            #para encontrar valores antes de unida de embalagens(cx, un...)
                            regex_antes_unidade = re.findall(r'^(.*?)\s*(?:{})'.format('|'.join(re.escape(p) for p in unidades_de_embalagens)), find_unidade, re.IGNORECASE)
                            #print('regex_antes_unidade', regex_antes_unidade)
                            regex_titulo = re.findall(r'^\[\'[\w\-\/�]+(?: [\w\-\/�]+)*\'(?:\s*,\s*nan)*\s*\]$', find_unidade, re.IGNORECASE)
                            #print('regex_titulo', regex_titulo)
                            fin_nan = re.search(r"^nan", find_unidade, re.IGNORECASE)
                            #print('fin_nan', fin_nan)
                            find_antes = str(regex_antes_unidade).replace("[","").replace("'","").replace(",","").replace("]","").replace('"', '').replace('nan','')
                            #print('antess:', regex_antes_unidade, find_unidade,'final: ', find_antes)
                            if find_antes or find_antes == 'nan':
                                tipo_produto = find_antes
                                #print("tipo: ",tipo_produto)
                                #print('antes')
                        
                            #print('fdfdf', produto)
                            if regex_titulo:
                                find_unidade = find_unidade.replace("[","").replace("'","").replace(",","").replace("]","").replace('"', '').replace("nan", '')
                                lista_produtos.append(find_unidade)
                                produto = lista_produtos[-1]
                                produto = str(produto)
                                #print('pord', produto)
                            

                            regex_produtos_comparar = re.findall(r'\b(' + '|'.join(lista_produtos_comparar) + r')\b', unidecode(find_antes), re.IGNORECASE)
                            if regex_produtos_comparar:
                                produto = str(regex_produtos_comparar).replace("[(", "").replace("'",'').replace(',','').replace(')]','')
                                lista_produtos.append(produto)
                        
                        
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
                        regex_tipos_de_unidade_de_medidas = re.findall(r'\b(\d*\.?\d+)\s*(kg|g|gr|kilo)\b', find_unidade, re.IGNORECASE) 
                        
                        #para identificar os preços(MIN/ M_C DO DIA/ MAX M>C/ DIA ANTERIOR/ VAR %)
                        regex_preco= re.findall(r'\b\d+,\d{2}\b', find_unidade)
                        #print('regex_prego', regex_preco, 'Length',len(regex_preco))
                        regex_produtos_2024= re.findall(r'^[A-Z]+(, "nan")+$', find_unidade, re.IGNORECASE)
                        
                        #verifica valores antes da unidade embalagem(cx...)
                        regex_antes_unidade = re.findall(r'^(.*?)\s*(?:{})'.format('|'.join(re.escape(p) for p in unidades_de_embalagens)), find_unidade, re.IGNORECASE)
                
                        tipo_antes_unidade = str(regex_antes_unidade).replace('[','').replace(']','').replace('"','').replace("'","").replace(',','')
                        
                        if type(tipo_produto) is str and len(tipo_produto) < len(tipo_antes_unidade):
                            tipo_produto = tipo_antes_unidade
                        
                        regex_produtos_comparar = re.findall(r'\b(' + '|'.join(lista_produtos_comparar) + r')\b', unidecode(find_unidade), re.IGNORECASE)
                        find_unidade_primeira_posicao = find_unidade.split()[0].replace("[","").replace("'", "").replace(",","")
                        #print('>>>>', find_unidade[0],'<<',find_unidade_primeira_posicao)
                        #print("comp::",regex_produtos_comparar)
                        #print('tte: ', find_unidade)
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
                        #Identifica SITUAÇAO MERCADO
                        if regex_sitacao_mercado:
                            situacao_mercado = regex_sitacao_mercado
                            #para obter o primeiro caso. Se tiver mais de um caso
                            situacao_mercado = situacao_mercado[0]
                        else:
                            situacao_mercado = 0
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
                            if situacao_mercado:
                                if len(regex_preco) == 6:
                                    min = regex_preco[0]
                                    m_c_do_dia = regex_preco[1]
                                    max = regex_preco[2]
                                    m_c_dia_anterior = regex_preco[3]  
                                    var = regex_preco[4] 
                            if '2012' in dia_da_semana:  
                                if len(regex_preco) == 6:
                                    min = regex_preco[1]
                                    m_c_do_dia = regex_preco[2]
                                    max = regex_preco[3]
                                    m_c_dia_anterior = regex_preco[4]  
                                    var = regex_preco[5]                          
                                elif len(regex_preco) == 6:
                                    situacao_mercado = situacao_mercado
                                    min = regex_preco[1]
                                    m_c_do_dia = regex_preco[2]
                                    max = regex_preco[3]
                                    m_c_dia_anterior = regex_preco[4]  
                                    var = regex_preco[5]
                                    total_valores = min, m_c_do_dia, max, m_c_dia_anterior, var
                                elif len(regex_preco) == 7:
                                    situacao_mercado = situacao_mercado
                                    min = regex_preco[1]
                                    m_c_do_dia = regex_preco[2]
                                    max = regex_preco[3]
                                    m_c_dia_anterior = regex_preco[4]  
                                    var = regex_preco[5]
                                    situacao_mercado = regex_preco[6]
                                    total_valores = min, m_c_do_dia, max, m_c_dia_anterior, var
                            #Identifica quais SIGLAS tem (PROCENDENCIA)
                            if regex_estados_siglas:
                                estados_siglas = regex_estados_siglas
                                estados_siglas = ', '.join(estados_siglas)
                            #caso o campo sigla esteja 0,00 ocorre quando não se possui procedencia 
                            if str(i[-1]) == '0,00':
                                estados_siglas = 'não informado'
                        #caso saia fora do padrão buscado ele prosseguir   
                        else:                    
                            continue
                        if lista_produtos:
                            produto = str(lista_produtos[-1])
                        #para testes
                        # result = '+++','cidade: ',cidade,'produto:', produto, type(produto) , 'tipo: ', tipo_produto, type(tipo_produto), 'unidade Emb: ',unidade_embalagem, type(unidade_embalagem),"Valor unidade de medida: ", valor_unidade_de_medidas, type(valor_unidade_de_medidas) ,"Unidade de medidas:", unidade_de_medidas, type(unidade_de_medidas), 'Situacao Mercado:',situacao_mercado, type(situacao_mercado), 'min: ', min, type(min), 'mc do dia: ', m_c_do_dia, type(m_c_do_dia), 'max: ', max, type(max),'M_C do dia Anterior: ', m_c_dia_anterior, type(m_c_dia_anterior), 'var: ', var, type(var),  'Procedencia: ', estados_siglas, type(estados_siglas),'Data: ', dia_da_semana
                        
                        if find_unidade[0] or tipo_produto: 
                            if unidade_embalagem or situacao_mercado or estados_siglas: 
                                #print(result)
                                cursor.execute("INSERT INTO Produtos (data, produto, tipo, unidade_embalagem, valor_unidade_de_medidas, unidade_de_medidas, situacao_mercado, valor_min, valor_m_c_do_dia, valor_max, valor_variacao, estados_siglas, cidade) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)",(dia_da_semana, produto, tipo_produto, unidade_embalagem, valor_unidade_de_medidas, unidade_de_medidas, situacao_mercado, min, m_c_dia_anterior, max, var, estados_siglas,'LONDRINA'))
                    conn.commit()
                    
