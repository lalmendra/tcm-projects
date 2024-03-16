import sys
import unittest
import unittest.mock
import p2
import datetime

from p2 import *
from io import StringIO
from tempfile import NamedTemporaryFile


class TestProjeto2(unittest.TestCase):
    def setUp(self):
        p2.estado_programa = {
            "hoje": datetime.date.today(),
            "empregado_id": 1,
            "tarefa_id": 1,
        }
        p2.tarefas = {}
        p2.empregados = {}


class TestProjeto2ComDados(unittest.TestCase):
    def setUp(self) -> None:
        p2.estado_programa = {
            "hoje": datetime.date.today(),
            "empregado_id": 2,
            "tarefa_id": 3,
        }
        self.tarefas = {
            1: {
                "descricao": "tarefa 1",
                "prazo": datetime.date(2022, 1, 1),
                "estados": [
                    ("POR ATRIBUIR", datetime.date(2021, 1, 1), None),
                    ("ATRIBUÍDA", datetime.date(2021, 1, 2), 1),
                ],
                "empregado_id": 1,
            },
            2: {
                "descricao": "tarefa 2",
                "prazo": datetime.date(2021, 1, 1),
                "estados": [
                    ("POR ATRIBUIR", datetime.date(2021, 1, 1), None),
                    ("ATRIBUÍDA", datetime.date(2021, 1, 2), 1),
                    ("FINALIZADA", datetime.date(2021, 1, 3), None),
                ],
                "empregado_id": 1,
            },
            3: {
                "descricao": "tarefa 3",
                "prazo": datetime.date(2022, 1, 1),
                "estados": [("POR ATRIBUIR", datetime.date(2021, 1, 1), None)],
                "empregado_id": None,
            },
        }
        p2.tarefas = self.tarefas
        self.empregados = {
            1: {
                "nif": "987654321",
                "nome": "Manuel Silva",
                "data_nasc": datetime.date(2000, 1, 1),
                "cargo": "GESTOR",
                "tarefas_id": [1, 2],
            },
            2: {
                "nif": "524353422",
                "nome": "Maria Santos",
                "data_nasc": datetime.date(2010, 3, 11),
                "cargo": "EMPREGADO",
                "tarefas_id": [2, 4],
            },
        }
        p2.empregados = self.empregados


class TestCriaTarefa(TestProjeto2):
    def test_cria_tarefa(self):
        tarefa_id = cria_tarefa("tarefa 1", "2022-01-01", "2021-01-01")
        self.assertEqual(tarefa_id, 1)
        self.assertEqual(p2.tarefas[1]["descricao"], "tarefa 1")
        self.assertEqual(p2.tarefas[1]["prazo"], datetime.date(2022, 1, 1))
        self.assertEqual(
            p2.tarefas[1]["estados"],
            [("POR ATRIBUIR", datetime.date(2021, 1, 1), None)],
        )
        self.assertIsNone(p2.tarefas[1]["empregado_id"])
        self.assertEqual(p2.estado_programa["tarefa_id"], 2)

    def test_cria_tarefa_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            cria_tarefa(1, "2022-01-01", "2021-01-01")
        self.assertEqual(str(ctx.exception), "argumento com tipo inválido")

    def test_cria_tarefa_invalido_descricao_longa(self):
        with self.assertRaises(ValueError) as ctx:
            cria_tarefa("a" * 257, "2022-01-01", "2021-01-01")
        self.assertEqual(
            str(ctx.exception), "descrição excede o limite de 256 caracteres"
        )

    def test_cria_tarefa_invalido_prazo(self):
        with self.assertRaises(ValueError) as ctx:
            cria_tarefa("tarefa 1", "2022-01-32", "2021-01-01")
        self.assertEqual(str(ctx.exception), "prazo com formato inválido")

    def test_cria_tarefa_invalido_data_criacao(self):
        with self.assertRaises(ValueError) as ctx:
            cria_tarefa("tarefa 1", "2022-01-01", "2021-01-32")
        self.assertEqual(str(ctx.exception),
                         "data de criação com formato inválido")


