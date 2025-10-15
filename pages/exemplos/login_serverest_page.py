from selenium.webdriver.common.by import By
from pages.base_page import PaginaBase


class PaginaLoginServeRest(PaginaBase):
    """
    Página de Login do ServeRest (https://front.serverest.dev/login)
    Exemplo didático para aprendizado de automação web.
    """
    
    URL_PAGINA = "https://front.serverest.dev/login"
    
    CAMPO_EMAIL = (By.ID, "email")
    CAMPO_SENHA = (By.ID, "password")
    BOTAO_ENTRAR = (By.CSS_SELECTOR, "button[data-testid='entrar']")
    LINK_CADASTRESE = (By.CSS_SELECTOR, "a[data-testid='cadastrar']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def carregar_pagina(self):
        """Abre a página de login do ServeRest"""
        self.driver.get(self.URL_PAGINA)
        print(f"[PAGINA] Login ServeRest carregada: {self.URL_PAGINA}")
    
    def preencher_email(self, email):
        """Preenche o campo de email"""
        self.preencher_campo_texto(self.CAMPO_EMAIL, email)
        print(f"[FORMULARIO] Email: {email}")
    
    def preencher_senha(self, senha):
        """Preenche o campo de senha"""
        self.preencher_campo_texto(self.CAMPO_SENHA, senha)
        print(f"[FORMULARIO] Senha: {'*' * len(senha)}")
    
    def clicar_botao_entrar(self):
        """Clica no botão Entrar"""
        self.clicar_no_elemento(self.BOTAO_ENTRAR)
        print("[ACAO] Botao Entrar clicado")
    
    def clicar_link_cadastrese(self):
        """Clica no link Cadastre-se"""
        self.clicar_no_elemento(self.LINK_CADASTRESE)
        print("[ACAO] Navegando para cadastro")
    
    def fazer_login(self, email, senha):
        """Método completo: preenche e faz login"""
        self.preencher_email(email)
        self.preencher_senha(senha)
        self.clicar_botao_entrar()
        print(f"[LOGIN] Tentativa com email: {email}")

