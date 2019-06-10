from faker import Faker
import db
import psycopg2 
import time
import random
from datetime import datetime  
from datetime import timedelta  

faker = Faker('pt_BR')
#É possivel ver que, os parametros de cada um dos metodos representam
# chaves estrangeiras para as outras entidades.
GlobalNumREG = 4
GlobalNumREGCONSUMIDOR = GlobalNumREG * 35

GlobalIcones = [
    'https://images.vexels.com/media/users/3/128437/isolated/preview/2dd809b7c15968cb7cc577b2cb49c84f-logotipo-de-restaurante-de-comida-de-pizza-by-vexels.png',
    'http://restaurantemarcos.hospedagemdesites.ws/site/wp-content/uploads/2019/04/logo2.fw_.png',
    'http://store.atendup.com.br/icones/mini/APP_ICON_2.png',
    'http://store.atendup.com.br/icones/mini/APP_ICON_3.png',
    'http://store.atendup.com.br/icones/mini/APP_ICON_4.png',
    'http://store.atendup.com.br/icones/mini/APP_ICON_5.png',
    'http://store.atendup.com.br/icones/mini/APP_ICON_6.png',
    'http://store.atendup.com.br/icones/mini/APP_ICON_7.png',
    'http://store.atendup.com.br/icones/mini/APP_ICON_8.png',
    'http://store.atendup.com.br/icones/APP_ICON_42.png'
  ]

#Secoes
Tradicionais = ["Don Bene", "Paulista", "Da Mama", "Dos Deuses", "Alho e Oleo", "Atum", "Catu-Atum", "Aliche", "Calabresa", "Baiana", "4 Queijos", "3 Queijos", "Muçarela", "Marguerita", "Portuguesa", "Caipira", "Bauru", "Siciliana", "Sertaneja", "Paito de Peru", "Peito de Peru EWspecial", "Champignon"]
Lights = ["Escarola", "Escarola com Aliche", "Brócolis", "Rucula", "Ao pesto", "Alcaparras", "Vegetariana"]
Doces = ["Banana", "Romeu e Julieta", "Brigadairo", "Prestigio", "Confeti", "Goiabada", "Leite Condesado"]
Bebidas = ["Coca-Cola", "Refrigerante 1L", "Refrigerante 2L", "Refrigerante 500ml", "lata", "Água", "Vinho Suave Mioranza", "Vinho Outros"]
Lanches = ["x-Tudo", "Hamburguer", "x-Salada", "x-EggBurguer", "x-Bacon", "x-EggBacon", "x-TudoDuplo"]
GlobalLista_Produtos = {}

GlobalLista_Produtos["Tradicionais"] = Tradicionais
GlobalLista_Produtos["Lights"] = Lights
GlobalLista_Produtos["Doces"] = Doces
GlobalLista_Produtos["Bebidas"] = Bebidas
GlobalLista_Produtos["Lanches"] = Lanches

# GERENCIA DO ESTABELECIMENTO #
def especialidade():
    lstEspecialidadeId = []
    try:
        listaEspecialidades = ["Pizza", "Lanches", "Japonesa", "Brasileira","Árabe", "Chinesa","Saudável","Bebidas", "Sorvete","Frutos do Mar", "Carnes", "Marmita","Açai", "Salgados", "Pastel"]
        INSERT_ESPECIALIDADE = " INSERT INTO ESPECIALIDADE (descricao) "

        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)  
        for _ in listaEspecialidades:
            
            try:
                values = str.format(" SELECT '{}' WHERE NOT EXISTS (SELECT DESCRICAO FROM ESPECIALIDADE WHERE DESCRICAO = '{}') ",_,_) 
                query = INSERT_ESPECIALIDADE + values
                cur = db.executar(conn,cur,query)[1]
                novoID = cur.fetchone()[0]                      
                lstEspecialidadeId.append(novoID)
                SCRIPT = query + '\n'        
                geraArquivoScript(SCRIPT)
            except:
                query = f"SELECT * FROM ESPECIALIDADE WHERE DESCRICAO LIKE '{_}'"
                cur = db.executar(conn,cur,query)[1]
                novoID = cur.fetchone()[0]
                lstEspecialidadeId.append(novoID)

        db.desconectarBanco(cur,conn)
        return lstEspecialidadeId
    except :
        print("Não foi possivel gerar seed especialidade")
        return 0

