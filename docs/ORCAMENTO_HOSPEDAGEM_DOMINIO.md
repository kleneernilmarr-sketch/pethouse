# Relatório de hospedagem e domínio — PetHouse

> **Trabalho acadêmico** · Disciplina: *Nome da disciplina* · Curso: *Nome do curso* · Instituição: *Nome da instituição*
> **Professor(a):** *Nome do(a) professor(a)* · **Turma:** *Turma / semestre* · **Data de entrega:** *dd/mm/aaaa*
> **Grupo:** *Integrante 1, Integrante 2, Integrante 3, Integrante 4* (quem fez o quê: página **Contato** do site)
> *(Preencham os campos acima e os dados em `TRABALHO` e `EQUIPE` no `app.py`.)*

**Objetivo deste relatório:** apresentar ao professor a pesquisa que nosso grupo fez de custos para colocar o projeto PetHouse na internet e justificar a opção que escolhemos.

**Data da pesquisa (feita pelo grupo):** 29/09/2026
**Premissas de conversão:** US$ 1,00 = R$ 5,50 (cotação de referência usada pelo Registro.br para suas tarifas em 2026; ajuste conforme o câmbio do dia). Valores em dólar **não incluem IOF** de cartão internacional nem impostos.

> ⚠️ Preços de hospedagem e domínio mudam com frequência e muitas ofertas têm valor promocional no
> primeiro período. Confirme os valores nas páginas oficiais antes de contratar (links na seção 9).

---

## 1. O que o projeto precisa

O nosso projeto, o PetHouse, é uma aplicação **Python/Flask** (não é um site estático nem PHP). Isso muda a escolha, e foi o critério que usamos na pesquisa:

| Requisito                                  | Por quê                                                                 |
|--------------------------------------------|-------------------------------------------------------------------------|
| Hospedagem que **execute Python/Flask**    | Hospedagens compartilhadas comuns (PHP/WordPress) não servem            |
| **Disco persistente**                      | Os dados ficam em arquivos `.json`; se o disco for apagado a cada reinício, clientes e pedidos somem |
| **SSL (HTTPS)**                            | Há login, cadastro e dados pessoais (CPF, endereço)                     |
| **Domínio próprio**                        | O e-mail da loja no projeto já está configurado como `contato@pethouse.com.br`    |
| Espaço e banda para **fotos e vídeos**     | Cada produto terá foto e vídeo (~15 MB cada)                            |
| Caminho para **banco de dados**            | O projeto prevê trocar o JSON por banco de dados                        |

---

## 2. Hospedagem — três opções

### Opção A — PythonAnywhere (gratuita e paga)

Plataforma especializada em Python, com painel no navegador (não exige conhecer servidores).

