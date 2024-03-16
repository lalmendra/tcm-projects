import datetime
import csv

estado_programa = {
    'hoje': datetime.date.today(),
    'empregado_id': 1,
    'tarefa_id': 1
}

empregados = {}
tarefas = {}


def valida_argumento(argumento, tipo_esperado):
    """
    Funcao auxiliar para validar argumentos fornecidos

    Argumentos:
        argumento (any): argumento a verificar
        tipo_esperado (any): tipo de argumento esperado

    Devolve:
        None

    Levanta:
        ValueError: Se argumento não for do tipo esperado
    """
    if not isinstance(argumento, tipo_esperado):
        raise ValueError('argumento com tipo inválido')


def valida_data(data: str):
    """
    Função auxiliar para verifica se data está no formato 'YYYY-YY-YY',
    onde Y deve ser um número inteiro.

    Requisitos para considerar válida:
    ter 10 caracteres
    caracteres na posição 4 e 7 devem ser '-'
    caracteres 0, 1, 2, 3, 5, 6, 8 e 9 devem ser núméricos

    Argumentos:
        data (str): data em formato ISO

    Devolve:
        boolean: True se data estiver no formato correto, False caso contrário
    """

    # verificar tamanho da string
    if len(data) != 10:
        return False

    # verificar se cada caracter atende aos requisitos
    for i, carac in enumerate(data):
        if i == 4 or i == 7:
            if carac != '-':
                return False
        else:
            if not carac.isdigit():
                return False

    # check 1 <= month <= 12
    if not (1 <= int(data[5:7]) <= 12):
        return False

    # check 1 <= day <= 31
    if not (1 <= int(data[8:10]) <= 31):
        return False

    return True


def cria_tarefa(descricao: str, prazo: str, data_criacao: str):
    """
    Cria uma nova tarefa, adicionando-a ao dicionário tarefas

    Argumentos:
        descricao (str): descrição da tarefa
        prazo (str): prazo da tarefa, data no formato AAAA-MM-DD
        data_criacao (str): data de criação da tarefa, no formato AAAA-MM-DD

    Devolve:
        int: identificador da tarefa criada

    Levanta:
        ValueError: Se descrição > 256 caracteres
        ValueError: Se prazo estiver num formato inválido
        ValueError: Se data_criacao estiver num formato inválido
    """

    valida_argumento(descricao, str)
    if not 0 < len(descricao) <= 256:
        raise ValueError('descrição excede o limite de 256 caracteres')

    valida_argumento(prazo, str)
    if not valida_data(prazo):
        raise ValueError('prazo com formato inválido')

    valida_argumento(data_criacao, str)
    if not valida_data(data_criacao):
        raise ValueError('data de criação com formato inválido')

    tarefa_id = estado_programa['tarefa_id']
    estado_programa['tarefa_id'] += 1
    tarefas[tarefa_id] = {
        'descricao': descricao,
        'prazo': datetime.date.fromisoformat(prazo),
        'estados': [
            ('POR ATRIBUIR', datetime.date.fromisoformat(data_criacao), None)
        ],
        'empregado_id': None
    }

    return tarefa_id


def valida_tipo_estado(estado: str):
    """
    Função auxiliar para validar se o tipo do estado é um dos
    valores permitidos:
    'POR ATRIBUIR'
    'ATRIBUÍDA'
    'EM PROGRESSO'
    'FINALIZADA'

    Argumentos:
        estado (string): tipo de estado da tarefa.

    Devolve:
        None

    Levanta:
        ValueError: Se tipo de estado for inválido
    """
    if estado not in ['POR ATRIBUIR', 'ATRIBUÍDA',
                      'EM PROGRESSO', 'FINALIZADA']:
        raise ValueError('estado inválido')


def valida_empregado(empregado_id: int):
    """
    Função auxiliar que verifica se empregado_id está no dicionário empregados

    Argumentos:
        empregado_id (int): id do empregado

    Devolve:
        None

    Levanta:
        ValueError: Se tipo de empregado_id não estiver no dicionário
    """
    if empregado_id not in empregados:
        raise ValueError('empregado inexistente')