def endereco():
    lstEnderecoId = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)

        INSERT_ENDERECO = " INSERT INTO ENDERECO (bairro,cidade,uf,logradouro,cep,complemento,numero) VALUES "

        numEnd = GlobalNumREG
        indice = 0
        
        while indice < numEnd:            
            bairro = faker.bairro()
            bairro.replace("'","")
            cidade = faker.city()
            uf = faker.state_abbr()
            logradouro = faker.street_prefix() + " " + faker.street_name()
            cep =  faker.postcode()
            cep = cep.replace("-", "")
            complemento = faker.neighborhood() 
            numero = faker.building_number() + faker.building_number() 
            
            temp = str.format("('{}','{}','{}','{}','{}','{}',{}) RETURNING ID; ",bairro,cidade,uf,logradouro,cep,complemento, numero) 
            query = INSERT_ENDERECO + temp

            cur = db.executar(conn,cur,query)[1]
            novoID = cur.fetchone()[0]
            lstEnderecoId.append(novoID)

            SCRIPT = query + '\n'
            geraArquivoScript(SCRIPT)

            indice = indice + 1

        db.desconectarBanco(cur,conn)
        return lstEnderecoId

    except:
        print("Não foi possivel gerar seed enderecos")
        return 0

def usuarioDono():
    lstUsuarioDonoId = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)
        
        INSERT_USUARIO = " INSERT INTO USUARIO (EMAIL,UID,ENUMORIGEMCRIACAO,ATIVO) VALUES "

        numDonos = GlobalNumREG

        while numDonos > 0:            
            email = faker.free_email()
            uid = faker.password(length=29, special_chars=False, digits=True, upper_case=True, lower_case=True)
            enumorigemcriacao = 1
            ativo = "true"
            
            temp = str.format(" ('{}','{}',{},{}) RETURNING ID ",email,uid,enumorigemcriacao,ativo)
            query = INSERT_USUARIO + temp

            cur = db.executar(conn,cur,query)[1]
            novoID = cur.fetchone()[0]
            lstUsuarioDonoId.append(novoID)

            SCRIPT = query + '\n'
            geraArquivoScript(SCRIPT)

            numDonos = numDonos - 1
            
        db.desconectarBanco(cur,conn)
        return lstUsuarioDonoId
    except:
        print("Não foi possivel gerar seed usuario dono")
        return 0

def dono(lstUsuarioDonoId):
    lstDonoId = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)

        INSERT_DONO = ' INSERT INTO DONO (nome,sobrenome,datanascimento,cpf,rg,enumorgaoemissor,celular,"usuarioId") VALUES '

        numDono = GlobalNumREG
        
        while numDono > 0:            
            nome = faker.first_name()
            sobrenome = faker.last_name()
            datanascimento = faker.date(pattern="%d/%m/%Y", end_datetime=None)
            cpf = faker.cpf()
            cpf = cpf.replace(".","").replace("-","")
            rg =  faker.rg()
            enumorgaoemissor = 1
            celular = faker.cellphone_number()
            celular = celular.replace(" ","").replace("+","")
            
            temp = str.format("('{}','{}','{}','{}','{}',{},'{}',{}) RETURNING ID; ",nome,sobrenome,datanascimento,cpf,rg,enumorgaoemissor,celular,lstUsuarioDonoId[numDono-1]) 
            query = INSERT_DONO + temp

            cur = db.executar(conn,cur,query)[1]
            novoID = cur.fetchone()[0]
            lstDonoId.append(novoID)

            SCRIPT = query + '\n'
            geraArquivoScript(SCRIPT)

            numDono = numDono - 1

        db.desconectarBanco(cur,conn)
        return lstDonoId

    except:
        print("Não foi possivel gerar seed dono")
        return 0

def criaDono():
    try:
        #Primeiro é a criação do usuário do dono
        lstUsuarioDonoId = usuarioDono()
        lstDonoId = dono(lstUsuarioDonoId)
        return lstDonoId
    except:
        return 0

def cardapio():
    lstCardapioId = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)
        INSERT_CARDAPIO = " INSERT INTO CARDAPIO (descricao,ativo) VALUES "
        numCar = GlobalNumREG
        indice = 0
        
        while indice < numCar:            
            descricao = faker.catch_phrase()
            ativo = True

            temp = str.format("('{}',{}) RETURNING ID; ",descricao,ativo) 
            query = INSERT_CARDAPIO + temp
            
            cur = db.executar(conn,cur,query)[1]
            novoID = cur.fetchone()[0]
            lstCardapioId.append(novoID)

            SCRIPT = query + '\n'
            geraArquivoScript(SCRIPT)            
            indice = indice + 1

        db.desconectarBanco(cur,conn)
        return lstCardapioId
    except:
        print("Não foi possivel gerar seed cardapio")
        return 0

