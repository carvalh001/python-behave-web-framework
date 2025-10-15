from selenium.webdriver.common.by import By
from pages.base_page import PaginaBase


class PaginaGestaoContratos(PaginaBase):
    """
    Página de Gestão de Contratos.
    Permite pesquisar contratos por diferentes filtros e acessar ações específicas.
    """
    
    _CAMPO_DROPDOWN_SITUACAO_CONTRATUAL = (By.ID, "situacaoContratual")
    _BOTAO_PESQUISAR = (By.XPATH, "//button[contains(., 'Pesquisar')]")
    _CORPO_TABELA_RESULTADOS = (By.CSS_SELECTOR, "tbody.mdc-data-table__content")
    _OPCAO_MENU_QUITACAO = (By.XPATH, "//a[contains(., 'Quitação')]")

    def __init__(self, driver, configuracao=None):
        super().__init__(driver)
        self.configuracao = configuracao
        self.url_pagina = configuracao.url_gestao_contratos if configuracao else \
            "https://sistemacreditogestaowebteste.hml.cloud.poupex/contrato"

    def carregar_pagina(self):
        """Navega para a página de Gestão de Contratos"""
        self.driver.get(self.url_pagina)
        print(f"[PÁGINA] Gestão de Contratos carregada: {self.url_pagina}")

    def filtrar_por_situacao_contratual(self, situacao_contratual: str):
        """
        Seleciona uma situação contratual no dropdown de filtros.
        
        Args:
            situacao_contratual: Texto da situação (ex: "Normal", "Em Atraso")
        """
        print(f"[FILTRO] Selecionando situação contratual: {situacao_contratual}")
        self.selecionar_opcao_dropdown(
            self._CAMPO_DROPDOWN_SITUACAO_CONTRATUAL,
            situacao_contratual
        )

    def clicar_botao_pesquisar(self):
        """Aciona o botão Pesquisar para aplicar os filtros"""
        print("[AÇÃO] Clicando no botão Pesquisar")
        self.clicar_no_elemento(self._BOTAO_PESQUISAR)

    def abrir_menu_acoes_do_contrato_por_cpf(self, cpf_cliente: str):
        """
        Localiza um contrato na tabela pelo CPF e abre seu menu de ações.
        
        Args:
            cpf_cliente: CPF do cliente no formato "000.000.000-00"
        """
        localizador_menu_acoes = (
            By.XPATH, 
            f"//tr[contains(., '{cpf_cliente}')]//button[@aria-haspopup='menu']"
        )
        print(f"[AÇÃO] Abrindo menu de ações para CPF: {cpf_cliente}")
        self.clicar_no_elemento(localizador_menu_acoes)

    def selecionar_opcao_quitacao_no_menu(self):
        """Seleciona a opção 'Quitação' no menu de ações já aberto"""
        print("[AÇÃO] Selecionando opção Quitação no menu")
        self.clicar_no_elemento(self._OPCAO_MENU_QUITACAO)
