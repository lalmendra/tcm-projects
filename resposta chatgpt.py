clientes = []
id_reparacao = 0


# Funções relacionadas com a gestão dos clientes


def valida_nif(nif):
    try:
        nif = list(map(int, nif))
        check_digit = (nif[7] * 2 + nif[6] * 3 + nif[5] * 4 + nif[4]
                       * 5 + nif[3] * 6 + nif[2] * 7 + nif[1] * 8 + nif[0] * 9) % 11
        check_digit = 0 if check_digit in (0, 1) else 11 - check_digit
        return nif[8] == check_digit
    except (ValueError, IndexError):
        return False


def adiciona_veiculo(cliente, veiculo):
    tipo, matricula, marca, _ = veiculo

    if tipo not in ["MOTOCICLO", "CARRO"]:
        raise ValueError('Tipo de veículo inválido')

    if not valida_matricula(matricula):
        raise ValueError('Matrícula inválida')

    if not 0 < len(marca) <= 25:
        raise ValueError('Marca inválida')

    if any(matricula == v[1] for v in cliente[3]):
        raise ValueError('Veículo já se encontra associado a este cliente')

    cliente[3].append(veiculo)


def valida_matricula(matricula):
    return len(matricula) == 8 and matricula[2] == matricula[5] == '-' and matricula[:2].isalnum() and matricula[3:5].isalnum() and matricula[6:].isalnum()


def adiciona_cliente(nome_completo, nif, telemovel, veiculos):
    if not valida_nif(nif):
        raise ValueError('NIF inválido')

    if not 0 < len(nome_completo) <= 255:
        raise ValueError('Nome completo inválido')

    if not telemovel.startswith('9') or not telemovel.isdigit() or len(telemovel) != 9:
        raise ValueError('Número de telemóvel inválido')

    for veiculo in veiculos:
        adiciona_veiculo((nome_completo, nif, telemovel, []), veiculo)

    for cliente in clientes:
        if cliente[1] == nif:
            if cliente[0] != nome_completo:
                raise ValueError('Nome completo incoerente')
            else:
                cliente[3].extend(veiculos)
            break
    else:
        clientes.append((nome_completo, nif, telemovel, veiculos))


def remove_cliente(nif):
    for cliente in clientes:
        if cliente[1] == nif:
            if any(cliente[3]):
                raise ValueError('Reparações em curso')
            clientes.remove(cliente)
            break


def procura_veiculo(matricula):
    for cliente in clientes:
        for veiculo in cliente[3]:
            if veiculo[1] == matricula:
                return veiculo
    raise ValueError('Veículo não encontrado')


# Funções relacionadas com a gestão de reparações

def inicia_reparacao(matricula, data_entrada, data_estimada):
    global id_reparacao

    try:
        cliente, _, reparacoes = procura_veiculo(matricula)
        for reparacao in reparacoes:
            if reparacao[3] == ():
                reparacao[2] = data_estimada
                break
        else:
            reparacoes.append([id_reparacao, data_entrada, data_estimada, ()])
            id_reparacao += 1
    except ValueError:
        raise ValueError('Veículo não encontrado')


def anula_reparacao(id_reparacao):
    for cliente in clientes:
        for veiculo in cliente[3]:
            for reparacao in veiculo[3]:
                if reparacao[0] == id_reparacao:
                    if reparacao[3] != ():
                        raise ValueError('Reparação já foi finalizada')
                    veiculo[3].remove(reparacao)
                    break


def procura_reparacao(id_reparacao):
    for cliente in clientes:
        for veiculo in cliente[3]:
            for reparacao in veiculo[3]:
                if reparacao[0] == id_reparacao:
                    return cliente[1], veiculo[1], reparacao
    raise ValueError('Reparação não encontrada')


def reparacao_atrasada(data):
    atrasadas = []

    for cliente in clientes:
        for veiculo in cliente[3]:
            for reparacao in veiculo[3]:
                if reparacao[3] == () and reparacao[2] < data:
                    atrasadas.append((cliente[1], veiculo[1], reparacao))

    return tuple(sorted(atrasadas, key=lambda x: (x[0], x[1])))


def finaliza_reparacao(id_reparacao, data_entrega):
    cliente_nif, veiculo_matricula, reparacao = procura_reparacao(id_reparacao)

    if reparacao[3] != ():
        raise ValueError('Reparação já foi finalizada')

    if reparacao[1] > data_entrega:
        raise ValueError(
            'Data de entrada não pode ser superior à data de entrega')

    reparacao[3] = data_entrega

    return cliente_nif, veiculo_matricula, reparacao


def imprime_recibo(recibo):
    print('-' * 49)
    print(f' Cliente: {recibo[0]}')
    print(f' Veículo: {recibo[1]}')
    print(
        f'Data de entrada: {recibo[2][0]:02d}/{recibo[2][1]:02d}/{recibo[2][2]}')
    print('-' * 49)
    print(
        f'Data de entrega: {recibo[3][0]:02d}/{recibo[3][1]:02d}/{recibo[3][2]}')
    print('-' * 49)


# Exemplos de utilização
# Adicionar cliente
adiciona_cliente('José Maria Rebelo de Sousa', '248537474',
                 '918765432', [('CARRO', 'CC-01-02', 'BMW', [])])

# Iniciar uma reparação
inicia_reparacao('CC-01-02', (1, 1, 2022), (3, 1, 2022))

# Anular uma reparação
anula_reparacao(0)

# Procurar veículo
veiculo = procura_veiculo('CC-01-02')
print(veiculo)

# Adicionar outro cliente
adiciona_cliente('António Manuel da Silva', '219072230', '912345678', [
                 ('MOTOCICLO', 'AA-01-02', 'SUZUKI', [])])

# Finalizar uma reparação
recibo = finaliza_reparacao(0, (5, 1, 2022))

# Imprimir recibo
imprime_recibo(recibo)