class TestModificaEstado(TestProjeto2ComDados):
    def test_modifica_estado_atribuida(self):
        modifica_estado(3, "ATRIBUÍDA", "2021-01-02", empregado_id=1)
        self.assertEqual(
            p2.tarefas[3]["estados"],
            [
                ("POR ATRIBUIR", datetime.date(2021, 1, 1), None),
                ("ATRIBUÍDA", datetime.date(2021, 1, 2), 1),
            ],
        )
        self.assertEqual(p2.empregados[1]["tarefas_id"], [1, 2, 3])
        self.assertEqual(p2.tarefas[3]["empregado_id"], 1)

    def test_modifica_estado_por_atribuir(self):
        self.assertEqual(p2.tarefas[1]["empregado_id"], 1)
        modifica_estado(1, "POR ATRIBUIR", "2021-01-03")
        self.assertIsNone(p2.tarefas[1]["empregado_id"])
        self.assertEqual(
            p2.tarefas[1]["estados"],
            [
                ("POR ATRIBUIR", datetime.date(2021, 1, 1), None),
                ("ATRIBUÍDA", datetime.date(2021, 1, 2), 1),
                ("POR ATRIBUIR", datetime.date(2021, 1, 3), None),
            ],
        )
        self.assertEqual(p2.empregados[1]["tarefas_id"], [2])

    def test_modifica_estado_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            modifica_estado("oh no", "ATRIBUÍDA", "2021-01-02", empregado_id=1)
        self.assertEqual(str(ctx.exception), "argumento com tipo inválido")

    def test_modifica_estado_tarefa_inexistente(self):
        with self.assertRaises(ValueError) as ctx:
            modifica_estado(4, "ATRIBUÍDA", "2021-01-02", empregado_id=1)
        self.assertEqual(str(ctx.exception), "tarefa inexistente")

    def test_modifica_estado_invalido_estado(self):
        with self.assertRaises(ValueError) as ctx:
            modifica_estado(1, "ATRIBUIDA", "2021-01-02", empregado_id=1)
        self.assertEqual(str(ctx.exception), "estado inválido")

    def test_modifica_estado_finalizada(self):
        with self.assertRaises(ValueError) as ctx:
            modifica_estado(2, "EM PROGRESSO", "2021-01-04")
        self.assertEqual(str(ctx.exception), "tarefa encontra-se finalizada")

    def test_modifica_estado_invalido_atribuida(self):
        with self.assertRaises(ValueError) as ctx:
            modifica_estado(3, "ATRIBUÍDA", "2021-01-02", empregado_id=None)
        self.assertEqual(
            str(ctx.exception),
            "identificador do empregado responsável não pode ser vazio",
        )

    def test_modifica_estado_empregado_inexistente(self):
        with self.assertRaises(ValueError) as ctx:
            modifica_estado(3, "ATRIBUÍDA", "2021-01-02", empregado_id=3)
        self.assertEqual(str(ctx.exception), "empregado inexistente")

    def test_modifica_estado_sem_empregado_responsavel(self):
        with self.assertRaises(ValueError) as ctx:
            modifica_estado(3, "EM PROGRESSO", "2021-01-03")
        self.assertEqual(str(ctx.exception),
                         "tarefa não tem empregado responsável")


class TestCarregaTarefas(TestProjeto2ComDados):
    def setUp(self):
        super().setUp()
        self.ficheiro_tarefas = NamedTemporaryFile(mode="w", delete=False)
        self.ficheiro_estados = NamedTemporaryFile(mode="w", delete=False)
        self.ficheiro_tarefas.write(
            "descricao,prazo,criacao\n"
            "Resolver bug #31 reportado pela empresa XPTO,2024-03-01,2024-01-05\n"
            "Concluir venda do produto Y,2024-05-01,2024-02-02\n"
        )
        self.ficheiro_tarefas.flush()
        self.ficheiro_estados.write(
            "tarefa_id,tipo,data,empregado_id\n"
            "1,ATRIBUÍDA,2024-01-07,1\n"
            "1,EM PROGRESSO,2024-01-08,\n"
        )
        self.ficheiro_estados.flush()

    def tearDown(self):
        self.ficheiro_tarefas.close()
        self.ficheiro_estados.close()

    def test_carrega_tarefas(self):
        carrega_tarefas(self.ficheiro_tarefas.name, self.ficheiro_estados.name)
        self.assertEqual(
            p2.tarefas[1],
            {
                "descricao": "Resolver bug #31 reportado pela empresa XPTO",
                "prazo": datetime.date(2024, 3, 1),
                "estados": [
                    ("POR ATRIBUIR", datetime.date(2024, 1, 5), None),
                    ("ATRIBUÍDA", datetime.date(2024, 1, 7), 1),
                    ("EM PROGRESSO", datetime.date(2024, 1, 8), None),
                ],
                "empregado_id": 1,
            },
        )
        self.assertEqual(
            p2.tarefas[2],
            {
                "descricao": "Concluir venda do produto Y",
                "prazo": datetime.date(2024, 5, 1),
                "estados": [("POR ATRIBUIR", datetime.date(2024, 2, 2), None)],
                "empregado_id": None,
            },
        )
        self.assertEqual(len(p2.tarefas), 2)
        self.assertEqual(p2.estado_programa["tarefa_id"], 3)

    def test_carrega_tarefas_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            carrega_tarefas(1, self.ficheiro_estados.name)
        self.assertEqual(str(ctx.exception), "argumento com tipo inválido")

    def test_carrega_tarefas_ficheiro_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            carrega_tarefas("ficheiro_invalido.csv",
                            self.ficheiro_estados.name)
        self.assertEqual(str(ctx.exception), "erro a abrir o ficheiro")
        self.assertEqual(p2.tarefas, self.tarefas)
        self.assertEqual(p2.estado_programa["tarefa_id"], 3)


