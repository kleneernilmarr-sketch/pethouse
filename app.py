"""
Loja de produtos pet estilo drop shipping) - rotas do aplicativo.

Como rodar
    pip install -r requirements.txt
    python app.py
Depois abra http://127.0.0.1:5000

Banco de dados: por enquanto tudo fica em arquivos .json dentro de
data/ (veja data_store.py). Quando o banco de dados de verdade for
criado só é preciso trocar as funções de data_store.py.
"""
import os
import unicodedata
from datetime import date
from functools import wraps

from flask import (Flask, abort, flash, redirect, render_template, request,
                    session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import data_store as db

app = Flask(__name__)
app.secret_key = "troque-esta-chave-antes-de-colocar-em-producao"

# ---------------------------------------------------------------------------
# Configuração da loja (edite aqui: aparece no topo, rodapé e contato)
# ---------------------------------------------------------------------------
LOJA = {
    "nome": "PetHouse",
    "slogan": "Tudo para o seu pet, direto na porta de casa",
    "email": "contato@pethouse.com.br",
    "whatsapp": "5511999999999",  # DDI + DDD + número, só dígitos
    "endereco": "Rua dos Pets, 456 - Vila Mariana, São Paulo - SP",
    "frete_gratis_acima": 199,
    "prazo_entrega": "7 a 15 dias úteis",
    "parcelas": 3,
}

# ---------------------------------------------------------------------------
# Dados do TRABALHO ACADÊMICO (aparecem na apresentação "/" e na documentação)
# Troque os textos abaixo pelos dados reais do grupo.
# ---------------------------------------------------------------------------
TRABALHO = {
    "instituicao": "Universidade Cidade de São Paulo",
    "curso": "Engenharia de Software",
    "disciplina": "Modelagem de Banco de Dados",
    "professor": "Clovis Jose Ramos Ferraro",
    "turma": "Grupo 7 / 2º Semestre",
}

# ---------------------------------------------------------------------------
# EQUIPE (aparece na página Contato)
#
# COMO ADICIONAR UM INTEGRANTE: copie um bloco { ... }, cole logo abaixo (com a
# vírgula no final) e troque os dados. Pode ter quantos precisar.
# COMO REMOVER: apague o bloco inteiro.
#
#   nome      -> nome completo
#   area      -> o que a pessoa fez no projeto
#   linkedin  -> link completo do perfil (deixe "" para não mostrar)
#   telefone  -> com DDD (deixe "" para não mostrar)
#   foto      -> nome do arquivo na pasta static/assets/imagens/equipe/
#                (sem a foto, aparece um círculo com as iniciais do nome)
# ---------------------------------------------------------------------------
EQUIPE = [
    {"nome": "Nome do integrante 1", "area": "Back-end e banco de dados",
     "linkedin": "https://www.linkedin.com/in/usuario-1", "telefone": "(11) 90000-0001",
     "foto": "integrante-1.jpg"},
    {"nome": "Nome do integrante 2", "area": "Front-end e design",
     "linkedin": "https://www.linkedin.com/in/usuario-2", "telefone": "(11) 90000-0002",
     "foto": "integrante-2.jpg"},
    {"nome": "Nome do integrante 3", "area": "Documentação e orçamento de hospedagem",
     "linkedin": "https://www.linkedin.com/in/usuario-3", "telefone": "(11) 90000-0003",
     "foto": "integrante-3.jpg"},
    {"nome": "Nome do integrante 4", "area": "Testes e apresentação",
     "linkedin": "https://www.linkedin.com/in/usuario-4", "telefone": "(11) 90000-0004",
     "foto": "integrante-4.jpg"},
]

# Níveis do programa de fidelidade (1 ponto = R$ 1 gasto em pedidos concluídos).
NIVEIS_FIDELIDADE = [
    {"nome": "Patinha Bronze", "minimo": 0,
     "beneficios": ["Acúmulo de pontos em toda compra", "Novidades em primeira mão por e-mail"]},
    {"nome": "Patinha Prata", "minimo": 200,
     "beneficios": ["5% de desconto em produtos de higiene", "Frete grátis a partir de R$ 150"]},
    {"nome": "Patinha Ouro", "minimo": 500,
     "beneficios": ["10% de desconto em toda a loja", "Frete grátis em qualquer valor",
                     "Prioridade para agendar banho e tosa"]},
]

# ---------------------------------------------------------------------------
# Categorias (slug é usado na URL: /categoria/<slug>)
# ---------------------------------------------------------------------------
CATEGORIAS = [
    {"slug": "caes", "nome": "Cães", "emoji": "🐶", "cor": "#FFE3B8"},
    {"slug": "gatos", "nome": "Gatos", "emoji": "🐱", "cor": "#D7E4FF"},
    {"slug": "brinquedos", "nome": "Brinquedos", "emoji": "🧸", "cor": "#FFD3D0"},
    {"slug": "higiene", "nome": "Higiene", "emoji": "🛁", "cor": "#CFF1E6"},
    {"slug": "passeio", "nome": "Passeio", "emoji": "🦮", "cor": "#E6DCFF"},
    {"slug": "camas", "nome": "Camas e casinhas", "emoji": "🛏️", "cor": "#FFF0A8"},
]
CATEGORIAS_POR_SLUG = {c["slug"]: c for c in CATEGORIAS}

# ---------------------------------------------------------------------------
# MÍDIAS DO SITE (fotos e vídeos)  -->  tudo fica em static/assets/
#
#   static/assets/imagens/site/          logo, favicon, banner da home
#   static/assets/imagens/produtos/      fotos dos produtos
#   static/assets/imagens/fornecedores/  fotos/logos dos fornecedores
#   static/assets/imagens/pets/          fotos dos pets
#   static/assets/imagens/equipe/        fotos dos integrantes do grupo
#   static/assets/videos/site/           vídeo institucional (home)
#   static/assets/videos/produtos/       vídeos dos produtos
#
# COMO USAR: coloque o arquivo na pasta certa e confira que o NOME aqui
# embaixo é igual ao nome do arquivo. Se o arquivo ainda não existir, o
# site continua funcionando normalmente (mostra emoji / esconde o vídeo).
# ---------------------------------------------------------------------------
PASTA_IMAGENS = "assets/imagens"   # relativa à pasta static/
PASTA_VIDEOS = "assets/videos"     # relativa à pasta static/

# Mídias gerais do site (troque só o nome do arquivo, se quiser).
MIDIA_SITE = {
    "logo": "logo.png",                          # cabeçalho (substitui o texto "PetHouse")
    "favicon": "favicon.png",                    # ícone da aba do navegador
    "banner_inicio": "banner-inicio.jpg",        # foto ao lado do texto de abertura da home
    "video_inicio": "video-institucional.mp4",   # vídeo da home (formato .mp4)
    "video_inicio_capa": "video-institucional-capa.jpg",  # imagem de capa do vídeo (opcional)
}

# Mídias de cada produto, pelo id do produto.
#   imagem -> arquivo em static/assets/imagens/produtos/
#   video  -> arquivo em static/assets/videos/produtos/   (.mp4)
# Troque os nomes abaixo pelos nomes reais dos seus arquivos.
MIDIA_PRODUTOS = {
    1:  {"imagem": "produto-01.jpg", "video": "produto-01.mp4"},
    2:  {"imagem": "produto-02.jpg", "video": "produto-02.mp4"},
    3:  {"imagem": "produto-03.jpg", "video": "produto-03.mp4"},
    4:  {"imagem": "produto-04.jpg", "video": "produto-04.mp4"},
    5:  {"imagem": "produto-05.jpg", "video": "produto-05.mp4"},
    6:  {"imagem": "produto-06.jpg", "video": "produto-06.mp4"},
    7:  {"imagem": "produto-07.jpg", "video": "produto-07.mp4"},
    8:  {"imagem": "produto-08.jpg", "video": "produto-08.mp4"},
    9:  {"imagem": "produto-09.jpg", "video": "produto-09.mp4"},
    10: {"imagem": "produto-10.jpg", "video": "produto-10.mp4"},
    11: {"imagem": "produto-11.jpg", "video": "produto-11.mp4"},
    12: {"imagem": "produto-12.jpg", "video": "produto-12.mp4"},
}
# Fornecedores: por padrão o site procura "fornecedor-<id>.jpg" em
# imagens/fornecedores/ (ou o nome digitado no campo "Foto" do painel admin).
# Pets: por padrão o site procura "pet-<id>.jpg" em imagens/pets/
# (ou o nome digitado no campo "Foto" do painel admin).


def _url_midia(pasta_base: str, subpasta: str, arquivo):
    """Devolve a URL do arquivo em static/<pasta_base>/<subpasta>/ ou None
    se o nome estiver vazio, for suspeito ou o arquivo ainda não existir."""
    if not arquivo or os.path.basename(arquivo) != arquivo:
        return None
    caminho = f"{pasta_base}/{subpasta}/{arquivo}"
    if os.path.isfile(os.path.join(app.static_folder, *caminho.split("/"))):
        return url_for("static", filename=caminho)
    return None


@app.template_global()
def imagem_url(subpasta: str, arquivo):
    """Uso nos templates: {{ imagem_url('produtos', p.imagem) }}"""
    return _url_midia(PASTA_IMAGENS, subpasta, arquivo)


@app.template_global()
def video_url(subpasta: str, arquivo):
    """Uso nos templates: {{ video_url('produtos', p.video) }}"""
    return _url_midia(PASTA_VIDEOS, subpasta, arquivo)


# ---------------------------------------------------------------------------
# Produtos (dados de exemplo - troque pelos produtos do seu fornecedor).
#   imagem/video: vêm da tabela MIDIA_PRODUTOS acima (nome do arquivo em static/assets/).
#                 Sem arquivo, o site mostra o emoji da categoria.
#   link_compra: link de checkout / página do fornecedor
#   destaque:    True = aparece em "Produtos em destaque" na página inicial
# ---------------------------------------------------------------------------
PRODUTOS = [
    {"id": 1, "nome": "Comedouro lento antiengasgo para cães", "categoria": "caes",
     "preco": 39.90, "preco_antigo": 69.90, "destaque": True,
     "descricao": "Relevos internos que forçam o cão a comer mais devagar, ajudando na digestão. Material atóxico e base antiderrapante."},
    {"id": 2, "nome": "Fonte de água elétrica para gatos 2L", "categoria": "gatos",
     "preco": 119.90, "preco_antigo": 189.90, "destaque": True,
     "descricao": "Água sempre corrente e fresca, que estimula o gato a beber mais. Filtro de carvão e funcionamento silencioso."},
    {"id": 3, "nome": "Arranhador torre com plataformas", "categoria": "gatos",
     "preco": 219.90, "preco_antigo": 329.90, "destaque": True,
     "descricao": "Torre com sisal, plataformas e toca para descansar. Protege o sofá e dá ao gato um lugar só dele."},
    {"id": 4, "nome": "Peitoral anti-puxão ajustável", "categoria": "passeio",
     "preco": 59.90, "preco_antigo": 94.90, "destaque": True,
     "descricao": "Distribui a pressão pelo peito e não pelo pescoço. Tecido respirável, refletivo e com ajuste em quatro pontos."},
    {"id": 5, "nome": "Escova removedora de pelos autolimpante", "categoria": "higiene",
     "preco": 34.90, "preco_antigo": 59.90, "destaque": True,
     "descricao": "Remove pelos soltos e desembaraça sem machucar. Um botão libera os pelos acumulados para o lixo."},
    {"id": 6, "nome": "Cama ortopédica macia para cães", "categoria": "camas",
     "preco": 129.90, "preco_antigo": 199.90, "destaque": True,
     "descricao": "Espuma de suporte com capa removível e lavável. Base antiderrapante e bordas elevadas para apoiar a cabeça."},
    {"id": 7, "nome": "Bolinha interativa automática para gatos", "categoria": "brinquedos",
     "preco": 49.90, "preco_antigo": 89.90, "destaque": True,
     "descricao": "Rola sozinha em direções imprevisíveis e desliga quando o gato se cansa. Carregamento por USB."},
    {"id": 8, "nome": "Luva de banho com massagem", "categoria": "higiene",
     "preco": 29.90, "preco_antigo": None, "destaque": True,
     "descricao": "Espalha o shampoo e massageia enquanto limpa. Cerdas de silicone macias, serve para cães e gatos."},
    {"id": 9, "nome": "Guia retrátil 5 metros", "categoria": "passeio",
     "preco": 44.90, "preco_antigo": 74.90, "destaque": False,
     "descricao": "Trava com um clique, cabo resistente e empunhadura antiderrapante. Indicada para cães de até 20 kg."},
    {"id": 10, "nome": "Casinha dobrável para gatos", "categoria": "camas",
     "preco": 79.90, "preco_antigo": 119.90, "destaque": False,
     "descricao": "Toca de feltro que dobra para guardar. Interior acolchoado e fácil de limpar."},
    {"id": 11, "nome": "Kit 5 brinquedos mordedores para cães", "categoria": "brinquedos",
     "preco": 54.90, "preco_antigo": 84.90, "destaque": False,
     "descricao": "Cinco peças de borracha e corda para roer, puxar e buscar. Ajudam a gastar energia e aliviam a ansiedade."},
    {"id": 12, "nome": "Bebedouro portátil para passeio", "categoria": "passeio",
     "preco": 24.90, "preco_antigo": 39.90, "destaque": False,
     "descricao": "Garrafa com cocho dobrável, que cabe na mochila. Fecha sem vazar."},
]

# Campos calculados (desconto, emoji e cor da categoria)
for _p in PRODUTOS:
    _cat = CATEGORIAS_POR_SLUG[_p["categoria"]]
    _p["categoria_nome"] = _cat["nome"]
    _p["emoji"] = _cat["emoji"]
    _p["cor"] = _cat["cor"]
    for _chave, _valor in MIDIA_PRODUTOS.get(_p["id"], {}).items():
        _p.setdefault(_chave, _valor)
    _p.setdefault("imagem", None)
    _p.setdefault("video", None)
    _p.setdefault("link_compra", "#")
    _p["desconto"] = (
        round((1 - _p["preco"] / _p["preco_antigo"]) * 100) if _p["preco_antigo"] else 0
    )

PRODUTOS_POR_ID = {p["id"]: p for p in PRODUTOS}


# ---------------------------------------------------------------------------
# Cadastro das novas áreas administrativas (Clientes, Pets, Estoque,
# Fornecedores, Transportadoras, Agendamentos, Orçamentos).
#
# Cada entrada descreve os campos do formulário; as rotas /admin/<entidade>
# são genéricas e leem esta configuração, então criar uma área nova é
# só adicionar um bloco aqui - não precisa de rota nem template novos.
#
# tipos de campo suportados: text, email, tel, number, date, time,
# textarea, select (com "opcoes" fixas) e select_ref (lista vinda de
# outra tabela / dos produtos).
# ---------------------------------------------------------------------------
ENTIDADES = {
    "clientes": {
        "titulo": "Clientes",
        "titulo_singular": "Cliente",
        "tabela": "clientes",
        "colunas_lista": ["nome", "email", "telefone", "pontos_fidelidade"],
        "campos": [
            {"nome": "nome", "rotulo": "Nome completo", "tipo": "text", "obrigatorio": True},
            {"nome": "email", "rotulo": "E-mail", "tipo": "email", "obrigatorio": True},
            {"nome": "telefone", "rotulo": "Telefone / WhatsApp", "tipo": "tel"},
            {"nome": "cpf", "rotulo": "CPF", "tipo": "text"},
            {"nome": "endereco", "rotulo": "Endereço", "tipo": "text"},
            {"nome": "cidade", "rotulo": "Cidade", "tipo": "text"},
            {"nome": "estado", "rotulo": "UF", "tipo": "text"},
            {"nome": "cep", "rotulo": "CEP", "tipo": "text"},
            {"nome": "pontos_fidelidade", "rotulo": "Pontos de fidelidade", "tipo": "number",
             "ajuda": "Ajuste manual (ex.: bônus de campanha). 1 ponto = R$ 1 em compras."},
        ],
    },
    "pets": {
        "titulo": "Pets",
        "titulo_singular": "Pet",
        "tabela": "pets",
        "colunas_lista": ["nome", "especie", "raca", "porte"],
        "campos": [
            {"nome": "nome", "rotulo": "Nome do pet", "tipo": "text", "obrigatorio": True},
            {"nome": "cliente_id", "rotulo": "Tutor(a)", "tipo": "select_ref",
             "ref_tabela": "clientes", "ref_campo_rotulo": "nome"},
            {"nome": "especie", "rotulo": "Espécie", "tipo": "select",
             "opcoes": ["Cachorro", "Gato", "Outro"]},
            {"nome": "raca", "rotulo": "Raça", "tipo": "text"},
            {"nome": "porte", "rotulo": "Porte", "tipo": "select",
             "opcoes": ["Pequeno", "Médio", "Grande"]},
            {"nome": "data_nascimento", "rotulo": "Data de nascimento", "tipo": "date"},
            {"nome": "observacoes", "rotulo": "Observações (alergias, cuidados...)", "tipo": "textarea"},
            {"nome": "foto", "rotulo": "Foto (nome do arquivo)", "tipo": "text",
             "ajuda": "Ex.: pet-2.jpg — arquivo em static/assets/imagens/pets/. Vazio = pet-<id>.jpg"},
        ],
    },
    "estoque": {
        "titulo": "Estoque",
        "titulo_singular": "Item de estoque",
        "tabela": "estoque",
        "colunas_lista": ["produto_id", "quantidade", "quantidade_minima", "localizacao"],
        "campos": [
            {"nome": "produto_id", "rotulo": "Produto", "tipo": "select_produto", "obrigatorio": True},
            {"nome": "quantidade", "rotulo": "Quantidade em estoque", "tipo": "number", "obrigatorio": True},
            {"nome": "quantidade_minima", "rotulo": "Estoque mínimo (alerta)", "tipo": "number"},
            {"nome": "localizacao", "rotulo": "Localização no depósito", "tipo": "text"},
            {"nome": "ultima_atualizacao", "rotulo": "Última atualização", "tipo": "date"},
        ],
    },
    "fornecedores": {
        "titulo": "Fornecedores",
        "titulo_singular": "Fornecedor",
        "tabela": "fornecedores",
        "colunas_lista": ["nome", "contato", "telefone", "prazo_entrega_dias"],
        "campos": [
            {"nome": "nome", "rotulo": "Nome / razão social", "tipo": "text", "obrigatorio": True},
            {"nome": "cnpj", "rotulo": "CNPJ", "tipo": "text"},
            {"nome": "contato", "rotulo": "Pessoa de contato", "tipo": "text"},
            {"nome": "telefone", "rotulo": "Telefone", "tipo": "tel"},
            {"nome": "email", "rotulo": "E-mail", "tipo": "email"},
            {"nome": "produtos_fornecidos", "rotulo": "Produtos fornecidos", "tipo": "textarea"},
            {"nome": "descricao_qualidade", "rotulo": "Qualidade e diferenciais da marca", "tipo": "textarea",
             "ajuda": "Texto exibido na página pública /fornecedores para o cliente."},
            {"nome": "certificacoes", "rotulo": "Certificações / especificações técnicas", "tipo": "text"},
            {"nome": "prazo_entrega_dias", "rotulo": "Prazo médio de entrega (dias)", "tipo": "number"},
            {"nome": "imagem", "rotulo": "Foto / logo (nome do arquivo)", "tipo": "text",
             "ajuda": "Ex.: fornecedor-1.jpg — arquivo em static/assets/imagens/fornecedores/. Vazio = fornecedor-<id>.jpg"},
        ],
    },
    "transportadoras": {
        "titulo": "Transportadoras",
        "titulo_singular": "Transportadora",
        "tabela": "transportadoras",
        "colunas_lista": ["nome", "regioes_atendidas", "prazo_medio_dias", "valor_frete_base"],
        "campos": [
            {"nome": "nome", "rotulo": "Nome", "tipo": "text", "obrigatorio": True},
            {"nome": "cnpj", "rotulo": "CNPJ", "tipo": "text"},
            {"nome": "telefone", "rotulo": "Telefone", "tipo": "tel"},
            {"nome": "email", "rotulo": "E-mail", "tipo": "email"},
            {"nome": "regioes_atendidas", "rotulo": "Regiões atendidas", "tipo": "text"},
            {"nome": "prazo_medio_dias", "rotulo": "Prazo médio (dias)", "tipo": "number"},
            {"nome": "valor_frete_base", "rotulo": "Valor base do frete (R$)", "tipo": "number"},
        ],
    },
    "agendamentos": {
        "titulo": "Agendamentos",
        "titulo_singular": "Agendamento",
        "tabela": "agendamentos",
        "colunas_lista": ["tipo", "data", "hora", "status"],
        "campos": [
            {"nome": "cliente_id", "rotulo": "Cliente", "tipo": "select_ref",
             "ref_tabela": "clientes", "ref_campo_rotulo": "nome"},
            {"nome": "pet_id", "rotulo": "Pet", "tipo": "select_ref",
             "ref_tabela": "pets", "ref_campo_rotulo": "nome"},
            {"nome": "tipo", "rotulo": "Tipo de serviço", "tipo": "select",
             "opcoes": ["Banho", "Tosa", "Consulta veterinária", "Entrega", "Outro"]},
            {"nome": "data", "rotulo": "Data", "tipo": "date", "obrigatorio": True},
            {"nome": "hora", "rotulo": "Hora", "tipo": "time"},
            {"nome": "status", "rotulo": "Status", "tipo": "select",
             "opcoes": ["Agendado", "Confirmado", "Concluído", "Cancelado"]},
            {"nome": "observacoes", "rotulo": "Observações", "tipo": "textarea"},
        ],
    },
    "orcamentos": {
        "titulo": "Orçamentos (tickets)",
        "titulo_singular": "Ticket de atendimento",
        "tabela": "orcamentos",
        "colunas_lista": ["assunto", "nome", "status", "data_criacao"],
        "campos": [
            {"nome": "cliente_id", "rotulo": "Cliente (se tiver conta)", "tipo": "select_ref",
             "ref_tabela": "clientes", "ref_campo_rotulo": "nome"},
            {"nome": "nome", "rotulo": "Nome de quem solicitou", "tipo": "text", "obrigatorio": True},
            {"nome": "contato", "rotulo": "Telefone ou e-mail de contato", "tipo": "text"},
            {"nome": "assunto", "rotulo": "Assunto", "tipo": "text", "obrigatorio": True},
            {"nome": "mensagem", "rotulo": "Mensagem do cliente", "tipo": "textarea"},
            {"nome": "status", "rotulo": "Status", "tipo": "select",
             "opcoes": ["Novo", "Em atendimento", "Respondido", "Concluído"]},
            {"nome": "resposta", "rotulo": "Resposta da loja", "tipo": "textarea",
             "ajuda": "Visível para o cliente na área 'Minha conta'."},
            {"nome": "data_criacao", "rotulo": "Data de abertura", "tipo": "date"},
        ],
    },
}


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------
def normalizar(texto: str) -> str:
    """Minúsculas e sem acentos, para a busca aceitar 'caes' e 'cães'."""
    texto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


@app.template_filter("so_digitos")
def so_digitos(texto) -> str:
    """'(11) 90000-0001' -> '11900000001' (usado no link tel:)."""
    return "".join(c for c in str(texto or "") if c.isdigit())


@app.template_filter("iniciais")
def iniciais(nome) -> str:
    """'Maria da Silva' -> 'MS' (círculo mostrado quando o integrante não tem foto)."""
    partes = [p for p in str(nome or "").split() if p[0].isalpha() and p.lower() not in ("da", "de", "do", "das", "dos")]
    return "".join(p[0].upper() for p in partes[:2]) or "?"


@app.template_filter("brl")
def formatar_brl(valor) -> str:
    if valor in (None, ""):
        return "-"
    inteiro = f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {inteiro}"


def nivel_fidelidade(pontos):
    """Devolve (nível atual, próximo nível ou None) a partir dos pontos acumulados."""
    pontos = pontos or 0
    atual = NIVEIS_FIDELIDADE[0]
    proximo = None
    for i, nivel in enumerate(NIVEIS_FIDELIDADE):
        if pontos >= nivel["minimo"]:
            atual = nivel
            proximo = NIVEIS_FIDELIDADE[i + 1] if i + 1 < len(NIVEIS_FIDELIDADE) else None
    return atual, proximo


def status_estoque(item):
    """'esgotado', 'baixo' ou 'ok', usado para os alertas da página de Estoque."""
    quantidade = item.get("quantidade") or 0
    minimo = item.get("quantidade_minima") or 0
    if quantidade <= 0:
        return "esgotado"
    if minimo and quantidade <= minimo:
        return "baixo"
    return "ok"


def cliente_atual():
    cliente_id = session.get("cliente_id")
    return db.encontrar("clientes", cliente_id) if cliente_id else None


def carrinho_itens():
    """Lê o carrinho da sessão e devolve a lista de itens já com produto e subtotal."""
    bruto = session.get("carrinho", {})
    itens = []
    for produto_id_str, quantidade in bruto.items():
        produto = PRODUTOS_POR_ID.get(int(produto_id_str))
        if produto:
            itens.append({
                "produto": produto,
                "quantidade": quantidade,
                "subtotal": produto["preco"] * quantidade,
            })
    return itens


def login_obrigatorio(rota):
    @wraps(rota)
    def decorada(*args, **kwargs):
        if not session.get("cliente_id"):
            flash("Faça login para continuar.", "aviso")
            return redirect(url_for("cliente_login", proximo=request.path))
        return rota(*args, **kwargs)
    return decorada


@app.context_processor
def dados_globais():
    """Variáveis disponíveis em todos os templates."""
    itens_carrinho = carrinho_itens()
    return {
        "loja": LOJA,
        "trabalho": TRABALHO,
        "categorias": CATEGORIAS,
        "ano": date.today().year,
        "contagem": {
            c["slug"]: sum(1 for p in PRODUTOS if p["categoria"] == c["slug"])
            for c in CATEGORIAS
        },
        "cliente_logado": cliente_atual(),
        "carrinho_qtd": sum(i["quantidade"] for i in itens_carrinho),
        "entidades_admin": ENTIDADES,
        "midia": {
            "logo": imagem_url("site", MIDIA_SITE["logo"]),
            "favicon": imagem_url("site", MIDIA_SITE["favicon"]),
            "banner_inicio": imagem_url("site", MIDIA_SITE["banner_inicio"]),
            "video_inicio": video_url("site", MIDIA_SITE["video_inicio"]),
            "video_inicio_capa": imagem_url("site", MIDIA_SITE["video_inicio_capa"]),
        },
    }


# ---------------------------------------------------------------------------
# Rotas da loja
# ---------------------------------------------------------------------------
@app.route("/")
def apresentacao():
    """Página de abertura do trabalho (templates/index.html): resumo + botões."""
    return render_template("index.html")


@app.route("/documentacao")
def documentacao():
    """Resumo da estrutura do projeto e do comparativo de hospedagem."""
    return render_template("documentacao.html")


@app.route("/inicio")
def inicio():
    """Primeira página da loja (o botão 'Acessar Site' leva para cá)."""
    destaques = [p for p in PRODUTOS if p["destaque"]]
    return render_template("inicio.html", destaques=destaques)


@app.route("/produtos")
def produtos():
    return render_template("produtos.html", titulo="Todos os produtos", produtos=PRODUTOS)


@app.route("/categoria/<slug>")
def categoria(slug):
    cat = CATEGORIAS_POR_SLUG.get(slug)
    if cat is None:
        abort(404)
    return render_template(
        "produtos.html",
        titulo=cat["nome"],
        produtos=[p for p in PRODUTOS if p["categoria"] == slug],
        categoria_ativa=slug,
    )


@app.route("/ofertas")
def ofertas():
    em_oferta = sorted((p for p in PRODUTOS if p["desconto"]), key=lambda p: p["desconto"], reverse=True)
    return render_template("produtos.html", titulo="Ofertas", produtos=em_oferta)


@app.route("/busca")
def busca():
    termo = request.args.get("q", "").strip()
    palavras = normalizar(termo).split()
    resultados = [
        p for p in PRODUTOS
        if palavras and all(
            w in normalizar(f"{p['nome']} {p['descricao']} {p['categoria_nome']}")
            for w in palavras
        )
    ]
    return render_template(
        "produtos.html",
        titulo=f"Resultados para “{termo}”" if termo else "Busca",
        produtos=resultados,
        termo=termo,
    )


@app.route("/produto/<int:id>")
def produto(id):
    item = PRODUTOS_POR_ID.get(id)
    if item is None:
        abort(404)
    relacionados = [p for p in PRODUTOS if p["categoria"] == item["categoria"] and p["id"] != id][:4]
    return render_template("produto.html", p=item, relacionados=relacionados)


@app.route("/contato")
def contato():
    equipe = [{**m, "foto_url": imagem_url("equipe", m.get("foto"))} for m in EQUIPE]
    return render_template("contato.html", equipe=equipe)

@app.route("/fornecedores")
def fornecedores_publico():
    """Vitrine institucional: de onde vêm os produtos e o que garante a qualidade deles."""
    fornecedores = db.carregar("fornecedores")
    return render_template("fornecedores.html", fornecedores=fornecedores)


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        cliente = cliente_atual()
        try:
            nota = max(1, min(5, int(request.form.get("nota", 5))))
        except ValueError:
            nota = 5
        db.inserir("feedbacks", {
            "cliente_id": cliente["id"] if cliente else None,
            "nome": cliente["nome"] if cliente else (request.form.get("nome", "").strip() or "Anônimo"),
            "nota": nota,
            "mensagem": request.form.get("mensagem", "").strip(),
            "data": date.today().isoformat(),
            "aprovado": False,
        })
        flash("Obrigado pelo feedback! Ele aparece na página assim que for moderado.", "sucesso")
        return redirect(url_for("feedback"))

    aprovados = sorted((f for f in db.carregar("feedbacks") if f.get("aprovado")),
                        key=lambda f: f["data"], reverse=True)
    media = round(sum(f["nota"] for f in aprovados) / len(aprovados), 1) if aprovados else None
    return render_template("feedback.html", feedbacks=aprovados, media=media, cliente=cliente_atual())


@app.route("/pet/<int:id>")
def pet_perfil(id):
    """Perfil público do pet: dados e histórico de serviços já realizados."""
    pet = db.encontrar("pets", id)
    if pet is None:
        abort(404)
    tutor = db.encontrar("clientes", pet["cliente_id"]) if pet.get("cliente_id") else None
    historico = sorted(
        (a for a in db.carregar("agendamentos") if a.get("pet_id") == id),
        key=lambda a: (a.get("data") or "", a.get("hora") or ""),
        reverse=True,
    )
    return render_template("pet_perfil.html", pet=pet, tutor=tutor, historico=historico)


@app.route("/cliente/pets/novo", methods=["GET", "POST"])
@login_obrigatorio
def cliente_pet_novo():
    if request.method == "POST":
        novo = db.inserir("pets", {
            "cliente_id": session["cliente_id"],
            "nome": request.form.get("nome", "").strip(),
            "especie": request.form.get("especie"),
            "raca": request.form.get("raca", "").strip(),
            "porte": request.form.get("porte"),
            "data_nascimento": request.form.get("data_nascimento") or None,
            "observacoes": request.form.get("observacoes", "").strip(),
        })
        flash(f"{novo['nome']} foi cadastrado(a) no seu perfil!", "sucesso")
        return redirect(url_for("pet_perfil", id=novo["id"]))
    return render_template("cliente_pet_novo.html")


@app.route("/agendamentos/novo", methods=["GET", "POST"])
@login_obrigatorio
def agendamento_novo():
    """Agenda de serviços (banho, tosa, consulta...) vista pelo lado do cliente."""
    cliente = cliente_atual()
    pets = [p for p in db.carregar("pets") if p.get("cliente_id") == cliente["id"]]
    if request.method == "POST":
        db.inserir("agendamentos", {
            "cliente_id": cliente["id"],
            "pet_id": int(request.form["pet_id"]) if request.form.get("pet_id") else None,
            "tipo": request.form.get("tipo"),
            "data": request.form.get("data"),
            "hora": request.form.get("hora"),
            "status": "Agendado",
            "observacoes": request.form.get("observacoes", "").strip(),
        })
        flash("Agendamento solicitado! Em breve confirmamos o horário por WhatsApp.", "sucesso")
        return redirect(url_for("cliente_perfil"))
    return render_template("agendamento_novo.html", pets=pets)


@app.route("/orcamentos/solicitar", methods=["GET", "POST"])
def orcamento_solicitar():
    """Ticket de atendimento personalizado - não exige login."""
    cliente = cliente_atual()
    if request.method == "POST":
        novo = db.inserir("orcamentos", {
            "cliente_id": cliente["id"] if cliente else None,
            "nome": cliente["nome"] if cliente else request.form.get("nome", "").strip(),
            "contato": (cliente.get("telefone") if cliente else request.form.get("contato", "").strip()) or "",
            "assunto": request.form.get("assunto", "").strip(),
            "mensagem": request.form.get("mensagem", "").strip(),
            "status": "Novo",
            "resposta": None,
            "data_criacao": date.today().isoformat(),
        })
        flash(f"Ticket #{novo['id']} enviado! Nossa equipe responde em até 1 dia útil.", "sucesso")
        return redirect(url_for("orcamento_solicitar"))
    return render_template("orcamento_solicitar.html", cliente=cliente)


# ---------------------------------------------------------------------------
# Carrinho de compras (guardado na sessão do navegador)
# ---------------------------------------------------------------------------
@app.route("/carrinho")
def carrinho():
    itens = carrinho_itens()
    subtotal = sum(i["subtotal"] for i in itens)
    frete = 0 if subtotal >= LOJA["frete_gratis_acima"] or not itens else 19.90
    return render_template("carrinho.html", itens=itens, subtotal=subtotal, frete=frete, total=subtotal + frete)


@app.route("/carrinho/adicionar/<int:produto_id>", methods=["POST"])
def carrinho_adicionar(produto_id):
    if produto_id not in PRODUTOS_POR_ID:
        abort(404)
    quantidade = max(1, int(request.form.get("quantidade", 1)))
    carrinho_sessao = session.get("carrinho", {})
    chave = str(produto_id)
    carrinho_sessao[chave] = carrinho_sessao.get(chave, 0) + quantidade
    session["carrinho"] = carrinho_sessao
    flash(f"{PRODUTOS_POR_ID[produto_id]['nome']} adicionado ao carrinho.", "sucesso")
    return redirect(request.referrer or url_for("carrinho"))


@app.route("/carrinho/atualizar/<int:produto_id>", methods=["POST"])
def carrinho_atualizar(produto_id):
    quantidade = int(request.form.get("quantidade", 0))
    carrinho_sessao = session.get("carrinho", {})
    chave = str(produto_id)
    if quantidade <= 0:
        carrinho_sessao.pop(chave, None)
    else:
        carrinho_sessao[chave] = quantidade
    session["carrinho"] = carrinho_sessao
    return redirect(url_for("carrinho"))


@app.route("/carrinho/remover/<int:produto_id>", methods=["POST"])
def carrinho_remover(produto_id):
    carrinho_sessao = session.get("carrinho", {})
    carrinho_sessao.pop(str(produto_id), None)
    session["carrinho"] = carrinho_sessao
    return redirect(url_for("carrinho"))


@app.route("/checkout", methods=["GET", "POST"])
@login_obrigatorio
def checkout():
    itens = carrinho_itens()
    if not itens:
        flash("Seu carrinho está vazio.", "aviso")
        return redirect(url_for("carrinho"))

    subtotal = sum(i["subtotal"] for i in itens)
    transportadoras = db.carregar("transportadoras")

    if request.method == "POST":
        transportadora_id = int(request.form.get("transportadora_id"))
        transportadora = db.encontrar("transportadoras", transportadora_id)
        frete = float(transportadora["valor_frete_base"]) if subtotal < LOJA["frete_gratis_acima"] else 0

        pedido = db.inserir("pedidos", {
            "cliente_id": session["cliente_id"],
            "itens": [
                {"produto_id": i["produto"]["id"], "nome": i["produto"]["nome"],
                 "preco_unitario": i["produto"]["preco"], "quantidade": i["quantidade"]}
                for i in itens
            ],
            "endereco_entrega": request.form.get("endereco", "").strip(),
            "transportadora_id": transportadora_id,
            "forma_pagamento": request.form.get("forma_pagamento"),
            "status": "Novo",
            "subtotal": subtotal,
            "frete": frete,
            "total": subtotal + frete,
            "data": date.today().isoformat(),
        })
        session["carrinho"] = {}

        cliente_atual_registro = db.encontrar("clientes", session["cliente_id"])
        pontos_ganhos = int(subtotal + frete)
        db.atualizar("clientes", session["cliente_id"], {
            "pontos_fidelidade": (cliente_atual_registro.get("pontos_fidelidade") or 0) + pontos_ganhos,
        })

        flash(f"Pedido realizado com sucesso! Você ganhou {pontos_ganhos} pontos de fidelidade.", "sucesso")
        return redirect(url_for("pedido_confirmacao", id=pedido["id"]))

    cliente = cliente_atual()
    return render_template(
        "checkout.html", itens=itens, subtotal=subtotal,
        transportadoras=transportadoras, cliente=cliente,
    )


@app.route("/pedido/<int:id>/confirmacao")
@login_obrigatorio
def pedido_confirmacao(id):
    pedido = db.encontrar("pedidos", id)
    if pedido is None or pedido["cliente_id"] != session["cliente_id"]:
        abort(404)
    transportadora = db.encontrar("transportadoras", pedido["transportadora_id"])
    return render_template("pedido_confirmacao.html", pedido=pedido, transportadora=transportadora)


# ---------------------------------------------------------------------------
# Conta do cliente (cadastro / login / perfil)
# ---------------------------------------------------------------------------
@app.route("/cliente/cadastro", methods=["GET", "POST"])
def cliente_cadastro():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if any(c["email"].lower() == email for c in db.carregar("clientes")):
            flash("Já existe uma conta com este e-mail.", "erro")
            return render_template("cliente_cadastro.html", dados=request.form)

        senha = request.form.get("senha", "")
        if len(senha) < 6:
            flash("A senha precisa ter pelo menos 6 caracteres.", "erro")
            return render_template("cliente_cadastro.html", dados=request.form)

        novo = db.inserir("clientes", {
            "nome": request.form.get("nome", "").strip(),
            "email": email,
            "senha_hash": generate_password_hash(senha),
            "telefone": request.form.get("telefone", "").strip(),
            "cpf": request.form.get("cpf", "").strip(),
            "endereco": request.form.get("endereco", "").strip(),
            "cidade": request.form.get("cidade", "").strip(),
            "estado": request.form.get("estado", "").strip(),
            "cep": request.form.get("cep", "").strip(),
            "pontos_fidelidade": 0,
            "data_cadastro": date.today().isoformat(),
        })
        session["cliente_id"] = novo["id"]
        flash(f"Bem-vindo(a), {novo['nome'].split()[0]}!", "sucesso")
        return redirect(url_for("cliente_perfil"))

    return render_template("cliente_cadastro.html", dados={})


@app.route("/cliente/login", methods=["GET", "POST"])
def cliente_login():
    proximo = request.args.get("proximo") or request.form.get("proximo") or url_for("cliente_perfil")
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        cliente = next((c for c in db.carregar("clientes") if c["email"].lower() == email), None)
        if cliente and cliente.get("senha_hash") and check_password_hash(cliente["senha_hash"], senha):
            session["cliente_id"] = cliente["id"]
            flash(f"Olá, {cliente['nome'].split()[0]}!", "sucesso")
            return redirect(proximo)
        flash("E-mail ou senha inválidos.", "erro")
    return render_template("cliente_login.html", proximo=proximo)


@app.route("/cliente/logout")
def cliente_logout():
    session.pop("cliente_id", None)
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for("inicio"))


