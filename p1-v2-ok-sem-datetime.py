# Coloque seu número e nome de aluno aqui!

# Variaveis globais
clientes = []
id_reparacao = 0


def valida_nif(nif):
    # testa se nif é apenas dígitos e tem 9 caracteres
    if not nif.isdigit() or len(nif) != 9:
        return False

    # calculos para validacao do nif
    soma = 0
    for i in range(0, 8):
        soma = soma + (int(nif[i]) * (9 - i))

    resto = soma % 11

    if resto in (0, 1):
        digito_controlo = 0
    else:
        digito_controlo = 11 - resto

    # retorna resultado True ou False
    return int(nif[8]) == digito_controlo


def adiciona_veiculo(cliente, veiculo):
    # Adiciona um veículo a um cliente existente

    # Dividir elementos de veiculo em variáveis separadas
    tipo, matricula, marca, reparacoes = veiculo

    # Error Handling

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
    # Checa requerimentos para tipo
    return tipo_veiculo in ['MOTOCICLO', 'CARRO']


def valida_matricula(matricula):
    # Checa requerimentos para matricula
    # matricula tem 8 caracteres?
    # caracteres na posição 2 e 5 são - ?
    # caracteres 0 e 1, 3 e 4, e 6 e 7 são alfanuméricos e maiúsculos?

    if len(matricula) != 8:
        return False

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
    # Verifica se matrícula já existe na lista_veiculos
    for veiculo_cadastrado in lista_veiculos:
        if veiculo_cadastrado[1] == matricula_veiculo:
            return True
    return False


def valida_marca_veiculo(marca_veiculo):
    # Checa requerimentos para marca
    return 0 < len(marca_veiculo) <= 25


def adiciona_cliente(nome_completo, nif, telemovel, veiculos):
    # Adiciona um novo cliente ao registro da oficina,
    # OU adiciona veículos ao registro já existente do cliente

    # Error Handling

    if not valida_nif(nif):
        raise ValueError('NIF inválido')

    if not 0 < len(nome_completo) <= 255:
        raise ValueError('nome completo inválido')

    if not len(telemovel) == 9 or not telemovel[0] == '9' or not telemovel.isdigit():
        raise ValueError('número de telemóvel inválido')

    # Checa se o novo cliente já existe na lista clientes
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
    # Remove cliente caso ele exista e não esteja com reparações em andamento

    # Error Handling

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
    # Retorna registro do veículo, se ele for encontrado

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
    # Não posso importar datetime, fiz uma função para trabalhar com datas
    # retorna 1 se data1 > data2
    # retorna -1 se data2 > data1
    # retorna 0 se data1 = data2
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
    # Registra uma nova reparação, ou atualiza uma reparação já iniciada mas ainda não finalizada

    # Esta função usa uma variável global para controlar o id_reparacao
    global id_reparacao

    # Verificar se data_entrada é menor ou igual a data_estimada
    if compara_datas(data_entrada, data_estimada) == 1:
        raise ValueError(
            'data de entrada não pode ser superior à data estimada de entrega')

    # Procurar em clientes
    for c in clientes:
        # procurar em veiculos
        for v in c[3]:
            if v[1] == matricula:
                reparacoes = v[3]

                # Caso existam reparacoes cadastradas, procurar se existem registros não finalizadas (r[3] == ())
                for r in reparacoes:
                    if r[3] == ():
                        # checar se data_entrada registrada anteriormente é diferente da informada
                        if r[1] != data_entrada:
                            raise ValueError('data de entrada incoerente')

                        # atualizar data_estimada
                        else:
                            # ATENÇÃO
                            # AQUI EU ACHO QUE O TEXTO DO EXERCÍCIO TINHA UM PROBLEMA. O TEXTO DIZ:
                            # "Caso o veículo já se encontre a ser reparado, a data estimada de entrega deve ser alterada para a nova data data_entrega."
                            # Porém não tem lógica alterar a data_estimada para o valor data_entrega, que é uma tupla vazia. Para mim, o lógico é atualizar a data_estimada_antiga para a data_estimada_atual
                            r[2] = data_estimada
                            return

                # Se reparações está vazia ou com todas as reparações registradas anteriormente concluídas, registrar nova reparação
                else:
                    reparacoes.append(
                        [id_reparacao, data_entrada, data_estimada, ()])
                    id_reparacao += 1
                    return

    else:
        raise ValueError('veículo não encontrado')


def anula_reparacao(id):
    # Deleta a reparacao com id_reparacao = id

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
    # Retorna uma tupla com dados da reparação, caso encontrada

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
    # Retorna uma tupla contendo todas as reparações não finalizadas e cuja data_estimativa é anterior a data

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
    # AQUI EXISTE UM ERRO ENTRE O QUE O PDF PEDE E O QUE O TESTER VERIFICA!

    # Padrão do PDF
    # texto_recibo = f'{"-" * 49}\n Cliente: {recibo[0]}\n Veículo: {recibo[1]}\nData de entrada: {recibo[2][0]:02d}/{recibo[2][1]:02d}/{recibo[2][2]}\n{"-" * 49}\nData de entrega: {recibo[3][0]:02d}/{recibo[3][1]:02d}/{recibo[3][2]}\n{"-" * 49}\n'

    # Padrão do tester_p1.py
    texto_recibo = f'{"-" * 49}\n Cliente: {recibo[0]}\n Veículo: {recibo[1]}\nData de entrada: {recibo[2][0]}/{recibo[2][1]}/{recibo[2][2]}\n{"-" * 49}\nData de entrega: {recibo[3][0]}/{recibo[3][1]}/{recibo[3][2]}\n{"-" * 49}\n'

    # Print por padrão já adiciona \n ao final,
    # por isso usei end=''
    return print(texto_recibo, end='')


if __name__ == '__main__':
    # adiciona_cliente('António Manuel da Silva', '219072230',
    #                  '912345678', [('MOTOCICLO', 'AA-01-02', 'SUZUKI', [])])

    # adiciona_cliente('António Manuel da Silva', '219072230',
    #                  '912345678', [('CARRO', 'AB-01-02', 'FORD', [[253, (21, 2, 2021), (27, 2, 2021), (28, 2, 2021)],])])

    # adiciona_cliente('António Manuel da Silva', '219072230',
    #                  '912345678', [('CARRO', 'CC-01-02', 'FORD', [[253, (1, 1, 2022), (2, 1, 2022), ()],])])

    # adiciona_cliente('António Manuel da Silva', '219072230',
    #                  '912345678', [('CARRO', 'DD-01-02', 'FORD', [[253, (21, 2, 2021), (27, 2, 2021), (28, 2, 2021)],])])

    # adiciona_cliente('Maria', '123456789',
    #                  '912345678', [('CARRO', 'AB-00-00', 'FERRARI', [])])

    # adiciona_cliente('Joana', '987654322',
    #                  '912345678', [('MOTOCICLO', 'ZZ-99-99', 'HONDA', [])])

    # clientes = [
    #     ('José Maria Rebelo de Sousa', '248537474', '918765432', []),
    #     ('António Manuel da Silva', '219072230', '912345678', [
    #         ('MOTOCICLO', 'AA-01-02', 'SUZUKI',
    #          [[0, (1, 1, 2022), (3, 1, 2022), ()]])
    #     ])
    # ]

    # cliente = (
    #     "António Manuel da Silva",
    #     "219072230",
    #     "912345678",
    #     [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
    # )

    # veiculo = ("CARRO", "Bc-01-02", "BMW", [])

    # print(valida_matricula(veiculo))
    # print(adiciona_veiculo(cliente, veiculo))

    pass
