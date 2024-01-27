# TIAGO, COLOQUE SEU NÚMERO DE ALUNO E SEU NOME AQUI

# Variaveis globais
clientes = []
id_reparacao = 0


def valida_nif(nif):
    """
    Verifica se o NIF tem o formato correto

    Argumentos:
        NIF (string): número do NIF

    Devolve:
        Boolean: True se NIF passar dos testes, False caso contrário
    """

    # testa se nif é apenas dígitos e tem 9 caracteres
    if not nif.isdigit() or len(nif) != 9:
        return False

    # cálculos para validacao do nif
    soma = 0
    for i in range(0, 8):
        soma = soma + (int(nif[i]) * (9 - i))

    resto = soma % 11

    if resto in (0, 1):
        digito_controlo = 0
    else:
        digito_controlo = 11 - resto

    return int(nif[8]) == digito_controlo


def adiciona_veiculo(cliente, veiculo):
    """
    Adiciona um veículo a um cliente existente

    Argumentos:
        cliente (tuplo): registro de cliente, no formato (
            nome (string),
            NIF (string),
            telemóvel (string),
            veículos (lista)
            )

        veiculo (tuplo): dados de um veículo, no formato (
            tipo (string),
            matricula (string),
            marca (string),
            reparacoes (lista)
        )

    Devolve:
        None

    Levanta:
        ValueError: Se tipo de veículo for inválido
        ValueError: Se matrícula for inválida
        ValueError: Se marca for inválida
        ValueError: Se veículo já estiver associado ao cliente
    """

    # Dividir elementos de veiculo em variáveis separadas
    tipo, matricula, marca, reparacoes = veiculo

    # Verificar erros possíveis
    if not valida_tipo_veiculo(tipo):
        raise ValueError('tipo de veículo inválido')

    if not valida_matricula(matricula):
        raise ValueError('matrícula inválida')

    if not valida_marca_veiculo(marca):
        raise ValueError('marca inválida')

    if verificar_veiculo_cadastrado(cliente[3], matricula):
        raise ValueError('veículo já se encontra associado a este cliente')

    # Adicionar veiculo após validações
    cliente[3].append(veiculo)


def valida_tipo_veiculo(tipo_veiculo):
    """
    Verifica se tipo_veiculo possui o valor 'MOTOCICLO' ou 'CARRO'

    Argumentos:
        tipo_veiculo (string): tipo do veículo --> 'MOTOCICLO' ou 'CARRO'

    Devolve:
        boolean: True se tipo_veiculo for um dos valores esperados,
            False caso contrário
    """

    # Checa requerimentos para tipo
    return tipo_veiculo in ['MOTOCICLO', 'CARRO']


def valida_matricula(matricula):
    """
    Verifica se matricula está no formato 'YY-YY-YY', onde Y pode ser um número ou letra maiúscula. 
    Requisitos:
    ter 8 caracteres
    caracteres na posição 2 e 5 devem ser '-'
    caracteres 0, 1, 3, 4, 6 e 7 devem ser alfanuméricos e maiúsculos

    Argumentos:
        matricula (string): matrícula do veículo

    Devolve:
        boolean: True se matrícula estiver no formato correto, False caso contrário
    """

    # verificar tamanho da string
    if len(matricula) != 8:
        return False

    # verificar se cada caracter atende aos requisitos
    for i, carac in enumerate(matricula):
        if i == 2 or i == 5:
            if carac != '-':
                return False
        else:
            if not carac.isalnum():
                return False
            elif carac.isalpha():
                if not carac.isupper():
                    return False

    return True


def verificar_veiculo_cadastrado(lista_veiculos, matricula_veiculo):
    """
    Verifica se matricula_veiculo já existe na lista_veiculos fornecida

    Argumentos:
        lista_veiculos (lista): dados dos veículos do cliente, lista contendo tuplos no formato (
            tipo (string),
            matricula (string),
            marca (string),
            reparacoes (lista)
        )
        matricula: string

    Devolve:
        boolean: True se matricula_veiculo já existir em lista_veiculos, False caso contrário
    """
    for veiculo_cadastrado in lista_veiculos:
        if veiculo_cadastrado[1] == matricula_veiculo:
            return True
    return False