def estabelecimento(lstEspecialidadeId,lstEnderecoId,lstDonoId,lstCardapioId):
    lstEstabelecimentoId = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)

        INSERT_ESTABELECIMENTO = ' INSERT INTO ESTABELECIMENTO (razaosocial,cnpj,nome,descricao,horariofuncionamento,telefone,logo,avaliacaomedia,ativo,aberto,"especialidadeId","enderecoId","donoId","cardapioId") VALUES '

        numEst = GlobalNumREG
        indice = 0
        
        while numEst > indice :      
            razaosocial = faker.bs()
            cnpj = faker.cnpj()
            cnpj = cnpj.replace(".","").replace("/","").replace("-","")            
            nome  = faker.company()
            descricao = faker.catch_phrase()
            horariofuncionamento = ""
            telefone = faker.phone_number()[3:]
            telefone = telefone.replace(")","").replace("(","").replace(" ","").replace("-","").replace("+","")
            logo = GlobalIcones[random.randrange(0,9)]
            avaliacaomedia = 9.0
            ativo = True
            aberto = True
            dono = lstDonoId[indice]
            cardapio = lstCardapioId[indice]   
            endereco = lstEnderecoId[indice]
            especialidade = lstEspecialidadeId[random.randrange(0,14)]    
            
            temp = str.format("('{}','{}','{}','{}','{}','{}','{}',{},{},{},{},{},{},{}) RETURNING ID; ",razaosocial,cnpj,nome,descricao,horariofuncionamento,telefone,logo,avaliacaomedia,ativo,aberto,especialidade,endereco,dono,cardapio)
            query = INSERT_ESTABELECIMENTO + temp

            cur = db.executar(conn,cur,query)[1]
            novoID = cur.fetchone()[0]
            lstEstabelecimentoId.append(novoID)

            SCRIPT = query + '\n'
            geraArquivoScript(SCRIPT)
            indice = indice + 1

        db.desconectarBanco(cur,conn)
        return lstEstabelecimentoId
    except:
        print("Não foi possivel gerar seed estabelecimento")
        return 0
    
def secao(lstCardapioId):
    dicSecoes = {}
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)
        INSERT_SECAO = ' INSERT INTO SECAO (descricao,ativo, "cardapioId") VALUES '
        numSec = GlobalNumREG
        indice = 0

        while numSec > indice:
            lstSecoes = []
            idCardapio = lstCardapioId[indice]
            for sessao in GlobalLista_Produtos.keys():
                ativo = True

                temp = str.format("('{}',{}, {}) RETURNING ID; ",sessao,ativo,idCardapio) 
                query = INSERT_SECAO + temp
                
                cur = db.executar(conn,cur,query)[1]
                novoID = cur.fetchone()[0]
                lstSecoes.append(novoID)

                SCRIPT = query + '\n'
                geraArquivoScript(SCRIPT)            
            dicSecoes[idCardapio] = lstSecoes
            indice = indice + 1
        db.desconectarBanco(cur,conn)
        return dicSecoes
    except:
        print("Não foi possivel gerar seed cardapio")
        return [0]