def modifica_estado(tarefa_id: int, estado: str,
                    data_modificacao: str, empregado_id: int = None):
    """
    Modifica o estado atual da tarefa cujo id = tarefa_id

    Argumentos:
        tarefa_id (int): id da tarefa a ser modificada
        estado (str): novo tipo de estado da tarefa
        data_modificacao (str): data de modificação da tarefa
        empregado_id (int): (Opcional) id do empregado

    Devolve:
        None

    Levanta:
        ValueError: Se tarefa_id não existir em tarefas
        ValueError: Se formato da data_modificacao estiver errado
        ValueError: Se tarefa já estiver finalizada
        ValueError: Se empregado_id não for None quando algum é esperado
    """
    valida_argumento(tarefa_id, int)
    if tarefa_id not in tarefas:
        raise ValueError('tarefa inexistente')

    valida_argumento(estado, str)
    valida_tipo_estado(estado)

    valida_argumento(data_modificacao, str)
    if not valida_data(data_modificacao):
        raise ValueError('data de modificação com formato inválido')

    if empregado_id is not None:
        valida_argumento(empregado_id, int)
        valida_empregado(empregado_id)

    if tarefas[tarefa_id]['estados'][-1][0] == 'FINALIZADA':
        raise ValueError('tarefa encontra-se finalizada')

    elif estado == 'POR ATRIBUIR':
        if tarefas[tarefa_id]['empregado_id'] is not None:
            empregado_id = tarefas[tarefa_id]['empregado_id']
            empregados[empregado_id]['tarefas_id'].remove(tarefa_id)

        tarefas[tarefa_id]['estados'].append(
            ('POR ATRIBUIR',
             datetime.date.fromisoformat(data_modificacao),
             None))
        tarefas[tarefa_id]['empregado_id'] = None

    elif estado == 'ATRIBUÍDA':
        if empregado_id is None:
            raise ValueError(
                'identificador do empregado responsável não pode ser vazio')

        tarefas[tarefa_id]['estados'].append(
            (estado,
                datetime.date.fromisoformat(data_modificacao),
                empregado_id))
        tarefas[tarefa_id]['empregado_id'] = empregado_id

        empregados[empregado_id]['tarefas_id'].append(tarefa_id)

    elif estado in ['EM PROGRESSO', 'FINALIZADA']:
        if tarefas[tarefa_id]['empregado_id'] is None:
            raise ValueError('tarefa não tem empregado responsável')

        tarefas[tarefa_id]['estados'].append(
            (estado,
                datetime.date.fromisoformat(data_modificacao),
                None))


def valida_csv(ficheiro: str):
    """
    Função auxiliar para validar se o ficheiro é um csv.
    Esta função lê as 5 primeiras linhas e identifica se existe pelo menos 1
    vírgula no conteúdo

    Argumentos:
        ficheiro (str): nome do ficheiro csv

    Devolve:
        boolean: True se arquivo for csv, False caso contrário

    Levanta:
        ValueError: Se não for possível abrir ficheiro
    """
    try:
        with open(ficheiro, 'r') as f:
            for _ in range(5):
                linha = f.readline()
                if ',' in linha:
                    return True
        return False
    except Exception:
        raise ValueError('erro a abrir o ficheiro')