@app.route("/cliente/perfil")
@login_obrigatorio
def cliente_perfil():
    cliente = cliente_atual()
    pedidos = [p for p in db.carregar("pedidos") if p["cliente_id"] == cliente["id"]]
    pets = [p for p in db.carregar("pets") if p.get("cliente_id") == cliente["id"]]
    agendamentos = sorted(
        (a for a in db.carregar("agendamentos") if a.get("cliente_id") == cliente["id"]),
        key=lambda a: (a.get("data") or "", a.get("hora") or ""),
    )
    tickets = [o for o in db.carregar("orcamentos") if o.get("cliente_id") == cliente["id"]]
    nivel, proximo_nivel = nivel_fidelidade(cliente.get("pontos_fidelidade"))
    return render_template(
        "cliente_perfil.html", cliente=cliente, pedidos=pedidos, pets=pets,
        agendamentos=agendamentos, tickets=tickets, nivel=nivel, proximo_nivel=proximo_nivel,
    )


# ---------------------------------------------------------------------------
# Área administrativa genérica: Clientes, Pets, Estoque, Fornecedores,
# Transportadoras, Agendamentos e Orçamentos usam as mesmas duas rotas
# de listagem/formulário, configuradas pelo dicionário ENTIDADES acima.
# ---------------------------------------------------------------------------
def _entidade_ou_404(chave):
    entidade = ENTIDADES.get(chave)
    if entidade is None:
        abort(404)
    return entidade