def produto(dicSecoes):
    #dicSecoes - Chave é o IdCardapio e Valor é uma lista de Seções
    lstPrudutos = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)

        INSERT_PRODUTO = ' INSERT INTO PRODUTO (nome,descricao,preco,foto,empromocao,descontopromocional,ativo,tempopreparo, "estabelecimentoId", "secaoId") VALUES '
        for idCardapio in dicSecoes.keys():
            SELECT_ESTABELECIMENTO = str.format(" Select E.id from Cardapio C inner join Estabelecimento E on E.\"cardapioId\" = C.id and C.id = {} ", idCardapio)
            cur = db.executar(conn,cur,SELECT_ESTABELECIMENTO)[1]
            idEstabelecimento = cur.fetchone()[0]
            
            for sessao in dicSecoes[idCardapio]:
                SELECT_SECAO = str.format(" Select descricao from Secao where id = {} ", sessao)
                cur = db.executar(conn,cur,SELECT_SECAO)[1]
                descricaoSecao = str(cur.fetchone()[0])
                
                for produto in GlobalLista_Produtos[descricaoSecao]:
                    descricao = "Um produto muito gostoso"
                    preco = random.randrange(1,45)
                    foto = ""
                    empromocao = False
                    descontopromocional = 0
                    ativo = True
                    tempopreparo = random.randrange(10,50)
                    
                    temp = str.format("('{}','{}', {},'{}',{},{},{},{},{},{}) RETURNING ID; ",
                                            produto,descricao,preco,foto,empromocao,descontopromocional,ativo,tempopreparo, idEstabelecimento, sessao)
                    query = INSERT_PRODUTO + temp
                    
                    
                    cur = db.executar(conn,cur,query)[1]
                    novoID = cur.fetchone()[0]
                    lstPrudutos.append(novoID)

                    SCRIPT = query + '\n'
                    geraArquivoScript(SCRIPT)            
        db.desconectarBanco(cur,conn)
        return lstPrudutos
    except:
        print("Não foi possivel gerar seed produtos")
        return 0
    
def usuarioFuncionario():
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)
        
        INSERT_USUARIO = " INSERT INTO USUARIO (EMAIL,UID,ENUMORIGEMCRIACAO,ATIVO) VALUES "

        numFuncionarios = 10 #10 - DONOS

        while numFuncionarios > 0:            
            email = faker.free_email()
            uid = faker.password(length=29, special_chars=False, digits=True, upper_case=True, lower_case=True)
            enumorigemcriacao = 3
            ativo = "true"
            
            temp = str.format(" ('{}','{}',{},{}) RETURNING ID ",email,uid,enumorigemcriacao,ativo)
            query = INSERT_USUARIO + temp

            cur = db.executar(conn,cur,query)[1]
            novoID = cur.fetchone()[0]
            lstUsuarioDonoId.append(novoID)

            #SCRIPT = query + '\n'
            # geraArquivoScript(SCRIPT)
            numFuncionarios = numFuncionarios - 1
            
        db.desconectarBanco(cur,conn)
        return 
    except:
        print("Não foi possivel gerar seed usuario funcionario")

def mesa(lstEstabelecimentoId):
    lstMesaId = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)
        INSERT_MESA = " INSERT INTO MESA (numero,codigo,enumestadomesa,ativo,\"estabelecimentoId\") VALUES "
        
        for estabelecimento in lstEstabelecimentoId:
            numMesa = random.randint(1,10)
            indice = 0
            
            while indice < numMesa:            
                
                numero = faker.building_number() + faker.building_number()
                codigo = faker.ean8()
                enumestadomesa = 1
                ativo = True                

                temp = str.format("({},'{}',{},{},{}) RETURNING ID; ",numero,codigo,enumestadomesa,ativo,estabelecimento) 
                query = INSERT_MESA + temp
                
                cur = db.executar(conn,cur,query)[1]
                novoID = cur.fetchone()[0]
                lstMesaId.append(novoID)

                SCRIPT = query + '\n'
                geraArquivoScript(SCRIPT)            
                indice = indice + 1

        db.desconectarBanco(cur,conn)
        return lstMesaId
    except:
        print("Não foi possivel gerar seed mesa")
        return 0

