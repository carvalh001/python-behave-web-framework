from behave import given, when, then
from pages.contrato.gestao_contratos_page import PaginaGestaoContratos
from pages.contrato.quitacao_page import PaginaQuitacao
from recursos.apis.contrato_service import ServicoContrato


@given('que um contrato com situação "{situacao}" foi gerado para o cliente de CPF "{cpf}"')
def criar_massa_dados_contrato_via_api(context, situacao, cpf):
    """
    Cria a massa de dados necessária via API.
    Garante que existe um contrato com a situação especificada.
    """
    print(f"[MASSA DE DADOS] Gerando contrato para CPF: {cpf} via API...")
    
    context.servico_contrato = ServicoContrato(
        configuracao=context.configuracao
    )
    
    resposta_api = context.servico_contrato.criar_contrato(situacaoContrato=1)
    
    assert resposta_api is not None, "Falha ao criar contrato via API"
    
    context.cpf_teste = cpf
    print("[MASSA DE DADOS] [OK] Contrato gerado com sucesso")


@given('eu acesso a tela de Gestão de Contratos')
def acessar_tela_gestao_contratos(context):
    """Navega para a página de Gestão de Contratos"""
    context.pagina_gestao = PaginaGestaoContratos(
        context.driver,
        context.configuracao
    )
    context.pagina_gestao.carregar_pagina()


@when('eu preencho o filtro "Situação Contratual" com o valor "{situacao}" e clico em "Pesquisar"')
def filtrar_por_situacao_e_pesquisar(context, situacao):
    """Aplica filtro de situação contratual e executa pesquisa"""
    context.pagina_gestao.filtrar_por_situacao_contratual(situacao)
    context.pagina_gestao.clicar_botao_pesquisar()


@when('eu aciono a opção "Quitação" no menu de ações do contrato com CPF "{cpf}"')
def abrir_quitacao_do_contrato(context, cpf):
    """Abre o menu de ações e seleciona Quitação para o CPF especificado"""
    context.pagina_gestao.abrir_menu_acoes_do_contrato_por_cpf(cpf)
    context.pagina_gestao.selecionar_opcao_quitacao_no_menu()


@then('a tela de "Quitação" é exibida com os dados do CPF "{cpf_esperado}"')
def validar_tela_quitacao_com_cpf(context, cpf_esperado):
    """Valida que a tela de Quitação foi aberta e exibe o CPF correto"""
    context.pagina_quitacao = PaginaQuitacao(context.driver)
    
    cpf_exibido_na_tela = context.pagina_quitacao.obter_cpf_exibido_na_tela()
    
    print(f"[VALIDAÇÃO] CPF esperado: '{cpf_esperado}'")
    print(f"[VALIDAÇÃO] CPF exibido: '{cpf_exibido_na_tela}'")
    
    assert cpf_exibido_na_tela == cpf_esperado, \
        f"CPF incorreto. Esperado: '{cpf_esperado}', Encontrado: '{cpf_exibido_na_tela}'"
    
    print("[VALIDACAO] [OK] Tela de Quitacao validada com sucesso")