def _opcoes_select_ref(campo):
    return [(r["id"], r.get(campo["ref_campo_rotulo"], f"#{r['id']}")) for r in db.carregar(campo["ref_tabela"])]


def _rotulo_referencia(tabela, id_, campo_rotulo):
    if id_ in (None, ""):
        return "-"
    registro = db.encontrar(tabela, id_)
    return registro.get(campo_rotulo, f"#{id_}") if registro else f"#{id_} (removido)"


def _valor_para_lista(entidade, registro, coluna):
    """Formata o valor de uma coluna para a tabela de listagem, resolvendo referências."""
    campo = next((c for c in entidade["campos"] if c["nome"] == coluna), None)
    valor = registro.get(coluna)
    if campo and campo["tipo"] == "select_ref":
        return _rotulo_referencia(campo["ref_tabela"], valor, campo["ref_campo_rotulo"])
    if campo and campo["tipo"] == "select_produto":
        produto = PRODUTOS_POR_ID.get(valor)
        return produto["nome"] if produto else f"#{valor}"
    return valor if valor not in (None, "") else "-"


@app.route("/admin")
def admin_painel():
    pendentes_feedback = sum(1 for f in db.carregar("feedbacks") if not f.get("aprovado"))
    return render_template("admin/painel.html", pendentes_feedback=pendentes_feedback)


