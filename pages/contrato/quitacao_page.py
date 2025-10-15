from selenium.webdriver.common.by import By
from pages.base_page import PaginaBase
import time


class PaginaQuitacao(PaginaBase):
    """
    Página de Quitação de Contrato.
    Exibe informações detalhadas sobre quitação de um contrato específico.
    """
    
    _CAMPO_TEXTO_CPF_CLIENTE = (
        By.XPATH,
        "/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div/pp-quitacao/section[1]/div[1]/div[1]/div[2]"
    )
    
    _CAMPO_TEXTO_CPF_CLIENTE_ALTERNATIVO = (
        By.CSS_SELECTOR,
        "body > app-root > mat-sidenav-container > mat-sidenav-content > div > pp-quitacao > section:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)"
    )

    def __init__(self, driver):
        super().__init__(driver)

    def obter_cpf_exibido_na_tela(self, tempo_espera_segundos=2) -> str:
        """
        Obtém o CPF do cliente exibido na tela de quitação.
        Aguarda o carregamento dinâmico do conteúdo antes de capturar.
        
        Args:
            tempo_espera_segundos: Tempo de espera inicial para carregamento da página
            
        Returns:
            CPF exibido no formato "000.000.000-00"
        """
        print("[QUITAÇÃO] Aguardando carregamento completo da página...")
        time.sleep(tempo_espera_segundos)
        
        print("[QUITAÇÃO] Capturando CPF exibido...")
        
        cpf_capturado = self.obter_texto_com_retentativa(
            self._CAMPO_TEXTO_CPF_CLIENTE,
            padrao_esperado=None,
            tentativas_maximas=3,
            espera_entre_tentativas=1
        )
        
        print(f"[QUITAÇÃO] CPF encontrado: {cpf_capturado}")
        return cpf_capturado
