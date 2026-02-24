from selenium.webdriver.common.by import By
from pages.base_page import PaginaBase


class PaginaLoginPortal(PaginaBase):
    """
    Página de Login do Portal de Colaboradores.
    Utiliza URL base configurada no .env (URL_BASE_SISTEMA) + /login.
    """

    CAMPO_USUARIO = (By.CSS_SELECTOR, "input[placeholder='Digite seu usuário ou e-mail']")
    CAMPO_SENHA = (By.CSS_SELECTOR, "input[placeholder='Digite sua senha']")
    BOTAO_ENTRAR = (By.CSS_SELECTOR, "button[type='submit']")
    TITULO_CARD = (By.CSS_SELECTOR, "h2.text-2xl, .text-2xl.font-bold")
    MENSAGEM_BEM_VINDO = (By.XPATH, "//h1[contains(., 'Olá')]")

    def __init__(self, driver, url_base: str):
        super().__init__(driver)
        self.url_base = url_base.rstrip("/")
        self.url_pagina = f"{self.url_base}/login"

    def carregar_pagina(self):
        """Abre a página de login do Portal de Colaboradores."""
        self.driver.get(self.url_pagina)
        print(f"[PAGINA] Login Portal carregada: {self.url_pagina}")

    def preencher_usuario(self, usuario: str):
        """Preenche o campo de usuário ou e-mail."""
        self.preencher_campo_texto(self.CAMPO_USUARIO, usuario)
        print(f"[FORMULARIO] Usuario: {usuario}")

    def preencher_senha(self, senha: str):
        """Preenche o campo de senha."""
        self.preencher_campo_texto(self.CAMPO_SENHA, senha)
        print(f"[FORMULARIO] Senha: {'*' * len(senha)}")

    def clicar_botao_entrar(self):
        """Clica no botão Entrar."""
        self.clicar_no_elemento(self.BOTAO_ENTRAR)
        print("[ACAO] Botao Entrar clicado")

    def fazer_login(self, usuario: str, senha: str):
        """Método completo: preenche usuário, senha e faz login."""
        self.preencher_usuario(usuario)
        self.preencher_senha(senha)
        self.clicar_botao_entrar()
        print(f"[LOGIN] Tentativa com usuario: {usuario}")