class TestGuardaTarefas(TestProjeto2ComDados):
    def setUp(self):
        super().setUp()
        self.ficheiro_tarefas = NamedTemporaryFile(mode="w", delete=False)
        self.ficheiro_estados = NamedTemporaryFile(mode="w", delete=False)

    def tearDown(self):
        self.ficheiro_tarefas.close()
        self.ficheiro_estados.close()

    def test_guarda_tarefas(self):
        guarda_tarefas(self.ficheiro_tarefas.name, self.ficheiro_estados.name)
        with open(self.ficheiro_tarefas.name, "r") as f:
            self.assertEqual(
                f.read(),
                "descricao,prazo,criacao\n"
                "tarefa 1,2022-01-01,2021-01-01\n"
                "tarefa 2,2021-01-01,2021-01-01\n"
                "tarefa 3,2022-01-01,2021-01-01\n",
            )
        with open(self.ficheiro_estados.name, "r") as f:
            self.assertEqual(
                f.read(),
                "tarefa_id,tipo,data,empregado_id\n"
                "1,ATRIBUÍDA,2021-01-02,1\n"
                "2,ATRIBUÍDA,2021-01-02,1\n"
                "2,FINALIZADA,2021-01-03,\n",
            )

    def test_guarda_tarefas_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            guarda_tarefas(1, self.ficheiro_estados.name)
        self.assertEqual(str(ctx.exception), "argumento com tipo inválido")


class TestGeraResumoDiario(TestProjeto2ComDados):
    def test_gera_resumo_diario(self):
        resumo = gera_resumo_diario("2021-01-03")
        self.assertEqual(len(resumo), 4)
        self.assertEqual(resumo[0], "2021-01-03")
        self.assertEqual(resumo[1], str(datetime.date.today()))
        self.assertEqual(len(resumo[2]), 1)
        self.assertEqual(resumo[2][0][0], "tarefa 2")
        self.assertEqual(resumo[2][0][1], "FINALIZADA")
        self.assertEqual(resumo[2][0][2], "Manuel Silva")
        self.assertEqual(len(resumo[3]), 0)

    def test_gera_resumo_diario_tarefas_atrasadas(self):
        # Remove estado FINALIZADA
        p2.tarefas[2]["estados"].pop()
        # Adiciona estado EM PROGRESSO **após** data do resumo
        p2.tarefas[2]["estados"].append(
            ("EM PROGRESSO", datetime.date(2021, 1, 3), None)
        )

        resumo = gera_resumo_diario("2021-01-02")
        self.assertEqual(len(resumo[3]), 1)
        self.assertEqual(resumo[3][0][0], "tarefa 2")
        self.assertEqual(resumo[3][0][1], "2021-01-01")
        self.assertEqual(resumo[3][0][2], "ATRIBUÍDA")
        self.assertEqual(resumo[3][0][3], "Manuel Silva")

    def test_gera_resumo_diario_tarefas_atrasadas_reatribuida(self):
        # Remove estado FINALIZADA
        p2.tarefas[2]["estados"].pop()
        # Atribuí tarefa a outro empregado **após** data do resumo
        p2.tarefas[2]["estados"].append(
            ("EM ATRIBUÍDA", datetime.date(2021, 1, 3), 2))
        p2.tarefas[2]["empregado_id"] = 2

        resumo = gera_resumo_diario("2021-01-02")
        self.assertEqual(len(resumo[3]), 1)
        self.assertEqual(resumo[3][0][0], "tarefa 2")
        self.assertEqual(resumo[3][0][1], "2021-01-01")
        self.assertEqual(resumo[3][0][2], "ATRIBUÍDA")
        self.assertEqual(resumo[3][0][3], "Manuel Silva")

    def test_gera_resumo_diario_estados_tarefa_reatribuida(self):
        # Atribuí tarefa a outro empregado **após** data do resumo
        p2.tarefas[1]["estados"].append(
            ("EM ATRIBUÍDA", datetime.date(2021, 1, 3), 2))
        p2.tarefas[1]["empregado_id"] = 2

        resumo = gera_resumo_diario("2021-01-02")
        self.assertEqual(len(resumo), 4)
        self.assertEqual(resumo[0], "2021-01-02")
        self.assertEqual(resumo[1], str(datetime.date.today()))
        self.assertEqual(len(resumo[2]), 2)
        self.assertEqual(resumo[2][0][0], "tarefa 1")
        self.assertEqual(resumo[2][0][1], "ATRIBUÍDA")
        self.assertEqual(resumo[2][0][2], "Manuel Silva")
        self.assertEqual(resumo[2][1][0], "tarefa 2")
        self.assertEqual(resumo[2][1][1], "ATRIBUÍDA")
        self.assertEqual(resumo[2][1][2], "Manuel Silva")
        self.assertEqual(len(resumo[3]), 1)
        self.assertEqual(resumo[3][0][0], "tarefa 2")
        self.assertEqual(resumo[3][0][1], "2021-01-01")
        self.assertEqual(resumo[3][0][2], "ATRIBUÍDA")
        self.assertEqual(resumo[3][0][3], "Manuel Silva")


