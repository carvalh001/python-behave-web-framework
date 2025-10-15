from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time


class PaginaBase:
    """
    Classe base para todas as páginas do framework.
    Fornece métodos reutilizáveis para interação com elementos web usando Selenium.
    Todos os métodos têm nomes descritivos em português para facilitar o entendimento.
    """
    
    def __init__(self, driver: WebDriver, timeout_padrao: int = 10):
        """
        Inicializa a página base com o WebDriver
        
        Args:
            driver: Instância do WebDriver do Selenium
            timeout_padrao: Tempo máximo de espera para elementos (padrão: 10 segundos)
        """
        self.driver = driver
        self.espera = WebDriverWait(self.driver, timeout_padrao)

    def _encontrar_elemento(self, localizador: tuple) -> WebElement:
        """
        Encontra um único elemento na página usando espera explícita.
        Aguarda até que o elemento esteja visível antes de retornar.
        
        Args:
            localizador: Tupla (By.TIPO, 'seletor') para localizar o elemento
            
        Returns:
            WebElement encontrado e visível
            
        Raises:
            TimeoutException: Se o elemento não for encontrado no tempo limite
        """
        try:
            return self.espera.until(EC.visibility_of_element_located(localizador))
        except TimeoutException:
            raise TimeoutException(
                f"Elemento não encontrado na página. Localizador: {localizador}"
            )
    
    def _encontrar_elementos(self, localizador: tuple) -> list:
        """
        Encontra múltiplos elementos na página usando espera explícita.
        Aguarda até que pelo menos um elemento esteja presente.
        
        Args:
            localizador: Tupla (By.TIPO, 'seletor') para localizar os elementos
            
        Returns:
            Lista de WebElements encontrados
            
        Raises:
            TimeoutException: Se nenhum elemento for encontrado no tempo limite
        """
        try:
            self.espera.until(EC.presence_of_element_located(localizador))
            return self.driver.find_elements(*localizador)
        except TimeoutException:
            raise TimeoutException(
                f"Elementos não encontrados na página. Localizador: {localizador}"
            )

    def clicar_no_elemento(self, localizador: tuple):
        """
        Clica em um elemento após garantir que ele esteja clicável.
        Aguarda até que o elemento esteja pronto para receber cliques.
        
        Args:
            localizador: Tupla (By.TIPO, 'seletor') do elemento a ser clicado
        """
        elemento = self.espera.until(EC.element_to_be_clickable(localizador))
        elemento.click()

    def preencher_campo_texto(self, localizador: tuple, texto: str):
        """
        Limpa um campo de texto e preenche com o texto fornecido.
        Útil para campos de input e textarea.
        
        Args:
            localizador: Tupla (By.TIPO, 'seletor') do campo de texto
            texto: Texto a ser inserido no campo
        """
        elemento = self._encontrar_elemento(localizador)
        elemento.clear()
        elemento.send_keys(texto)

    def obter_texto_do_elemento(self, localizador: tuple, aguardar_texto_aparecer=False, timeout=10) -> str:
        """
        Obtém o texto exibido em um elemento.
        
        Args:
            localizador: Tupla (By.TIPO, 'seletor') do elemento
            aguardar_texto_aparecer: Se True, aguarda até que o texto não esteja vazio
            timeout: Tempo máximo de espera em segundos
            
        Returns:
            Texto do elemento como string
        """
        elemento = self._encontrar_elemento(localizador)
        
        if aguardar_texto_aparecer:
            espera_customizada = WebDriverWait(self.driver, timeout)
            espera_customizada.until(lambda driver: elemento.text.strip() != "")
        
        return elemento.text
    
    def obter_texto_com_retentativa(self, localizador: tuple, padrao_esperado=None, tentativas_maximas=3, espera_entre_tentativas=1) -> str:
        """
        Obtém texto de um elemento com múltiplas tentativas.
        Útil para conteúdo que carrega dinamicamente e pode demorar a aparecer.
        
        Args:
            localizador: Tupla (By.TIPO, 'seletor') do elemento
            padrao_esperado: Texto que deve estar presente no conteúdo (opcional)
            tentativas_maximas: Número máximo de tentativas de leitura
            espera_entre_tentativas: Segundos para aguardar entre cada tentativa
            
        Returns:
            Texto do elemento
        """
        for tentativa in range(tentativas_maximas):
            try:
                elemento = self._encontrar_elemento(localizador)
                texto = elemento.text.strip()
                
                if padrao_esperado:
                    if padrao_esperado in texto and texto != "000.000.000-00":
                        return texto
                elif texto and texto != "000.000.000-00":
                    return texto
                
                if tentativa < tentativas_maximas - 1:
                    time.sleep(espera_entre_tentativas)
            except TimeoutException:
                if tentativa < tentativas_maximas - 1:
                    time.sleep(espera_entre_tentativas)
                else:
                    raise
        
        elemento = self._encontrar_elemento(localizador)
        return elemento.text

    def elemento_esta_visivel(self, localizador: tuple) -> bool:
        """
        Verifica se um elemento está visível na página.
        
        Args:
            localizador: Tupla (By.TIPO, 'seletor') do elemento
            
        Returns:
            True se o elemento está visível, False caso contrário
        """
        try:
            self._encontrar_elemento(localizador)
            return True
        except TimeoutException:
            return False

    def selecionar_opcao_dropdown(self, localizador: tuple, texto_visivel: str):
        """
        Seleciona uma opção em um dropdown (select) pelo texto visível.
        
        Args:
            localizador: Tupla (By.TIPO, 'seletor') do elemento select
            texto_visivel: Texto exato da opção a ser selecionada
        """
        elemento_select = self._encontrar_elemento(localizador)
        select = Select(elemento_select)
        select.select_by_visible_text(texto_visivel)
        
    def obter_titulo_pagina(self) -> str:
        """
        Obtém o título da página atual (tag <title>).
        
        Returns:
            Título da página como string
        """
        return self.driver.title
