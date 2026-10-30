"""Testes de regressao do SSH Log Analyzer (somente biblioteca padrao)."""

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = RAIZ / "src" / "ssh_log_analyzer.py"
ESPECIFICACAO = importlib.util.spec_from_file_location("ssh_log_analyzer", SCRIPT)
analisador = importlib.util.module_from_spec(ESPECIFICACAO)
ESPECIFICACAO.loader.exec_module(analisador)


def analisar(nome_arquivo):
    eventos = analisador.ler_eventos(RAIZ / "data" / nome_arquivo)
    contagem, horarios = analisador.organizar_falhas(eventos)
    alertas = analisador.detectar_alertas(horarios)
    return eventos, contagem, alertas


class TesteSSHLogAnalyzer(unittest.TestCase):

    def test_cenario_principal_com_alerta(self):
        eventos, contagem, alertas = analisar("sample-auth.log")
        self.assertEqual(len(eventos), 7)
        self.assertEqual(contagem, {"192.0.2.10": 6, "192.0.2.20": 1})
        self.assertEqual(len(alertas), 1)
        self.assertEqual(alertas[0]["ip"], "192.0.2.10")
        self.assertEqual(alertas[0]["falhas"], 6)
        self.assertEqual(alertas[0]["intervalo"], 30.0)

    def test_seis_falhas_em_grupos_distantes_nao_geram_alerta(self):
        _, contagem, alertas = analisar("teste-acima-60s.log")
        self.assertEqual(contagem["192.0.2.10"], 6)
        self.assertEqual(alertas, [])

    def test_exatamente_sessenta_segundos_gera_alerta(self):
        _, contagem, alertas = analisar("teste-limite-60s.log")
        self.assertEqual(contagem["192.0.2.30"], 5)
        self.assertEqual(len(alertas), 1)
        self.assertEqual(alertas[0]["intervalo"], 60.0)

    def test_sessenta_e_um_segundos_nao_gera_alerta(self):
        _, contagem, alertas = analisar("teste-limite-61s.log")
        self.assertEqual(contagem["192.0.2.30"], 5)
        self.assertEqual(alertas, [])

    def test_ips_distintos_e_usuario_invalido(self):
        eventos, contagem, alertas = analisar("teste-multiplos-ips.log")
        self.assertEqual(len(eventos), 8)
        self.assertEqual(
            contagem,
            {"192.0.2.40": 3, "192.0.2.50": 3, "192.0.2.60": 1}
        )
        self.assertEqual(alertas, [])

    def test_repeticoes_sem_falha_nao_incrementam_contagem(self):
        eventos, contagem, alertas = analisar("teste-repeticoes-nao-falhas.log")
        self.assertEqual(len(eventos), 4)
        self.assertEqual(contagem, {"192.0.2.70": 1, "192.0.2.80": 1})
        self.assertEqual(alertas, [])

    def test_ignora_registro_sudo_e_timestamp_invalido(self):
        linha_sudo = (
            "2026-10-28T16:36:00+00:00 ubuntu-ssh-lab sudo: "
            "COMMAND=/usr/bin/grep 'Failed password' /var/log/auth.log"
        )
        linha_invalida = (
            "nao-e-data ubuntu-ssh-lab sshd[1]: "
            "Failed password for aluno from 192.0.2.1 port 22 ssh2"
        )
        self.assertIsNone(analisador.interpretar_linha(linha_sudo))
        self.assertIsNone(analisador.interpretar_linha(linha_invalida))

    def test_geracao_de_relatorios_csv_e_markdown(self):
        eventos, contagem, alertas = analisar("sample-auth.log")

        with tempfile.TemporaryDirectory() as diretorio:
            pasta = Path(diretorio)
            csv_saida = pasta / "resultado.csv"
            md_saida = pasta / "relatorio.md"

            analisador.gerar_relatorio_csv(alertas, csv_saida)
            analisador.gerar_relatorio_markdown(
                "sample-auth.log", eventos, contagem, alertas, md_saida
            )

            with csv_saida.open(encoding="utf-8-sig", newline="") as arquivo:
                linhas = list(csv.DictReader(arquivo, delimiter=";"))

            self.assertEqual(len(linhas), 1)
            self.assertEqual(linhas[0]["ip_origem"], "192.0.2.10")
            self.assertEqual(linhas[0]["falhas_na_janela"], "6")
            self.assertEqual(linhas[0]["intervalo_segundos"], "30,00")

            markdown = md_saida.read_text(encoding="utf-8")
            self.assertIn("Eventos SSH reconhecidos: 7", markdown)
            self.assertIn("Alertas identificados: 1", markdown)
            self.assertIn("192.0.2.10", markdown)

    def test_csv_sem_alertas_contem_apenas_cabecalho(self):
        _, _, alertas = analisar("teste-multiplos-ips.log")
        with tempfile.TemporaryDirectory() as diretorio:
            arquivo = Path(diretorio) / "sem-alerta.csv"
            analisador.gerar_relatorio_csv(alertas, arquivo)
            with arquivo.open(encoding="utf-8-sig", newline="") as leitor:
                linhas = list(csv.reader(leitor, delimiter=";"))
            self.assertEqual(len(linhas), 1)
            self.assertEqual(linhas[0][0], "ip_origem")


if __name__ == "__main__":
    unittest.main()