def comanda(lstMesaId,lstConsumidorId):
    lstComanda = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)
        INSERT_COMANDA = " INSERT INTO COMANDA (horarioinicio,horariofim,enumsituacaocomanda,\"responsavelId\",\"mesaId\") VALUES "
        INSERT_COMANDA_CONSUMIDORES = " INSERT INTO comanda_consumidores_consumidor (\"comandaId\",\"consumidorId\") VALUES "
        
        numMesa = len(lstMesaId)
        indice = 0
        enumsituacaocomanda = 4
        #fazer um random para escolher o numero de responsaveis de uma mesa
        while indice < numMesa:
            for _ in range(random.randint(1,3)):
                consumidorId = lstConsumidorId[random.randint(0,len(lstConsumidorId)-1)]  

                addMinutes = random.randint(30,120)
                horarioinicio = faker.date_time_between(start_date="-5y",end_date = datetime.today()-timedelta(days=1))
                horariofim = horarioinicio + timedelta(minutes=addMinutes)

                horarioinicio = datetime.isoformat(horarioinicio)
                horariofim = datetime.isoformat(horariofim)
                                
                temp = str.format("('{}','{}',{},{},{}) RETURNING ID; ",horarioinicio,horariofim,enumsituacaocomanda,consumidorId,lstMesaId[indice]) 
                query = INSERT_COMANDA + temp
                
                cur = db.executar(conn,cur,query)[1]
                novoID = cur.fetchone()[0]
                lstComanda.append(novoID)

                SCRIPT = query + '\n'
                geraArquivoScript(SCRIPT)   
                 

                #outros consumidores na comanda:
                tempConsumidores = [consumidorId]
                while len(tempConsumidores) < 3:
                    x = lstConsumidorId[random.randint(0,len(lstConsumidorId)-1)]  
                    if (x not in tempConsumidores):
                        tempConsumidores.append(x)                    
                
                for consumidor in range(3):
                    temp = str.format("({},{})  ",novoID,tempConsumidores[consumidor])
                    query = INSERT_COMANDA_CONSUMIDORES + temp
                    print(query)   
                    cur = db.executar(conn,cur,query)[1] 
                    

                    SCRIPT = query + '\n'
                    geraArquivoScript(SCRIPT)   
                        
            indice = indice + 1
        db.desconectarBanco(cur,conn)
        return lstComanda
    except:
        print("Não foi possivel gerar seed comanda")
        return 0

def pedido():
    return

def item():
    return

def conta():
    return

def plano():
    return

# GERENCIA DO CLIENTE  

def usuarioConsumidor():
    lstUsuarioConsumidor = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)
        
        INSERT_USUARIO = " INSERT INTO USUARIO (EMAIL,UID,ENUMORIGEMCRIACAO,ATIVO) VALUES "

        numConsumidores = GlobalNumREGCONSUMIDOR

        while numConsumidores > 0:            
            email = faker.free_email()
            uid = faker.password(length=29, special_chars=False, digits=True, upper_case=True, lower_case=True)
            enumorigemcriacao = 2
            ativo = "true"
            
            temp = str.format(" ('{}','{}',{},{}) RETURNING ID ",email,uid,enumorigemcriacao,ativo)
            query = INSERT_USUARIO + temp

            cur = db.executar(conn,cur,query)[1]
            novoID = cur.fetchone()[0]
            lstUsuarioConsumidor.append(novoID)

            SCRIPT = query + '\n'
            geraArquivoScript(SCRIPT)

            numConsumidores = numConsumidores - 1
            
        db.desconectarBanco(cur,conn)
        return lstUsuarioConsumidor
    except:
        print("Não foi possivel gerar seed usuario consumidor")
        return 0

def consumidor(lstUsuarioConsumidor):
    lstConsumidorId = []
    try:
        conn = db.connectarBanco()
        cur = db.gerarCursor(conn)

        INSERT_CONSUMIDOR = ' INSERT INTO CONSUMIDOR (nome,datanascimento,celular,"usuarioId") VALUES '

        numConsumidor = GlobalNumREGCONSUMIDOR
        
        while numConsumidor > 0:            
            nome = faker.first_name() + ' ' + faker.last_name()
            datanascimento = faker.date(pattern="%d/%m/%Y", end_datetime=None)
            celular = faker.cellphone_number()
            celular = celular.replace(" ","").replace("+","")[2:]
            
            temp = str.format("('{}','{}','{}',{}) RETURNING ID; ",nome,datanascimento,celular,lstUsuarioConsumidor[numConsumidor-1]) 
            query = INSERT_CONSUMIDOR + temp
            
            cur = db.executar(conn,cur,query)[1]
            novoID = cur.fetchone()[0]
            lstConsumidorId.append(novoID)

            SCRIPT = query + '\n'
            geraArquivoScript(SCRIPT)

            numConsumidor = numConsumidor - 1

        db.desconectarBanco(cur,conn)
        return lstConsumidorId

    except:
        print("Não foi possivel gerar seed consumidor")
        return 0

def criaConsumidor():
    try:
        #Primeiro é a criação do usuário do Consumidor
        lstUsuarioConsumidor = usuarioConsumidor()
        lstConsumidorId = consumidor(lstUsuarioConsumidor)
        return lstConsumidorId
    except:
        return 0

def geraArquivoScript(script):
    # f = open("script_seed.sql", "a+")
    # f.write(script)
    # f.close()
    return 0