# 🐾 PetHouse

> **Trabalho acadêmico** · Disciplina: *Nome da disciplina* · Curso: *Nome do curso* · Instituição: *Nome da instituição*
> **Professor(a):** *Nome do(a) professor(a)* · **Turma:** *Turma / semestre* · **Data de entrega:** *dd/mm/aaaa*
> **Grupo:** *Integrante 1, Integrante 2, Integrante 3, Integrante 4* (quem fez o quê: página **Contato** do site)
> *(Preencham os campos acima e os dados em `TRABALHO` e `EQUIPE` no `app.py`.)*


Projeto entregue ao professor: uma loja online de produtos pet (estilo *drop shipping*) com área do cliente, perfil dos pets,
agendamento de serviços, programa de fidelidade, tickets de atendimento/orçamento, vitrine de
fornecedores e painel administrativo. Feita em **Python + Flask**, com armazenamento
temporário em arquivos `.json`.

> 📚 Documentação completa do site: [`DOCUMENTACAO.md`](DOCUMENTACAO.md)
> 💰 Relatório de hospedagem e domínio (pesquisa do grupo): [`ORCAMENTO_HOSPEDAGEM_DOMINIO.md`](ORCAMENTO_HOSPEDAGEM_DOMINIO.md)

---

## Como rodar no seu computador

Requisitos: Python 3.10 ou superior.

```bash
# 1) entre na pasta do projeto
cd pethouse

# 2) (opcional, recomendado) crie um ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

# 3) instale as dependências
pip install -r requirements.txt

# 4) inicie o site
python app.py
```

Abra **http://127.0.0.1:5000** no navegador: a primeira tela é a **apresentação do trabalho**, com os botões **Acessar Site** (loja, em `/inicio`) e **Documentação** (`/documentacao`).
O painel administrativo fica em **http://127.0.0.1:5000/admin**.

---

## Estrutura resumida

```
pethouse/
├── app.py                 rotas, configurações da loja, produtos e nomes das mídias
├── data_store.py          "banco de dados" em arquivos .json
├── requirements.txt
├── data/                  tabelas .json (clientes, pets, pedidos, estoque...)
├── templates/             páginas HTML (Jinja2) — sem CSS nem JS dentro
├── static/
│   ├── css/style.css      TODO o CSS, dividido por página  ([S00] a [S26])
│   ├── js/scripts.js      TODO o JavaScript, dividido por página ([J01] a [J07])
│   └── assets/            fotos e vídeos do site
│       ├── imagens/{site,produtos,fornecedores,pets}/
│       └── videos/{site,produtos}/
└── docs/                  esta documentação
```

---

## Como editar

| Quero mudar…                     | Onde                                                       |
|----------------------------------|------------------------------------------------------------|
| Cores do site inteiro            | `static/css/style.css` → seção **[S00]** (variáveis)       |
| O visual de uma página           | `static/css/style.css` → procure o nome da página (ex.: `produto.html`) |
| O comportamento (JS) de uma página | `static/js/scripts.js` → procure o nome da página        |
| Nome, e-mail, WhatsApp, frete    | `app.py` → dicionário `LOJA`                               |
| Disciplina, professor, turma     | `app.py` → dicionário `TRABALHO`                           |
| Integrantes do grupo (Contato)   | `app.py` → lista `EQUIPE` (fotos em `static/assets/imagens/equipe/`) |
| Produtos, preços e descrições    | `app.py` → lista `PRODUTOS`                                |
| Fotos e vídeos dos produtos      | coloque nas pastas de `static/assets/` e ajuste `MIDIA_PRODUTOS` no `app.py` |
| Fornecedores, estoque, clientes  | Painel admin: `/admin`                                     |

## Como adicionar fotos e vídeos

1. Coloque o arquivo na pasta certa (cada pasta tem um `LEIA-ME.txt` com os nomes esperados).
2. Se o nome do arquivo for diferente do padrão, ajuste o nome em `app.py`
   (`MIDIA_SITE` e `MIDIA_PRODUTOS`).
3. Recarregue a página. Enquanto o arquivo não existir, o site mostra emojis/oculta o vídeo
   sem quebrar nada.

Resumo dos padrões de nome:

| Mídia                | Pasta                                   | Nome padrão                    |
|----------------------|-----------------------------------------|--------------------------------|
| Foto de produto      | `static/assets/imagens/produtos/`       | `produto-01.jpg` … `produto-12.jpg` |
| Vídeo de produto     | `static/assets/videos/produtos/`        | `produto-01.mp4` … `produto-12.mp4` |
| Logo / favicon / banner | `static/assets/imagens/site/`        | `logo.png`, `favicon.png`, `banner-inicio.jpg` |
| Vídeo da home        | `static/assets/videos/site/`            | `video-institucional.mp4`      |
| Foto de fornecedor   | `static/assets/imagens/fornecedores/`   | `fornecedor-<id>.jpg`          |
| Foto de pet          | `static/assets/imagens/pets/`           | `pet-<id>.jpg`                 |
| Foto de integrante   | `static/assets/imagens/equipe/`         | `integrante-1.jpg` (nome definido em `EQUIPE`) |

---

## Status do projeto

**Telas funcionando (revisar):** Início · Produtos · Perfil de cliente · Agendamento de
serviços · Orçamento personalizado · Feedback · Carrinho · Fornecedores.

**A fazer:**
- [ ] Blog (dicas, informações sobre pets e novidades)
- [ ] Foto própria do pet no perfil (a estrutura já está pronta: basta enviar `pet-<id>.jpg`)
- [ ] Trocar os arquivos `.json` por um banco de dados de verdade
- [ ] Banco/CDN de imagens para não guardar tudo localmente
- [ ] Criar repositório no GitHub
- [ ] **Proteger o painel `/admin` com login** (hoje qualquer pessoa com o link acessa)

Lista completa de pontos de atenção antes de publicar: seção 12 da
[`DOCUMENTACAO.md`](DOCUMENTACAO.md).
