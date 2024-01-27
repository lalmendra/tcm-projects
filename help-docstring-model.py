    """
    DescriçãoXXX

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
        
        tipo (string): tipo do veículo --> 'MOTOCICLO' ou 'CARRO'
        
        matricula (string): matrícula do veículo, no formato 'YY-YY-YY', onde Y pode ser um número ou letra maiúscula
        
        marca (string): marca do veículo, mínimo 1 e máximo 25 caracteres
        
        reparacoes (lista): registro de reparações do veículo, lista contendo outras listas no formato [
            id_reparacao (inteiro), 
            data_entrada (tuplo),
            data_estimada (tuplo),
            data_entrega (tuplo)            
        ]


        id_reparacao (inteiro): ID de reparação, número inteiro positivo
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
        data_entrega (tuplo): data de entrega ao cliente, no formato (
            dia (int),
            mês (int),
            ano (int)
        )

    Devolve:
        XXXX

    Levanta:
        XXXX
    """