class TestImprimeResumo(unittest.TestCase):
    def setUp(self) -> None:
        sys.stdout = self._stringio = StringIO()
        self.maxDiff = None

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__

    def test_imprime_resumo(self):
        resumo = (
            "2024-04-01",
            "2024-04-02",
            [
                (
                    "Resolver bug #31 reportado pela empresa XPTO",
                    "EM PROGRESSO",
                    "Manuel Silva",
                ),
                ("Concluir venda do produto Y", "POR ATRIBUIR", ""),
            ],
            [
                (
                    "Resolver bug #31 reportado pela empresa XPTO",
                    "2024-03-01",
                    "EM PROGRESSO",
                    "Manuel Silva",
                ),
                ("Concluir venda do produto Y", "2024-03-01", "POR ATRIBUIR", ""),
            ],
        )
        imprime_resumo(resumo)
        self.assertEqual(
            self._stringio.getvalue(),
            """--------------------------------------------------
DATA DO RESUMO: 2024-04-01
DATA DE CRIAÇÃO: 2024-04-02
--------------------------------------------------
             ** ESTADO DAS TAREFAS **
--------------------------------------------------
Resolver bug #31 reportado pela empresa XPTO
EM PROGRESSO
Manuel Silva

Concluir venda do produto Y
POR ATRIBUIR

--------------------------------------------------
             ** TAREFAS EM ATRASO **
--------------------------------------------------
Resolver bug #31 reportado pela empresa XPTO
PRAZO: 2024-03-01
EM PROGRESSO
Manuel Silva

Concluir venda do produto Y
PRAZO: 2024-03-01
POR ATRIBUIR

--------------------------------------------------\n""",
        )


class TestCriaEmpregado(TestProjeto2):
    def test_cria_empregado(self):
        empregado_id = cria_empregado(
            "987654321", "Manuel Silva", "2000-01-01", "GESTOR"
        )
        self.assertEqual(empregado_id, 1)
        self.assertEqual(p2.empregados[1]["nif"], "987654321")
        self.assertEqual(p2.empregados[1]["nome"], "Manuel Silva")
        self.assertEqual(
            p2.empregados[1]["data_nasc"], datetime.date(2000, 1, 1))
        self.assertEqual(p2.empregados[1]["cargo"], "GESTOR")
        self.assertEqual(p2.empregados[1]["tarefas_id"], [])
        self.assertEqual(p2.estado_programa["empregado_id"], 2)

    def test_cria_empregado_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            cria_empregado(987654321, "Manuel Silva", "2000-01-01", "GESTOR")
        self.assertEqual(str(ctx.exception), "argumento com tipo inválido")

    def test_cria_empregado_invalido_nif(self):
        with self.assertRaises(ValueError) as ctx:
            cria_empregado("9876543210", "Manuel Silva",
                           "2000-01-01", "GESTOR")
        self.assertEqual(str(ctx.exception),
                         "nif não pode exceder os 9 caracteres")

    def test_cria_empregado_invalido_nome(self):
        with self.assertRaises(ValueError) as ctx:
            cria_empregado("987654321", "a" * 51, "2000-01-01", "GESTOR")
        self.assertEqual(str(ctx.exception),
                         "nome não pode exceder os 50 caracteres")

    def test_cria_empregado_invalido_data_nasc(self):
        with self.assertRaises(ValueError) as ctx:
            cria_empregado("987654321", "Manuel Silva", "2000-01-32", "GESTOR")
        self.assertEqual(str(ctx.exception),
                         "data de nascimento com formato inválido")


