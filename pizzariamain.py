import matplotlib.pyplot as plt
import pymysql.cursors

conexao = pymysql.connect(

    host='localhost',
    user='root',
    password='',
    db='erp',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

autentico = False


def logarCadastrar():
    usuarioExistente = 0
    autenticado = False
    usuarioMaster = False

    if decisao == 1:
        nome = input('Loguin: ')
        senha = input('Senha: ')
        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                autenticado = True
                break
            else:
                autenticado = False
        if not autenticado:
            print('email ou senha errado')

    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input('digite seu loguin')
        senha = input('digite sua senha ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1
        if usuarioExistente == 1:
            print('Usuario já cadastrado, Tente outro loguin ou volte para sse logar')
        elif usuarioExistente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros (nome, senha, nivel) values (%s, %s, %s)', (nome, senha, 1))
                    conexao.commit()
                    print('Usuario cadastrado com sucesso')
            except:
                print('Erro ao inserir os dados')
    return autenticado, usuarioMaster


def cadastrarProdutos():
    nome = input('Nome do produto: ')
    ingrediente = input('Ingredientes do produto')
    grupo = input('Qual grupo de produtos ele irá pertencer\n -Bebidas\n -Lanches\n -Pizzas\n')
    preco = float(input('Preço do produto: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('insert into produtos (nome, ingredientes, grupo , preco) values (%s, %s,%s, %s)',
                           (nome, ingrediente, grupo, preco))
            conexao.commit()
            print('produto cadastrado')
    except:
        print('erro ao inserir os produtos no banco de dados')


def listarProdutos():
    produtos = []

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtosCadastrados = cursor.fetchall()
    except:
        print('Erro ao conectar o banco de dados')

    for i in produtosCadastrados:
        produtos.append(i)
    if len(produtos) != 0:
        for i in range(0, len(produtos)):
            print(produtos[i])
    else:
        print('Nenhum produto cadastrado ')

def excluirProduto():
    idDeletar = int(input('digite o id do produto que deseja apagar'))
    try:
        with conexao.cursor() as cursor:
            cursor.execute('delete from produto where id ={}'._format(idDeletar))
    except:
        print('erro ao excluir os produtos no banco de dados')


def listarPedidos():
    pedidos = []
    decision = 0

    while decision != 2:
        pedidos.clear()
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from pedidos')
                listaPedidos= cursor.fetchall()
        except:
            print('erro ao listar os produtos no banco de dados')
        for i in listaPedidos:
            pedidos.append(i)
        if len(pedidos) !=0:
            for i in range(0, len(pedidos)):
                print(pedidos[i])
        else:
            print('nenhum pedido pendente')
        decision = int(input('Digite 1- Para dar o pedido como entregue\n Digite 2- Para voltar'))
        if decision == 1:
            idDeletar = int(input('Digite o id do pedido entregue'))
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('delete from pedidos where id = {}'.format(idDeletar))
                    print(f'pedido {i} entregue ')
                    listaPedidos = cursor.fetchall()
            except:
                print('erro ao dar pedido como entregue')

def gerarEstatistica():
    nomeProdutos = []
    nomeProdutos.clear()

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
    except:
        print('erro ao fazer consulta no banco de dados')
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from estatisticaVendido')
            vendido = cursor.fetchall()
    except:
        print('erro ao fazer consulta no banco de dados')

    estado = int(input(' Digite:\n 0 Para sair\n 1 para pesquisar por nome\n 2 para pesquisar por grupo'))
    if estado == 1:
        decisao3 = int(input(' Digite:\n 1 para pesquisar por valor\n 2 por quantidade unitaria'))
        if decisao3 == 1:
            for i in produtos:
                nomeProdutos.append(i['nome'])
            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['nome'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor+1)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('quantidade vendida em reais')
            plt.xlabel('produtos')
            plt.show()
        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('erro na consulta')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('erro na consulta')
            for i in grupo:
                grupoUnico.append(i['nome'])
            grupoUnico = sorted(set(grupoUnico))
            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['nome']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)
            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('quantidade unitatia vendida')
            plt.xlabel('produtos')
            plt.show()

    elif estado == 2:
        decisao3 = int(input(' Digite:\n 1 para pesquisar por valor\n 2 por quantidade unitaria'))
        if decisao3 == 1:
            for i in produtos:
                nomeProdutos.append(i['grupo'])
            valores = []
            valores.clear()

            for h in range(0, len(nomeProdutos)):
                somaValor = -1
                for i in vendido:
                    if i['grupo'] == nomeProdutos[h]:
                        somaValor += i['preco']
                if somaValor == -1:
                    valores.append(0)
                elif somaValor > 0:
                    valores.append(somaValor + 1)

            plt.plot(nomeProdutos, valores)
            plt.ylabel('quantidade vendida em reais')
            plt.xlabel('produtos')
            plt.show()
        if decisao3 == 2:
            grupoUnico = []
            grupoUnico.clear()

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from produtos')
                    grupo = cursor.fetchall()
            except:
                print('erro na consulta')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('select * from estatisticaVendido')
                    vendidoGrupo = cursor.fetchall()
            except:
                print('erro na consulta')
            for i in grupo:
                grupoUnico.append(i['grupo'])
            grupoUnico = sorted(set(grupoUnico))
            qntFinal = []
            qntFinal.clear()

            for h in range(0, len(grupoUnico)):
                qntUnitaria = 0
                
                for i in vendidoGrupo:
                    if grupoUnico[h] == i['grupo']:
                        qntUnitaria += 1
                qntFinal.append(qntUnitaria)
            plt.plot(grupoUnico, qntFinal)
            plt.ylabel('quantidade unitatia vendida')
            plt.xlabel('produtos')
            plt.show()

while not autentico:
    decisao = int(input('*** Bem vindo a pizzaria ALL ***\n Possui cadastro? digite 1\n Para se cadastrar digite 2\n'))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from  cadastros')
            resultado = cursor.fetchall()

    except:
        print('erro ao conectar no banco de dados')
    autentico, usuarioSupremo = logarCadastrar()

    if autentico:
        print('autenticado')

    if usuarioSupremo == True:

        decisaoUsuario = 1

        while decisaoUsuario != 0:
            decisaoUsuario = int(input(' digite 0 para sair\n 1 para cadastrar produtos\n 2 para listarprodutos\n 3 para listar os pedidos\n 4 para visualizar as estatisticas'))

            if decisaoUsuario == 1:
                cadastrarProdutos()
            elif decisaoUsuario == 2:
                listarProdutos()

                delete= int(input('\n-Digite 1- Para excluir algum produto\n-Digite 2- Voltar ao MENU principal '))
                if delete == 1:
                    excluirProduto()
            elif decisaoUsuario == 3:
                listarPedidos()
            elif decisaoUsuario == 4:
                gerarEstatistica()