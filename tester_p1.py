import sys
import unittest
import p1

from p1 import *
from io import StringIO


class TestValidaNif(unittest.TestCase):
    def test_nif_valido(self):
        self.assertTrue(valida_nif("219072230"))

    def test_nif_invalido_1(self):
        self.assertFalse(valida_nif("219172230"))

    def test_nif_invalido_2(self):
        self.assertFalse(valida_nif("290"))


class TestAdicionaVeiculo(unittest.TestCase):
    def setUp(self):
        self.cliente = (
            "António Manuel da Silva",
            "219072230",
            "912345678",
            [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
        )

    def test_adiciona_veiculo_valido(self):
        veiculo = ("CARRO", "BB-01-02", "BMW", [])
        adiciona_veiculo(self.cliente, veiculo)
        self.assertEqual(self.cliente[3][1], veiculo)

    def test_adiciona_veiculo_invalido_1(self):
        veiculo = ("CARRO", "Bc-01-02", "BMW", [])
        with self.assertRaises(ValueError) as ctx:
            adiciona_veiculo(self.cliente, veiculo)
        self.assertEqual(str(ctx.exception), "matrícula inválida")

    def test_adiciona_veiculo_invalido_2(self):
        veiculo = ("CARRO", "BB-01-02", "BMW", [])
        adiciona_veiculo(self.cliente, veiculo)
        with self.assertRaises(ValueError) as ctx:
            adiciona_veiculo(self.cliente, veiculo)
        self.assertEqual(
            str(ctx.exception), "veículo já se encontra associado a este cliente"
        )

    def test_adiciona_veiculo_invalido_3(self):
        veiculo = ("AUTOCARRO", "BB-01-02", "BMW", [])
        with self.assertRaises(ValueError) as ctx:
            adiciona_veiculo(self.cliente, veiculo)
        self.assertEqual(str(ctx.exception), "tipo de veículo inválido")

    def test_adiciona_veiculo_invalido_4(self):
        veiculo = ("CARRO", "BB-01-02", "BMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM", [])
        with self.assertRaises(ValueError) as ctx:
            adiciona_veiculo(self.cliente, veiculo)
        self.assertEqual(str(ctx.exception), "marca inválida")


class TestAdicionaCliente(unittest.TestCase):
    def setUp(self) -> None:
        p1.clientes = [("José Maria Rebelo de Sousa", "248537474", "918765432", [])]

    def test_adiciona_cliente_valido(self):
        adiciona_cliente(
            "António Manuel da Silva",
            "219072230",
            "912345678",
            [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
        )
        self.assertEqual(
            p1.clientes[1],
            (
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
            ),
        )

    def test_adiciona_cliente_valido_2(self):
        adiciona_cliente(
            "António Manuel da Silva",
            "219072230",
            "912345678",
            [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
        )
        adiciona_cliente(
            "António Manuel da Silva",
            "219072230",
            "912345678",
            [("MOTOCICLO", "BB-01-02", "SUZUKI", [])],
        )
        self.assertEqual(
            p1.clientes[1],
            (
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [
                    ("MOTOCICLO", "AA-01-02", "SUZUKI", []),
                    ("MOTOCICLO", "BB-01-02", "SUZUKI", []),
                ],
            ),
        )

    def test_adiciona_cliente_invalido_1(self):
        with self.assertRaises(ValueError) as ctx:
            adiciona_cliente(
                "fgLEo0krmOwRfqFNrK4ZA1WADNsNuhG6uLP8sT04FcJbiYo1xCuBwRW2VXtg5UruJ1DXUioLRxMXR1EwLRNHAWyDCKdz44VQ47oXLvVRYpjauuT4Ms5AMGIpTTNhjPsnyH3bQ77Hovl6vw9gJbvFi8M1Hh69gSAVMpIPlWYARe3ogiBcZw0sOopUbf5pqHBUi7GFXJZaUYb3cmeuvTeUZ019f35fVhkViEd4aU2B2LYNI3s7jwzmxzaUKAcWOEwe",
                "219072230",
                "912345678",
                [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
            )
        self.assertEqual(str(ctx.exception), "nome completo inválido")

    def test_adiciona_cliente_invalido_2(self):
        with self.assertRaises(ValueError) as ctx:
            adiciona_cliente(
                "António Manuel da Silva",
                "219172230",
                "912345678",
                [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
            )
        self.assertEqual(str(ctx.exception), "NIF inválido")

    def test_adiciona_cliente_invalido_3(self):
        with self.assertRaises(ValueError) as ctx:
            adiciona_cliente(
                "António Manuel da Silva",
                "219072230",
                "812345678",
                [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
            )
        self.assertEqual(str(ctx.exception), "número de telemóvel inválido")

    def test_adiciona_cliente_invalido_4(self):
        with self.assertRaises(ValueError) as ctx:
            adiciona_cliente(
                "José Maria Rebelo",
                "248537474",
                "912345678",
                [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
            )
        self.assertEqual(str(ctx.exception), "nome completo incoerente")

    def test_adiciona_cliente_invalido_5(self):
        adiciona_cliente(
            "António Manuel da Silva",
            "219072230",
            "912345678",
            [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
        )
        with self.assertRaises(ValueError) as ctx:
            adiciona_cliente(
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
            )
        self.assertEqual(
            str(ctx.exception), "veículo já se encontra associado a este cliente"
        )


class TestRemoveCliente(unittest.TestCase):
    def setUp(self) -> None:
        p1.clientes = [
            ("José Maria Rebelo de Sousa", "248537474", "918765432", []),
            (
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
            ),
        ]

    def test_remove_cliente_valido(self):
        remove_cliente("219072230")
        self.assertEqual(
            p1.clientes, [("José Maria Rebelo de Sousa", "248537474", "918765432", [])]
        )

    def test_remove_client_nif_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            remove_cliente("219072231")
        self.assertEqual(str(ctx.exception), "NIF inválido")

    def test_remove_cliente_com_reparacoes_em_curso(self):
        p1.clientes = [
            (
                "José Maria Rebelo de Sousa",
                "248537474",
                "918765432",
                [
                    (
                        "MOTOCICLO",
                        "AA-01-02",
                        "SUZUKI",
                        [[0, (1, 1, 2022), (3, 1, 2022), ()]],
                    )
                ],
            )
        ]
        with self.assertRaises(ValueError) as ctx:
            remove_cliente("248537474")
        self.assertEqual(str(ctx.exception), "reparações em curso")


class TestProcuraVeiculo(unittest.TestCase):
    def setUp(self) -> None:
        p1.clientes = [
            ("José Maria Rebelo de Sousa", "248537474", "918765432", []),
            (
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
            ),
        ]

    def test_procura_veiculo_valido(self):
        self.assertEqual(
            procura_veiculo("AA-01-02"), ("MOTOCICLO", "AA-01-02", "SUZUKI", [])
        )

    def test_procura_veiculo_matricula_invalida(self):
        with self.assertRaises(ValueError) as ctx:
            procura_veiculo("aa-01-03")
        self.assertEqual(str(ctx.exception), "matrícula inválida")

    def test_procura_veiculo_invalido(self):
        with self.assertRaises(ValueError) as ctx:
            procura_veiculo("AA-01-03")
        self.assertEqual(str(ctx.exception), "veículo não encontrado")


class TestIniciaReparacao(unittest.TestCase):
    def setUp(self):
        p1.id_reparacao = 0
        p1.clientes = [
            ("José Maria Rebelo de Sousa", "248537474", "918765432", []),
            (
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [("MOTOCICLO", "AA-01-02", "SUZUKI", [])],
            ),
        ]

    def test_inicia_reparacao_valida(self):
        inicia_reparacao("AA-01-02", (1, 1, 2022), (3, 1, 2022))
        self.assertEqual(p1.clientes[1][3][0][3], [[0, (1, 1, 2022), (3, 1, 2022), ()]])
        self.assertEqual(p1.id_reparacao, 1)

    def test_inicia_reparacao_invalida_1(self):
        with self.assertRaises(ValueError) as ctx:
            inicia_reparacao("AA-01-03", (1, 1, 2022), (3, 1, 2022))
        self.assertEqual(str(ctx.exception), "veículo não encontrado")

    def test_inicia_reparacao_invalida_2(self):
        with self.assertRaises(ValueError) as ctx:
            inicia_reparacao("AA-01-02", (3, 1, 2022), (1, 1, 2022))
        self.assertEqual(
            str(ctx.exception),
            "data de entrada não pode ser superior à data estimada de entrega",
        )

    def test_inicia_reparacao_invalida_3(self):
        inicia_reparacao("AA-01-02", (1, 1, 2022), (3, 1, 2022))
        with self.assertRaises(ValueError) as ctx:
            inicia_reparacao("AA-01-02", (2, 1, 2022), (4, 1, 2022))
        self.assertEqual(str(ctx.exception), "data de entrada incoerente")


class TestAnulaReparacao(unittest.TestCase):
    def setUp(self):
        p1.id_reparacao = 1
        p1.clientes = [
            ("José Maria Rebelo de Sousa", "248537474", "918765432", []),
            (
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [
                    (
                        "MOTOCICLO",
                        "AA-01-02",
                        "SUZUKI",
                        [[0, (1, 1, 2022), (3, 1, 2022), ()]],
                    )
                ],
            ),
        ]

    def test_anula_reparacao_valida(self):
        anula_reparacao(0)
        self.assertEqual(p1.clientes[1][3][0][3], [])
        self.assertEqual(p1.id_reparacao, 1)


class TestProcuraReparacao(unittest.TestCase):
    def setUp(self):
        p1.id_reparacao = 1
        p1.clientes = [
            ("José Maria Rebelo de Sousa", "248537474", "918765432", []),
            (
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [
                    (
                        "MOTOCICLO",
                        "AA-01-02",
                        "SUZUKI",
                        [[0, (1, 1, 2022), (3, 1, 2022), ()]],
                    )
                ],
            ),
        ]

    def test_procura_reparacao_valida(self):
        self.assertEqual(
            procura_reparacao(0),
            ("219072230", "AA-01-02", [0, (1, 1, 2022), (3, 1, 2022), ()]),
        )

    def test_procura_reparacao_invalida(self):
        with self.assertRaises(ValueError) as ctx:
            procura_reparacao(1)
        self.assertEqual(str(ctx.exception), "reparação não encontrada")


class TestReparacaoAtrasada(unittest.TestCase):
    def setUp(self):
        p1.clientes = [
            (
                "José Maria Rebelo de Sousa",
                "248537474",
                "918765432",
                [
                    ("CARRO", "CC-01-02", "BMW", [[0, (1, 1, 2022), (3, 1, 2022), ()]]),
                    (
                        "CARRO",
                        "DD-01-02",
                        "BMW",
                        [[0, (1, 1, 2022), (3, 1, 2022), (3, 1, 2022)]],
                    ),
                    ("CARRO", "EE-01-02", "BMW", [[0, (1, 1, 2022), (5, 1, 2022), ()]]),
                ],
            ),
            (
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [
                    (
                        "MOTOCICLO",
                        "AA-01-02",
                        "SUZUKI",
                        [[0, (1, 1, 2022), (3, 1, 2022), ()]],
                    ),
                    (
                        "MOTOCICLO",
                        "BB-01-02",
                        "SUZUKI",
                        [[0, (1, 1, 2022), (2, 1, 2022), ()]],
                    ),
                ],
            ),
        ]

    def test_reparacao_atrasada_valida(self):
        self.assertEqual(
            reparacao_atrasada((4, 1, 2022)),
            (
                ("248537474", "CC-01-02", [0, (1, 1, 2022), (3, 1, 2022), ()]),
                ("219072230", "AA-01-02", [0, (1, 1, 2022), (3, 1, 2022), ()]),
                ("219072230", "BB-01-02", [0, (1, 1, 2022), (2, 1, 2022), ()]),
            ),
        )


class TestFinalizaReparacao(unittest.TestCase):
    def setUp(self):
        p1.clientes = [
            ("José Maria Rebelo de Sousa", "248537474", "918765432", []),
            (
                "António Manuel da Silva",
                "219072230",
                "912345678",
                [
                    (
                        "MOTOCICLO",
                        "AA-01-02",
                        "SUZUKI",
                        [[0, (1, 1, 2022), (3, 1, 2022), ()]],
                    )
                ],
            ),
        ]

    def test_finaliza_reparacao_valida(self):
        self.assertEqual(
            finaliza_reparacao(0, (4, 1, 2022)),
            ("219072230", "AA-01-02", (1, 1, 2022), (4, 1, 2022)),
        )
        self.assertEqual(
            p1.clientes[1][3][0][3], [[0, (1, 1, 2022), (3, 1, 2022), (4, 1, 2022)]]
        )

    def test_finaliza_reparacao_invalida_1(self):
        with self.assertRaises(ValueError) as ctx:
            finaliza_reparacao(1, (4, 1, 2022))
        self.assertEqual(str(ctx.exception), "reparação não encontrada")

    def test_finaliza_reparacao_invalida_2(self):
        finaliza_reparacao(0, (4, 1, 2022))
        with self.assertRaises(ValueError) as ctx:
            finaliza_reparacao(0, (4, 1, 2022))
        self.assertEqual(str(ctx.exception), "reparação já foi finalizada")

    def test_finaliza_reparacao_invalida_3(self):
        with self.assertRaises(ValueError) as ctx:
            finaliza_reparacao(0, (1, 1, 2021))
        self.assertEqual(
            str(ctx.exception),
            "data de entrada não pode ser superior à data de entrega",
        )


class TestImprimeRecibo(unittest.TestCase):
    def setUp(self) -> None:
        sys.stdout = self._stringio = StringIO()

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__

    def test_imprime_recibo(self):
        imprime_recibo(("219072230", "AA-01-02", (1, 1, 2022), (4, 1, 2022)))
        self.assertEqual(
            self._stringio.getvalue(),
            "-------------------------------------------------\n"
            " Cliente: 219072230\n"
            " Veículo: AA-01-02\n"
            "Data de entrada: 1/1/2022\n"
            "-------------------------------------------------\n"
            "Data de entrega: 4/1/2022\n"
            "-------------------------------------------------\n",
        )


if __name__ == "__main__":
    unittest.main()
