from behave import given, when, then
from pages.contrato.renegociacao_page import PaginaRenegociacao
from recursos.utils.auxiliar_datas import AuxiliarDatas


@given('que eu estou na tela de "Renegociação de Contrato"')
def acessar_tela_renegociacao(context):
    """Navega para a tela de Renegociação de Contrato"""
    context.pagina_renegociacao = PaginaRenegociacao(
        context.driver,
        context.configuracao
    )
    context.pagina_renegociacao.carregar_pagina()


@when('eu preencho o CPF "{cpf}" no filtro de pesquisa')
def preencher_cpf_no_filtro(context, cpf):
    """
    Preenche o campo CPF no filtro de pesquisa.
    
    Args:
        cpf: CPF do cliente no formato "000.000.000-00"
    """
    context.pagina_renegociacao.preencher_campo_cpf(cpf)


@when('eu seleciono o status "{status}" no filtro')
def selecionar_status_no_filtro(context, status):
    """
    Seleciona o status da renegociação no dropdown de filtro.
    
    Args:
        status: Status da renegociação (ex: "Calculada", "Em Implantação")
    """
    context.pagina_renegociacao.selecionar_status_da_renegociacao(status)


@when('eu clico no botão "Pesquisar"')
def clicar_botao_pesquisar(context):
    """Aciona o botão Pesquisar para executar a busca"""
    context.pagina_renegociacao.clicar_botao_pesquisar()


@when('eu clico no botão "Editar" da primeira renegociação da lista')
def clicar_editar_primeira_renegociacao(context):
    """Abre a primeira renegociação encontrada em modo de edição"""
    context.pagina_renegociacao.clicar_botao_editar_primeira_renegociacao()


@when('eu preencho a data de referência com o dia posterior ao corrente')
def preencher_data_referencia_dia_posterior(context):
    """Preenche a data de referência com o dia seguinte ao atual"""
    data_calculada = AuxiliarDatas.obter_dia_posterior()
    context.pagina_renegociacao.preencher_campo_data_referencia(data_calculada)
    print(f"[DATA] Referência: {data_calculada}")


@when('eu preencho a data do primeiro vencimento com 1 mês e 2 dias a partir do dia corrente')
def preencher_data_vencimento_um_mes_dois_dias(context):
    """Preenche a data do primeiro vencimento com 1 mês e 2 dias a partir de hoje"""
    data_calculada = AuxiliarDatas.obter_data_um_mes_e_dois_dias()
    context.pagina_renegociacao.preencher_campo_data_vencimento_primeira_prestacao(data_calculada)
    print(f"[DATA] Vencimento 1ª prestação: {data_calculada}")


@when('eu seleciono a forma de pagamento "{forma_pagamento}"')
def selecionar_forma_pagamento(context, forma_pagamento):
    """
    Seleciona a forma de pagamento no formulário.
    
    Args:
        forma_pagamento: Forma de pagamento (ex: "Pix", "Consignado")
    """
    context.pagina_renegociacao.selecionar_forma_de_pagamento(forma_pagamento)


@when('eu preencho a margem consignável com "{valor}"')
def preencher_margem_consignavel(context, valor):
    """
    Preenche o campo Margem Consignável.
    
    Args:
        valor: Valor da margem (ex: "150,00")
    """
    context.pagina_renegociacao.preencher_campo_margem_consignavel(valor)


@when('eu preencho a prestação com "{valor}"')
def preencher_prestacao(context, valor):
    """
    Preenche o campo Prestação.
    
    Args:
        valor: Valor da prestação (ex: "1,30")
    """
    context.pagina_renegociacao.preencher_campo_prestacao(valor)


@when('eu preencho o prazo com "{valor}"')
def preencher_prazo(context, valor):
    """
    Preenche o campo Prazo (quantidade de meses).
    
    Args:
        valor: Número de meses (ex: "12")
    """
    context.pagina_renegociacao.preencher_campo_prazo(valor)


@when('eu preencho a taxa de juros com "{valor}"')
def preencher_taxa_juros(context, valor):
    """
    Preenche o campo Taxa de Juros.
    
    Args:
        valor: Taxa de juros (ex: "1,72")
    """
    context.pagina_renegociacao.preencher_campo_taxa_juros(valor)


@when('eu limpo o campo "{nome_campo}"')
def limpar_campo_formulario(context, nome_campo):
    """
    Limpa um campo específico do formulário.
    
    Args:
        nome_campo: Nome do campo a ser limpo (ex: "Desconto", "Entrada de Renegociação")
    """
    context.pagina_renegociacao.limpar_campo_por_nome(nome_campo)


@when('eu clico no botão "Calcular"')
def clicar_botao_calcular(context):
    """Aciona o botão Calcular para gerar as opções de parcelamento"""
    context.pagina_renegociacao.clicar_botao_calcular()


@then('a tabela de opções de parcelamento é exibida')
def validar_tabela_opcoes_exibida(context):
    """Valida que a tabela de opções de parcelamento está visível"""
    tabela_visivel = context.pagina_renegociacao.verificar_se_tabela_opcoes_esta_visivel()
    
    assert tabela_visivel, "A tabela de opções de parcelamento não foi exibida"
    
    print("[VALIDACAO] [OK] Tabela de opcoes exibida com sucesso")


@then('uma opção com prazo de "{prazo}" meses, prestação de "{prestacao}" e taxas de "{taxas}" está disponível')
def validar_opcao_especifica_na_tabela(context, prazo, prestacao, taxas):
    """
    Valida que uma opção específica existe na tabela de parcelamento.
    
    Args:
        prazo: Número de meses (ex: "13")
        prestacao: Valor da prestação (ex: "R$ 1,30")
        taxas: Valor das taxas (ex: "R$ 1,84")
    """
    opcao_encontrada = context.pagina_renegociacao.buscar_opcao_especifica_na_tabela(
        prazo,
        prestacao,
        taxas
    )
    
    assert opcao_encontrada, \
        f"Opção não encontrada - Prazo: {prazo}, Prestação: {prestacao}, Taxas: {taxas}"
    
    print(f"[VALIDACAO] [OK] Opcao encontrada - Prazo: {prazo} meses, Prestacao: {prestacao}, Taxas: {taxas}")
