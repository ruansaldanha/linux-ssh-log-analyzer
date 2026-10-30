import csv
import re
import sys

from datetime import datetime, timedelta
from pathlib import Path


# Configuracoes do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

LIMITE_FALHAS = 5
JANELA_SEGUNDOS = 60


# Expressoes regulares
PADRAO_LOG = re.compile(
    r"^(?P<timestamp>\S+)\s+\S+\s+sshd\[\d+\]:\s+(?P<mensagem>.+)$"
)

PADRAO_REPETICAO = re.compile(
    r"^message repeated (?P<vezes>\d+) times:\s*\[(?P<mensagem>.+)\]$"
)

PADRAO_AUTENTICACAO = re.compile(
    r"^(?:Failed|Accepted) password for (?:invalid user )?"
    r"(?P<usuario>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})\b"
)

PADRAO_USUARIO_INVALIDO = re.compile(
    r"^Invalid user (?P<usuario>\S+) from "
    r"(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\b"
)


def calcular_quantidade_falhas(tipo, mensagem, repeticoes):
    """
    Calcula quantas falhas de autenticacao uma linha representa.
    """

    if not mensagem.startswith("Failed password"):
        return 0

    if tipo == "REPETICAO":
        return repeticoes

    return 1


def interpretar_linha(linha):
    """
    Extrai os dados relevantes de um registro SSH.

    Retorna um dicionario com os campos encontrados
    ou None quando a linha nao e reconhecida.
    """

    cabecalho = PADRAO_LOG.match(linha.strip())

    if not cabecalho:
        return None

    timestamp = cabecalho.group("timestamp")

    try:
        horario = datetime.fromisoformat(timestamp)
    except ValueError:
        return None

    mensagem = cabecalho.group("mensagem")
    repeticoes = 0

    registro_repetido = PADRAO_REPETICAO.fullmatch(mensagem)

    # Identifica o tipo do evento
    if registro_repetido:
        repeticoes = int(registro_repetido.group("vezes"))
        mensagem = registro_repetido.group("mensagem")
        tipo = "REPETICAO"

    elif mensagem.startswith("Failed password"):
        tipo = "FALHA"

    elif mensagem.startswith("Accepted password"):
        tipo = "SUCESSO"

    elif mensagem.startswith("Invalid user"):
        tipo = "USUARIO INVALIDO"

    else:
        return None

    # Extrai usuario e IP de origem
    dados = PADRAO_AUTENTICACAO.match(mensagem)

    if not dados:
        dados = PADRAO_USUARIO_INVALIDO.match(mensagem)

    if not dados:
        return None

    quantidade = calcular_quantidade_falhas(
        tipo, mensagem, repeticoes
    )

    return {
        "tipo": tipo,
        "timestamp": timestamp,
        "horario": horario,
        "usuario": dados.group("usuario"),
        "ip": dados.group("ip"),
        "quantidade": quantidade
    }


