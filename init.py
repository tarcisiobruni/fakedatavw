import seed
import threading
import time

def start():
    lstEspecialidadeId = seed.especialidade()
    lstEnderecoId = seed.endereco()
    lstDonoId = seed.criaDono()
    lstCardapioId = seed.cardapio()
    lstEstabelecimentoId = seed.estabelecimento(lstEspecialidadeId,lstEnderecoId,lstDonoId,lstCardapioId)    
    dicSecao = seed.secao(lstCardapioId)
    lstProdutoId = seed.produto(dicSecao)
    lstMesaId = seed.mesa(lstEstabelecimentoId)
    lstConsumidorId = seed.criaConsumidor()
    lstComandaId = seed.comanda(lstMesaId,lstConsumidorId)
    lstPedidoId = seed.pedido(lstComandaId)
    lstPlanoId = seed.plano()
    lstItemId = seed.item(lstPedidoId)
    seed.conta()

    return 0

def main():    
    start()
    return 0

    
if __name__ == "__main__":
    main()