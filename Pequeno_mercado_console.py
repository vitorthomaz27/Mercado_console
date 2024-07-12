from abc import ABC, abstractmethod
from typing import List, Dict

# Classe Produto
class Produto:
    # Classe que representa um produto no mercado.
    def __init__(self, nome: str, preco: float, quantidade: int):
        self._nome = nome  # Nome do produto (privado)
        self._preco = preco  # Preço do produto (privado)
        self._quantidade = quantidade  # Quantidade em estoque (privado)

    @property
    def nome(self) -> str:
        return self._nome  # Getter para o nome do produto

    @property
    def preco(self) -> float:
        return self._preco  # Getter para o preço do produto

    @property
    def quantidade(self) -> int:
        return self._quantidade  # Getter para a quantidade do produto

    @quantidade.setter
    def quantidade(self, quantidade: int):
        self._quantidade = quantidade  # Setter para a quantidade do produto

    def __str__(self) -> str:
        return f"Produto: {self.nome}, Preço: R${self.preco:.2f}, Quantidade em estoque: {self.quantidade}"

# Classe abstrata Usuario
class Usuario(ABC):
    # Classe abstrata que representa um usuário do sistema.
    def __init__(self, nome: str):
        self._nome = nome  # Nome do usuário (privado)

    @property
    def nome(self) -> str:
        return self._nome  # Getter para o nome do usuário

    @abstractmethod
    def tipo_usuario(self) -> str:
        pass  # Método abstrato para retornar o tipo de usuário

# Classe Dono, herda de Usuario
class Dono(Usuario):
    # Classe que representa o dono do mercado, herdando de Usuario.
    def tipo_usuario(self) -> str:
        return "Dono"  # Retorna o tipo de usuário como "Dono"

    def adicionar_produto(self, mercado, nome: str, preco: float, quantidade: int):
        # Adiciona um novo produto ao mercado.
        novo_produto = Produto(nome, preco, quantidade)  # Cria um novo produto
        mercado.adicionar_produto(novo_produto)  # Adiciona o produto ao mercado
        print(f"{self.nome}, produto {nome} adicionado com sucesso!")  # Mensagem de sucesso

# Classe Cliente, herda de Usuario
class Cliente(Usuario):
    # Classe que representa um cliente do mercado, herdando de Usuario.
    def tipo_usuario(self) -> str:
        return "Cliente"  # Retorna o tipo de usuário como "Cliente"

    def fazer_pedido(self, mercado, produtos: Dict[str, int], endereco: str):
        # Realiza um pedido no mercado.
        itens_pedido = []  # Lista para armazenar itens do pedido
        indisponiveis = []  # Lista para armazenar produtos indisponíveis

        # Verifica a disponibilidade dos produtos no estoque.
        for nome_produto, qtd_desejada in produtos.items():
            produto_encontrado = next((p for p in mercado.produtos if p.nome == nome_produto), None)
            if produto_encontrado:
                if produto_encontrado.quantidade >= qtd_desejada:
                    itens_pedido.append((produto_encontrado, qtd_desejada))  # Adiciona produto ao pedido
                else:
                    indisponiveis.append((produto_encontrado, produto_encontrado.quantidade))  # Adiciona produto indisponível
            else:
                indisponiveis.append((Produto(nome_produto, 0, 0), 0))  # Adiciona produto não encontrado

        # Processa o pedido se houver produtos disponíveis.
        if itens_pedido:
            novo_pedido = Pedido(self, itens_pedido, endereco)  # Cria um novo pedido
            mercado.adicionar_pedido(novo_pedido)  # Adiciona o pedido ao mercado
            mercado.atualizar_estoque(itens_pedido)  # Atualiza o estoque dos produtos
            print(f"Pedido realizado com sucesso para {self.nome}! Será entregue em {endereco}")  # Mensagem de sucesso
            print(f"Valor total: R${novo_pedido.calcular_total():.2f}")  # Mostra o valor total do pedido
            print(f"Itens: {', '.join(f'{item[0].nome} (Qtd: {item[1]})' for item in itens_pedido)}")  # Lista os itens do pedido
        else:
            print("Nenhum produto encontrado para o pedido.")  # Mensagem caso nenhum produto esteja disponível

        # Informa sobre produtos indisponíveis.
        if indisponiveis:
            print("Os seguintes itens não estão disponíveis na quantidade desejada:")
            for item, qtd_disp in indisponiveis:
                if qtd_disp == 0:
                    print(f"{item.nome}: Produto não encontrado")  # Produto não encontrado
                else:
                    print(f"{item.nome}: Quantidade disponível: {qtd_disp}")  # Quantidade disponível do produto

# Classe Pedido
class Pedido:
    # Classe que representa um pedido feito por um cliente.
    def __init__(self, cliente: Cliente, itens: List[tuple], endereco: str):
        self._cliente = cliente  # Cliente que fez o pedido (privado)
        self._itens = itens  # Lista de tuplas (Produto, quantidade) (privado)
        self._endereco = endereco  # Endereço de entrega (privado)

    @property
    def cliente(self) -> Cliente:
        return self._cliente  # Getter para o cliente do pedido

    @property
    def itens(self) -> List[tuple]:
        return self._itens  # Getter para os itens do pedido

    @property
    def endereco(self) -> str:
        return self._endereco  # Getter para o endereço do pedido

    def calcular_total(self) -> float:
        # Calcula o valor total do pedido.
        return sum(item[0].preco * item[1] for item in self.itens)  # Soma dos preços dos produtos multiplicados pela quantidade

    def __str__(self) -> str:
        itens_str = ", ".join([f"{item[0].nome} (Qtd: {item[1]})" for item in self.itens])  # Converte itens para string
        return f"Pedido de {self.cliente.nome}: {itens_str}, Entregar em: {self.endereco}, Valor total: R${self.calcular_total():.2f}"  # Representação do pedido como string