@app.route("/admin/estoque")
def admin_estoque():
    """Listagem de estoque com alertas de itens baixos/esgotados (rota mais específica que /admin/<entidade>)."""
    entidade = ENTIDADES["estoque"]
    linhas = []
    for r in db.carregar("estoque"):
        produto = PRODUTOS_POR_ID.get(r.get("produto_id"))
        linhas.append({
            "id": r["id"],
            "produto": produto["nome"] if produto else f"#{r.get('produto_id')}",
            "quantidade": r.get("quantidade") or 0,
            "quantidade_minima": r.get("quantidade_minima") or 0,
            "localizacao": r.get("localizacao") or "-",
            "status": status_estoque(r),
        })
    esgotados = sum(1 for l in linhas if l["status"] == "esgotado")
    baixos = sum(1 for l in linhas if l["status"] == "baixo")
    return render_template("admin/estoque_lista.html", entidade=entidade, chave="estoque",
                            linhas=linhas, esgotados=esgotados, baixos=baixos)


@app.route("/admin/feedbacks")
def admin_feedbacks():
    todos = db.carregar("feedbacks")
    pendentes = [f for f in todos if not f.get("aprovado")]
    aprovados = sorted((f for f in todos if f.get("aprovado")), key=lambda f: f["data"], reverse=True)
    return render_template("admin/feedbacks.html", pendentes=pendentes, aprovados=aprovados)