def carrega_tarefas(ficheiro_tarefas: str, ficheiro_estados: str):
    """
    Utiliza dois ficheiros csv, ficheiro_tarefas e ficheiro_estados, para
    preencher o dicionário tarefas com tarefas e seus estados

    Argumentos:
        ficheiro_tarefas (str): nome do ficheiro com as tarefas
        ficheiro_estados (str): nome do ficheiro com os estados das tarefas

    Devolve:
        None
    """
    valida_argumento(ficheiro_tarefas, str)
    valida_argumento(ficheiro_estados, str)
    valida_csv(ficheiro_tarefas)
    valida_csv(ficheiro_estados)

    with open(ficheiro_tarefas, 'r') as tarefas_csv:
        reader_tarefas = csv.reader(tarefas_csv)

        tarefas.clear()
        estado_programa['tarefa_id'] = 1

        for i, row in enumerate(reader_tarefas):
            if i == 0:
                pass
            else:
                descricao, prazo, data_criacao = row
                tarefa_id = estado_programa['tarefa_id']
                cria_tarefa(descricao, prazo, data_criacao)
                with open(ficheiro_estados, 'r') as estados_csv:
                    reader_estados = csv.reader(estados_csv)
                    for i2, row2 in enumerate(reader_estados):
                        if i2 == 0:
                            pass
                        else:
                            tarefa_id_csv, \
                                estado, \
                                data_modificacao, \
                                empregado_id = row2

                            tarefa_id_csv = int(tarefa_id_csv)

                            if empregado_id == '':
                                empregado_id = None
                            else:
                                empregado_id = int(empregado_id)

                            if tarefa_id_csv > tarefa_id:
                                break
                            elif tarefa_id_csv == tarefa_id:
                                modifica_estado(tarefa_id,
                                                estado,
                                                data_modificacao,
                                                empregado_id)


def guarda_tarefas(ficheiro_tarefas: str, ficheiro_estados: str):
    """
    Cria dois ficheiros csv, ficheiro_tarefas e ficheiro_estados,
    com dados das tarefas e estados das tarefas, respectivamente

    Ordem dos dados em ficheiro_tarefas:
    'descricao', 'prazo', 'criacao'

    Ordem dos dados em ficheiro_estados:
    'tarefa_id', 'tipo', 'data', 'empregado_id'

    Argumentos:
        ficheiro_tarefas (str): nome do ficheiro para as tarefas
        ficheiro_estados (str): nome do ficheiro para os estados das tarefas

    Devolve:
        None
    """
    valida_argumento(ficheiro_tarefas, str)
    valida_argumento(ficheiro_estados, str)

    with open(ficheiro_tarefas, 'w') as tarefas_csv:
        tarefas_writer = csv.writer(tarefas_csv)
        tarefas_writer.writerow(['descricao', 'prazo', 'criacao'])

        with open(ficheiro_estados, 'w') as estados_csv:
            estados_writer = csv.writer(estados_csv)
            estados_writer.writerow(
                ['tarefa_id', 'tipo', 'data', 'empregado_id'])

            for tarefa_chave, tarefa in tarefas.items():
                tarefas_writer.writerow([tarefa["descricao"],
                                        str(tarefa["prazo"]),
                                        str(tarefa["estados"][0][1])])

                for i, estado in enumerate(tarefa['estados']):
                    if i == 0:
                        pass
                    else:
                        if estado[2] is None:
                            empregado_id = ''
                        else:
                            empregado_id = estado[2]

                        estados_writer.writerow([tarefa_chave,
                                                estado[0],
                                                str(estado[1]),
                                                empregado_id])


