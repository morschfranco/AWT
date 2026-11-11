"""
Programa XV_CBPE — versão consolidada para Google Colab ou execução local.

Modelagem matemática de rotor eólico de eixo vertical H-Darrieus.

Perfis:
    NACA 0012, NACA 0018, NACA 0025 e SD7080.

Origens disponíveis:
    github: baixa polares para uma pasta temporária local.
    drive: utiliza a pasta do programa/notebook no Google Drive.

Correções:
    - Funções e constantes definidas antes de serem utilizadas.
    - Remoção da execução antecipada e de ArgsDummy.
    - Importação de shutil.
    - Uso consistente de args.tsr.
    - Download com timeout e gravação temporária.
    - Diagnóstico explícito de arquivos ausentes.

Observações:
    - Os nomes e caminhos das polares no GitHub precisam corresponder
      ao padrão <perfil>_Re<inteiro>.dat, .csv ou .txt.
    - Cp cinemático é um indicador relativo, não um Cp absoluto validado.
    - As equações aerodinâmicas e energéticas foram mantidas nesta versão;
      a correção de execução não constitui validação científica do modelo.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# =============================================================================
# 0. CONFIGURAÇÃO E CONSTANTES
# =============================================================================

FONTE_EXECUCAO = "github"  # "github" ou "drive"
FORCAR_DOWNLOAD_GITHUB = True

GITHUB_REPO_URL = (
    "https://github.com/morschfranco/AWT/tree/main/XV_CBPE/Python"
)
GITHUB_RAW_BASE = (
    "https://raw.githubusercontent.com/morschfranco/AWT/main/XV_CBPE/Python"
)

PASTA_TEMP_BASE = (
    "/content" if os.path.isdir("/content") else tempfile.gettempdir()
)
PASTA_POLAR_GITHUB = os.path.join(PASTA_TEMP_BASE, "polars_temp")
PASTA_SAIDA_GITHUB = os.path.join(PASTA_TEMP_BASE, "saidas_temp")

EXTENSOES_POLAR = (".dat", ".csv", ".txt")

RHO_AIR = 1.225
NU_AIR = 1.46e-5
CP_BETZ = 16.0 / 27.0

PERFIS_ARTIGO = ["NACA 0012", "NACA 0018", "NACA 0025", "SD7080"]
PERFIS_TODOS = PERFIS_ARTIGO.copy()

RE_LIST = [1.0e5, 2.0e5, 3.0e5]
RE_OPERACAO = 3.0e5

TSR_REF = 3.75
SIGMA_REF = 0.30
N_PAS_REF = 3
AR_REF = 2.6
CP_PROJ = 0.48

V_NOMINAL_MS = 10.0
P_NOMINAL_W = 1000.0
FAIXA_VENTO_KMH = (10.0, 70.0)
V_CUT_IN_KMH = 10.0
V_CUT_OUT_KMH = 70.0

PERFIS_METADADOS = {
    "NACA 0012": {
        "familia": "NACA 4 dígitos, simétrico",
        "espessura_rel": 0.12,
    },
    "NACA 0018": {
        "familia": "NACA 4 dígitos, simétrico",
        "espessura_rel": 0.18,
    },
    "NACA 0025": {
        "familia": "NACA 4 dígitos, simétrico",
        "espessura_rel": 0.25,
    },
    "SD7080": {
        "familia": "Série SD",
        "espessura_rel": None,
    },
}

REFERENCIA_ARTIGO = {
    "indicador_re3e5": {
        "SD7080": 2.3637,
        "NACA 0025": 2.0729,
        "NACA 0018": 1.9202,
        "NACA 0012": 1.3389,
    },
    "indicador_re3e5_descricao": (
        "Valores reportados no artigo para Re = 3 x 10^5. "
        "A natureza exata do indicador está pendente de confirmação."
    ),
    "indicador_re3e5_desvios_pct": {
        "NACA 0025": 14.0,
        "NACA 0018": 23.0,
        "NACA 0012": 77.0,
    },
    "cl_cd_max_naca0025": 22.1,
    "cl_max_reportado": {
        "valores": (1.43, 1.35),
        "atribuicao": None,
    },
    "ranking_artigo": [
        "SD7080",
        "NACA 0025",
        "NACA 0018",
        "NACA 0012",
    ],
    "reynolds_operacao": 3.0e5,
    "rotacao_operacao_rpm": 626.2,
    "dimensoes_artigo": {
        "D": 1.144,
        "H": 2.974,
        "c": 0.114,
        "A": 3.401,
        "R": 0.572,
    },
}


# =============================================================================
# 1. AMBIENTE E DOWNLOAD
# =============================================================================

def _nome_arquivo_base(nome: str) -> str:
    return nome.replace(" ", "").replace("-", "")


def localizar_arquivo_polar(
    nome: str,
    Re: float,
    pasta: str,
) -> str | None:
    base = _nome_arquivo_base(nome)

    for extensao in EXTENSOES_POLAR:
        caminho = os.path.join(
            pasta,
            f"{base}_Re{int(Re)}{extensao}",
        )
        if os.path.isfile(caminho):
            return caminho

    return None


def _baixar_polares_do_github(
    pasta_destino: str,
    perfis: list[str],
    re_list: list[float],
) -> dict:
    """Baixa arquivos usando o padrão de nomes esperado pelo programa."""
    os.makedirs(pasta_destino, exist_ok=True)

    baixados = 0
    existentes = 0
    ausentes = []

    for nome in perfis:
        base = _nome_arquivo_base(nome)

        for Re in re_list:
            if localizar_arquivo_polar(nome, Re, pasta_destino):
                existentes += 1
                continue

            sucesso = False
            erros = []

            for extensao in EXTENSOES_POLAR:
                nome_arq = f"{base}_Re{int(Re)}{extensao}"
                url = f"{GITHUB_RAW_BASE}/polars/{nome_arq}"
                destino = os.path.join(pasta_destino, nome_arq)
                temporario = destino + ".part"

                requisicao = urllib.request.Request(
                    url,
                    headers={"User-Agent": "XV_CBPE-Python"},
                )

                try:
                    with urllib.request.urlopen(
                        requisicao,
                        timeout=30,
                    ) as resposta:
                        conteudo = resposta.read()

                    if not conteudo.strip():
                        raise ValueError("arquivo recebido está vazio")

                    with open(temporario, "wb") as arquivo:
                        arquivo.write(conteudo)

                    os.replace(temporario, destino)
                    print(f"[github] Polar baixada: {nome_arq}")
                    baixados += 1
                    sucesso = True
                    break

                except urllib.error.HTTPError as erro:
                    erros.append(f"{extensao}: HTTP {erro.code}")

                except (
                    urllib.error.URLError,
                    TimeoutError,
                    OSError,
                    ValueError,
                ) as erro:
                    erros.append(f"{extensao}: {erro}")

                finally:
                    if os.path.exists(temporario):
                        os.remove(temporario)

            if not sucesso:
                esperado = f"{base}_Re{int(Re)}"
                ausentes.append(esperado)
                print(
                    f"[aviso] Não foi possível baixar {esperado}: "
                    + "; ".join(erros)
                )

    print(
        f"[github] Baixados: {baixados} | "
        f"Já existentes: {existentes} | Ausentes: {len(ausentes)}"
    )

    return {
        "baixados": baixados,
        "existentes": existentes,
        "ausentes": ausentes,
    }


def _localizar_pasta_no_drive() -> str:
    """Tenta identificar a pasta do programa/notebook no Drive."""
    if "__file__" in globals():
        return os.path.dirname(os.path.abspath(__file__))

    try:
        from google.colab import drive, _message
    except ImportError:
        return os.getcwd()

    if not os.path.ismount("/content/drive"):
        print("[drive] Montando Google Drive...")
        drive.mount("/content/drive")

    cwd = os.getcwd()
    if cwd.startswith("/content/drive"):
        return cwd

    raizes = [
        "/content/drive/MyDrive",
        "/content/drive/Meu Drive",
    ]
    raiz = next(
        (p for p in raizes if os.path.isdir(p)),
        "/content/drive/MyDrive",
    )

    try:
        resposta = _message.blocking_request(
            "get_ipynb",
            timeout_sec=2,
        )
        nome_nb = resposta["ipynb"]["metadata"]["colab"]["name"]
        achados = glob.glob(
            os.path.join(raiz, "**", nome_nb),
            recursive=True,
        )
        if achados:
            return os.path.dirname(achados[0])
    except Exception:
        pass

    for padrao in (
        os.path.join(raiz, "**", "XV_CBPE", "Python"),
        os.path.join(raiz, "**", "polars"),
    ):
        achados = [
            p for p in glob.glob(padrao, recursive=True)
            if os.path.isdir(p)
        ]
        if achados:
            return (
                achados[0]
                if padrao.endswith("Python")
                else os.path.dirname(achados[0])
            )

    pasta_colab = os.path.join(raiz, "Colab Notebooks")
    return pasta_colab if os.path.isdir(pasta_colab) else raiz


def configurar_ambiente(
    fonte: str,
    perfis: list[str],
    re_list: list[float],
) -> tuple[str, str]:
    fonte = fonte.lower().strip()

    if fonte == "github":
        pasta_polar = PASTA_POLAR_GITHUB
        pasta_saida = PASTA_SAIDA_GITHUB

        if FORCAR_DOWNLOAD_GITHUB and os.path.isdir(pasta_polar):
            print(f"[github] Limpando pasta temporária: {pasta_polar}")
            shutil.rmtree(pasta_polar)

        os.makedirs(pasta_polar, exist_ok=True)
        os.makedirs(pasta_saida, exist_ok=True)

        print("[github] Baixando polares diretamente do repositório...")
        relatorio = _baixar_polares_do_github(
            pasta_polar,
            perfis,
            re_list,
        )

        if relatorio["ausentes"]:
            print(
                "[aviso] Verifique os nomes das polares, o caminho "
                "no repositório e a conexão com a internet."
            )

        return pasta_polar, pasta_saida

    if fonte == "drive":
        pasta_base = _localizar_pasta_no_drive()
        pasta_polar = os.path.join(pasta_base, "polars")
        pasta_saida = os.path.join(pasta_base, "saidas")

        os.makedirs(pasta_polar, exist_ok=True)
        os.makedirs(pasta_saida, exist_ok=True)

        print(f"[drive] Diretório base: {pasta_base}")
        return pasta_polar, pasta_saida

    raise ValueError("FONTE_EXECUCAO deve ser 'github' ou 'drive'.")


# =============================================================================
# 2. POLARES
# =============================================================================

@dataclass
class Polar:
    nome: str
    Re: float
    alpha: list[float]
    cl: list[float]
    cd: list[float]
    origem: str = "XFOIL"

    @staticmethod
    def _interp(x, xs, ys):
        if x <= xs[0]:
            return ys[0]
        if x >= xs[-1]:
            return ys[-1]

        i = 0
        while i < len(xs) - 2 and x > xs[i + 1]:
            i += 1

        t = (x - xs[i]) / (xs[i + 1] - xs[i])
        return ys[i] + t * (ys[i + 1] - ys[i])

    def cl_cd(self, alpha_deg):
        return (
            self._interp(alpha_deg, self.alpha, self.cl),
            self._interp(alpha_deg, self.alpha, self.cd),
        )

    def razao(self):
        return [
            cl / cd if cd > 0 else 0.0
            for cl, cd in zip(self.cl, self.cd)
        ]

    def resumo(self):
        razoes = self.razao()
        i = razoes.index(max(razoes))

        return {
            "Cl/Cd max": max(razoes),
            "alpha* (deg)": self.alpha[i],
            "Cl em alpha*": self.cl[i],
            "Cl max": max(self.cl),
            "Cd em alpha*": self.cd[i],
            "alpha de Cl max (deg)": self.alpha[
                self.cl.index(max(self.cl))
            ],
        }

    def validar(self):
        avisos = []

        if len(self.alpha) < 5:
            avisos.append("polar com menos de cinco pontos")

        if any(
            b <= a
            for a, b in zip(self.alpha, self.alpha[1:])
        ):
            avisos.append("ângulos não estritamente crescentes")

        if any(cd <= 0 for cd in self.cd):
            avisos.append("coeficiente de arrasto não positivo")

        return avisos

    def para_dataframe(self):
        return pd.DataFrame({
            "Perfil": self.nome,
            "Re": self.Re,
            "alpha (deg)": self.alpha,
            "Cl": self.cl,
            "Cd": self.cd,
            "Cl/Cd": self.razao(),
            "Origem": self.origem,
        })


def _parse_polar(caminho: str, nome: str, Re: float) -> Polar:
    """Lê as três primeiras colunas numéricas: alpha, Cl e Cd."""
    alphas, cls, cds = [], [], []

    with open(
        caminho,
        "r",
        encoding="utf-8",
        errors="replace",
    ) as arquivo:
        for linha in arquivo:
            partes = linha.replace(",", " ").split()

            if len(partes) < 3:
                continue

            try:
                a, cl, cd = map(float, partes[:3])
            except ValueError:
                continue

            if not all(math.isfinite(v) for v in (a, cl, cd)):
                continue

            alphas.append(a)
            cls.append(cl)
            cds.append(cd)

    if len(alphas) < 3:
        raise ValueError(f"Polar sem dados suficientes: {caminho}")

    return Polar(nome, Re, alphas, cls, cds)


_CACHE_POLAR: dict[tuple[str, float, str], Polar | None] = {}
_ERROS_POLAR: dict[tuple[str, float, str], str] = {}


def carregar_polar(nome: str, Re: float, pasta: str) -> Polar | None:
    chave = (nome, Re, os.path.abspath(pasta))

    if chave in _CACHE_POLAR:
        return _CACHE_POLAR[chave]

    caminho = localizar_arquivo_polar(nome, Re, pasta)

    if caminho is None:
        _CACHE_POLAR[chave] = None
        _ERROS_POLAR[chave] = "arquivo não encontrado"
        return None

    try:
        polar = _parse_polar(caminho, nome, Re)

        # A interpolação exige ângulos estritamente crescentes.
        if any(
            b <= a
            for a, b in zip(polar.alpha, polar.alpha[1:])
        ):
            raise ValueError(
                "ângulos de ataque não estritamente crescentes"
            )

    except (OSError, ValueError) as erro:
        _CACHE_POLAR[chave] = None
        _ERROS_POLAR[chave] = str(erro)
        print(f"[aviso] Polar inválida: {caminho}: {erro}")
        return None

    _CACHE_POLAR[chave] = polar
    return polar


def polar_disponivel(nome, re_list, pasta) -> bool:
    return all(
        carregar_polar(nome, Re, pasta) is not None
        for Re in re_list
    )


def filtrar_perfis_disponiveis(perfis, re_list, pasta):
    ok, pendentes = [], []

    for nome in perfis:
        destino = (
            ok if polar_disponivel(nome, re_list, pasta)
            else pendentes
        )
        destino.append(nome)

    return ok, pendentes


def diagnosticar_polares(perfis, re_list, pasta) -> pd.DataFrame:
    linhas = []

    for nome in perfis:
        for Re in re_list:
            polar = carregar_polar(nome, Re, pasta)
            chave = (nome, Re, os.path.abspath(pasta))

            if polar is None:
                linhas.append({
                    "Perfil": nome,
                    "Re": Re,
                    "Origem": "ausente ou inválida",
                    "N pontos": 0,
                    "alpha mín (deg)": None,
                    "alpha máx (deg)": None,
                    "Cl máx": None,
                    "Cd mín": None,
                    "Avisos": _ERROS_POLAR.get(
                        chave,
                        "polar indisponível",
                    ),
                })
                continue

            avisos = polar.validar()
            linhas.append({
                "Perfil": nome,
                "Re": Re,
                "Origem": polar.origem,
                "N pontos": len(polar.alpha),
                "alpha mín (deg)": min(polar.alpha),
                "alpha máx (deg)": max(polar.alpha),
                "Cl máx": round(max(polar.cl), 4),
                "Cd mín": round(min(polar.cd), 5),
                "Avisos": "; ".join(avisos) or "sem avisos",
            })

    return pd.DataFrame(linhas)


# =============================================================================
# 3. DIMENSIONAMENTO
# =============================================================================

@dataclass
class Parametros:
    P_nominal: float = P_NOMINAL_W
    V_nominal: float = V_NOMINAL_MS
    Cp: float = CP_PROJ
    N_pas: int = N_PAS_REF
    AR: float = AR_REF
    sigma: float = SIGMA_REF
    TSR: float = TSR_REF
    rho: float = RHO_AIR
    nu: float = NU_AIR

    def __post_init__(self):
        if not 500.0 <= self.P_nominal <= 1000.0:
            raise ValueError("P_nominal deve estar entre 500 e 1000 W.")

        if not 0 < self.Cp < CP_BETZ:
            raise ValueError(
                f"Cp deve estar entre zero e {CP_BETZ:.3f}."
            )

        if min(
            self.V_nominal,
            self.AR,
            self.sigma,
            self.TSR,
            self.rho,
            self.nu,
        ) <= 0:
            raise ValueError(
                "V_nominal, AR, sigma, TSR, rho e nu devem ser positivos."
            )

        if not 2 <= self.N_pas <= 5:
            raise ValueError("N_pas deve estar entre 2 e 5.")


@dataclass
class Rotor:
    D: float
    H: float
    c: float
    A: float
    P_nominal: float
    V_nominal: float
    Cp: float
    TSR: float
    rho: float
    nu: float
    sigma: float
    AR: float
    N_pas: int

    @property
    def R(self):
        return self.D / 2.0

    def potencia(self, V, limitar=True, cp=None):
        cp = self.Cp if cp is None else cp
        potencia = 0.5 * self.rho * self.A * V**3 * cp
        return min(potencia, self.P_nominal) if limitar else potencia

    def rpm(self, V):
        return (
            self.TSR * V / self.R
        ) * 60.0 / (2.0 * math.pi)

    def re_corda(self, V, tsr=None):
        tsr = self.TSR if tsr is None else tsr
        W = V * math.sqrt(tsr**2 + 1.0)
        return W * self.c / self.nu

    def torque(self, V, cp=None):
        omega = self.TSR * V / self.R
        if omega <= 0:
            return 0.0
        return self.potencia(V, limitar=False, cp=cp) / omega


def dimensionar(p: Parametros) -> Rotor:
    A = p.P_nominal / (
        0.5 * p.rho * p.V_nominal**3 * p.Cp
    )
    D = math.sqrt(A / p.AR)
    H = p.AR * D
    c = p.sigma * D / p.N_pas

    rotor = Rotor(
        D=D,
        H=H,
        c=c,
        A=A,
        P_nominal=p.P_nominal,
        V_nominal=p.V_nominal,
        Cp=p.Cp,
        TSR=p.TSR,
        rho=p.rho,
        nu=p.nu,
        sigma=p.sigma,
        AR=p.AR,
        N_pas=p.N_pas,
    )

    assert math.isclose(
        rotor.c * p.N_pas / rotor.D,
        p.sigma,
        rel_tol=1e-9,
    )
    assert math.isclose(
        rotor.H / rotor.D,
        p.AR,
        rel_tol=1e-9,
    )

    return rotor


# =============================================================================
# 4. MODELO CINEMÁTICO E COMPARAÇÃO
# =============================================================================

def cp_cinematica(polar, tsr, sigma, n=1440):
    """Indicador relativo; não utilizar como Cp absoluto."""
    soma = 0.0

    for i in range(n):
        theta = 2.0 * math.pi * i / n
        w2 = 1.0 + tsr**2 + 2.0 * tsr * math.sin(theta)
        alfa = math.degrees(
            math.atan2(
                math.cos(theta),
                tsr + math.sin(theta),
            )
        )
        cl, cd = polar.cl_cd(alfa)
        alfa_rad = math.radians(alfa)
        ct = cl * math.sin(alfa_rad) - cd * math.cos(alfa_rad)
        soma += w2 * ct

    return sigma * tsr * soma / n


def coef_torque(polar, tsr, sigma, n=1440):
    """Mantém o indicador de torque do código original."""
    soma = 0.0

    for i in range(n):
        theta = 2.0 * math.pi * i / n
        alfa = math.degrees(
            math.atan2(
                math.cos(theta),
                tsr + math.sin(theta),
            )
        )
        cl, cd = polar.cl_cd(alfa)
        alfa_rad = math.radians(alfa)
        ct = cl * math.sin(alfa_rad) - cd * math.cos(alfa_rad)
        soma += ct

    return sigma * soma / n


def curva_cp_tsr(
    polar,
    sigma,
    tsr_min=1.0,
    tsr_max=7.0,
    n=60,
):
    tsrs = np.linspace(tsr_min, tsr_max, n)
    cps = np.array([
        cp_cinematica(polar, float(t), sigma)
        for t in tsrs
    ])
    return tsrs, cps


def comparar_perfis(
    perfis,
    re_list,
    tsr_ref=TSR_REF,
    sigma=SIGMA_REF,
    pasta=None,
):
    if pasta is None:
        raise ValueError("Informe a pasta das polares.")

    resultados = {}

    for nome in perfis:
        disponivel = polar_disponivel(nome, re_list, pasta)
        resultados[nome] = {"_disponivel": disponivel}

        if not disponivel:
            continue

        for Re in re_list:
            polar = carregar_polar(nome, Re, pasta)
            info = polar.resumo()
            info["Cp_kin"] = cp_cinematica(polar, tsr_ref, sigma)
            info["Ct"] = coef_torque(polar, tsr_ref, sigma)
            info["Ct estatico"] = coef_torque(polar, 0.0, sigma)

            tsrs, cps = curva_cp_tsr(polar, sigma)
            info["tsr de Cp max"] = float(tsrs[np.argmax(cps)])
            info["fonte"] = polar.origem
            resultados[nome][Re] = info

    return resultados


def perfis_analisados(res):
    return [
        nome for nome, info in res.items()
        if info.get("_disponivel")
    ]


def melhor_perfil(res, Re=RE_OPERACAO, chave="Cl/Cd max"):
    candidatos = perfis_analisados(res)
    if not candidatos:
        return None
    return max(candidatos, key=lambda nome: res[nome][Re][chave])


def fatores_perfil(res, Re=RE_OPERACAO, chave="Cp_kin"):
    melhor = melhor_perfil(res, Re, chave)

    if melhor is None:
        return {}, None

    referencia = res[melhor][Re][chave]

    if referencia == 0:
        return {
            nome: 0.0 for nome in perfis_analisados(res)
        }, melhor

    return {
        nome: res[nome][Re][chave] / referencia
        for nome in perfis_analisados(res)
    }, melhor


def tabela_perfis(res, re_list):
    colunas = [
        "Perfil", "Re", "Cl/Cd max", "alpha* (deg)",
        "Cl max", "Ct", "Ct estatico", "Cp_kin",
        "TSR de Cp max", "Origem",
    ]
    linhas = []

    for nome in perfis_analisados(res):
        for Re in re_list:
            info = res[nome][Re]
            linhas.append({
                "Perfil": nome,
                "Re": Re,
                "Cl/Cd max": round(info["Cl/Cd max"], 4),
                "alpha* (deg)": round(info["alpha* (deg)"], 2),
                "Cl max": round(info["Cl max"], 4),
                "Ct": round(info["Ct"], 4),
                "Ct estatico": round(info["Ct estatico"], 4),
                "Cp_kin": round(info["Cp_kin"], 4),
                "TSR de Cp max": round(info["tsr de Cp max"], 2),
                "Origem": info["fonte"],
            })

    return pd.DataFrame(linhas, columns=colunas)


# =============================================================================
# 5. COMPARAÇÃO COM O ARTIGO
# =============================================================================

def tabela_validacao(res, Re=RE_OPERACAO):
    colunas = [
        "Perfil",
        "Cl/Cd max (modelo)",
        "Indicador de referência (artigo)",
        "Desvio relativo (%)",
        "Origem da polar",
        "Observação",
    ]
    linhas = []

    for nome in PERFIS_ARTIGO:
        if not res.get(nome, {}).get("_disponivel"):
            continue

        info = res[nome][Re]
        referencia = REFERENCIA_ARTIGO["indicador_re3e5"][nome]
        modelo = info["Cl/Cd max"]

        linhas.append({
            "Perfil": nome,
            "Cl/Cd max (modelo)": round(modelo, 4),
            "Indicador de referência (artigo)": referencia,
            "Desvio relativo (%)": round(
                100.0 * (modelo - referencia) / referencia,
                2,
            ),
            "Origem da polar": info["fonte"],
            "Observação": (
                "Comparação exploratória: natureza do indicador "
                "de referência ainda não confirmada"
            ),
        })

    return pd.DataFrame(linhas, columns=colunas)


def verificar_ranking(res, Re=RE_OPERACAO):
    disponiveis = [
        nome for nome in PERFIS_ARTIGO
        if res.get(nome, {}).get("_disponivel")
    ]
    modelo = sorted(
        disponiveis,
        key=lambda nome: res[nome][Re]["Cl/Cd max"],
        reverse=True,
    )
    referencia = [
        nome for nome in REFERENCIA_ARTIGO["ranking_artigo"]
        if nome in disponiveis
    ]
    return modelo, referencia, modelo == referencia


def ranking_spearman(ordem_a, ordem_b):
    if set(ordem_a) != set(ordem_b):
        raise ValueError("Os rankings devem conter os mesmos perfis.")

    n = len(ordem_a)
    if n < 2:
        return float("nan")

    postos_a = {nome: i for i, nome in enumerate(ordem_a)}
    postos_b = {nome: i for i, nome in enumerate(ordem_b)}
    d2 = sum(
        (postos_a[nome] - postos_b[nome])**2
        for nome in ordem_a
    )
    return 1.0 - 6.0 * d2 / (n * (n**2 - 1))


# =============================================================================
# 6. ENERGIA E SENSIBILIDADE
# =============================================================================

def weibull_pdf(v, k, A):
    if k <= 0 or A <= 0:
        raise ValueError("Os parâmetros de Weibull devem ser positivos.")
    return (k / A) * (v / A)**(k - 1) * np.exp(-(v / A)**k)


def curva_potencia_perfil(rotor, fator, v_kmh=None):
    if v_kmh is None:
        v_kmh = np.linspace(*FAIXA_VENTO_KMH, 121)

    v_kmh = np.asarray(v_kmh)
    v_ms = v_kmh / 3.6

    return pd.DataFrame({
        "V (km/h)": v_kmh,
        "V (m/s)": v_ms,
        "P (W)": [
            rotor.potencia(float(v), cp=CP_PROJ * fator)
            for v in v_ms
        ],
        "RPM": [rotor.rpm(float(v)) for v in v_ms],
        "Re corda": [rotor.re_corda(float(v)) for v in v_ms],
    })


def aep_weibull(
    rotor,
    fator,
    k,
    A_weib,
    v_max=25.0,
    n=400,
    horas_ano=8760.0,
):
    """Estimativa provisória, mantendo a integração do código original."""
    v = np.linspace(0.01, v_max, n)
    dv = v[1] - v[0]

    potencia = np.array([
        rotor.potencia(float(vi), cp=CP_PROJ * fator)
        for vi in v
    ])
    densidade = weibull_pdf(v, k, A_weib)

    energia = float(
        np.sum(potencia * densidade) * dv * horas_ano / 1000.0
    )
    fc = energia / (rotor.P_nominal * horas_ano / 1000.0)

    return {
        "AEP (kWh/ano)": energia,
        "Fator de capacidade": fc,
        "Weibull k": k,
        "Weibull A (m/s)": A_weib,
        "Status dos parâmetros": (
            "provisórios (N/A) até a coleta anemométrica"
        ),
    }


def varredura_sigma_tsr(polar, sigmas, tsrs):
    return pd.DataFrame([
        {
            "sigma": float(s),
            "TSR": float(t),
            "Cp_kin": cp_cinematica(polar, float(t), float(s)),
        }
        for t in tsrs
        for s in sigmas
    ])


# =============================================================================
# 7. VISUALIZAÇÕES
# =============================================================================

def salvar_figura(fig, nome, args):
    os.makedirs(args.outdir, exist_ok=True)
    caminho = os.path.join(args.outdir, f"{nome}.{args.formato}")
    fig.savefig(caminho, dpi=args.dpi, bbox_inches="tight")

    if args.mostrar:
        plt.show()

    plt.close(fig)
    print(f"[figura] {caminho}")


def _perfis_para_figura(perfis, re_list, pasta):
    ok, pendentes = filtrar_perfis_disponiveis(
        perfis, re_list, pasta
    )
    if pendentes:
        print(
            "[aviso] Perfis excluídos da figura: "
            + ", ".join(pendentes)
        )
    return ok


def _plotar_polares(perfis, re_list, args, diagrama=False):
    perfis = _perfis_para_figura(
        perfis, re_list, args.pasta_polar
    )
    if not perfis:
        return

    largura = 3.6 if diagrama else 5.0
    fig, axs = plt.subplots(
        1,
        len(re_list),
        figsize=(largura * len(re_list), 5),
        sharey=True,
        squeeze=False,
    )

    fig.suptitle(
        "Diagrama polar, Cl versus Cd"
        if diagrama
        else "Cl/Cd versus ângulo de ataque",
        fontsize=14,
    )

    for j, Re in enumerate(re_list):
        ax = axs[0, j]

        for nome in perfis:
            polar = carregar_polar(nome, Re, args.pasta_polar)
            x = polar.cd if diagrama else polar.alpha
            y = polar.cl if diagrama else polar.razao()
            ax.plot(x, y, lw=1.4, label=nome)

        ax.set_title(f"Re = {Re:.0e}")
        ax.set_xlabel("Cd" if diagrama else "alpha (graus)")
        if j == 0:
            ax.set_ylabel("Cl" if diagrama else "Cl/Cd")
        if not diagrama:
            ax.axvline(0, color="k", lw=0.5)

        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    salvar_figura(
        fig,
        "fig02_diagrama_polar" if diagrama else "fig01_cl_cd_alpha",
        args,
    )


def plotar_cl_cd_alpha(perfis, re_list, args):
    _plotar_polares(perfis, re_list, args, diagrama=False)


def plotar_polar_cl_cd(perfis, re_list, args):
    _plotar_polares(perfis, re_list, args, diagrama=True)


def plotar_cp_tsr(perfis, args, Re=RE_OPERACAO):
    perfis = _perfis_para_figura(
        perfis, [Re], args.pasta_polar
    )
    if not perfis:
        return

    fig, ax = plt.subplots(figsize=(8.5, 8.5))

    for nome in perfis:
        polar = carregar_polar(nome, Re, args.pasta_polar)
        tsrs, cps = curva_cp_tsr(polar, args.sigma)
        ax.plot(tsrs, cps, lw=2.4, label=nome)

    ax.axvline(
        args.tsr,
        ls="--",
        c="k",
        label=f"TSR projeto = {args.tsr}",
    )
    ax.set_title(
        f"Cp cinemático versus TSR, Re = {Re:.0e}",
        fontsize=24,
    )
    ax.set_xlabel("Tip Speed Ratio (TSR)", fontsize=19)
    ax.set_ylabel("Cp cinemático (relativo)", fontsize=19)
    ax.tick_params(labelsize=16)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=16)
    fig.tight_layout()
    salvar_figura(fig, "fig03_cp_tsr", args)


def plotar_cp_barras(res, perfis, re_list, args):
    perfis = [
        nome for nome in perfis
        if res.get(nome, {}).get("_disponivel")
    ]
    if not perfis:
        return

    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(len(perfis))
    largura = 0.8 / len(re_list)

    for j, Re in enumerate(re_list):
        posicoes = x + (j - (len(re_list) - 1) / 2) * largura
        valores = [res[nome][Re]["Cp_kin"] for nome in perfis]
        barras = ax.bar(
            posicoes, valores, largura, label=f"Re = {Re:.0e}"
        )
        ax.bar_label(barras, fmt="%.3f", padding=3, fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(perfis, rotation=25, ha="right")
    ax.set_ylabel(f"Cp cinemático em TSR {args.tsr}")
    ax.set_title("Comparação por perfil e Reynolds")
    ax.grid(alpha=0.3, axis="y")
    ax.legend()
    fig.tight_layout()
    salvar_figura(fig, "fig04_cp_barras", args)


def plotar_curva_potencia(rotor, res, perfis, args):
    fatores, melhor = fatores_perfil(res)
    if melhor is None:
        return

    fig, ax = plt.subplots(figsize=(11, 6))

    for nome in perfis:
        if nome not in fatores:
            continue

        df = curva_potencia_perfil(rotor, fatores[nome])
        ax.plot(
            df["V (km/h)"],
            df["P (W)"],
            label=f"{nome} (fator {fatores[nome]:.3f})",
        )

    for v, rotulo in (
        (V_CUT_IN_KMH, "cut-in"),
        (rotor.V_nominal * 3.6, "nominal"),
        (V_CUT_OUT_KMH, "cut-out"),
    ):
        ax.axvline(v, ls=":", c="k", lw=0.8)
        ax.text(
            v,
            ax.get_ylim()[1] * 0.04,
            rotulo,
            rotation=90,
            fontsize=8,
        )

    ax.set_title(
        "Curva de potência com Cp escalado pelo fator relativo\n"
        f"Melhor perfil: {melhor}"
    )
    ax.set_xlabel("Velocidade do vento (km/h)")
    ax.set_ylabel("Potência (W)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)
    fig.tight_layout()
    salvar_figura(fig, "fig05_curva_potencia", args)


def plotar_reynolds_operacao(rotor, args, Re=RE_OPERACAO):
    v_kmh = np.linspace(*FAIXA_VENTO_KMH, 121)
    reynolds = [rotor.re_corda(v / 3.6) for v in v_kmh]

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(v_kmh, reynolds, label="Re de corda em operação")

    for v in (
        V_CUT_IN_KMH,
        rotor.V_nominal * 3.6,
        V_CUT_OUT_KMH,
    ):
        ax.axvline(v, ls=":", c="k", lw=0.8)

    ax.axhline(
        1.0e5, color="r", ls="--", label="Limite inferior: 1e5"
    )
    ax.axhline(
        Re, color="darkred", ls="--", label=f"Re operação: {Re:.1e}"
    )
    ax.set_title("Envelope de Reynolds de corda")
    ax.set_xlabel("Velocidade do vento (km/h)")
    ax.set_ylabel("Reynolds de corda")
    ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
    ax.grid(alpha=0.5)
    ax.legend(fontsize=9)
    fig.tight_layout()
    salvar_figura(fig, "fig06_reynolds_operacao", args)


def plotar_cl_max_alpha(res, perfis, re_list, args):
    perfis = [
        nome for nome in perfis
        if res.get(nome, {}).get("_disponivel")
    ]
    if not perfis:
        return

    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    x = np.arange(len(perfis))
    largura = 0.8 / len(re_list)

    configuracoes = (
        ("Cl max", "Coeficiente de sustentação máximo", "Cl máx"),
        ("alpha* (deg)", "Ângulo no melhor Cl/Cd", "alpha* (graus)"),
    )

    for ax, (metrica, titulo, rotulo) in zip(axs, configuracoes):
        for j, Re in enumerate(re_list):
            posicoes = x + (j - (len(re_list) - 1) / 2) * largura
            valores = [res[nome][Re][metrica] for nome in perfis]
            barras = ax.bar(
                posicoes, valores, largura, label=f"Re = {Re:.0e}"
            )
            ax.bar_label(barras, fmt="%.2f", padding=3, fontsize=8)

        ax.set_xticks(x)
        ax.set_xticklabels(perfis, rotation=25, ha="right")
        ax.set_title(titulo)
        ax.set_ylabel(rotulo)
        ax.grid(axis="y", alpha=0.5)
        ax.legend(fontsize=9)

    fig.tight_layout()
    salvar_figura(fig, "fig07_clmax_alpha", args)


def plotar_tabela_potencia(rotor, res, perfis, args):
    fatores, melhor = fatores_perfil(res)
    if melhor is None:
        return None

    perfis = [nome for nome in perfis if nome in fatores]
    velocidades = (10, 20, 30, 36, 50, 70)

    dados = [
        [v] + [
            round(
                rotor.potencia(v / 3.6, cp=CP_PROJ * fatores[nome]),
                0,
            )
            for nome in perfis
        ]
        for v in velocidades
    ]
    df = pd.DataFrame(dados, columns=["V (km/h)"] + perfis)

    fig, ax = plt.subplots(figsize=(14, len(perfis) * 0.5 + 2))
    ax.axis("off")
    ax.set_title("Potência por perfil (W), Cp escalado pelo fator relativo")
    tabela = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="center",
    )
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1.2, 1.2)
    fig.tight_layout()
    salvar_figura(fig, "fig08_tabela_potencia", args)
    df.to_csv(
        os.path.join(args.outdir, "tabela_potencia.csv"),
        index=False,
    )
    return df


def plotar_mapa_sensibilidade(
    res,
    args,
    perfil=None,
    sigma_min=0.15,
    sigma_max=0.60,
    n_sigma=25,
    tsr_min=1.0,
    tsr_max=7.0,
    n_tsr=25,
):
    perfil = perfil or melhor_perfil(res, chave="Cp_kin")
    if perfil is None:
        return None

    polar = carregar_polar(perfil, RE_OPERACAO, args.pasta_polar)
    sigmas = np.linspace(sigma_min, sigma_max, n_sigma)
    tsrs = np.linspace(tsr_min, tsr_max, n_tsr)
    df = varredura_sigma_tsr(polar, sigmas, tsrs)

    Z = (
        df.pivot(index="TSR", columns="sigma", values="Cp_kin")
        .reindex(index=tsrs, columns=sigmas)
        .to_numpy()
    )

    fig, ax = plt.subplots(figsize=(10, 7))
    mesh = ax.pcolormesh(
        sigmas, tsrs, Z, shading="auto", cmap="viridis"
    )
    fig.colorbar(mesh, ax=ax, label="Cp cinemático (relativo)")

    i, j = np.unravel_index(np.argmax(Z), Z.shape)
    ax.plot(
        sigmas[j], tsrs[i], "r*", ms=12, label="Máximo da malha"
    )
    ax.set_xlabel("Solidez sigma")
    ax.set_ylabel("TSR")
    ax.set_title(
        f"\nMapa de sensibilidade, perfil {perfil}, "
        f"Re = {RE_OPERACAO:.1e}",
        fontsize=12,
        pad=20,
    )
    ax.legend()
    fig.tight_layout()
    salvar_figura(fig, "fig09_mapa_sensibilidade", args)

    df.to_csv(
        os.path.join(args.outdir, "sensibilidade_sigma_tsr.csv"),
        index=False,
    )
    return df


def plotar_radar(res, perfis, args, Re=RE_OPERACAO):
    perfis = [
        nome for nome in perfis
        if res.get(nome, {}).get("_disponivel")
    ]
    if not perfis:
        return

    metricas = ["Cl/Cd max", "Cl max", "alpha* (deg)", "Ct", "Cp_kin"]
    valores = {
        nome: [res[nome][Re][metrica] for metrica in metricas]
        for nome in perfis
    }
    maximos = [
        max(valores[nome][i] for nome in perfis)
        for i in range(len(metricas))
    ]
    angulos = np.linspace(
        0, 2 * np.pi, len(metricas), endpoint=False
    ).tolist()
    angulos_fechados = angulos + angulos[:1]

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, polar=True)

    for nome in perfis:
        normalizados = [
            valor / maximos[i] if maximos[i] else 0.0
            for i, valor in enumerate(valores[nome])
        ]
        normalizados += normalizados[:1]
        ax.plot(angulos_fechados, normalizados, lw=2.4, label=nome)
        ax.fill(angulos_fechados, normalizados, alpha=0.08)

    ax.set_xticks(angulos)
    ax.set_xticklabels([])
    ax.tick_params(axis="y", labelsize=13)

    deslocamentos = {
        "Cl/Cd max": (0.14, 0.12),
        "alpha* (deg)": (0.14, -0.12),
    }

    for angulo, metrica in zip(angulos, metricas):
        dr, dtheta = deslocamentos.get(metrica, (0.0, 0.0))
        ax.text(
            angulo + dtheta,
            1.18 + dr,
            metrica,
            fontsize=15,
            ha="center",
            va="center",
        )

    ax.set_title(
        f"Métricas normalizadas, Re = {Re:.0e}",
        fontsize=18,
        pad=42,
    )
    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.38, 1.14),
        fontsize=14,
    )
    fig.tight_layout()
    salvar_figura(fig, "fig10_radar_metricas", args)


def plotar_weibull(rotor, res, args, perfil=None):
    fatores, melhor = fatores_perfil(res)
    perfil = perfil or melhor
    if perfil is None:
        return None

    k, A = args.k_weibull, args.A_weibull
    v = np.linspace(0.01, 25.0, 400)
    pdf = weibull_pdf(v, k, A)
    energia = aep_weibull(rotor, fatores[perfil], k, A)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(v, pdf, label=f"Weibull k = {k}, A = {A} m/s")

    # Destaca a faixa declarada, sem alterar a integração original da AEP.
    faixa = (
        (v >= V_CUT_IN_KMH / 3.6)
        & (v <= V_CUT_OUT_KMH / 3.6)
    )
    ax.fill_between(
        v,
        pdf,
        where=faixa,
        color="tab:orange",
        alpha=0.15,
        label="Faixa declarada entre cut-in e cut-out",
    )

    for velocidade, rotulo in (
        (V_CUT_IN_KMH / 3.6, "cut-in"),
        (rotor.V_nominal, "nominal"),
        (V_CUT_OUT_KMH / 3.6, "cut-out"),
    ):
        ax.axvline(velocidade, ls=":", c="k", lw=0.9)
        ax.text(
            velocidade,
            max(pdf) * 0.9,
            rotulo,
            rotation=90,
            fontsize=8,
            va="top",
        )

    ax.set_title(
        f"Weibull, perfil {perfil}\n"
        f"AEP provisória: {energia['AEP (kWh/ano)']:.1f} kWh/ano | "
        f"FC: {energia['Fator de capacidade']:.3f}",
        fontsize=11,
    )
    ax.set_xlabel("Velocidade do vento (m/s)")
    ax.set_ylabel("Densidade de probabilidade")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)
    fig.tight_layout()
    salvar_figura(fig, "fig11_weibull_aep", args)
    return energia


def plotar_validacao(val_df, args):
    if val_df.empty:
        return

    fig, ax = plt.subplots(figsize=(11, 6))
    x = np.arange(len(val_df))

    for deslocamento, coluna, rotulo, formato in (
        (-0.2, "Cl/Cd max (modelo)", "Modelo: Cl/Cd máximo", "%.3f"),
        (
            0.2,
            "Indicador de referência (artigo)",
            "Indicador reportado no artigo",
            "%.4f",
        ),
    ):
        barras = ax.bar(
            x + deslocamento,
            val_df[coluna],
            0.4,
            label=rotulo,
        )
        ax.bar_label(barras, fmt=formato, padding=3, fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(val_df["Perfil"])
    ax.set_ylabel("Valor")
    ax.set_title(
        "Comparação exploratória com o artigo\n"
        "Natureza do indicador de referência pendente de confirmação",
        fontsize=12,
    )
    ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=9)
    fig.tight_layout()
    salvar_figura(fig, "fig12_validacao_artigo", args)


def plotar_ct_estatico(res, perfis, args, Re=RE_OPERACAO):
    perfis = [
        nome for nome in perfis
        if res.get(nome, {}).get("_disponivel")
    ]
    if not perfis:
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    valores = [res[nome][Re]["Ct estatico"] for nome in perfis]
    barras = ax.bar(perfis, valores, color="tab:green")
    ax.bar_label(barras, fmt="%.4f", padding=3, fontsize=9)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Indicador de torque estático")
    ax.set_title(
        f"Indicador de autopartida, TSR = 0, Re = {Re:.0e}"
    )
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    salvar_figura(fig, "fig13_ct_estatico", args)


# =============================================================================
# 8. RELATÓRIO E EXECUÇÃO
# =============================================================================

def imprimir_rotor(rotor):
    print("=" * 68)
    print("DIMENSIONAMENTO DO ROTOR")
    print("=" * 68)

    for rotulo, valor, unidade in (
        ("Diâmetro (D)", rotor.D, "m"),
        ("Altura (H)", rotor.H, "m"),
        ("Corda (c)", rotor.c, "m"),
        ("Área varrida (A)", rotor.A, "m²"),
        ("Raio (R)", rotor.R, "m"),
        ("Razão de aspecto (H/D)", rotor.AR, ""),
        ("Solidez (sigma)", rotor.sigma, ""),
        ("Potência nominal", rotor.P_nominal, "W"),
        ("Rotação nominal", rotor.rpm(rotor.V_nominal), "rpm"),
        ("Torque nominal", rotor.torque(rotor.V_nominal), "N.m"),
    ):
        print(f"{rotulo:<26} {valor:.3f} {unidade}")

    print(f"Número de pás:            {rotor.N_pas}")
    print(
        f"Re de corda nominal:       "
        f"{rotor.re_corda(rotor.V_nominal):.3e}"
    )
    print(
        "Dimensões de referência:   "
        f"{REFERENCIA_ARTIGO['dimensoes_artigo']}"
    )
    print()


def parse_args(argv=None):
    ap = argparse.ArgumentParser(
        description="Análise paramétrica de rotor H-Darrieus."
    )

    # Os caminhos são resolvidos em main(), após a leitura dos argumentos.
    ap.add_argument("--pasta-polar", default=None)
    ap.add_argument("--outdir", default=None)
    ap.add_argument(
        "--formato", default="png", choices=["png", "pdf", "svg"]
    )
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument(
        "--mostrar",
        dest="mostrar",
        action="store_true",
        default=True,
    )
    ap.add_argument(
        "--nao-mostrar",
        dest="mostrar",
        action="store_false",
    )
    ap.add_argument("--perfis", nargs="+", default=PERFIS_TODOS.copy())
    ap.add_argument("--potencia", type=float, default=P_NOMINAL_W)
    ap.add_argument("--vento-nominal", type=float, default=V_NOMINAL_MS)
    ap.add_argument("--cp", type=float, default=CP_PROJ)
    ap.add_argument("--pas", type=int, default=N_PAS_REF)
    ap.add_argument("--ar", type=float, default=AR_REF)
    ap.add_argument("--sigma", type=float, default=SIGMA_REF)
    ap.add_argument("--tsr", type=float, default=TSR_REF)
    ap.add_argument("--k-weibull", type=float, default=2.0)
    ap.add_argument("--A-weibull", type=float, default=6.0)
    ap.add_argument("--sem-graficos", action="store_true")

    # Evita interpretar os argumentos internos do kernel como opções do programa.
    if argv is None and "ipykernel" in sys.modules:
        argv = []

    args, desconhecidos = ap.parse_known_args(argv)

    if desconhecidos:
        print(
            "[aviso] Argumentos não reconhecidos, ignorados: "
            f"{desconhecidos}"
        )

    if args.dpi <= 0:
        ap.error("--dpi deve ser positivo.")

    if args.k_weibull <= 0 or args.A_weibull <= 0:
        ap.error("Os parâmetros de Weibull devem ser positivos.")

    return args


def main(argv=None):
    args = parse_args(argv)

    # Valida o projeto antes de realizar downloads.
    parametros = Parametros(
        P_nominal=args.potencia,
        V_nominal=args.vento_nominal,
        Cp=args.cp,
        N_pas=args.pas,
        AR=args.ar,
        sigma=args.sigma,
        TSR=args.tsr,
    )

    # Uma pasta informada explicitamente não é apagada nem substituída.
    if args.pasta_polar is None:
        pasta_polar, pasta_saida = configurar_ambiente(
            FONTE_EXECUCAO,
            args.perfis,
            RE_LIST,
        )
        args.pasta_polar = pasta_polar
        if args.outdir is None:
            args.outdir = pasta_saida

    elif args.outdir is None:
        args.outdir = (
            PASTA_SAIDA_GITHUB
            if FONTE_EXECUCAO.lower().strip() == "github"
            else os.path.join(
                os.path.dirname(os.path.abspath(args.pasta_polar)),
                "saidas",
            )
        )

    args.pasta_polar = os.path.abspath(args.pasta_polar)
    args.outdir = os.path.abspath(args.outdir)

    os.makedirs(args.pasta_polar, exist_ok=True)
    os.makedirs(args.outdir, exist_ok=True)

    # Necessário em notebooks: evita reutilizar polares de execuções anteriores.
    _CACHE_POLAR.clear()
    _ERROS_POLAR.clear()

    print(f"[diretório] Polares: {args.pasta_polar}")
    print(f"[diretório] Saídas:  {args.outdir}\n")

    rotor = dimensionar(parametros)
    imprimir_rotor(rotor)

    print("=" * 68)
    print("SALVAGUARDA DE PRÉ-AVALIAÇÃO DAS POLARES")
    print("=" * 68)

    diagnostico = diagnosticar_polares(
        args.perfis,
        RE_LIST,
        args.pasta_polar,
    )
    print(diagnostico.to_string(index=False))
    diagnostico.to_csv(
        os.path.join(args.outdir, "diagnostico_polares.csv"),
        index=False,
    )

    res = comparar_perfis(
        args.perfis,
        RE_LIST,
        args.tsr,
        args.sigma,
        args.pasta_polar,
    )
    disponiveis = perfis_analisados(res)
    pendentes = [
        nome for nome in args.perfis if nome not in disponiveis
    ]

    print(f"\nPerfis carregados: {disponiveis}")

    if pendentes:
        print(
            "[aviso] Perfis sem todas as polares válidas: "
            + ", ".join(pendentes)
        )
        print(
            "[aviso] Padrão esperado: "
            "<perfil>_Re<inteiro>.dat, .csv ou .txt"
        )

    print("\n" + "=" * 68)
    print(f"COMPARAÇÃO DE PERFIS EM TSR {args.tsr}")
    print("=" * 68)

    for nome in disponiveis:
        familia = PERFIS_METADADOS.get(nome, {}).get("familia", "N/A")
        print(f"\n{nome} ({familia}):")

        for Re in RE_LIST:
            info = res[nome][Re]
            print(
                f"  Re = {Re:.0e}: "
                f"Cp_kin = {info['Cp_kin']:.4f} | "
                f"Ct = {info['Ct']:.4f} | "
                f"Ct estático = {info['Ct estatico']:.4f} | "
                f"Cl/Cd máx = {info['Cl/Cd max']:.2f} | "
                f"Cl máx = {info['Cl max']:.2f}"
            )

    tabela_perfis(res, RE_LIST).to_csv(
        os.path.join(args.outdir, "resultados_perfis.csv"),
        index=False,
    )

    print("\n" + "=" * 68)
    print("COMPARAÇÃO EXPLORATÓRIA COM O ARTIGO")
    print("=" * 68)

    df_val = tabela_validacao(res)
    df_val.to_csv(
        os.path.join(args.outdir, "validacao_artigo.csv"),
        index=False,
    )

    if df_val.empty:
        print("Sem polares disponíveis para comparação.")
    else:
        print(df_val.to_string(index=False))
        modelo, referencia, coincide = verificar_ranking(res)
        print(f"\nRanking do modelo:     {modelo}")
        print(f"Ranking de referência: {referencia}")
        print(f"Coincidência: {'sim' if coincide else 'não'}")
        print(
            "Spearman: "
            f"{ranking_spearman(modelo, referencia):.3f}"
        )

    fatores, melhor = fatores_perfil(res)

    if melhor is None:
        energia = {
            "AEP (kWh/ano)": None,
            "Fator de capacidade": None,
            "Weibull k": args.k_weibull,
            "Weibull A (m/s)": args.A_weibull,
            "Status dos parâmetros": "sem perfil analisável",
        }
        print("\n[aviso] Nenhum perfil disponível para estimar a AEP.")

    else:
        print(f"\nMelhor perfil pelo Cp cinemático: {melhor}")
        print(
            "Fatores relativos: "
            + ", ".join(
                f"{nome} = {fator:.3f}"
                for nome, fator in fatores.items()
            )
        )

        if any(fator < 0 for fator in fatores.values()):
            print(
                "[aviso] Há fatores negativos; as estimativas de "
                "potência desses perfis exigem revisão do modelo."
            )

        if res[melhor][RE_OPERACAO]["Cp_kin"] <= 0:
            print(
                "[aviso] O maior Cp cinemático não é positivo; "
                "a normalização energética exige revisão."
            )

        energia = aep_weibull(
            rotor,
            fatores[melhor],
            args.k_weibull,
            args.A_weibull,
        )
        print(
            f"AEP provisória: {energia['AEP (kWh/ano)']:.1f} kWh/ano | "
            f"FC: {energia['Fator de capacidade']:.3f}"
        )

    resumo = {
        "parametros": vars(args),
        "fonte_execucao": FONTE_EXECUCAO,
        "rotor": {
            "D": rotor.D,
            "H": rotor.H,
            "c": rotor.c,
            "A": rotor.A,
            "R": rotor.R,
            "rpm": rotor.rpm(rotor.V_nominal),
            "torque_Nm": rotor.torque(rotor.V_nominal),
            "Re_corda_nominal": rotor.re_corda(rotor.V_nominal),
        },
        "perfis_analisados": disponiveis,
        "perfis_pendentes": pendentes,
        "fatores_perfil": fatores,
        "melhor_perfil": melhor,
        "aep": energia,
        "referencia_artigo": REFERENCIA_ARTIGO,
        "ressalvas": [
            "Cp cinemático utilizado como indicador relativo.",
            "Indicador do artigo ainda não confirmado.",
            "Parâmetros de Weibull provisórios.",
            (
                "A integração de AEP mantém a formulação original, "
                "sem aplicar corte de potência em cut-in e cut-out."
            ),
            (
                "O indicador Ct original não inclui a ponderação "
                "w2 utilizada no Cp cinemático; portanto, não se "
                "deve assumir Cp_kin = TSR * Ct nesta implementação."
            ),
        ],
    }

    caminho_resumo = os.path.join(args.outdir, "resumo.json")
    with open(caminho_resumo, "w", encoding="utf-8") as arquivo:
        json.dump(
            resumo,
            arquivo,
            ensure_ascii=False,
            indent=2,
        )
    print(f"[dados] {caminho_resumo}")

    if not args.sem_graficos:
        print("\nGerando visualizações...")

        plotar_cl_cd_alpha(args.perfis, RE_LIST, args)
        plotar_polar_cl_cd(args.perfis, RE_LIST, args)
        plotar_cp_tsr(args.perfis, args)
        plotar_cp_barras(res, args.perfis, RE_LIST, args)
        plotar_curva_potencia(rotor, res, args.perfis, args)
        plotar_reynolds_operacao(rotor, args)
        plotar_cl_max_alpha(res, args.perfis, RE_LIST, args)
        plotar_tabela_potencia(rotor, res, args.perfis, args)
        plotar_mapa_sensibilidade(res, args, perfil=melhor)
        plotar_radar(res, args.perfis, args)
        plotar_weibull(rotor, res, args, perfil=melhor)
        plotar_validacao(df_val, args)
        plotar_ct_estatico(res, args.perfis, args)

    if disponiveis:
        print("\nExecução concluída.")
    else:
        print(
            "\nExecução concluída sem perfis analisáveis. "
            "Consulte diagnostico_polares.csv e os avisos de download."
        )

    return res, rotor


if __name__ == "__main__":
    res, rotor = main()