def ler_eventos(caminho_log):
    """
    Le o arquivo e transforma os registros SSH
    reconhecidos em dicionarios.
    """

    eventos = []

    with open(caminho_log, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:

            evento = interpretar_linha(linha)

            if evento is not None:
                eventos.append(evento)

    return eventos


def organizar_falhas(eventos):
    """
    Organiza a quantidade total de falhas
    e seus horarios por endereco IP.
    """

    contagem_por_ip = {}
    eventos_por_ip = {}

    for evento in eventos:

        quantidade = evento["quantidade"]

        if quantidade == 0:
            continue

        ip = evento["ip"]

        # Contagem total por IP
        contagem_por_ip[ip] = (
            contagem_por_ip.get(ip, 0) + quantidade
        )

        # Armazena os horarios das falhas
        if ip not in eventos_por_ip:
            eventos_por_ip[ip] = []

        eventos_por_ip[ip].append(
            (evento["horario"], quantidade)
        )

    return contagem_por_ip, eventos_por_ip


def detectar_alertas(eventos_por_ip):
    """
    Identifica cinco ou mais falhas do mesmo IP
    dentro de uma janela de 60 segundos.

    Utiliza a tecnica de janela deslizante.
    """

    alertas = []

    janela = timedelta(seconds=JANELA_SEGUNDOS)

    for ip, eventos in eventos_por_ip.items():

        # Ordena os eventos cronologicamente
        ordenados = sorted(
            eventos,
            key=lambda evento: evento[0]
        )

        inicio = 0
        falhas_janela = 0

        for horario, quantidade in ordenados:

            falhas_janela += quantidade

            # Remove eventos fora da janela
            while horario - ordenados[inicio][0] > janela:
                falhas_janela -= ordenados[inicio][1]
                inicio += 1

            # Verifica se a regra foi atingida
            if falhas_janela >= LIMITE_FALHAS:

                intervalo = (
                    horario - ordenados[inicio][0]
                ).total_seconds()

                alertas.append({
                    "ip": ip,
                    "falhas": falhas_janela,
                    "intervalo": intervalo
                })

                # Um alerta por IP nesta versao
                break

    return alertas


def gerar_relatorio_csv(alertas, caminho_saida):
    """
    Gera um relatorio CSV com os alertas identificados.
    """

    # Garante que a pasta de relatorios exista
    caminho_saida.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Define as colunas do arquivo
    colunas = [
        "ip_origem",
        "falhas_na_janela",
        "intervalo_segundos",
        "classificacao"
    ]

    with open(
        caminho_saida,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas,
            delimiter=";"
        )

        # Escreve o cabecalho
        escritor.writeheader()

        # Escreve os alertas encontrados
        for alerta in alertas:

            escritor.writerow({
                "ip_origem": alerta["ip"],
                "falhas_na_janela": alerta["falhas"],
                "intervalo_segundos": (
                    f"{alerta['intervalo']:.2f}".replace(".", ",")
                ),
                "classificacao": "Potencialmente suspeito"
            })

    return caminho_saida


def gerar_relatorio_markdown(
    nome_arquivo,
    eventos,
    contagem_por_ip,
    alertas,
    caminho_saida
):
    """
    Gera um relatorio tecnico em Markdown
    com o resumo da analise SSH.
    """

    caminho_saida.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    momento_analise = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    total_eventos = len(eventos)
    total_falhas = sum(contagem_por_ip.values())
    total_ips = len(contagem_por_ip)

    linhas = [
        "# Relatorio de Investigacao - SSH",
        "",
        "## Informacoes da analise",
        "",
        f"- Arquivo analisado: `{nome_arquivo}`",
        f"- Data da analise: {momento_analise}",
        f"- Eventos SSH reconhecidos: {total_eventos}",
        f"- Falhas contabilizadas: {total_falhas}",
        f"- IPs com falhas: {total_ips}",
        f"- Alertas identificados: {len(alertas)}",
        "",
        "## Regra de deteccao",
        "",
        "Cinco ou mais falhas de autenticacao do mesmo IP "
        "em uma janela de ate 60 segundos.",
        "",
        "## Contagem de falhas por IP",
        "",
        "| IP de origem | Total de falhas |",
        "|---|---:|"
    ]

    if contagem_por_ip:
        for ip, total in sorted(contagem_por_ip.items()):
            linhas.append(f"| {ip} | {total} |")
    else:
        linhas.append("| Nenhum IP com falhas | 0 |")

    linhas.extend([
        "",
        "## Alertas identificados",
        ""
    ])

    if alertas:
        linhas.extend([
            "| IP | Falhas na janela | Intervalo (s) | Classificacao |",
            "|---|---:|---:|---|"
        ])

        for alerta in alertas:
            linhas.append(
                f"| {alerta['ip']} "
                f"| {alerta['falhas']} "
                f"| {alerta['intervalo']:.2f} "
                f"| Potencialmente suspeito |"
            )

    else:
        linhas.append(
            "Nenhum comportamento suspeito identificado "
            "pela regra atual."
        )

    linhas.extend([
        "",
        "## Observacoes e limitacoes",
        "",
        "- Os alertas indicam comportamentos que merecem investigacao, "
        "nao ataques confirmados.",
        "- Mensagens agrupadas sao contabilizadas usando o horario "
        "do respectivo registro.",
        "- A implementacao gera somente o primeiro alerta por IP.",
        "- Os resultados dependem dos formatos de log reconhecidos "
        "pelo analisador.",
        "",
        "## Conclusao automatica",
        ""
    ])

    if alertas:
        linhas.append(
            f"Foram identificados {len(alertas)} endereco(s) IP "
            "que atingiram o criterio de deteccao. "
            "Recomenda-se examinar os registros correspondentes "
            "e considerar o contexto das autenticacoes."
        )
    else:
        linhas.append(
            "Nenhum endereco IP atingiu o criterio de deteccao "
            "nos registros analisados. Isso nao garante a ausencia "
            "de atividade maliciosa."
        )

    caminho_saida.write_text(
        "\n".join(linhas) + "\n",
        encoding="utf-8"
    )

    return caminho_saida


def exibir_resultados(eventos, contagem_por_ip, alertas):
    """
    Apresenta os eventos interpretados,
    a contagem por IP e os alertas.
    """

    # Eventos identificados
    for evento in eventos:

        print(f"Tipo: {evento['tipo']}")
        print(f"Timestamp: {evento['timestamp']}")
        print(f"Usuario: {evento['usuario']}")
        print(f"IP: {evento['ip']}")
        print("-" * 40)

    # Resumo de falhas
    print("\nRESUMO DE FALHAS POR IP")

    for ip, total in contagem_por_ip.items():
        print(f"IP: {ip} | Falhas: {total}")

    # Analise temporal
    print("\nANALISE TEMPORAL")

    if not alertas:
        print(
            "Nenhum comportamento suspeito "
            "identificado pela regra atual."
        )
        return

    for alerta in alertas:

        print(f"[ALERTA] IP: {alerta['ip']}")
        print(f"Falhas na janela: {alerta['falhas']}")
        print(
            f"Intervalo observado: "
            f"{alerta['intervalo']:.2f} segundos"
        )
        print(
            "Classificacao: comportamento "
            "potencialmente suspeito"
        )
        print("-" * 40)


def main():
    """
    Coordena as etapas principais do analisador.
    """

    # Permite escolher o arquivo pelo terminal
    if len(sys.argv) > 1:
        nome_arquivo = sys.argv[1]
    else:
        nome_arquivo = "sample-auth.log"

    caminho_log = BASE_DIR / "data" / nome_arquivo

    if not caminho_log.is_file():
        print(f"Arquivo nao encontrado: {caminho_log}")
        return

    # 1. Leitura e interpretacao
    eventos = ler_eventos(caminho_log)

    # 2. Organizacao das falhas
    contagem_por_ip, eventos_por_ip = organizar_falhas(
        eventos
    )

    # 3. Deteccao temporal
    alertas = detectar_alertas(eventos_por_ip)

    # 4. Apresentacao dos resultados
    exibir_resultados(
        eventos,
        contagem_por_ip,
        alertas
    )
    
    # 5. Geracao do relatorio CSV
    caminho_relatorio = BASE_DIR / "reports" / "resultado-analise.csv"

    gerar_relatorio_csv(
        alertas,
        caminho_relatorio
    )

    
    # 6. Geracao do relatorio tecnico
    caminho_markdown = (
        BASE_DIR / "reports" / "relatorio-investigacao.md"
    )

    gerar_relatorio_markdown(
        nome_arquivo,
        eventos,
        contagem_por_ip,
        alertas,
        caminho_markdown
    )

    print(f"Relatorio Markdown salvo em: {caminho_markdown}")

    
    print(f"\nRelatorio CSV salvo em: {caminho_relatorio}")



if __name__ == "__main__":
    main()
