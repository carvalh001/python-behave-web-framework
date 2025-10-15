import os
from datetime import datetime
from pathlib import Path
import unicodedata


class GerenciadorDeEvidencias:
    """
    Gerencia a captura e organização de evidências (screenshots e vídeos) dos testes.
    Responsável por criar diretórios, capturar screenshots em falhas e gerenciar gravações.
    """
    
    def __init__(self, configuracao):
        """
        Inicializa o gerenciador de evidências
        
        Args:
            configuracao: Instância de GerenciadorDeConfiguracao
        """
        self.configuracao = configuracao
        self.contador_passos = 0
        self.gravador_video_atual = None
        self.nome_arquivo_video_atual = None
        self.nome_cenario_atual = None
    
    def preparar_diretorios(self):
        """Cria e limpa os diretórios de evidências antes da execução"""
        self._criar_diretorio(self.configuracao.diretorio_screenshots)
        self._criar_diretorio(self.configuracao.diretorio_videos)
        
        self._limpar_diretorio(self.configuracao.diretorio_screenshots)
        self._limpar_diretorio(self.configuracao.diretorio_videos)
        
        print("[EVIDENCIAS] Diretorios preparados")
    
    def _criar_diretorio(self, caminho_diretorio):
        """
        Cria um diretório se ele não existir
        
        Args:
            caminho_diretorio: Path do diretório a ser criado
        """
        if not caminho_diretorio.exists():
            caminho_diretorio.mkdir(parents=True, exist_ok=True)
            print(f"[EVIDENCIAS] Diretorio criado: {caminho_diretorio}")
    
    def _limpar_diretorio(self, caminho_diretorio):
        """
        Remove todos os arquivos de um diretório
        
        Args:
            caminho_diretorio: Path do diretório a ser limpo
        """
        if not caminho_diretorio.exists():
            return
        
        arquivos_removidos = 0
        for arquivo in caminho_diretorio.iterdir():
            caminho_arquivo = caminho_diretorio / arquivo
            try:
                if caminho_arquivo.is_file():
                    caminho_arquivo.unlink()
                    arquivos_removidos += 1
            except Exception as erro:
                print(f"[EVIDENCIAS] Erro ao limpar arquivo {arquivo}: {erro}")
        
        if arquivos_removidos > 0:
            print(f"[EVIDENCIAS] {arquivos_removidos} arquivo(s) antigo(s) removido(s)")
    
    def iniciar_contagem_passos(self):
        """Reseta o contador de passos para um novo cenário"""
        self.contador_passos = 0
    
    def capturar_screenshot_falha(self, driver, nome_passo):
        """
        Captura screenshot quando um passo falha
        
        Args:
            driver: Instância do WebDriver
            nome_passo: Nome do passo que falhou
            
        Returns:
            Nome do arquivo de screenshot criado ou None se falhar
        """
        if not self.configuracao.screenshot_em_falhas:
            return None
        
        self.contador_passos += 1
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            nome_passo_sanitizado = self._sanitizar_nome_arquivo(nome_passo)
            nome_arquivo = f'step_{self.contador_passos}_{timestamp}_{nome_passo_sanitizado}.png'
            caminho_completo = self.configuracao.diretorio_screenshots / nome_arquivo
            
            driver.save_screenshot(str(caminho_completo))
            print(f"[SCREENSHOT] Capturado: {nome_arquivo}")
            
            return nome_arquivo
            
        except Exception as erro:
            print(f"[SCREENSHOT] Erro ao capturar: {erro}")
            return None
    
    def _sanitizar_nome_arquivo(self, nome):
        """
        Remove caracteres especiais e limita o tamanho do nome do arquivo
        
        Args:
            nome: Nome original do arquivo
            
        Returns:
            Nome sanitizado e seguro para uso em arquivo
        """
        caracteres_proibidos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        nome_limpo = nome.replace(" ", "_")
        
        for caractere in caracteres_proibidos:
            nome_limpo = nome_limpo.replace(caractere, "_")
        
        return nome_limpo[:50]
    
    def iniciar_gravacao_video(self, driver, nome_cenario):
        """
        Inicia a gravação de vídeo para um cenário
        
        Args:
            driver: Instância do WebDriver
            nome_cenario: Nome do cenário sendo testado
        """
        try:
            from recursos.utils.gravador_video import VideoRecorder
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            nome_cenario_normalizado = self._normalizar_para_ascii(nome_cenario)
            nome_cenario_sanitizado = self._sanitizar_nome_arquivo(nome_cenario_normalizado)
            
            self.nome_arquivo_video_atual = f"video_{timestamp}_{nome_cenario_sanitizado}.mp4"
            caminho_video = self.configuracao.diretorio_videos / self.nome_arquivo_video_atual
            
            self.gravador_video_atual = VideoRecorder(
                str(caminho_video),
                driver=driver,
                fps=self.configuracao.video_fps
            )
            self.gravador_video_atual.start_recording()
            self.nome_cenario_atual = nome_cenario
            
            print(f"[VIDEO] Gravacao iniciada: {self.nome_arquivo_video_atual}")
        except Exception as erro:
            print(f"[VIDEO] Erro ao iniciar gravacao: {erro}")
            self.gravador_video_atual = None
    
    def finalizar_gravacao_video(self, cenario_falhou, tem_tag_video_always):
        """
        Finaliza a gravação de vídeo e decide se mantém ou descarta
        
        Args:
            cenario_falhou: Boolean indicando se o cenário falhou
            tem_tag_video_always: Boolean indicando se o cenário tem tag @video_always
            
        Returns:
            Nome do arquivo de vídeo se foi mantido, None caso contrário
        """
        if not self.gravador_video_atual:
            return None
        
        deve_manter_video = (
            cenario_falhou or 
            tem_tag_video_always or 
            self.configuracao.gravar_video_sempre
        )
        
        try:
            self.gravador_video_atual.stop_recording(save=deve_manter_video)
            
            if deve_manter_video:
                motivo = self._obter_motivo_gravacao(cenario_falhou, tem_tag_video_always)
                print(f"[VIDEO] Mantido ({motivo}): {self.nome_arquivo_video_atual}")
                return self.nome_arquivo_video_atual
            else:
                print(f"[VIDEO] Descartado (cenario passou): {self.nome_arquivo_video_atual}")
                return None
                
        except Exception as erro:
            print(f"[VIDEO] Erro ao finalizar gravacao: {erro}")
            return None
        finally:
            self.gravador_video_atual = None
            self.nome_arquivo_video_atual = None
    
    def _obter_motivo_gravacao(self, cenario_falhou, tem_tag_video_always):
        """
        Retorna o motivo pelo qual o vídeo foi mantido
        
        Args:
            cenario_falhou: Boolean indicando se o cenário falhou
            tem_tag_video_always: Boolean indicando se tem tag @video_always
            
        Returns:
            String com o motivo
        """
        if cenario_falhou:
            return "falha detectada"
        elif tem_tag_video_always:
            return "tag @video_always"
        elif self.configuracao.gravar_video_sempre:
            return "configuração GRAVAR_VIDEO_SEMPRE"
        return "motivo desconhecido"
    
    def _normalizar_para_ascii(self, texto):
        """
        Normaliza texto removendo acentos e caracteres especiais
        
        Args:
            texto: Texto original com possíveis acentos
            
        Returns:
            Texto normalizado em ASCII
        """
        texto_normalizado = unicodedata.normalize('NFKD', texto)
        texto_ascii = texto_normalizado.encode('ASCII', 'ignore').decode('ASCII')
        return texto_ascii