def valida_marca_veiculo(marca_veiculo):
    """
    Verifica se marca_veiculo possui no mínimo 1 e no máximo 25 caracteres

    Argumentos:
        marca_veiculo (string): marca do veículo

    Devolve:
        boolean: True se marca_veiculo possui até 25 caracteres, False se for string vazia ou tiver mais de 25 caracteres
    """

    return 0 < len(marca_veiculo) <= 25


def adiciona_cliente(nome_completo, nif, telemovel, veiculos):
    """
    Adiciona um novo cliente ao registro de clientes. Caso cliente já exista, atualiza os veículos

    Argumentos:
        nome (string): nome completo, mínimo 1 e máximo 255 caracteres
        nif (string): número do NIF
        telemovel (string): número do telemovel com 9 dígitos e iniciado em 9
        veiculos (lista): dados dos veículos do cliente, lista contendo tuplos no formato (
            tipo (string),
            matricula (string),
            marca (string),
            reparacoes (lista)
        )

    Devolve:
        None

    Levanta:
        ValueError: Se NIF for inválido
        ValueError: Se nome_completo for inválido
        ValueError: Se telemovel for inválido
        ValueError: Se nome_completo for diferente do que já está cadastrado para o cliente
    """

    # Verificar erros possíveis
    if not valida_nif(nif):
        raise ValueError('NIF inválido')

    if not 0 < len(nome_completo) <= 255:
        raise ValueError('nome completo inválido')

    if not len(telemovel) == 9 or not telemovel[0] == '9' or not telemovel.isdigit():
        raise ValueError('número de telemóvel inválido')

    # Verificar se o novo cliente já existe na lista clientes
    for c in clientes:
        if c[1] == nif:
            if c[0] != nome_completo:
                raise ValueError('nome completo incoerente')
            # Caso exista, apenas adicionar veículos
            else:
                for v in veiculos:
                    adiciona_veiculo(c, v)

            break
    # Caso não exista, criar novo registro
    else:
        novo_cliente = (nome_completo, nif, telemovel, [])
        for v in veiculos:
            adiciona_veiculo(novo_cliente, v)
        clientes.append(novo_cliente)


def remove_cliente(nif):
    """
    Remove cliente da lista de clientes, caso ele exista e não esteja com reparações em andamento

    Argumentos:
        nif (string): número do NIF

    Devolve:
        None

    Levanta:
        ValueError: Se NIF for inválido
        ValueError: Se houverem reparações em curso
    """

    # Verificar erros possíveis
    if not valida_nif(nif):
        raise ValueError('NIF inválido')

    # Procurar em clientes
    for c in clientes:
        if c[1] == nif:
            cliente = c
            # Procurar em veículos
            for v in c[3]:
                # Procurar em reparações
                for r in v[3]:
                    # Se reparação está sem data de entrega
                    if r[3] == ():
                        raise ValueError('reparações em curso')

            # Remover caso não haja reparações em andamento
            clientes.remove(cliente)
            return


def procura_veiculo(matricula):
    """
    Retorna registro do veículo, se ele for encontrado

    Argumentos:
        matricula (string): matrícula do veículo, no formato 'YY-YY-YY', onde Y pode ser um número ou letra maiúscula

    Devolve:
        tuplo: tuplo contendo os dados do veículo que tem matrícula = matricula

    Levanta:
        XXXX
    """

    # Error Handling
    if not valida_matricula(matricula):
        raise ValueError('matrícula inválida')

    # Procurar em clientes
    for c in clientes:
        # procurar em veiculos
        for v in c[3]:
            if v[1] == matricula:
                return v

    raise ValueError('veículo não encontrado')


def compara_datas(data1, data2):
    """
    Função para comparar 2 datas diferentes
    *Uma regra do projeto era não importar bibliotecas, se não era possível usar a datetime

    Argumentos:
        data1 (tuplo): data no formato (
            dia (int),
            mês (int),
            ano (int)
        )

        data2 (tuplo): data no formato (
            dia (int),
            mês (int),
            ano (int)
        )

    Devolve:
        inteiro: Se data1 > data2, retorna 1; Se data1 = data2, retorna 0; Se data1 < data2, retorna -1
    """

    dia1, mes1, ano1 = data1
    dia2, mes2, ano2 = data2

    if ano1 < ano2:
        return -1
    elif ano1 > ano2:
        return 1
    elif mes1 < mes2:
        return -1
    elif mes1 > mes2:
        return 1
    elif dia1 < dia2:
        return -1
    elif dia1 > dia2:
        return 1
    else:
        return 0


