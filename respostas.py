# Coloque seu número e nome de aluno aqui!

from datetime import datetime

# Variaveis globais
clientes = []
id_reparacao = 0


def valida_nif(nif):
    # testa se nif tem 9 dígitos
    if len(nif) != 9:
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
        raise ValueError('Tipo de veículo inválido')

    if not valida_matricula(matricula):
        raise ValueError('Matrícula inválida')

    if not valida_marca_veiculo(marca):
        raise ValueError('Marca inválida')

    if verificar_veiculo_cadastrado(cliente[3], matricula):
        raise ValueError('Veículo já se encontra associado a este cliente')

    # Adicionar veiculo após validações
    cliente[3].append(veiculo)


def valida_tipo_veiculo(tipo_veiculo):
    # Checa requerimentos para tipo
    return tipo_veiculo in ['MOTOCICLO', 'CARRO']


def valida_matricula(matricula):
    # Checa requerimentos para matricula
    # matricula tem 8 caracteres?
    # caracteres na posição 2 e 5 são - ?
    # caracteres 0 e 1, 3 e 4, e 6 e 7 são alfanuméricos?
    return len(matricula) == 8 \
        and matricula[2] == matricula[5] == '-' \
        and matricula[:2].isalnum() \
        and matricula[3:5].isalnum() \
        and matricula[6:].isalnum()


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
        raise ValueError('Nome completo inválido')

    if not len(telemovel) == 9 or not telemovel[0] == '9' or not telemovel.isdigit():
        raise ValueError('Número de telemóvel inválido')

    # Checa se o novo cliente já existe na lista clientes
    for c in clientes:
        if c[1] == nif:
            if c[0] != nome_completo:
                raise ValueError('Nome completo incoerente')
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
                        raise ValueError('Reparações em curso')

            # Remover caso não haja reparações em andamento
            clientes.remove(cliente)
            return


def procura_veiculo(matricula):
    # Retorna registro do veículo, se ele for encontrado

    # Error Handling
    if not valida_matricula(matricula):
        raise ValueError('Matrícula inválida')

    # Procurar em clientes
    for c in clientes:
        # procurar em veiculos
        for v in c[3]:
            if v[1] == matricula:
                return print(v)

    raise ValueError('Veículo não encontrado')


def inicia_reparacao(matricula, data_entrada, data_estimada):
    # Registra uma nova reparação, ou atualiza uma reparação já iniciada mas ainda não finalizada

    # Esta função usa uma variável global para controlar o id_reparacao
    global id_reparacao

    # Verificar se data_entrada é menor ou igual a data_estimada
    # Uso a biblioteca datetime para comparar datas
    d_data_entrada = datetime(
        data_entrada[2], data_entrada[1], data_entrada[0])

    d_data_estimada = datetime(
        data_estimada[2], data_estimada[1], data_estimada[0])

    if d_data_entrada > d_data_estimada:
        raise ValueError(
            'Data de entrada não pode ser superior à data estimada de entrega')

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
                            raise ValueError('Data de entrada incoerente')

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
        raise ValueError('Veículo não encontrado')


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

    raise ValueError('Reparação não encontrada')


def reparacao_atrasada(data):
    # Retorna uma tupla contendo todas as reparações não finalizadas e cuja data_estimativa é anterior a data

    d_data = datetime(data[2], data[1], data[0])

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
                        d_data_estimada = datetime(
                            data_estimada[2], data_estimada[1], data_estimada[0])
                        # se estiver atrasada
                        if d_data > d_data_estimada:
                            nif = c[1]
                            matricula = v[1]
                            reparacao = r
                            registro_atrasado = (nif, matricula, reparacao)
                            reparacoes_atrasadas.append(registro_atrasado)

    return tuple(reparacoes_atrasadas)


def finaliza_reparacao(id, data):

    d_data = datetime(data[2], data[1], data[0])

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
                            raise ValueError('Reparação já foi finalizada')
                        else:
                            # se data_entrada > data, erro
                            data_entrada = r[1]
                            d_data_entrada = datetime(
                                data_entrada[2], data_entrada[1], data_entrada[0])
                            if d_data_entrada > d_data:
                                raise ValueError(
                                    'Data de entrada não pode ser superior à data de entrega')
                            else:
                                r[3] = data
                                nif = c[1]
                                matricula = v[1]
                                recibo = (nif, matricula, data_entrada, data)
                                return recibo

    raise ValueError('Reparação não encontrada')


def imprime_recibo(recibo):
    texto_recibo = f'{"-" * 49}\n Cliente: {recibo[0]}\n Veiculo: {recibo[1]}\nData de entrada: {recibo[2]}\n{"-" * 49}\nData de entrega: {recibo[3]}\n{"-" * 49}'

    return texto_recibo


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

    clientes = [
        ('José Maria Rebelo de Sousa', '248537474', '918765432', []),
        ('António Manuel da Silva', '219072230', '912345678', [
            ('MOTOCICLO', 'AA-01-02', 'SUZUKI',
             [[0, (1, 1, 2022), (3, 1, 2022), ()]])
        ])
    ]

    print(imprime_recibo(finaliza_reparacao(0, (4, 1, 2022))))