def gera_resumo_diario(data: str):
    """
    Devolve um resumo das tarefas filtrados conforme data.

    Argumentos:
        data (str): data, no formato 'YYYY-MM-DD', usada para filtrar os
            registros no dicionário tarefas

    Devolve:
        tuplo: dados do resumo diario, no formado (
            data do resumo (str),
            data de geração do resumo (str),
            lista de tarefas alteradas em 'data' (tuplo),
            lista de tarefas atrasadas em 'data' e não finalizadas (tuplo)
        )

    Levanta:
        ValueError: Se data estiver em formato inválido
    """
    valida_argumento(data, str)
    if not valida_data(data):
        raise ValueError('data de modificação com formato inválido')

    tarefas_alteradas = []
    for tarefa in tarefas.values():
        for estado in tarefa['estados']:
            if estado[1] == datetime.date.fromisoformat(data):
                descricao = tarefa['descricao']
                tipo_estado = estado[0]

                if tipo_estado == 'ATRIBUÍDA':
                    id_empregado = estado[2]
                else:
                    id_empregado = tarefa['empregado_id']

                if id_empregado is None:
                    nome_empregado = ''
                else:
                    nome_empregado = empregados[id_empregado]['nome']

                tarefa_alterada = (descricao,
                                   tipo_estado,
                                   nome_empregado)
                tarefas_alteradas.append(tarefa_alterada)
                break

    tarefas_atrasadas = []
    for tarefa in tarefas.values():
        ultimo_estado = tarefa['estados'][-1]
        if tarefa['prazo'] < datetime.date.fromisoformat(data) and \
            (ultimo_estado[0] != 'FINALIZADA' or
             (ultimo_estado[0] == 'FINALIZADA' and
              ultimo_estado[1] > datetime.date.fromisoformat(data))):
            for estado in tarefa['estados']:
                if estado[1] == datetime.date.fromisoformat(data):
                    descricao = tarefa['descricao']
                    prazo = str(tarefa['prazo'])
                    tipo_estado = estado[0]

                    if tipo_estado == 'ATRIBUÍDA':
                        id_empregado = estado[2]
                    else:
                        id_empregado = tarefa['empregado_id']

                    if id_empregado is None:
                        nome_empregado = ''
                    else:
                        nome_empregado = empregados[id_empregado]['nome']

                    tarefa_atrasada = (descricao,
                                       prazo,
                                       tipo_estado,
                                       nome_empregado)
                    tarefas_atrasadas.append(tarefa_atrasada)
                    break

    resumo = (data,
              str(estado_programa['hoje']),
              tarefas_alteradas,
              tarefas_atrasadas
              )
    return resumo


def imprime_resumo(resumo):
    """
    Imprime informações de um resumo diário

    Argumentos:
        resumo (tuplo): dados do resumo diario, no formado (
            data do resumo (str),
            data de geração do resumo (str),
            lista de tarefas alteradas em 'data' (tuplo),
            lista de tarefas atrasadas em 'data' e não finalizadas (tuplo)
        )

    Devolve:
        None
    """
    print('-' * 50)
    print(f'DATA DO RESUMO: {resumo[0]}')
    print(f'DATA DE CRIAÇÃO: {resumo[1]}')
    print('-' * 50)
    print(f'{" " * 13}** ESTADO DAS TAREFAS **')
    print('-' * 50)
    for tarefa in resumo[2]:
        print(tarefa[0])
        print(tarefa[1])
        if tarefa[2] != '':
            print(tarefa[2])
        print()
    print('-' * 50)
    print(f'{" " * 13}** TAREFAS EM ATRASO **')
    print('-' * 50)
    for tarefa in resumo[3]:
        print(tarefa[0])
        print(f'PRAZO: {tarefa[1]}')
        print(tarefa[2])
        if tarefa[3] != '':
            print(tarefa[3])
        print()
    print('-' * 50)


def cria_empregado(nif: str, nome: str, data_nasc: str, cargo: str):
    """
    Adiciona um novo empregado ao dicionário empregados

    Argumentos:
        nif (str): nif do funcionário
        nome (str): nome do usuário
        data_nasc (str): data de nascimento do usuário no formato 'YYYY-MM-DD'
        cargo (str): cargo do funcionário --> 'EMPREGADO' ou 'GESTOR'

    Devolve:
        int: id do novo empregado registrado

    Levanta:
        ValueError: Se tipo de possuir mais de 9 caracteres
        ValueError: Se nome exceder 50 caracteres
        ValueError: Se data de nascimento estiver num formato inválido
        ValueError: Se cargo não for um dos 2 valores permitidos
    """
    valida_argumento(nif, str)
    valida_argumento(nome, str)
    valida_argumento(data_nasc, str)
    valida_argumento(cargo, str)

    if len(nif) > 9:
        raise ValueError('nif não pode exceder os 9 caracteres')

    if len(nome) > 50:
        raise ValueError('nome não pode exceder os 50 caracteres')

    if not valida_data(data_nasc):
        raise ValueError('data de nascimento com formato inválido')

    if cargo not in ['EMPREGADO', 'GESTOR']:
        raise ValueError('cargo inválido')

    empregado_id = estado_programa['empregado_id']
    empregados[empregado_id] = {'nif': nif,
                                'nome': nome,
                                'data_nasc':
                                datetime.date.fromisoformat(data_nasc),
                                'cargo': cargo,
                                'tarefas_id': []}

    estado_programa['empregado_id'] += 1
    return empregado_id