def inicia_reparacao(matricula, data_entrada, data_estimada):
    """
    Registra uma nova reparação, ou atualiza uma reparação já iniciada mas ainda não finalizada

    Argumentos:
        matricula (string): matrícula do veículo, no formato 'YY-YY-YY', onde Y pode ser um número ou letra maiúscula
        data_entrada (tuplo): data de entrada na oficina, no formato (
            dia (int),
            mês (int),
            ano (int)
        )
        data_estimada (tuplo): data estimada de entrega, no formato (
            dia (int),
            mês (int),
            ano (int)
        )

    Devolve:
        None

    Levanta:
        ValueError: Se data de entrada for superior à data estimada de entrega
        ValueError: Se data de entrada fornecida for diferente da já cadastrada previamente
        ValueError: Se veículo com matrícula matricula não for encontrado
    """

    # Esta função usa uma variável global para controlar o id_reparacao
    global id_reparacao

    # Verificar se data_entrada é maior que a data_estimada
    if compara_datas(data_entrada, data_estimada) == 1:
        raise ValueError(
            'data de entrada não pode ser superior à data estimada de entrega')

    # Procurar em clientes
    for c in clientes:
        # procurar em veiculos
        for v in c[3]:
            if v[1] == matricula:
                reparacoes = v[3]

                # Caso existam reparacoes cadastradas, verificar se existem registros não finalizadas (r[3] == ())
                for r in reparacoes:
                    if r[3] == ():
                        # verificar se data_entrada registrada anteriormente é diferente da informada
                        if r[1] != data_entrada:
                            raise ValueError('data de entrada incoerente')

                        # atualizar data_estimada
                        else:
                            # ATENÇÃO
                            # AQUI EU ACHO QUE O TEXTO DO EXERCÍCIO TINHA UM PROBLEMA. O TEXTO DIZ:
                            # "Caso o veículo já se encontre a ser reparado, a data estimada de entrega deve ser alterada para a nova data data_entrega."
                            # Porém não seria correto alterar a data_estimada para o valor data_entrega, que é uma tupla vazia. Para mim, o correto é atualizar a data_estimada_antiga para a data_estimada_atual
                            r[2] = data_estimada
                            return

                # Se reparações está vazia, ou com todas as reparações registradas anteriormente concluídas, registrar nova reparação
                else:
                    reparacoes.append(
                        [id_reparacao, data_entrada, data_estimada, ()])
                    id_reparacao += 1
                    return

    else:
        raise ValueError('veículo não encontrado')


def anula_reparacao(id):
    """
    Deleta a reparacao cujo id_reparacao = id

    Argumentos:
        id (inteiro): ID de reparação, número inteiro positivo

    Devolve:
        None
    """

    # procurar em clientes
    for c in clientes:
        # procurar em veiculos
        for v in c[3]:
            # checar se lista de reparações não está vazia
            if v[3] != []:
                # procurar id e deletar registro, caso encontre
                for r in v[3]:
                    if r[0] == id:
                        v[3].remove(r)
                        return


def procura_reparacao(id):
    """
    Retorna uma tupla com o NIF, matricula e a própria reparação cujo id_reparação = id, caso ela exista na lista de clientes

    Argumentos:
        id_reparacao (inteiro): ID de reparação, número inteiro positivo

    Devolve:
        tuplo: retorna um tuplo, no formato (
            NIF (string),
            matricula (string),
            reparação (lista)
        )

    Levanta:
        ValueError: caso reparação não seja encontrada
    """

    for c in clientes:
        for v in c[3]:
            for r in v[3]:
                if r[0] == id:
                    nif = c[1]
                    matricula = v[1]
                    reparacao = r
                    reparacao_encontrada = (nif, matricula, reparacao)
                    return reparacao_encontrada

    raise ValueError('reparação não encontrada')


