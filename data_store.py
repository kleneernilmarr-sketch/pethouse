"""
Camada simples de "banco de dados" em arquivos .json.

Cada tabela é um arquivo em data/<nome>.json contendo uma lista de
dicionários com um campo "id" inteiro sequencial. Quando o banco de
dados de verdade for criado, basta trocar as funções abaixo por
chamadas ao ORM/SQL - o resto do app.py não muda.
"""
import json
import os
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

_lock = threading.Lock()  # evita corrida entre requisições simultâneas


def _caminho(tabela: str) -> str:
    return os.path.join(DATA_DIR, f"{tabela}.json")


def carregar(tabela: str) -> list:
    """Lê data/<tabela>.json e devolve a lista de registros (ou [])."""
    caminho = _caminho(tabela)
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read().strip()
        return json.loads(conteudo) if conteudo else []


def salvar(tabela: str, registros: list) -> None:
    """Sobrescreve data/<tabela>.json com a lista fornecida."""
    caminho = _caminho(tabela)
    with _lock:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)


def proximo_id(registros: list) -> int:
    return (max((r["id"] for r in registros), default=0)) + 1


def encontrar(tabela: str, id_: int) -> dict | None:
    return next((r for r in carregar(tabela) if r["id"] == int(id_)), None)


def inserir(tabela: str, dados: dict) -> dict:
    registros = carregar(tabela)
    dados = dict(dados)
    dados["id"] = proximo_id(registros)
    registros.append(dados)
    salvar(tabela, registros)
    return dados


def atualizar(tabela: str, id_: int, dados: dict) -> dict | None:
    registros = carregar(tabela)
    for i, r in enumerate(registros):
        if r["id"] == int(id_):
            atualizado = {**r, **dados, "id": r["id"]}
            registros[i] = atualizado
            salvar(tabela, registros)
            return atualizado
    return None


def excluir(tabela: str, id_: int) -> bool:
    registros = carregar(tabela)
    novos = [r for r in registros if r["id"] != int(id_)]
    if len(novos) == len(registros):
        return False
    salvar(tabela, novos)
    return True
