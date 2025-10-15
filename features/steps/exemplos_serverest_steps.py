from behave import given, when, then
from pages.exemplos.login_serverest_page import PaginaLoginServeRest
from pages.exemplos.cadastro_serverest_page import PaginaCadastroServeRest


@given('que estou na página de login do ServeRest')
def acessar_login_serverest(context):
    """Abre a página de login do ServeRest"""
    context.pagina_login = PaginaLoginServeRest(context.driver)
    context.pagina_login.carregar_pagina()


@given('que estou na página de cadastro do ServeRest')
def acessar_cadastro_serverest(context):
    """Abre a página de cadastro do ServeRest"""
    context.pagina_cadastro = PaginaCadastroServeRest(context.driver)
    context.pagina_cadastro.carregar_pagina()


@when('eu clico no link Cadastre-se')
def clicar_link_cadastrese(context):
    """Clica no link para ir ao cadastro"""
    context.pagina_login.clicar_link_cadastrese()


@when('eu preencho o email "{email}" no ServeRest')
def preencher_email_serverest(context, email):
    """Preenche o campo de email"""
    if hasattr(context, 'pagina_login'):
        context.pagina_login.preencher_email(email)
    elif hasattr(context, 'pagina_cadastro'):
        context.pagina_cadastro.preencher_email(email)


@when('eu preencho a senha "{senha}" no ServeRest')
def preencher_senha_serverest(context, senha):
    """Preenche o campo de senha"""
    if hasattr(context, 'pagina_login'):
        context.pagina_login.preencher_senha(senha)
    elif hasattr(context, 'pagina_cadastro'):
        context.pagina_cadastro.preencher_senha(senha)


@when('eu preencho o nome "{nome}" no ServeRest')
def preencher_nome_serverest(context, nome):
    """Preenche o campo de nome"""
    context.pagina_cadastro.preencher_nome(nome)


@when('eu marco o checkbox de administrador')
def marcar_administrador(context):
    """Marca o checkbox de administrador"""
    context.pagina_cadastro.marcar_administrador()


@when('eu clico no botão Entrar do ServeRest')
def clicar_entrar_serverest(context):
    """Clica no botão Entrar"""
    context.pagina_login.clicar_botao_entrar()


@when('eu clico no botão Cadastrar do ServeRest')
def clicar_cadastrar_serverest(context):
    """Clica no botão Cadastrar"""
    context.pagina_cadastro.clicar_botao_cadastrar()


@then('vejo o campo de email')
def verificar_campo_email(context):
    """Verifica se o campo de email está visível"""
    if hasattr(context, 'pagina_login'):
        campo_visivel = context.pagina_login.elemento_esta_visivel(
            context.pagina_login.CAMPO_EMAIL
        )
    else:
        campo_visivel = context.pagina_cadastro.elemento_esta_visivel(
            context.pagina_cadastro.CAMPO_EMAIL
        )
    assert campo_visivel, "Campo de email não está visível"
    print("[VALIDACAO] [OK] Campo de email visivel")


@then('vejo o campo de senha')
def verificar_campo_senha(context):
    """Verifica se o campo de senha está visível"""
    if hasattr(context, 'pagina_login'):
        campo_visivel = context.pagina_login.elemento_esta_visivel(
            context.pagina_login.CAMPO_SENHA
        )
    else:
        campo_visivel = context.pagina_cadastro.elemento_esta_visivel(
            context.pagina_cadastro.CAMPO_SENHA
        )
    
    assert campo_visivel, "Campo de senha não está visível"
    print("[VALIDACAO] [OK] Campo de senha visivel")


@then('vejo o botão Entrar')
def verificar_botao_entrar(context):
    """Verifica se o botão Entrar está visível"""
    botao_visivel = context.pagina_login.elemento_esta_visivel(
        context.pagina_login.BOTAO_ENTRAR
    )
    assert botao_visivel, "Botão Entrar não está visível"
    print("[VALIDACAO] [OK] Botao Entrar visivel")


@then('vejo o campo de nome')
def verificar_campo_nome(context):
    """Verifica se o campo de nome está visível"""
    campo_visivel = context.pagina_cadastro.elemento_esta_visivel(
        context.pagina_cadastro.CAMPO_NOME
    )
    assert campo_visivel, "Campo de nome não está visível"
    print("[VALIDACAO] [OK] Campo de nome visivel")


@then('vejo o checkbox de administrador')
def verificar_checkbox_admin(context):
    """Verifica se o checkbox de administrador está visível"""
    checkbox_visivel = context.pagina_cadastro.elemento_esta_visivel(
        context.pagina_cadastro.CHECKBOX_ADMINISTRADOR
    )
    assert checkbox_visivel, "Checkbox de administrador não está visível"
    print("[VALIDACAO] [OK] Checkbox administrador visivel")


@then('vejo o botão Cadastrar')
def verificar_botao_cadastrar(context):
    """Verifica se o botão Cadastrar está visível"""
    botao_visivel = context.pagina_cadastro.elemento_esta_visivel(
        context.pagina_cadastro.BOTAO_CADASTRAR
    )
    assert botao_visivel, "Botão Cadastrar não está visível"
    print("[VALIDACAO] [OK] Botao Cadastrar visivel")


@then('sou redirecionado para a página de cadastro')
def validar_pagina_cadastro(context):
    """Valida que está na página de cadastro"""
    url_atual = context.driver.current_url
    assert "cadastrarusuarios" in url_atual, \
        f"URL incorreta. Esperado: cadastrarusuarios, Atual: {url_atual}"
    print(f"[VALIDACAO] [OK] Pagina de cadastro: {url_atual}")

