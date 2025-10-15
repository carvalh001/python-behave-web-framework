from selenium.webdriver.common.by import By
from pages.base_page import PaginaBase


class PaginaCadastroServeRest(PaginaBase):
    """
    Página de Cadastro de Usuários do ServeRest (https://front.serverest.dev/cadastrarusuarios)
    Exemplo didático para aprendizado de automação web.
    """
    
    URL_PAGINA = "https://front.serverest.dev/cadastrarusuarios"
    
    CAMPO_NOME = (By.ID, "nome")
    CAMPO_EMAIL = (By.ID, "email")
    CAMPO_SENHA = (By.ID, "password")
    CHECKBOX_ADMINISTRADOR = (By.ID, "administrador")
    BOTAO_CADASTRAR = (By.CSS_SELECTOR, "button[data-testid='cadastrar']")
    LINK_ENTRAR = (By.CSS_SELECTOR, "a[data-testid='entrar']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def carregar_pagina(self):
        """Abre a página de cadastro do ServeRest"""
        self.driver.get(self.URL_PAGINA)
        print(f"[PAGINA] Cadastro ServeRest carregada: {self.URL_PAGINA}")
    
    def preencher_nome(self, nome):
        """Preenche o campo nome"""
        self.preencher_campo_texto(self.CAMPO_NOME, nome)
        print(f"[FORMULARIO] Nome: {nome}")
    
    def preencher_email(self, email):
        """Preenche o campo email"""
        self.preencher_campo_texto(self.CAMPO_EMAIL, email)
        print(f"[FORMULARIO] Email: {email}")
    
    def preencher_senha(self, senha):
        """Preenche o campo senha"""
        self.preencher_campo_texto(self.CAMPO_SENHA, senha)
        print(f"[FORMULARIO] Senha: {'*' * len(senha)}")
    
    def marcar_administrador(self):
        """Marca o checkbox de administrador"""
        self.clicar_no_elemento(self.CHECKBOX_ADMINISTRADOR)
        print("[FORMULARIO] Checkbox Administrador marcado")
    
    def clicar_botao_cadastrar(self):
        """Clica no botão Cadastrar"""
        self.clicar_no_elemento(self.BOTAO_CADASTRAR)
        print("[ACAO] Botao Cadastrar clicado")
    
    def clicar_link_entrar(self):
        """Clica no link Entrar (voltar para login)"""
        self.clicar_no_elemento(self.LINK_ENTRAR)
        print("[ACAO] Navegando para login")
    
    def cadastrar_usuario_completo(self, nome, email, senha, administrador=False):
        """Método completo: preenche e cadastra usuário"""
        self.preencher_nome(nome)
        self.preencher_email(email)
        self.preencher_senha(senha)
        
        if administrador:
            self.marcar_administrador()
        
        self.clicar_botao_cadastrar()
        print(f"[CADASTRO] Usuario '{nome}' cadastrado")

