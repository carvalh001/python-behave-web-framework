# Steps reutilizáveis para telas de login (Portal, ServeRest, etc.).
# Usam context.pagina_login definido no Given de cada feature.
from behave import then


@then('vejo o campo de senha na tela de login')
def verificar_campo_senha_na_tela_de_login(context):
    """Verifica se o campo de senha está visível na tela de login (reutilizável)."""
    pagina = context.pagina_login
    campo_visivel = pagina.elemento_esta_visivel(pagina.CAMPO_SENHA)
    assert campo_visivel, "Campo de senha não está visível na tela de login"
    print("[VALIDACAO] [OK] Campo de senha visivel")


@then('vejo o botão Entrar na tela de login')
def verificar_botao_entrar_na_tela_de_login(context):
    """Verifica se o botão Entrar está visível na tela de login (reutilizável)."""
    pagina = context.pagina_login
    botao_visivel = pagina.elemento_esta_visivel(pagina.BOTAO_ENTRAR)
    assert botao_visivel, "Botão Entrar não está visível na tela de login"
    print("[VALIDACAO] [OK] Botao Entrar visivel")