def carrega_empregados(nome_ficheiro: str):
    """
    Utiliza um ficheiro csv com dados de empregados para preencher o
    dicionário empregados

    Argumentos:
        nome_ficheiro (str): nome do ficheiro csv com os dados dos empregados

    Devolve:
        None
    """
    valida_argumento(nome_ficheiro, str)
    valida_csv(nome_ficheiro)

    with open(nome_ficheiro, 'r') as empregados_csv:
        reader_empregados = csv.reader(empregados_csv)
        empregados.clear()
        estado_programa['empregado_id'] = 1

        for i, row in enumerate(reader_empregados):
            if i == 0:
                pass
            else:
                nif, nome, data_nasc, cargo = row
                cria_empregado(nif, nome, data_nasc, cargo)


def guarda_empregados(nome_ficheiro: str):
    """
    Cria um ficheiro csv com dados do dicionário empregados
    Ordem dos dados:
    'nif', 'nome', 'data_nasc', 'cargo'

    Argumentos:
        nome_ficheiro (str): nome do ficheiro a ser criado

    Devolve:
        None
    """
    valida_argumento(nome_ficheiro, str)

    with open(nome_ficheiro, 'w') as empregados_csv:
        empregados_writer = csv.writer(empregados_csv)
        empregados_writer.writerow(['nif', 'nome', 'data_nasc', 'cargo'])

        for empregado in empregados.values():
            empregados_writer.writerow([empregado['nif'],
                                       empregado['nome'],
                                       str(empregado['data_nasc']),
                                       empregado['cargo']])


def imprime_tarefas(empregado_id: int):
    """
    Imprime informações sobre todas as tarefas não finalizadas associadas
    a um empregado com identificador empregado_id no dicionário empregados.

    Argumentos:
        empregado_id (int): id do empregado no dicionário empregados

    Devolve:
        None
    """
    valida_argumento(empregado_id, int)
    valida_empregado(empregado_id)

    print('-' * 50)
    print(f'NOME DO EMPREGADO: {empregados[empregado_id]["nome"]}')
    print('-' * 50)
    print(f'{" " * 13}** TAREFAS A REALIZAR **')
    print('-' * 50)
    for tarefa_id in empregados[empregado_id]['tarefas_id']:
        tarefa = tarefas[tarefa_id]
        if tarefa['estados'][-1][0] != 'FINALIZADA':
            print(tarefa['descricao'])
            print(tarefa['estados'][-1][0])
            print(str(tarefa['prazo']))
            print()
    print('-' * 50)


def inicia_dia(data: str = None):
    """
    Devolve um resumo diário da nova data atual

    Argumentos:
        data (str): (Opcional) nova data desejada, no formato 'YYYY-MM-DD'

    Devolve:
        tuplo: resumo da nova data, obtido utilizando a função
            'gera_resumo_diario'

    Levanta:
        ValueError: Se formato da data for inválido
    """
    valida_argumento(data, str)
    if not valida_data(data):
        raise ValueError('data com formato inválido')

    if data is None:
        estado_programa['hoje'] += datetime.timedelta(days=1)
        return gera_resumo_diario(str(estado_programa['hoje']))
    else:
        estado_programa['hoje'] = datetime.date.fromisoformat(data)
        return gera_resumo_diario(data)
