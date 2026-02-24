from behave import given, when, then
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.portal.login_portal_page import PaginaLoginPortal


@given('que estou na página de login do Portal de Colaboradores')
def acessar_login_portal(context):
    """Abre a página de login do Portal usando URL_BASE_SISTEMA do .env."""
    context.pagina_login = PaginaLoginPortal(
        context.driver,
        context.configuracao.url_base_sistema
    )
    context.pagina_login.carregar_pagina()


@when('eu preencho o usuário "{usuario}" no Portal')
def preencher_usuario_portal(context, usuario):
    """Preenche o campo de usuário ou e-mail."""
    context.pagina_login.preencher_usuario(usuario)


@when('eu preencho a senha "{senha}" no Portal')
def preencher_senha_portal(context, senha):
    """Preenche o campo de senha."""
    context.pagina_login.preencher_senha(senha)


@when('eu clico no botão Entrar do Portal')
def clicar_entrar_portal(context):
    """Clica no botão Entrar."""
    context.pagina_login.clicar_botao_entrar()


@then('vejo o campo de usuário ou e-mail')
def verificar_campo_usuario(context):
    """Verifica se o campo de usuário está visível."""
    campo_visivel = context.pagina_login.elemento_esta_visivel(
        context.pagina_login.CAMPO_USUARIO
    )
    assert campo_visivel, "Campo de usuário ou e-mail não está visível"
    print("[VALIDACAO] [OK] Campo de usuario visivel")


@then('sou redirecionado para a página inicial do Portal')
def validar_redirecionamento_home(context):
    """Valida que a URL atual contém /home após login bem-sucedido."""
    espera = WebDriverWait(context.driver, 15)
    espera.until(lambda d: "/home" in d.current_url)
    url_atual = context.driver.current_url
    assert "/home" in url_atual, (
        f"URL incorreta após login. Esperado: conter '/home', Atual: {url_atual}"
    )
    print(f"[VALIDACAO] [OK] Redirecionado para: {url_atual}")


@then('vejo a área logada do Portal')
def verificar_area_logada(context):
    """Verifica que a área logada (Home) está visível, ex.: mensagem de boas-vindas."""
    espera = WebDriverWait(context.driver, 10)
    elemento_boas_vindas = espera.until(
        EC.visibility_of_element_located(PaginaLoginPortal.MENSAGEM_BEM_VINDO)
    )
    assert elemento_boas_vindas.is_displayed(), "Área logada (Olá, ...) não está visível"
    print("[VALIDACAO] [OK] Area logada visivel (mensagem de boas-vindas)")