| Item               | Plano gratuito (Beginner)                          | Plano pago **Developer**                                   |
|--------------------|----------------------------------------------------|------------------------------------------------------------|
| Preço              | US$ 0                                              | **US$ 10/mês** (≈ R$ 55,00)                                |
| Espaço em disco    | 512 MB                                             | 5 GB                                                       |
| Largura de banda   | Sem franquia divulgada (limitada por CPU)          | Sem franquia divulgada (limitada por CPU/*workers* do plano) |
| Domínio próprio    | ❌ Só `usuario.pythonanywhere.com`                 | ✅ 1 aplicação web em domínio próprio                       |
| SSL                | ✅ HTTPS no subdomínio da plataforma               | ✅ HTTPS gratuito                                           |
| Suporte            | Comunidade/fórum (desde jan/2026)                  | Suporte direto por e-mail                                  |
| Extras             | Aplicativos sem uso expiram em 1 mês               | 3 *web workers*, 20 tarefas agendadas, MySQL, 5.000 s de CPU |
| Disco persistente  | ✅ (JSON não é perdido)                            | ✅                                                          |

**Pontos fortes:** simples de configurar, disco persistente, MySQL disponível no plano pago (combina com a futura troca do JSON), ótimo para aprender e validar.
**Pontos fracos:** plano gratuito não aceita domínio próprio; o plano base subiu de US$ 5 para US$ 10 em 2026; menos flexível para escalar (o degrau seguinte é bem mais caro).

### Opção B — Render (gratuita e paga)

Plataforma em nuvem com deploy automático a partir do GitHub (o projeto já prevê um repositório).

| Item               | Plano gratuito (Free)                                       | Plano pago **Starter** + disco                              |
|--------------------|-------------------------------------------------------------|-------------------------------------------------------------|
| Preço              | US$ 0                                                       | **US$ 7/mês** (≈ R$ 38,50) + disco persistente US$ 0,25/GB/mês |
| Recursos           | 512 MB RAM, 0,1 CPU                                         | 512 MB RAM, 0,5 CPU, sempre ligado                          |
| Espaço em disco    | ⚠️ Efêmero (apagado a cada reinício/deploy)                 | Disco persistente opcional (1 GB ≈ US$ 0,25/mês ≈ R$ 1,38)  |
| Largura de banda   | Franquia mensal incluída no *workspace*; excedente US$ 0,15/GB | Idem                                                     |
| Domínio próprio    | ✅                                                          | ✅                                                          |
| SSL                | ✅ TLS gerenciado gratuito                                  | ✅ TLS gerenciado gratuito                                  |
| Suporte            | Documentação e comunidade                                   | Documentação e comunidade; canais adicionais variam conforme o plano do *workspace* |
| Comportamento      | "Dorme" após 15 min sem acesso; ~1 min para acordar         | Sem *spin-down*                                             |

**Pontos fortes:** deploy por `git push`, HTTPS e domínio próprio já no início, disco persistente barato, banco Postgres gerenciado disponível para a migração futura, degraus de escala claros (Standard US$ 25/mês e acima).
**Pontos fracos:** o plano gratuito **não serve para produção** deste projeto (o JSON seria apagado e o site "dorme"); cobrança em dólar; tráfego de vídeo acima da franquia gera custo extra.

### Opção C — Hostinger VPS KVM 1 (paga)

Servidor virtual completo em data center no Brasil (São Paulo). Você administra o servidor.

| Item               | Detalhe                                                          |
|--------------------|------------------------------------------------------------------|
| Preço              | **R$ 29,99/mês** no contrato de 24 meses (≈ R$ 719,76 pagos de uma vez); **renova a R$ 59,99/mês** |
| Recursos           | 1 vCPU, 4 GB RAM                                                 |
| Espaço em disco    | 50 GB NVMe                                                       |
| Largura de banda   | 4 TB/mês (página oficial); alguns comparativos brasileiros citam 1 TB — confirmar no ato da compra |
| Domínio próprio    | ✅ (o registro do domínio **não** vem incluso)                   |
| SSL                | ✅ Gratuito via Let's Encrypt (você instala e mantém com o Certbot) |
| Suporte            | Chat 24/7 em português; garantia de reembolso de 30 dias         |
| Extras             | IP dedicado, backup semanal gratuito, upgrade de plano sem trocar de servidor |
| Disco persistente  | ✅                                                               |

**Pontos fortes:** melhor relação recursos × preço, muito espaço e banda para vídeos, cobrança em reais, servidor no Brasil.
**Pontos fracos:** exige instalar e manter Nginx, Gunicorn, HTTPS e atualizações de segurança; o preço **dobra** na renovação; pagamento de 24 meses adiantado para obter o preço promocional.

---

## 3. Domínio — três opções (extensões diferentes)

| # | Extensão      | Registrador              | Registro/ano                     | Renovação/ano                    | Requisitos e observações |
|---|---------------|--------------------------|----------------------------------|----------------------------------|--------------------------|
| 1 | **.com.br**   | Registro.br (oficial)    | **R$ 40,00**                     | R$ 40,00 (fixo)                  | Exige CPF ou CNPJ brasileiro. Pix, cartão ou boleto. Descontos para registrar vários anos de uma vez (ex.: 2 anos = R$ 76). Único registrador oficial do .br; os demais são revendedores |
| 2 | **.com**      | Cloudflare Registrar     | **US$ 10,46 ≈ R$ 57,53**         | US$ 10,46 (preço de custo, sem margem) | Sem restrição de nacionalidade; privacidade WHOIS gratuita; exige usar o DNS da Cloudflare (que inclui CDN gratuita). Pagamento em cartão internacional. Alternativas: Porkbun ≈ US$ 11,08; Hostinger R$ 29,99 no 1º ano e R$ 79,99 na renovação |
| 3 | **.pet**      | Cloudflare Registrar     | **US$ 20,20 ≈ R$ 111,10**        | US$ 20,20 (preço de custo)       | Extensão temática (lojas, clínicas e serviços para animais). Alternativa nacional: SuperDomínios, R$ 49,99 no 1º ano (confirmar renovação) |

**Sobre o `.edu.br`:** essa extensão é reservada a instituições de ensino e pesquisa (regra do
Registro.br). Um petshop **não é elegível**, portanto ela não entra na comparação. Para referência,
as extensões `.br` seguem a tarifa padrão do Registro.br de R$ 40/ano (confirme no ato do registro).

> ✅ **Antes de tudo**, verifique se `pethouse.com.br` está disponível em <https://registro.br>.
> Esta pesquisa não checou a disponibilidade do nome.

---

## 4. Tabela comparativa — custos e recursos

### 4.1 Hospedagem

| Critério                | A) PythonAnywhere Free | A) PythonAnywhere Developer | B) Render Free | B) Render Starter + 1 GB | C) Hostinger VPS KVM 1 |
|-------------------------|:---:|:---:|:---:|:---:|:---:|
| **Custo mensal**        | R$ 0 | R$ 55,00 | R$ 0 | ≈ R$ 39,88 | R$ 29,99 (24 meses) → R$ 59,99 |
| **Custo anual**         | R$ 0 | R$ 660,00 | R$ 0 | ≈ R$ 478,50 | R$ 359,88 (1º período) / R$ 719,88 (renovação) |
| **Espaço**              | 512 MB | 5 GB | efêmero | 1 GB (expansível) | 50 GB NVMe |
| **Largura de banda**    | sem franquia divulgada | sem franquia divulgada | franquia do *workspace* | franquia do *workspace* + US$ 0,15/GB extra | 4 TB (confirmar) |
| **SSL**                 | ✅ (subdomínio) | ✅ | ✅ | ✅ | ✅ (Let's Encrypt, manual) |
| **Domínio próprio**     | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Suporte**             | comunidade | e-mail | comunidade/docs | comunidade/docs | chat 24/7 em português |
| **Mantém o JSON?**      | ✅ | ✅ | ❌ | ✅ (com disco) | ✅ |
| **Dificuldade**         | baixa | baixa | baixa | baixa/média | **alta** |
| **Serve para produção?**| só demonstração | ✅ | ❌ | ✅ | ✅ |

### 4.2 Domínio

| Critério             | .com.br (Registro.br) | .com (Cloudflare) | .pet (Cloudflare) |
|----------------------|:---:|:---:|:---:|
| **Custo anual**      | R$ 40,00 | ≈ R$ 57,53 | ≈ R$ 111,10 |
| **Renovação**        | R$ 40,00 | ≈ R$ 57,53 | ≈ R$ 111,10 |
| **Diferença p/ .com.br** | — | + R$ 17,53/ano | + R$ 71,10/ano |
| **Pagamento**        | Pix / boleto / cartão nacional | cartão internacional (+ IOF) | cartão internacional (+ IOF) |
| **Percepção no Brasil** | ⭐⭐⭐ máxima confiança local | ⭐⭐ neutra | ⭐⭐ temática/memorável |

### 4.3 Custo total estimado (hospedagem + domínio `.com.br`)

| Cenário                                   | 1º ano       | Média mensal (1º ano) | Total em 3 anos |
|-------------------------------------------|-------------:|----------------------:|----------------:|
| A) PythonAnywhere Developer + .com.br     | R$ 700,00    | R$ 58,33              | R$ 2.100,00     |
| B) Render Starter + 1 GB + .com.br        | R$ 518,50    | R$ 43,21              | R$ 1.555,50     |
| C) Hostinger VPS KVM 1 + .com.br          | R$ 399,88    | R$ 33,32              | R$ 1.559,64     |
| Gratuitos (PythonAnywhere/Render Free)    | R$ 0         | R$ 0                  | R$ 0 (só demonstração, sem domínio próprio ou sem persistência de dados) |

*Cálculos: 3 anos da Hostinger = 24 meses × R$ 29,99 + 12 meses × R$ 59,99 (renovação); domínio
.com.br = R$ 40 × 3. Se trocar o domínio, some a diferença da tabela 4.2.*

---

## 5. Escolha final do grupo

**Nossa escolha: Render (plano Starter + disco persistente de 1 GB) com o domínio `.com.br` registrado
no Registro.br**, totalizando cerca de **R$ 518,50 no primeiro ano (≈ R$ 43/mês)**. Para o estágio atual
do nosso projeto — uma aplicação Flask que guarda dados em JSON, ainda sem banco, e que já prevê um
repositório no GitHub — o Render entrega o melhor equilíbrio entre custo, simplicidade e crescimento: custa
menos que o PythonAnywhere Developer (cerca de R$ 180 a menos por ano), dispensa administrar servidor
(diferentemente da VPS, que é mais barata só enquanto vale o preço promocional de 24 meses e dobra na
renovação), já entrega HTTPS e domínio próprio, e o disco persistente de US$ 0,25/mês resolve o principal
risco do projeto atual, que é perder os arquivos `.json`. Em escalabilidade, o caminho é claro e gradual: quando
o banco de dados for criado, o Postgres gerenciado da própria plataforma substitui o JSON sem trocar de
fornecedor, e o aumento de tráfego se resolve subindo de plano (Standard, US$ 25/mês). O `.com.br` é a melhor
escolha de domínio por custo (R$ 40 fixos, sem reajuste na renovação), pela confiança que transmite ao consumidor
brasileiro e por já ser o endereço usado no e-mail da loja; o `.com` e o `.pet` ficam como registros opcionais de
proteção da marca, por R$ 17,53 e R$ 71,10 a mais por ano. Os planos gratuitos servem apenas para testes: no Render Free o
JSON seria apagado a cada reinício, e o PythonAnywhere Free não aceita domínio próprio.

### Quando reavaliar
- **Vídeos com muito acesso:** o tráfego de vídeo passa da franquia e gera cobrança extra → colocar a Cloudflare (CDN gratuita) na frente, comprimir os vídeos ou migrar para a **VPS da Hostinger** (4 TB de banda e 50 GB de disco).
- **Equipe com conhecimento de servidores:** a VPS vira a opção mais barata por GB e por CPU, desde que se planeje o reajuste de R$ 29,99 para R$ 59,99 na renovação.
- **Custo em reais:** se a variação do dólar incomodar, a Hostinger é a única das três cobrada em reais.

---

## 6. O que este orçamento não inclui

- E-mail profissional (`contato@pethouse.com.br`): hospedagem de caixas postais é cobrada à parte (ex.: serviços de e-mail em torno de US$ 3/mês por caixa, ou encaminhamento gratuito oferecido por alguns registradores).
- Banco de dados gerenciado (Postgres no Render: a partir de ≈ US$ 6–7/mês para a menor instância; MySQL já vem no plano Developer do PythonAnywhere).
- Gateway de pagamento (Pix/cartão): taxas por transação, definidas pelo provedor escolhido.
- Certificado de loja/nota fiscal, contabilidade, marketing (fora do escopo do trabalho).

## 7. Próximos passos (se o projeto fosse publicado)

Como este é um trabalho acadêmico, **não contratamos nenhum serviço**. Estes seriam os passos:

1. Verificar a disponibilidade de `pethouse.com.br` no Registro.br e registrar (CPF ou CNPJ).
2. Criar o repositório no GitHub e enviar o projeto.
3. Antes de publicar, resolver os itens de segurança da `DOCUMENTACAO.md` (seção 12): **login do painel `/admin`**, chave secreta em variável de ambiente, `debug` desligado e servidor de produção (`gunicorn` no `requirements.txt`).
4. Criar o serviço Web no Render ligado ao repositório, com comando de inicialização `gunicorn app:app`.
5. Anexar um disco de 1 GB e apontar a pasta de dados (`data/`) para ele, para que os `.json` sobrevivam a reinícios e novos deploys. (Isso exige uma pequena alteração no `data_store.py`: ler o caminho da pasta de dados de uma variável de ambiente, em vez de fixar `data/`.)
6. Cadastrar o domínio no Render e apontar o DNS (registro `CNAME`/`A` no painel do Registro.br).
7. Testar HTTPS, cadastro, login, checkout e uploads de mídia em produção.

## 8. Resumo em uma linha

| | Hospedagem | Domínio | 1º ano | Observação |
|---|---|---|---:|---|
| **Escolha do grupo** | Render Starter + 1 GB | .com.br | **≈ R$ 518,50** | Melhor custo-benefício para o estágio atual, com caminho claro para banco de dados e mais tráfego |

## 9. Fontes consultadas pelo grupo (29/09/2026)

- Registro.br — valores e regras do `.br`: <https://registro.br/dominio/> e <https://registro.br/ajuda/pagamento-de-dominio/>
- Cloudflare Registrar — tabela de preços por extensão (`.com`, `.pet`): <https://cfdomainpricing.com/>
- PythonAnywhere — novos planos e mudanças na conta gratuita (dez/2025): <https://blog.pythonanywhere.com/222/> e <https://blog.pythonanywhere.com/221/>
- Render — documentação do plano gratuito e comparativos de preço 2026: <https://render.com/docs/free>
- Hostinger — planos VPS KVM e comparativos de renovação (ago/2026): <https://www.hostinger.com/vps-hosting>
- Comparativos de registradores (Porkbun, Namecheap, Hostinger): <https://elvisonunwa.com/vs/cloudflare-vs-porkbun-vs-namecheap>
