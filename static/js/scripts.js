/* ==========================================================================
   PETHOUSE - scripts.js (ÚNICO arquivo de JavaScript do site)
   ==========================================================================

   COMO FUNCIONA
   Cada página HTML declara o seu nome em <body data-pagina="...">
   (o nome vem do bloco {% block pagina %} no topo de cada template).
   No fim deste arquivo, o site roda SOMENTE o código da página aberta.

   COMO ENCONTRAR AS COISAS
   Procure (Ctrl+F) pelo código da seção, por exemplo:  [J03]  ou  carrinho.html

   ÍNDICE
   --------------------------------------------------------------------------
   [J01]  UTILITÁRIOS COMPARTILHADOS (funções usadas por mais de uma página)
   [J02]  base.html ................ roda em TODAS as páginas
   [J03]  carrinho.html ............ envia o formulário ao mudar a quantidade
   [J04]  admin/lista.html ......... confirmação antes de excluir
   [J05]  admin/estoque_lista.html . confirmação antes de excluir
   [J06]  admin/feedbacks.html ..... confirmação antes de excluir
   [J07]  MAPA DE PÁGINAS E INICIALIZAÇÃO

   PÁGINAS SEM JAVASCRIPT (nada a fazer aqui)
   inicio, produtos, produto, checkout, pedido_confirmacao, cliente_cadastro,
   cliente_login, cliente_perfil, cliente_pet_novo, pet_perfil, agendamento_novo,
   orcamento_solicitar, feedback, fornecedores, contato, 404, admin/painel, admin/form

   COMO CRIAR O JS DE UMA PÁGINA NOVA
   1) No template, defina  {% block pagina %}nome-da-pagina{% endblock %}
   2) Crie uma função nova numa seção [Jxx] abaixo.
   3) Registre-a no mapa de [J07]:  "nome-da-pagina": suaFuncao
   ========================================================================== */

(function () {
  "use strict";


  /* ========================================================================
     [J01] UTILITÁRIOS COMPARTILHADOS
     ======================================================================== */

  /**
   * Pede confirmação antes de enviar formulários marcados com data-confirmar.
   * No HTML:  <form ... data-confirmar="Tem certeza que deseja excluir?">
   * Usado em: admin/lista.html, admin/estoque_lista.html, admin/feedbacks.html
   */
  function ativarConfirmacaoDeFormularios() {
    document.querySelectorAll("form[data-confirmar]").forEach(function (formulario) {
      formulario.addEventListener("submit", function (evento) {
        if (!window.confirm(formulario.dataset.confirmar)) {
          evento.preventDefault();   // usuário clicou em "Cancelar": não envia
        }
      });
    });
  }


  /* ========================================================================
     [J02] base.html  -  roda em TODAS as páginas
     (por enquanto não há nada global; coloque aqui o que valer para o site todo,
     como menu mobile, banner de cookies etc.)
     ======================================================================== */
  function iniciarBase() {
    // reservado
  }


  /* ========================================================================
     [J03] carrinho.html
     Ao mudar a quantidade de um item, envia o formulário sozinho
     (quantidade 0 remove o item). No HTML: <input ... data-auto-submit>
     ======================================================================== */
  function iniciarCarrinho() {
    document.querySelectorAll("input[data-auto-submit]").forEach(function (campo) {
      campo.addEventListener("change", function () {
        campo.form.submit();
      });
    });
  }


  /* ========================================================================
     [J04] admin/lista.html  -  confirmação antes de excluir um registro
     ======================================================================== */
  function iniciarAdminLista() {
    ativarConfirmacaoDeFormularios();
  }


  /* ========================================================================
     [J05] admin/estoque_lista.html  -  confirmação antes de excluir um item
     ======================================================================== */
  function iniciarAdminEstoque() {
    ativarConfirmacaoDeFormularios();
  }


  /* ========================================================================
     [J06] admin/feedbacks.html  -  confirmação antes de excluir um feedback
     ======================================================================== */
  function iniciarAdminFeedbacks() {
    ativarConfirmacaoDeFormularios();
  }


  /* ========================================================================
     [J07] MAPA DE PÁGINAS E INICIALIZAÇÃO
     "nome da página" (data-pagina do <body>)  ->  função a executar
     ======================================================================== */
  var PAGINAS = {
    "carrinho": iniciarCarrinho,              // [J03]
    "admin-lista": iniciarAdminLista,         // [J04]
    "admin-estoque": iniciarAdminEstoque,     // [J05]
    "admin-feedbacks": iniciarAdminFeedbacks  // [J06]
  };

  document.addEventListener("DOMContentLoaded", function () {
    iniciarBase();                                        // sempre
    var pagina = document.body.getAttribute("data-pagina");
    if (pagina && PAGINAS[pagina]) {
      PAGINAS[pagina]();                                  // só a página atual
    }
  });

})();
