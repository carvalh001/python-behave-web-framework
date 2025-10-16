import os
from dotenv import load_dotenv
from pathlib import Path


class GerenciadorDeConfiguracao:
    """
    Gerencia todas as configurações do framework de automação.
    Carrega variáveis do arquivo .env e fornece valores padrão quando necessário.
    """
    
    def __init__(self, arquivo_env=".env"):
        """
        Inicializa o gerenciador e carrega as configurações do arquivo .env
        
        Args:
            arquivo_env: Caminho para o arquivo .env (padrão: ".env" na raiz do projeto)
        """
        self.caminho_raiz_projeto = Path(__file__).parent.parent.parent
        self.caminho_arquivo_env = self.caminho_raiz_projeto / arquivo_env
        
        self._carregar_variaveis_ambiente()
        self._validar_configuracoes_obrigatorias()
    
    def _carregar_variaveis_ambiente(self):
        """Carrega as variáveis de ambiente do arquivo .env"""
        if self.caminho_arquivo_env.exists():
            load_dotenv(self.caminho_arquivo_env)
            print(f"[CONFIG] Configurações carregadas de: {self.caminho_arquivo_env}")
        else:
            print(f"[CONFIG] Arquivo .env não encontrado. Usando configurações padrão.")
    
    def _validar_configuracoes_obrigatorias(self):
        """Valida se configurações obrigatórias estão presentes"""
        configuracoes_obrigatorias = ['URL_BASE_SISTEMA']
        
        for config in configuracoes_obrigatorias:
            if not self._obter_valor(config):
                raise ValueError(
                    f"Configuração obrigatória '{config}' não encontrada no arquivo .env"
                )
    
    def _obter_valor(self, chave, valor_padrao=None):
        """
        Obtém um valor de configuração do ambiente
        
        Args:
            chave: Nome da variável de ambiente
            valor_padrao: Valor padrão caso a variável não exista
            
        Returns:
            Valor da configuração ou valor padrão
        """
        return os.getenv(chave, valor_padrao)
    
    def _obter_booleano(self, chave, valor_padrao=False):
        """
        Obtém um valor booleano de configuração
        
        Args:
            chave: Nome da variável de ambiente
            valor_padrao: Valor padrão booleano
            
        Returns:
            True ou False
        """
        valor = self._obter_valor(chave, str(valor_padrao))
        return valor.lower() in ('true', 'yes', '1', 'sim', 'verdadeiro')
    
    def _obter_inteiro(self, chave, valor_padrao=0):
        """
        Obtém um valor inteiro de configuração
        
        Args:
            chave: Nome da variável de ambiente
            valor_padrao: Valor padrão inteiro
            
        Returns:
            Valor inteiro
        """
        valor = self._obter_valor(chave, str(valor_padrao))
        try:
            return int(valor)
        except ValueError:
            return valor_padrao
    
    @property
    def url_base_sistema(self):
        """URL base do sistema sendo testado"""
        return self._obter_valor(
            'URL_BASE_SISTEMA',
            'https://sistemacreditogestaowebteste.hml.cloud.poupex'
        )
    
    @property
    def url_gestao_contratos(self):
        """URL da página de gestão de contratos"""
        return self._obter_valor(
            'URL_GESTAO_CONTRATOS',
            f'{self.url_base_sistema}/contrato'
        )
    
    @property
    def url_renegociacao(self):
        """URL da página de renegociação"""
        return self._obter_valor(
            'URL_RENEGOCIACAO',
            f'{self.url_base_sistema}/renegociacao'
        )
    
    @property
    def url_api_base(self):
        """URL base da API"""
        return self._obter_valor(
            'URL_API_BASE',
            f'{self.url_base_sistema}/api'
        )
    
    @property
    def tipo_navegador(self):
        """Tipo de navegador a ser usado (chrome, firefox, edge)"""
        return self._obter_valor('NAVEGADOR_TIPO', 'chrome').lower()
    
    @property
    def navegador_headless(self):
        """Se o navegador deve executar em modo headless"""
        return self._obter_booleano('NAVEGADOR_HEADLESS', False)
    
    @property
    def navegador_maximizar(self):
        """Se o navegador deve ser maximizado ao iniciar"""
        return self._obter_booleano('NAVEGADOR_MAXIMIZAR', True)
    
    @property
    def navegador_largura(self):
        """Largura da janela do navegador"""
        return self._obter_inteiro('NAVEGADOR_LARGURA', 1920)
    
    @property
    def navegador_altura(self):
        """Altura da janela do navegador"""
        return self._obter_inteiro('NAVEGADOR_ALTURA', 1080)
    
    @property
    def timeout_implicito(self):
        """Timeout implícito do Selenium em segundos"""
        return self._obter_inteiro('TIMEOUT_IMPLICITO', 10)
    
    @property
    def timeout_explicito(self):
        """Timeout para esperas explícitas em segundos"""
        return self._obter_inteiro('TIMEOUT_EXPLICITO', 10)
    
    @property
    def timeout_carregamento_pagina(self):
        """Timeout para carregamento de página em segundos"""
        return self._obter_inteiro('TIMEOUT_CARREGAMENTO_PAGINA', 30)
    
    @property
    def timeout_conteudo_dinamico(self):
        """Timeout para esperar conteúdo dinâmico carregar"""
        return self._obter_inteiro('TIMEOUT_CONTEUDO_DINAMICO', 2)
    
    @property
    def diretorio_relatorios(self):
        """Diretório raiz para relatórios"""
        return Path(self._obter_valor('DIRETORIO_RELATORIOS', './reports'))
    
    @property
    def diretorio_screenshots(self):
        """Diretório para screenshots temporários"""
        return Path(self._obter_valor('DIRETORIO_SCREENSHOTS', './reports/screenshots'))
    
    @property
    def diretorio_videos(self):
        """Diretório para vídeos temporários"""
        return Path(self._obter_valor('DIRETORIO_VIDEOS', './reports/videos'))
    
    @property
    def diretorio_metadados(self):
        """Diretório para arquivos de metadados"""
        return Path(self._obter_valor('DIRETORIO_METADADOS', './reports'))
    
    @property
    def gravar_video_sempre(self):
        """Se deve gravar vídeo de todos os cenários"""
        return self._obter_booleano('GRAVAR_VIDEO_SEMPRE', False)
    
    @property
    def video_fps(self):
        """FPS (quadros por segundo) para gravação de vídeo"""
        return self._obter_inteiro('VIDEO_FPS', 15)
    
    @property
    def video_qualidade(self):
        """Qualidade do vídeo (1-10)"""
        return self._obter_inteiro('VIDEO_QUALIDADE', 7)
    
    @property
    def screenshot_em_falhas(self):
        """Se deve capturar screenshot quando um passo falhar"""
        return self._obter_booleano('SCREENSHOT_EM_FALHAS', True)
    
    @property
    def screenshot_em_todos_passos(self):
        """Se deve capturar screenshot em todos os passos"""
        return self._obter_booleano('SCREENSHOT_EM_TODOS_PASSOS', False)
    
    @property
    def screenshot_ultimo_passo(self):
        """Se deve capturar screenshot apenas no último passo de cada cenário"""
        return self._obter_booleano('SCREENSHOT_ULTIMO_PASSO', False)
    
    @property
    def api_modo_mock(self):
        """Se as chamadas de API devem usar dados mockados"""
        return self._obter_booleano('API_MODO_MOCK', True)
    
    @property
    def api_verificar_ssl(self):
        """Se deve verificar certificados SSL em chamadas de API"""
        return self._obter_booleano('API_VERIFICAR_SSL', False)
    
    @property
    def usuario_login(self):
        """Usuário para login no sistema"""
        return self._obter_valor('USUARIO_LOGIN', '')
    
    @property
    def senha_login(self):
        """Senha para login no sistema"""
        return self._obter_valor('SENHA_LOGIN', '')
    
    @property
    def api_token(self):
        """Token de autenticação para API"""
        return self._obter_valor('API_TOKEN', '')
    
    @property
    def relatorio_abrir_automaticamente(self):
        """Se deve abrir o relatório HTML automaticamente após execução"""
        return self._obter_booleano('RELATORIO_ABRIR_AUTOMATICAMENTE', True)
    
    @property
    def relatorio_organizar_por_data(self):
        """Se deve organizar relatórios em pastas por data"""
        return self._obter_booleano('RELATORIO_ORGANIZAR_POR_DATA', True)
    
    @property
    def nivel_log(self):
        """Nível de log (DEBUG, INFO, WARNING, ERROR)"""
        return self._obter_valor('NIVEL_LOG', 'INFO').upper()
    
    @property
    def pausar_em_erro(self):
        """Se deve pausar a execução quando ocorrer um erro"""
        return self._obter_booleano('PAUSAR_EM_ERRO', False)
    
    def exibir_configuracoes(self):
        """Exibe um resumo das configurações carregadas (útil para debug)"""
        print("\n" + "="*60)
        print("CONFIGURAÇÕES DO FRAMEWORK")
        print("="*60)
        print(f"URL Base: {self.url_base_sistema}")
        print(f"Navegador: {self.tipo_navegador}")
        print(f"Headless: {self.navegador_headless}")
        print(f"Timeout Implícito: {self.timeout_implicito}s")
        print(f"API Modo Mock: {self.api_modo_mock}")
        print(f"Gravar Vídeo Sempre: {self.gravar_video_sempre}")
        print("="*60 + "\n")