class TestCarregaEmpregados(TestProjeto2ComDados):
    def setUp(self):
        super().setUp()
        self.ficheiro = NamedTemporaryFile(mode="w", delete=False)
        self.ficheiro.write(
            "nif,nome,data_nasc,cargo\n"
            "987654321,José Silva,2000-01-01,GESTOR\n"
            "524353422,Manuela Santos,2010-03-11,EMPREGADO\n"
        )
        self.ficheiro.flush()

    def tearDown(self):
        self.ficheiro.close()

    def test_carrega_empregados(self):
        carrega_empregados(self.ficheiro.name)
        self.assertEqual(len(p2.empregados), 2)
        self.assertEqual(
            p2.empregados[1],
            {
                "nif": "987654321",
                "nome": "José Silva",
                "data_nasc": datetime.date(2000, 1, 1),
                "cargo": "GESTOR",
                "tarefas_id": [],
            },
        )
        self.assertEqual(
            p2.empregados[2],
            {
                "nif": "524353422",
                "nome": "Manuela Santos",
                "data_nasc": datetime.date(2010, 3, 11),
                "cargo": "EMPREGADO",
                "tarefas_id": [],
            },
        )
        self.assertEqual(len(p2.empregados), 2)
        self.assertEqual(p2.estado_programa["empregado_id"], 3)

    def test_carrega_empregados_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            carrega_empregados(1)
        self.assertEqual(str(ctx.exception), "argumento com tipo inválido")

    def test_carrega_empregados_ficheiro_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            carrega_empregados("ficheiro_invalido.csv")
        self.assertEqual(str(ctx.exception), "erro a abrir o ficheiro")
        self.assertEqual(p2.empregados, self.empregados)
        self.assertEqual(p2.estado_programa["empregado_id"], 2)


class TestGuardaEmpregados(TestProjeto2ComDados):
    def setUp(self):
        super().setUp()
        self.ficheiro = NamedTemporaryFile(mode="w", delete=False)

    def tearDown(self):
        self.ficheiro.close()

    def test_guarda_empregados(self):
        guarda_empregados(self.ficheiro.name)
        with open(self.ficheiro.name, "r") as f:
            self.assertEqual(
                f.read(),
                "nif,nome,data_nasc,cargo\n"
                "987654321,Manuel Silva,2000-01-01,GESTOR\n"
                "524353422,Maria Santos,2010-03-11,EMPREGADO\n",
            )

    def test_guarda_empregados_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            guarda_empregados(1)
        self.assertEqual(str(ctx.exception), "argumento com tipo inválido")


class TestImprimeTarefas(TestProjeto2ComDados):
    def setUp(self) -> None:
        sys.stdout = self._stringio = StringIO()
        self.maxDiff = None

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__

    def test_imprime_tarefas(self):
        imprime_tarefas(1)
        self.assertEqual(
            self._stringio.getvalue(),
            """--------------------------------------------------
NOME DO EMPREGADO: Manuel Silva
--------------------------------------------------
             ** TAREFAS A REALIZAR **
--------------------------------------------------
tarefa 1
ATRIBUÍDA
2022-01-01

--------------------------------------------------
""",
        )

    def test_imprime_tarefas_empregado_inexistente(self):
        with self.assertRaises(ValueError) as ctx:
            imprime_tarefas(3)
        self.assertEqual(str(ctx.exception), "empregado inexistente")


class TestIniciaDia(TestProjeto2ComDados):
    def test_inicia_dia(self):
        resumo = inicia_dia("2021-01-02")
        self.assertEqual(p2.estado_programa["hoje"], datetime.date(2021, 1, 2))
        self.assertEqual(resumo, gera_resumo_diario("2021-01-02"))

    def test_inicia_dia_invalido_data(self):
        with self.assertRaises(ValueError) as ctx:
            inicia_dia("2021-01-32")
        self.assertEqual(str(ctx.exception), "data com formato inválido")

    def test_inicia_dia_chama_resumo_diario(self):
        with unittest.mock.patch("p2.gera_resumo_diario") as mock_resumo:
            inicia_dia("2021-01-02")
            mock_resumo.assert_called_once_with("2021-01-02")


if __name__ == "__main__":
    unittest.main()
