import psycopg2

def desconectarBanco(cur,conn):
    try:
        cur.close()
        conn.close()
    except:
        print("Não foi possivel fechar a connexão")

def executar(conn,cur,query):
    cur.execute(query)
    conn.commit()
    return conn,cur

def gerarCursor(conn):
    try:
        cur = conn.cursor()
        return cur
    except:
        print("Não foi possivel gerar o cursor")

def connectarBanco():
    try:
        conn = psycopg2.connect("dbname='virtualback' user='postgres' password='admin' host='localhost' ")
        return conn
    except:
        print("Nao foi possivel conectar no Banco de Dados")