@app.route("/admin/feedbacks/<int:id>/aprovar", methods=["POST"])
def admin_feedback_aprovar(id):
    if db.atualizar("feedbacks", id, {"aprovado": True}) is None:
        abort(404)
    flash("Feedback aprovado e publicado na página.", "sucesso")
    return redirect(url_for("admin_feedbacks"))


@app.route("/admin/feedbacks/<int:id>/excluir", methods=["POST"])
def admin_feedback_excluir(id):
    db.excluir("feedbacks", id)
    flash("Feedback removido.", "sucesso")
    return redirect(url_for("admin_feedbacks"))


@app.route("/admin/<entidade_chave>")
def admin_lista(entidade_chave):
    entidade = _entidade_ou_404(entidade_chave)
    registros = db.carregar(entidade["tabela"])
    linhas = [
        {"id": r["id"], "valores": [_valor_para_lista(entidade, r, c) for c in entidade["colunas_lista"]]}
        for r in registros
    ]
    return render_template("admin/lista.html", entidade=entidade, chave=entidade_chave, linhas=linhas)


def _opcoes_de_campo(campo):
    if campo["tipo"] == "select_ref":
        return _opcoes_select_ref(campo)
    if campo["tipo"] == "select_produto":
        return [(p["id"], p["nome"]) for p in PRODUTOS]
    if campo["tipo"] == "select":
        return campo["opcoes"]
    return None


