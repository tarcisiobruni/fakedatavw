import seed
import threading
import time

def start():
    lstEspecialidadeId = seed.especialidade()
    lstEnderecoId = seed.endereco()
    lstDonoId = seed.criaDono()
    lstCardapioId = seed.cardapio()
    lstEstabelecimentoId = seed.estabelecimento(lstEspecialidadeId,lstEnderecoId,lstDonoId,lstCardapioId)    
    dicSecoes = seed.secao(lstCardapioId)
    lstProdutosId = seed.produto(dicSecoes)
    lstMesaId = seed.mesa(lstEstabelecimentoId)
    lstConsumidorId = seed.criaConsumidor()
    lstComandaId = seed.comanda(lstMesaId,lstConsumidorId)
    lstPedidos = seed.pedido(lstComandaId)
    lstPlanos = seed.plano()
    
    return 0

def main():    
    start()
    return 0

    
if __name__ == "__main__":
    main()