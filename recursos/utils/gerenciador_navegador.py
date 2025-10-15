from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class GerenciadorDeNavegador:
    """
    Gerencia a criação e configuração do navegador para automação.
    Suporta Chrome, Firefox e Edge com configurações centralizadas.
    """
    
    def __init__(self, configuracao):
        """
        Inicializa o gerenciador de navegador
        
        Args:
            configuracao: Instância de GerenciadorDeConfiguracao
        """
        self.configuracao = configuracao
        self.driver = None
        self.informacoes_navegador = {}
    
    def inicializar_navegador(self):
        """
        Cria e configura o navegador conforme as configurações
        
        Returns:
            WebDriver configurado e pronto para uso
        """
        tipo_navegador = self.configuracao.tipo_navegador
        
        print(f"[NAVEGADOR] Inicializando navegador: {tipo_navegador}")
        
        if tipo_navegador == 'chrome':
            self.driver = self._criar_chrome()
        elif tipo_navegador == 'firefox':
            self.driver = self._criar_firefox()
        elif tipo_navegador == 'edge':
            self.driver = self._criar_edge()
        else:
            raise ValueError(
                f"Navegador '{tipo_navegador}' não suportado. "
                f"Use: chrome, firefox ou edge"
            )
        
        self._aplicar_configuracoes_gerais()
        self._coletar_informacoes_navegador()
        
        return self.driver
    
    def _criar_chrome(self):
        """Cria instância do Chrome com configurações"""
        opcoes = webdriver.ChromeOptions()
        
        if self.configuracao.navegador_headless:
            opcoes.add_argument('--headless')
            print("[NAVEGADOR] Modo headless ativado")
        
        opcoes.add_argument('--disable-gpu')
        opcoes.add_argument('--no-sandbox')
        opcoes.add_argument('--disable-dev-shm-usage')
        
        servico = ChromeService(executable_path=ChromeDriverManager().install())
        return webdriver.Chrome(service=servico, options=opcoes)
    
    def _criar_firefox(self):
        """Cria instância do Firefox com configurações"""
        opcoes = webdriver.FirefoxOptions()
        
        if self.configuracao.navegador_headless:
            opcoes.add_argument('--headless')
            print("[NAVEGADOR] Modo headless ativado")
        
        servico = FirefoxService(executable_path=GeckoDriverManager().install())
        return webdriver.Firefox(service=servico, options=opcoes)
    
    def _criar_edge(self):
        """Cria instância do Edge com configurações"""
        opcoes = webdriver.EdgeOptions()
        
        if self.configuracao.navegador_headless:
            opcoes.add_argument('--headless')
            print("[NAVEGADOR] Modo headless ativado")
        
        servico = EdgeService(executable_path=EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=servico, options=opcoes)
    
    def _aplicar_configuracoes_gerais(self):
        """Aplica configurações gerais ao navegador"""
        if self.configuracao.navegador_headless:
            self.driver.set_window_size(
                self.configuracao.navegador_largura,
                self.configuracao.navegador_altura
            )
            print(
                f"[NAVEGADOR] Resolucao headless: "
                f"{self.configuracao.navegador_largura}x{self.configuracao.navegador_altura}"
            )
        elif self.configuracao.navegador_maximizar:
            self.driver.maximize_window()
            print("[NAVEGADOR] Janela maximizada")
        else:
            self.driver.set_window_size(
                self.configuracao.navegador_largura,
                self.configuracao.navegador_altura
            )
            print(
                f"[NAVEGADOR] Resolucao definida: "
                f"{self.configuracao.navegador_largura}x{self.configuracao.navegador_altura}"
            )
        
        self.driver.implicitly_wait(self.configuracao.timeout_implicito)
        print(f"[NAVEGADOR] Timeout implicito: {self.configuracao.timeout_implicito}s")
        
        self.driver.set_page_load_timeout(self.configuracao.timeout_carregamento_pagina)
        print(f"[NAVEGADOR] Timeout de carregamento: {self.configuracao.timeout_carregamento_pagina}s")
    
    def _coletar_informacoes_navegador(self):
        """Coleta informações sobre o navegador para o relatório"""
        try:
            capabilities = self.driver.capabilities
            self.informacoes_navegador = {
                'navegador': capabilities.get('browserName', 'Desconhecido'),
                'versao_navegador': capabilities.get('browserVersion', 'Desconhecida'),
                'versao_driver': self._obter_versao_driver(capabilities),
                'user_agent': self.driver.execute_script("return navigator.userAgent;"),
                'resolucao_tela': self.driver.execute_script("return screen.width + 'x' + screen.height;"),
                'tamanho_viewport': self.driver.execute_script("return window.innerWidth + 'x' + window.innerHeight;"),
                'plataforma': self.driver.execute_script("return navigator.platform;")
            }
            
            print(f"[NAVEGADOR] {self.informacoes_navegador['navegador']} {self.informacoes_navegador['versao_navegador']}")
            print(f"[NAVEGADOR] Resolução: {self.informacoes_navegador['resolucao_tela']}")
            
        except Exception as erro:
            print(f"[NAVEGADOR] Erro ao coletar informações: {erro}")
            self.informacoes_navegador = {
                'navegador': self.configuracao.tipo_navegador,
                'versao_navegador': 'Desconhecida',
                'versao_driver': 'Desconhecida',
                'user_agent': 'Desconhecido',
                'resolucao_tela': 'Desconhecida',
                'tamanho_viewport': 'Desconhecido',
                'plataforma': 'Desconhecida'
            }
    
    def _obter_versao_driver(self, capabilities):
        """Extrai a versão do driver das capabilities"""
        tipo_navegador = self.configuracao.tipo_navegador
        
        if tipo_navegador == 'chrome':
            versao_completa = capabilities.get('chrome', {}).get('chromedriverVersion', 'Desconhecida')
            return versao_completa.split()[0] if versao_completa else 'Desconhecida'
        elif tipo_navegador == 'firefox':
            return capabilities.get('moz:geckodriverVersion', 'Desconhecida')
        elif tipo_navegador == 'edge':
            versao_completa = capabilities.get('msedge', {}).get('msedgedriverVersion', 'Desconhecida')
            return versao_completa.split()[0] if versao_completa else 'Desconhecida'
        
        return 'Desconhecida'
    
    def obter_informacoes(self):
        """
        Retorna as informações coletadas sobre o navegador
        
        Returns:
            Dict com informações do navegador
        """
        return self.informacoes_navegador
    
    def fechar_navegador(self):
        """Fecha o navegador de forma segura"""
        if self.driver:
            try:
                self.driver.quit()
                print("[NAVEGADOR] Navegador fechado com sucesso")
            except Exception as erro:
                print(f"[NAVEGADOR] Erro ao fechar navegador: {erro}")