@app.route("/admin/<entidade_chave>/novo", methods=["GET", "POST"])
def admin_novo(entidade_chave):
    entidade = _entidade_ou_404(entidade_chave)
    if request.method == "POST":
        dados = _ler_formulario(entidade)
        db.inserir(entidade["tabela"], dados)
        flash(f"{entidade['titulo_singular']} cadastrado com sucesso.", "sucesso")
        return redirect(url_for("admin_lista", entidade_chave=entidade_chave))
    campos = [{"config": c, "opcoes": _opcoes_de_campo(c)} for c in entidade["campos"]]
    return render_template("admin/form.html", entidade=entidade, chave=entidade_chave,
                            campos=campos, registro={}, novo=True)


@app.route("/admin/<entidade_chave>/<int:id>/editar", methods=["GET", "POST"])
def admin_editar(entidade_chave, id):
    entidade = _entidade_ou_404(entidade_chave)
    registro = db.encontrar(entidade["tabela"], id)
    if registro is None:
        abort(404)
    if request.method == "POST":
        dados = _ler_formulario(entidade)
        db.atualizar(entidade["tabela"], id, dados)
        flash(f"{entidade['titulo_singular']} atualizado com sucesso.", "sucesso")
        return redirect(url_for("admin_lista", entidade_chave=entidade_chave))
    campos = [{"config": c, "opcoes": _opcoes_de_campo(c)} for c in entidade["campos"]]
    return render_template("admin/form.html", entidade=entidade, chave=entidade_chave,
                            campos=campos, registro=registro, novo=False)


@app.route("/admin/<entidade_chave>/<int:id>/excluir", methods=["POST"])
def admin_excluir(entidade_chave, id):
    entidade = _entidade_ou_404(entidade_chave)
    db.excluir(entidade["tabela"], id)
    flash(f"{entidade['titulo_singular']} excluído.", "sucesso")
    return redirect(url_for("admin_lista", entidade_chave=entidade_chave))


def _ler_formulario(entidade):
    dados = {}
    for campo in entidade["campos"]:
        valor = request.form.get(campo["nome"], "").strip()
        if campo["tipo"] in ("select_ref", "select_produto") and valor:
            valor = int(valor)
        elif campo["tipo"] == "number" and valor != "":
            valor = float(valor) if "." in valor else int(valor)
        dados[campo["nome"]] = valor if valor != "" else None
    return dados


@app.errorhandler(404)
def nao_encontrado(_erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
