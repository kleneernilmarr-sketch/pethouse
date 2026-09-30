# Documentação do site — PetHouse

> **Trabalho acadêmico** · Disciplina: *Nome da disciplina* · Curso: *Nome do curso* · Instituição: *Nome da instituição*
> **Professor(a):** *Nome do(a) professor(a)* · **Turma:** *Turma / semestre* · **Data de entrega:** *dd/mm/aaaa*
> **Grupo:** *Integrante 1, Integrante 2, Integrante 3, Integrante 4* (quem fez o quê: página **Contato** do site)
> *(Preencham os campos acima e os dados em `TRABALHO` e `EQUIPE` no `app.py`.)*

Este documento, escrito pelo grupo para o professor, descreve **como o site funciona e onde mexer em cada coisa**.
Para instalar e rodar, veja o [`README.md`](README.md).

## Índice

1. [Visão geral](#1-visão-geral)
2. [Estrutura de pastas](#2-estrutura-de-pastas)
3. [Configurações centrais (`app.py`)](#3-configurações-centrais-apppy)
4. [Mapa das páginas](#4-mapa-das-páginas)
5. [Fluxos principais](#5-fluxos-principais)
6. [Painel administrativo](#6-painel-administrativo)
7. [Dados (arquivos JSON)](#7-dados-arquivos-json)
8. [CSS: como está organizado](#8-css-como-está-organizado)
9. [JavaScript: como está organizado](#9-javascript-como-está-organizado)
10. [Fotos e vídeos (`static/assets`)](#10-fotos-e-vídeos-staticassets)
11. [Como fazer as tarefas mais comuns](#11-como-fazer-as-tarefas-mais-comuns)
12. [Pontos de atenção e pendências](#12-pontos-de-atenção-e-pendências)
13. [Histórico de mudanças](#13-histórico-de-mudanças)

---

## 1. Visão geral

| Item                | Detalhe                                                       |
|---------------------|---------------------------------------------------------------|
| Linguagem           | Python 3.10+                                                  |
| Framework           | Flask 3 (templates Jinja2)                                    |
| Armazenamento       | Arquivos `.json` em `data/` (camada `data_store.py`)          |
| Sessão              | Cookie assinado do Flask (login do cliente e carrinho)        |
| Front-end           | HTML + 1 CSS + 1 JS, sem frameworks                           |
| Senhas              | Guardadas com hash (`werkzeug.security`)                      |

A loja funciona no modelo *drop shipping*: os produtos vêm de fornecedores parceiros e a
página **Fornecedores** mostra ao cliente de onde vem cada linha de produtos.

---

## 2. Estrutura de pastas

```
pethouse/
├── app.py                        rotas + configurações + produtos + nomes das mídias + TRABALHO e EQUIPE
├── data_store.py                 leitura/gravação dos .json (trocar aqui quando houver banco)
├── requirements.txt              Flask e Werkzeug
├── PetHouse_Documentação.txt   anotações originais (conteúdo incorporado nesta doc)
│
├── data/                         "tabelas"
│   ├── clientes.json   pets.json   pedidos.json   agendamentos.json
│   ├── orcamentos.json feedbacks.json   estoque.json
│   └── fornecedores.json   transportadoras.json
│
├── templates/                    páginas (nenhuma tem CSS ou JS dentro)
│   ├── base.html                 layout: cabeçalho, mensagens, rodapé, <link> do CSS, <script> do JS
│   ├── _card.html                componente do card de produto (macro)
│   ├── index.html                apresentação do trabalho (abre em "/")
│   ├── documentacao.html         resumo da estrutura e do comparativo de hospedagem
│   ├── base_trabalho.html        layout simples das duas páginas acima
│   ├── inicio.html  produtos.html  produto.html  carrinho.html  checkout.html
│   ├── pedido_confirmacao.html  contato.html  fornecedores.html  feedback.html
│   ├── cliente_cadastro.html  cliente_login.html  cliente_perfil.html
│   ├── cliente_pet_novo.html  pet_perfil.html
│   ├── agendamento_novo.html  orcamento_solicitar.html  404.html
│   └── admin/  painel.html  lista.html  form.html  estoque_lista.html  feedbacks.html
│
├── static/
│   ├── css/style.css             ÚNICO arquivo de CSS
│   ├── js/scripts.js             ÚNICO arquivo de JavaScript
│   └── assets/
│       ├── imagens/  site/  produtos/  fornecedores/  pets/  equipe/
│       └── videos/   site/  produtos/
│
└── docs/                         README, esta documentação e o orçamento de hospedagem
```

---

## 3. Configurações centrais (`app.py`)

Tudo o que se edita com frequência está no começo do `app.py`:

| Bloco               | O que controla                                                              |
|---------------------|-----------------------------------------------------------------------------|
| `TRABALHO`          | Instituição, curso, disciplina, professor e turma (apresentação e rodapé) |
| `EQUIPE`            | Integrantes do grupo na página Contato: nome, área, LinkedIn, telefone e foto |
| `LOJA`              | Nome, slogan, e-mail, WhatsApp, endereço, frete grátis acima de R$ X, prazo, nº de parcelas |
| `NIVEIS_FIDELIDADE` | Níveis do programa de fidelidade (Bronze 0 pts, Prata 200, Ouro 500) e benefícios |
| `CATEGORIAS`        | Categorias (slug da URL, nome, emoji, cor do card)                          |
| `PASTA_IMAGENS` / `PASTA_VIDEOS` | Pastas das mídias, relativas a `static/`                        |
| `MIDIA_SITE`        | Nomes de logo, favicon, banner da home, vídeo da home e capa do vídeo       |
| `MIDIA_PRODUTOS`    | Nome da foto e do vídeo de cada produto (por id)                            |
| `PRODUTOS`          | Lista de produtos: nome, categoria, preço, preço antigo, destaque, descrição |
| `ENTIDADES`         | Campos de cada tela do painel admin (clientes, pets, estoque, fornecedores...) |

Funções auxiliares expostas aos templates:

- `imagem_url('pasta', 'arquivo.jpg')` → URL da imagem, ou vazio se o arquivo não existir.
- `video_url('pasta', 'arquivo.mp4')` → URL do vídeo, ou vazio se o arquivo não existir.
- filtro `brl` → formata número como `R$ 1.234,56`.

Variáveis disponíveis em **todos** os templates: `loja`, `categorias`, `ano`, `contagem`,
`cliente_logado`, `carrinho_qtd`, `entidades_admin` e `midia` (URLs de logo, favicon, banner e
vídeo da home).

---

## 4. Mapa das páginas

A coluna **CSS** e **JS** indicam a seção do arquivo (`Ctrl+F` pelo código).

| Página (template)            | Rota(s)                                   | Login? | CSS   | JS    |
|------------------------------|-------------------------------------------|:------:|-------|-------|
| `base.html` (todas)          | —                                         | —      | [S02] | [J02] |
| `index.html`                 | `/`                                       | não    | [S25] | —     |
| `documentacao.html`          | `/documentacao`                           | não    | [S26] | —     |
| `inicio.html`                | `/inicio`                                 | não    | [S03] | —     |
| `produtos.html`              | `/produtos`, `/ofertas`, `/categoria/<slug>`, `/busca?q=` | não | [S04] | — |
| `produto.html`               | `/produto/<id>`                           | não    | [S05] | —     |
| `carrinho.html`              | `/carrinho` (+ adicionar/atualizar/remover) | não  | [S06] | [J03] |
| `checkout.html`              | `/checkout`                               | **sim**| [S07] | —     |
| `pedido_confirmacao.html`    | `/pedido/<id>/confirmacao`                | **sim**| [S08] | —     |
| `cliente_cadastro.html`      | `/cliente/cadastro`                       | não    | [S09] | —     |
| `cliente_login.html`         | `/cliente/login`, `/cliente/logout`       | não    | [S10] | —     |
| `cliente_perfil.html`        | `/cliente/perfil`                         | **sim**| [S11] | —     |
| `cliente_pet_novo.html`      | `/cliente/pets/novo`                      | **sim**| [S12] | —     |
| `pet_perfil.html`            | `/pet/<id>`                               | não    | [S13] | —     |
| `agendamento_novo.html`      | `/agendamentos/novo`                      | **sim**| [S14] | —     |
| `orcamento_solicitar.html`   | `/orcamentos/solicitar`                   | não    | [S15] | —     |
| `feedback.html`              | `/feedback`                               | não    | [S16] | —     |
| `fornecedores.html`          | `/fornecedores`                           | não    | [S17] | —     |
| `contato.html`               | `/contato` (contatos da loja + equipe)    | não    | [S18] | —     |
| `404.html`                   | qualquer rota inexistente                 | —      | [S19] | —     |
| `admin/painel.html`          | `/admin`                                  | ⚠️ não | [S20] | —     |
| `admin/lista.html`           | `/admin/<entidade>`                       | ⚠️ não | [S21] | [J04] |
| `admin/form.html`            | `/admin/<entidade>/novo` e `/<id>/editar` | ⚠️ não | [S22] | —     |
| `admin/estoque_lista.html`   | `/admin/estoque`                          | ⚠️ não | [S23] | [J05] |
| `admin/feedbacks.html`       | `/admin/feedbacks`                        | ⚠️ não | [S24] | [J06] |

⚠️ O painel administrativo **ainda não exige senha** (ver seção 12).

---

## 5. Fluxos principais

### 5.1 Compra
1. O cliente navega em **Produtos / Categorias / Ofertas / Busca** e clica em *Adicionar ao carrinho*.
2. O carrinho fica na **sessão** (`session["carrinho"]` = `{id_do_produto: quantidade}`).
3. Em **Carrinho**, alterar a quantidade envia o formulário sozinho (JS [J03]); quantidade `0` remove o item.
4. **Finalizar compra** exige login. No checkout o cliente confirma endereço, escolhe a
   **transportadora** e a **forma de pagamento** (cartão, Pix ou boleto).
5. O pedido é gravado em `data/pedidos.json` com status `Novo`, o carrinho é esvaziado e o cliente
   recebe pontos de fidelidade (1 ponto por R$ 1 do total).
6. A página de **confirmação** mostra o resumo; o histórico fica em *Minha conta*.

**Frete:** no carrinho é estimado em R$ 19,90 (grátis a partir do valor definido em `LOJA`);
no checkout vale o `valor_frete_base` da transportadora escolhida (grátis acima do mesmo valor).

### 5.2 Conta do cliente e pets
- **Cadastro** cria o cliente (senha com hash) e já faz login.
- **Minha conta** reúne: cartão de fidelidade com barra de progresso, pedidos, pets, agendamentos e tickets.
- **Cadastrar pet** vincula o pet ao cliente logado; o **perfil do pet** mostra dados e histórico de serviços.
  Se existir a foto `static/assets/imagens/pets/pet-<id>.jpg`, ela aparece no lugar do emoji.

### 5.3 Agendamento de serviços
O cliente escolhe pet, tipo (banho, tosa, consulta, entrega, outro), data, hora e observações.
O agendamento nasce com status `Agendado`; a equipe muda o status pelo painel admin.

### 5.4 Orçamento / ticket de atendimento
Qualquer visitante (logado ou não) abre um ticket. A equipe responde pelo painel admin
(campo **Resposta da loja**) e o cliente logado vê a resposta em *Minha conta*.

### 5.5 Feedback (avaliações)
O cliente envia nota (1 a 5) e mensagem. O feedback só aparece no site depois de **aprovado**
em `/admin/feedbacks` (moderação). A média de estrelas é calculada sobre os feedbacks publicados.

### 5.6 Fidelidade
Níveis definidos em `NIVEIS_FIDELIDADE`. Os pontos são somados a cada pedido e podem ser
ajustados manualmente em `/admin/clientes` (ex.: bônus de campanha).

---

## 6. Painel administrativo

Acesse `/admin`. Cada card abre uma lista com **Novo / Editar / Excluir** (a exclusão pede
confirmação — JS [J04]–[J06]).

| Área             | Tabela (`data/`)   | Observações                                              |
|------------------|--------------------|----------------------------------------------------------|
| Clientes         | `clientes.json`    | inclui ajuste manual de pontos                           |
| Pets             | `pets.json`        | campo **Foto** (nome do arquivo em `assets/imagens/pets/`) |
| Estoque          | `estoque.json`     | tela própria com alertas de **esgotado** e **estoque baixo** |
| Fornecedores     | `fornecedores.json`| texto de qualidade aparece em `/fornecedores`; campo **Foto / logo** |
| Transportadoras  | `transportadoras.json` | aparecem no checkout                                 |
| Agendamentos     | `agendamentos.json`|                                                          |
| Orçamentos (tickets) | `orcamentos.json` | resposta visível ao cliente                           |
| Feedbacks        | `feedbacks.json`   | tela própria de moderação (aprovar / excluir)            |

Para criar uma nova área no admin basta adicionar um bloco em `ENTIDADES` (`app.py`): as rotas e
templates genéricos (`lista.html`, `form.html`) já cuidam do resto.

---

## 7. Dados (arquivos JSON)

Cada arquivo é uma lista de objetos com `id` inteiro sequencial.

| Arquivo              | Campos principais                                                                 |
|----------------------|-----------------------------------------------------------------------------------|
| `clientes.json`      | id, nome, email, senha_hash, telefone, cpf, endereco, cidade, estado, cep, pontos_fidelidade, data_cadastro |
| `pets.json`          | id, cliente_id, nome, especie, raca, porte, data_nascimento, observacoes, foto (opcional) |
| `pedidos.json`       | id, cliente_id, itens[{produto_id, nome, preco_unitario, quantidade}], endereco_entrega, transportadora_id, forma_pagamento, status, subtotal, frete, total, data |
| `agendamentos.json`  | id, cliente_id, pet_id, tipo, data, hora, status, observacoes                     |
| `orcamentos.json`    | id, cliente_id, nome, contato, assunto, mensagem, status, resposta, data_criacao  |
| `feedbacks.json`     | id, cliente_id, nome, nota, mensagem, data, aprovado                              |
| `estoque.json`       | id, produto_id, quantidade, quantidade_minima, localizacao, ultima_atualizacao    |
| `fornecedores.json`  | id, nome, cnpj, contato, telefone, email, imagem, anos_mercado, produtos_fornecidos, descricao_qualidade, certificacoes, prazo_entrega_dias |
| `transportadoras.json` | id, nome, cnpj, telefone, email, regioes_atendidas, prazo_medio_dias, valor_frete_base |

> Os **produtos** e **categorias** não estão em JSON: ficam no `app.py` (listas `PRODUTOS` e `CATEGORIAS`).

**Migração futura para banco de dados:** todo o acesso a dados passa por `data_store.py`
(`carregar`, `salvar`, `inserir`, `atualizar`, `excluir`, `encontrar`). Ao criar o banco, basta
reimplementar essas funções — o restante do `app.py` não muda.

---

## 8. CSS: como está organizado

Arquivo único: **`static/css/style.css`**. Nenhum HTML tem `<style>` ou `style="..."`, com duas
exceções intencionais, porque o valor vem do Python e muda a cada item:

- `style="--cor: ..."` nos cards de produto/categoria (cor da categoria);
- `style="width: X%"` na barra de progresso da fidelidade.

**Índice do arquivo** (procure com `Ctrl+F` pelo código):

| Código | Conteúdo                                                        |
|--------|-----------------------------------------------------------------|
| [S00]  | Variáveis (cores, raios, sombra) e reset                        |
| [S01]  | **Componentes compartilhados** (botões, formulários, tabelas, card de produto, linhas de carrinho, tags...) — cada bloco diz "Usado em: …" |
| [S02]  | `base.html` — cabeçalho, mensagens, rodapé                      |
| [S03]  | `inicio.html`                                                   |
| [S04]  | `produtos.html` (usa só componentes de [S01])                   |
| [S05]  | `produto.html`                                                  |
| [S06]  | `carrinho.html`                                                 |
| [S07]  | `checkout.html`                                                 |
| [S08]  | `pedido_confirmacao.html`                                       |
| [S09]–[S10] | `cliente_cadastro.html`, `cliente_login.html` (só componentes de [S01]) |
| [S11]  | `cliente_perfil.html`                                           |
| [S12]  | `cliente_pet_novo.html` (só componentes de [S01])               |
| [S13]  | `pet_perfil.html`                                               |
| [S14]  | `agendamento_novo.html`                                         |
| [S15]  | `orcamento_solicitar.html`                                      |
| [S16]  | `feedback.html`                                                 |
| [S17]  | `fornecedores.html` (antes ficava em `<style>` dentro do HTML)  |
| [S18]  | `contato.html`                                                  |
| [S19]  | `404.html`                                                      |
| [S20]–[S24] | páginas do admin                                           |
| [S25]  | `base_trabalho.html` e `index.html` (apresentação)              |
| [S26]  | `documentacao.html`                                             |

**Regras para manter organizado**
1. Estilo que só existe em uma página → seção dessa página, com classes que começam pelo nome da página (`.produto-…`, `.perfil-…`).
2. Estilo usado em duas ou mais páginas → **[S01]**, com o comentário "Usado em:".
3. As seções de página vêm depois de [S01]; se duas regras tiverem o mesmo peso, a da página ganha.
4. As regras responsivas (`@media`) ficam dentro da seção da própria página.

---

## 9. JavaScript: como está organizado

Arquivo único: **`static/js/scripts.js`**, carregado no fim do `base.html` (`defer`).

Cada template declara seu nome no topo: `{% block pagina %}carrinho{% endblock %}`. O `base.html`
coloca esse nome em `<body data-pagina="carrinho">` e o `scripts.js` executa **somente** o código
da página aberta.

| Código | Página / uso                | O que faz                                                |
|--------|-----------------------------|----------------------------------------------------------|
| [J01]  | Utilitários compartilhados  | `ativarConfirmacaoDeFormularios()` (formulários com `data-confirmar`) |
| [J02]  | `base.html` (todas)         | gancho reservado para código global                      |
| [J03]  | `carrinho.html`             | envia o formulário ao mudar a quantidade (`data-auto-submit`) |
| [J04]  | `admin/lista.html`          | confirmação antes de excluir                             |
| [J05]  | `admin/estoque_lista.html`  | confirmação antes de excluir                             |
| [J06]  | `admin/feedbacks.html`      | confirmação antes de excluir                             |
| [J07]  | Mapa de páginas             | liga cada `data-pagina` à sua função                     |

Não há JavaScript nas demais páginas.

**Para criar o JS de uma página nova:** (1) defina `{% block pagina %}nome{% endblock %}` no template;
(2) escreva a função numa nova seção `[Jxx]`; (3) registre-a no mapa `PAGINAS` de [J07].

---

## 10. Fotos e vídeos (`static/assets`)

```
static/assets/
├── imagens/
│   ├── site/           logo.png · favicon.png · banner-inicio.jpg · video-institucional-capa.jpg
│   ├── produtos/       produto-01.jpg … produto-12.jpg
│   ├── fornecedores/   fornecedor-<id>.jpg
│   └── pets/           pet-<id>.jpg
└── videos/
    ├── site/           video-institucional.mp4
    └── produtos/       produto-01.mp4 … produto-12.mp4
```

Cada pasta tem um `LEIA-ME.txt` com os nomes esperados. Onde cada mídia aparece:

| Mídia                | Onde aparece                                                     |
|----------------------|------------------------------------------------------------------|
| Logo                 | Cabeçalho (substitui o texto "PetHouse")                        |
| Favicon              | Aba do navegador                                                 |
| Banner da home       | Coluna direita da abertura da página inicial                     |
| Vídeo da home        | Seção logo abaixo da abertura (só aparece se o arquivo existir)  |
| Foto de produto      | Cards de produto e página do produto                             |
| Vídeo de produto     | Página do produto, abaixo da foto (a foto vira a capa do vídeo)  |
| Foto de fornecedor   | Card em `/fornecedores`                                          |
| Foto de pet          | Perfil do pet                                                    |
| Foto de integrante   | Página Contato, seção Equipe do projeto                          |

**Comportamento seguro:** se o arquivo não existir, nada quebra — o site mostra o emoji da
categoria (produtos/pets), o texto "Foto de …" (fornecedores) ou simplesmente oculta o vídeo/banner.

**Recomendações técnicas**
- Fotos: JPG/WEBP, ~800×800 px para produtos, até ~300 KB.
- Vídeos: `.mp4` (H.264 + AAC), 720p, de preferência até 15 MB cada.
- O formato de vídeo esperado é `.mp4`. Para usar outro formato seria preciso ajustar o `type` da tag `<source>` nos templates `inicio.html` e `produto.html`.

---

## 11. Como fazer as tarefas mais comuns

**Trocar o nome, WhatsApp ou e-mail da loja** → `LOJA` em `app.py`.

**Preencher os dados do trabalho** (disciplina, professor, turma) → `TRABALHO` em `app.py`.

**Adicionar ou remover um integrante do grupo** → copie ou apague um bloco na lista `EQUIPE` em `app.py` e coloque a foto em `static/assets/imagens/equipe/` (sem foto, o site mostra as iniciais).

**Cadastrar um produto novo**
1. Acrescente um item em `PRODUTOS` (`app.py`) com um `id` novo.
2. Acrescente a linha correspondente em `MIDIA_PRODUTOS` com o nome da foto e do vídeo.
3. Coloque os arquivos em `static/assets/imagens/produtos/` e `static/assets/videos/produtos/`.

**Adicionar a foto de um fornecedor** → envie `fornecedor-<id>.jpg` para
`static/assets/imagens/fornecedores/` (ou digite outro nome no campo *Foto / logo* em
`/admin/fornecedores`).

**Mudar a cor principal** → `--sol` e `--sol-escuro` em [S00] do CSS.

**Trocar o texto de uma página** → o template correspondente em `templates/`.

**Adicionar uma categoria** → novo item em `CATEGORIAS` (`app.py`).

---

## 12. Pontos de atenção e pendências

### Pendências do projeto (anotações originais)
- Blog com informações de pet, dicas e novidades.
- Foto própria do pet no perfil (estrutura pronta; falta o upload pelo cliente).
- Substituir o armazenamento em JSON por banco de dados.
- Banco/CDN de imagens (hoje as mídias ficam locais).
- Criar repositório no GitHub.

### Segurança — resolver ANTES de publicar
1. **`/admin` sem login.** Qualquer pessoa que descobrir o endereço pode ler, editar e excluir dados (inclui clientes). Criar login de administrador é o item mais urgente.
2. **`app.secret_key` fixa no código.** Trocar por uma chave secreta longa vinda de variável de ambiente.
3. **`debug=True`** no `app.run`. Em produção, desligar e usar um servidor de produção (ex.: `gunicorn`).
4. **Formulários sem proteção CSRF.** Recomenda-se `Flask-WTF`/`CSRFProtect`.
5. **Dados pessoais (LGPD).** Há CPF, endereço e telefone em `clientes.json`; ao migrar para banco, definir política de privacidade, backup e acesso restrito.

### Regras de negócio para revisar
- Os níveis Prata/Ouro **listam** benefícios (descontos, frete grátis), mas o código ainda **não aplica** esses descontos no carrinho/checkout.
- Os pontos são creditados **na criação do pedido**, e não quando ele é *concluído* (o texto do sistema fala em pedidos concluídos).
- Frete do carrinho (R$ 19,90 fixo) e frete do checkout (valor da transportadora) podem divergir.
- O estoque **não** é baixado automaticamente quando um pedido é feito.
- Pagamento é apenas uma escolha no formulário; não há integração com gateway (Pix, cartão, boleto).
- O carrinho é guardado na sessão: some se o cliente limpar os cookies.

### Desempenho
- Vídeos servidos direto pelo Flask consomem banda e CPU do servidor. Comprimir os vídeos e, com tráfego maior, usar CDN (ex.: Cloudflare) ou hospedagem de vídeo dedicada.
- `data_store.py` regrava o arquivo inteiro a cada alteração; adequado para poucos registros, não para muitos acessos simultâneos.

---

## 13. Histórico de mudanças

### Apresentação do trabalho, equipe e renomeação para PetHouse
- **Nome:** o projeto passou de *Rabo Feliz* para **PetHouse** (site, e-mail `contato@pethouse.com.br`, documentos e nome da pasta).
- **Apresentação:** nova página inicial `index.html` em `/`, com resumo das funcionalidades e os botões **Acessar Site** e **Documentação**. A home da loja passou de `/` para `/inicio`.
- **Documentação no site:** nova página `/documentacao` com a estrutura do projeto e o comparativo de hospedagem.
- **Contato:** nova seção *Equipe do projeto*, alimentada pela lista `EQUIPE` do `app.py`.
- **Documentos em `docs/`:** reescritos como entrega do grupo ao professor.

### Reorganização de CSS, JS, mídias e documentação
- **CSS:** `static/style.css` → `static/css/style.css`. Todo CSS que estava em atributos `style=""` e no `<style>` de `fornecedores.html` foi movido para o arquivo único, dividido em seções por página ([S00]–[S24]).
- **JS:** os `onchange`/`onsubmit` embutidos nos HTMLs viraram atributos (`data-auto-submit`, `data-confirmar`) tratados em `static/js/scripts.js`, dividido por página ([J01]–[J07]).
- **Templates:** novo bloco `{% block pagina %}` em cada página e `<body data-pagina="…">` no `base.html`.
- **Mídias:** criada a estrutura `static/assets/` (imagens e vídeos), com tabelas de nomes em `app.py` (`MIDIA_SITE`, `MIDIA_PRODUTOS`) e funções `imagem_url()` / `video_url()`. Novos pontos de mídia: logo, favicon, banner e vídeo da home, vídeo do produto, foto de fornecedor e de pet. Campos de foto adicionados ao admin de Fornecedores e Pets.
- **Pequena melhoria de layout:** o carrinho passa a usar uma coluna no celular.
- **Limpeza:** removidas as pastas vazias `{data,templates` e `__pycache__` que estavam no projeto.
- **Documentação:** criada a pasta `docs/`.