def reparacao_atrasada(data):
    """
    Retorna uma tupla contendo informações de todas as reparações não finalizadas e cuja data_estimativa é anterior a data. Cada reparação é uma tupla dentro da tupla reparações

    Argumentos:
        data (tuplo): as reparações não concluídas terão suas datas estimadas de entrega comparadas a esta data. Caso a data estimada de entrega seja inferior a data, a reparação está atrasada. Formato de data é (
            dia (int),
            mês (int),
            ano (int)
        )

    Devolve:
        tuplo: retorna um tuplo contendo outros tuplos com informações de reparações que estão atrasadas.
    """

    reparacoes_atrasadas = []

    # procurar em clientes
    for c in clientes:
        # procurar em veiculos
        for v in c[3]:
            # caso existam registros de reparações
            if v[3] != []:
                # procurar em reparações
                for r in v[3]:
                    # se houver reparações não finalizadas
                    if r[3] == ():
                        data_estimada = r[2]
                        # se estiver atrasada
                        if compara_datas(data, data_estimada) == 1:
                            nif = c[1]
                            matricula = v[1]
                            reparacao = r
                            registro_atrasado = (nif, matricula, reparacao)
                            reparacoes_atrasadas.append(registro_atrasado)

    return tuple(reparacoes_atrasadas)


def finaliza_reparacao(id, data):
    """
    Finaliza uma reparação cujo id_reparação = 'id', preenchendo a data_entrega com 'data'.

    Argumentos:
        id (inteiro): ID de reparação
        data (tuplo): data da entrega do veículo ao cliente, no formato (
            dia (int),
            mês (int),
            ano (int)
        )

    Devolve:
        tuplo: recibo em com as informações no formato (
            nif (string),
            matricula (string),
            data_entrada (tuplo),
            data_entrega (tuplo)
        )

    Levanta:
        ValueError: Se a reparação já estiver registrada como finalizada
        ValueError: Se a data de entrada for superior à data informada de entrega
        ValueError: Se a reparação for encontrada
    """

    # procurar em clientes
    for c in clientes:
        # procurar em veiculos
        for v in c[3]:
            # caso existam registros de reparações
            if v[3] != []:
                # procurar em reparações
                for r in v[3]:
                    # se id reparacao (r[0]) for o id procurado
                    if r[0] == id:
                        # se data_entrega (r[3]) já foi preenchida, erro
                        if r[3] != ():
                            raise ValueError('reparação já foi finalizada')
                        else:
                            # se data_entrada > data, erro
                            data_entrada = r[1]
                            if compara_datas(data_entrada, data) == 1:
                                raise ValueError(
                                    'data de entrada não pode ser superior à data de entrega')
                            else:
                                r[3] = data
                                nif = c[1]
                                matricula = v[1]
                                recibo = (nif, matricula, data_entrada, data)
                                return recibo

    raise ValueError('reparação não encontrada')


def imprime_recibo(recibo):
    """
    Escreve no ecrã a informação de um recibo 'recibo'

    Argumentos:
        recibo (tuplo): recibo com as informações no formato (
            nif (string),
            matricula (string),
            data_entrada (tuplo),
            data_entrega (tuplo)
        )

    Devolve:
        string: Texto estilizado num formato de recibo, contendo os dados recebidos na variável 'recibo'
    """

    # AQUI EXISTE UM ERRO ENTRE O QUE O PDF PEDE E O QUE O Tester_p1.py VERIFICA!

    # Padrão do PDF
    # texto_recibo = f'{"-" * 49}\n Cliente: {recibo[0]}\n Veículo: {recibo[1]}\nData de entrada: {recibo[2][0]:02d}/{recibo[2][1]:02d}/{recibo[2][2]}\n{"-" * 49}\nData de entrega: {recibo[3][0]:02d}/{recibo[3][1]:02d}/{recibo[3][2]}\n{"-" * 49}\n'

    # Padrão do tester_p1.py
    texto_recibo = f'{"-" * 49}\n Cliente: {recibo[0]}\n Veículo: {recibo[1]}\nData de entrada: {recibo[2][0]}/{recibo[2][1]}/{recibo[2][2]}\n{"-" * 49}\nData de entrega: {recibo[3][0]}/{recibo[3][1]}/{recibo[3][2]}\n{"-" * 49}\n'

    # comando print, por padrão, já adiciona \n ao final,
    # por isso usei end=''
    return print(texto_recibo, end='')