# Classe Mercado
class Mercado:
    # Classe que representa o mercado, contendo produtos e pedidos.
    def __init__(self):
        self._produtos: List[Produto] = []  # Lista de produtos no mercado (privada)
        self._pedidos: List[Pedido] = []  # Lista de pedidos feitos no mercado (privada)

    @property
    def produtos(self) -> List[Produto]:
        return self._produtos  # Getter para a lista de produtos

    @property
    def pedidos(self) -> List[Pedido]:
        return self._pedidos  # Getter para a lista de pedidos

    def adicionar_produto(self, produto: Produto):
        # Adiciona um produto ao mercado.
        self.produtos.append(produto)  # Adiciona o produto à lista de produtos

    def adicionar_pedido(self, pedido: Pedido):
        # Adiciona um pedido ao mercado.
        self.pedidos.append(pedido)  # Adiciona o pedido à lista de pedidos

    def listar_produtos(self):
        # Lista todos os produtos disponíveis no mercado.
        for produto in self.produtos:
            print(produto)  # Imprime as informações de cada produto

    def listar_pedidos(self):
        # Lista todos os pedidos feitos no mercado.
        for pedido in self.pedidos:
            print(pedido)  # Imprime as informações de cada pedido

    def atualizar_estoque(self, itens_pedido: List[tuple]):
        # Atualiza o estoque dos produtos com base nos itens de um pedido.
        for produto, qtd in itens_pedido:
            produto_encontrado = next((p for p in self.produtos if p.nome == produto.nome), None)
            if produto_encontrado:
                produto_encontrado.quantidade -= qtd  # Atualiza a quantidade do produto no estoque

# Função principal
def main():
    # Função principal que gerencia o fluxo do programa.
    mercado = Mercado()  # Cria uma instância de Mercado

    while True:
        print("Bem vindo ao Mercado do Vitor!")
        print("1. Acessar como Dono da Loja")
        print("2. Acessar como Cliente")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")
        #Para acessar como dono, usuário: "@dono" e senha "123456"
        if opcao == "1":
            usuario = input("Digite o usuário: ")
            senha = input("Digite a senha: ")
            if usuario == "@dono" and senha == "123456":
                nome_dono = input("Digite o seu nome: ")
                dono = Dono(nome_dono)  # Cria uma instância de Dono
                while True:
                    print("\nOpções do Dono:")
                    print("1. Adicionar Produto")
                    print("2. Listar Produtos")
                    print("3. Voltar")
                    opcao_dono = input("Escolha uma opção: ")

                    if opcao_dono == "1":
                        nome_produto = input("Digite o nome do produto: ")
                        preco_produto = float(input("Digite o preço do produto: "))
                        quantidade_produto = int(input("Digite a quantidade do produto: "))
                        dono.adicionar_produto(mercado, nome_produto, preco_produto, quantidade_produto)  # Adiciona um produto ao mercado
                    elif opcao_dono == "2":
                        mercado.listar_produtos()  # Lista todos os produtos
                    elif opcao_dono == "3":
                        break  # Volta ao menu principal
                    else:
                        print("Opção inválida. Tente novamente.")  # Mensagem de erro para opção inválida
            else:
                print("Usuário ou senha incorretos. Tente novamente.")  # Mensagem de erro para login inválido

        elif opcao == "2":
            nome_cliente = input("Digite o seu nome: ")
            cliente = Cliente(nome_cliente)  # Cria uma instância de Cliente
            while True:
                print("\nOpções do Cliente:")
                print("1. Fazer Pedido")
                print("2. Listar Produtos")
                print("3. Voltar")
                opcao_cliente = input("Escolha uma opção: ")

                if opcao_cliente == "1":
                    mercado.listar_produtos()  # Lista todos os produtos disponíveis
                    produtos_str = input("Digite os nomes dos produtos e quantidades desejadas (ex: Arroz 2, Feijão 3): ")
                    produtos = {}
                    for item in produtos_str.split(","):
                        nome, qtd = item.strip().split(" ")
                        produtos[nome] = int(qtd)  # Cria um dicionário com produtos e quantidades
                    endereco = input("Digite o endereço para entrega: ")
                    cliente.fazer_pedido(mercado, produtos, endereco)  # Faz um pedido no mercado
                elif opcao_cliente == "2":
                    mercado.listar_produtos()  # Lista todos os produtos
                elif opcao_cliente == "3":
                    break  # Volta ao menu principal
                else:
                    print("Opção inválida. Tente novamente.")  # Mensagem de erro para opção inválida

        elif opcao == "3":
            print("Saindo...")  # Mensagem de saída
            break  # Sai do loop principal
        else:
            print("Opção inválida. Tente novamente.")  # Mensagem de erro para opção inválida


main()  # Executa a função principal
