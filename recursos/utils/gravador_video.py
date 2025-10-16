#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gravador de Vídeo para Evidência de Testes
Captura apenas a janela do navegador com timestamp overlay
"""
import os
import sys
import warnings

# === CONFIGURAÇÕES PARA SUPRIMIR AVISOS DO OPENCV/FFMPEG ===
# Estas configurações evitam mensagens de erro assustadoras sobre codecs
# que não estão disponíveis (como OpenH264), mas não afetam a funcionalidade

# Desabilita avisos do OpenCV sobre codecs
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
os.environ['OPENCV_LOG_LEVEL'] = 'SILENT'
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'

# Variáveis do FFmpeg para suprimir mensagens de log
os.environ['FFREPORT'] = 'level=quiet'
os.environ['AV_LOG_FORCE_NOCOLOR'] = '1'

# Desabilita completamente o carregamento do OpenH264 (codec problemático)
os.environ['OPENCV_FFMPEG_LOGLEVEL'] = '-8'  # AV_LOG_QUIET
os.environ['OPENCV_FFMPEG_READ_ATTEMPTS'] = '1'
os.environ['OPENCV_VIDEOCODEC_SKIP_H264_ENCODER'] = '1'
os.environ['OPENH264_DISABLED'] = '1'

# Força OpenCV a não tentar carregar plugins externos
os.environ['OPENCV_VIDEOIO_PLUGINS'] = ''

# Redireciona stderr temporariamente para suprimir mensagens de FFmpeg
# (as mensagens de erro do FFmpeg são impressas em C++ e não podem ser
# completamente suprimidas do Python, mas podemos minimizá-las)
try:
    _stderr_fd = sys.stderr.fileno()
    _stderr_backup = os.dup(_stderr_fd)
    _devnull = os.open(os.devnull, os.O_WRONLY)
    os.dup2(_devnull, _stderr_fd)
    
    try:
        import cv2
    finally:
        # Restaura stderr após importar cv2
        sys.stderr.flush()
        os.dup2(_stderr_backup, _stderr_fd)
        os.close(_devnull)
        os.close(_stderr_backup)
except (AttributeError, OSError):
    # Se der erro ao manipular stderr, importa cv2 normalmente
    import cv2

import numpy as np
import pyautogui
from datetime import datetime
from pathlib import Path
import threading
import time

# Desabilita todos os níveis de log do OpenCV
cv2.setLogLevel(0)  # 0 = Silent
warnings.filterwarnings('ignore', category=UserWarning, module='cv2')


# === FUNÇÃO AUXILIAR PARA SUPRIMIR STDERR EM WINDOWS ===
def _suprimir_stderr_contexto():
    """
    Context manager que suprime stderr em nível de sistema operacional.
    Funciona mesmo com código C/C++ que escreve diretamente no console.
    """
    import contextlib
    
    @contextlib.contextmanager
    def _suprimir():
        stderr_dup = None
        devnull = None
        stderr_fd = None
        
        try:
            # Tenta obter file descriptor do stderr
            try:
                stderr_fd = sys.stderr.fileno()
            except (AttributeError, OSError, ValueError, IOError) as e:
                # Se não conseguir, não faz nada (ex: stderr já foi redirecionado)
                yield
                return
            
            stderr_dup = os.dup(stderr_fd)
            devnull = os.open(os.devnull, os.O_WRONLY)
            
            # Suprime stderr
            sys.stderr.flush()
            os.dup2(devnull, stderr_fd)
            os.close(devnull)
            devnull = None  # Já foi fechado
            
            yield
            
        finally:
            # Restaura stderr se foi inicializado
            if stderr_dup is not None and stderr_fd is not None:
                try:
                    sys.stderr.flush()
                    os.dup2(stderr_dup, stderr_fd)
                    os.close(stderr_dup)
                except (OSError, ValueError, IOError):
                    pass  # Ignora erros ao restaurar
            
            # Fecha devnull se ainda estiver aberto
            if devnull is not None:
                try:
                    os.close(devnull)
                except OSError:
                    pass
    
    try:
        return _suprimir()
    except (AttributeError, OSError):
        # Se não conseguir suprimir, retorna um context manager que não faz nada
        return contextlib.nullcontext()


class VideoRecorder:
    """
    Gravador de vídeo para evidência de testes automatizados.
    
    Características:
    - Captura apenas a janela do navegador (não a tela inteira)
    - Adiciona timestamp overlay no vídeo
    - Grava em formato MP4
    - Executa em thread separada para não impactar performance dos testes
    """
    
    def __init__(self, output_path, driver=None, fps=15):
        """
        Inicializa o gravador de vídeo.
        
        Args:
            output_path (str): Caminho onde o vídeo será salvo
            driver: Instância do Selenium WebDriver para capturar posição da janela
            fps (int): Frames por segundo (padrão: 15)
        """
        self.output_path = output_path
        self.driver = driver
        self.fps = fps
        self.recording = False
        self.frames = []
        self.thread = None
        self.window_rect = None
        
    def start_recording(self):
        """Inicia a gravação do vídeo"""
        # Captura dimensões da janela do navegador
        if self.driver:
            try:
                self.window_rect = self.driver.get_window_rect()
                print(f"[VIDEO] Janela do navegador: {self.window_rect['width']}x{self.window_rect['height']}")
            except Exception as e:
                print(f"[VIDEO] Erro ao obter dimensões da janela: {e}")
                print(f"[VIDEO] Gravando tela inteira como fallback")
                self.window_rect = None
        
        self.recording = True
        self.frames = []
        self.thread = threading.Thread(target=self._record_loop, daemon=True)
        self.thread.start()
        print(f"[VIDEO] Gravação iniciada: {Path(self.output_path).name}")
        
    def _record_loop(self):
        """Loop de captura de frames em thread separada"""
        while self.recording:
            try:
                # Tenta usar screenshot do Selenium (funciona em headless)
                if self.driver:
                    try:
                        # Captura screenshot usando Selenium (funciona em headless)
                        png_bytes = self.driver.get_screenshot_as_png()
                        # Converte PNG bytes para array numpy
                        nparr = np.frombuffer(png_bytes, np.uint8)
                        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    except Exception as e:
                        # Fallback: usa pyautogui se Selenium falhar
                        print(f"[VIDEO] Erro ao capturar via Selenium: {e}, usando pyautogui")
                        if self.window_rect:
                            screenshot = pyautogui.screenshot(region=(
                                self.window_rect['x'],
                                self.window_rect['y'],
                                self.window_rect['width'],
                                self.window_rect['height']
                            ))
                        else:
                            screenshot = pyautogui.screenshot()
                        frame = np.array(screenshot)
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                else:
                    # Sem driver: usa pyautogui
                    if self.window_rect:
                        screenshot = pyautogui.screenshot(region=(
                            self.window_rect['x'],
                            self.window_rect['y'],
                            self.window_rect['width'],
                            self.window_rect['height']
                        ))
                    else:
                        screenshot = pyautogui.screenshot()
                    frame = np.array(screenshot)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Adiciona timestamp overlay
                timestamp_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Fundo semi-transparente para o texto
                overlay = frame.copy()
                cv2.rectangle(overlay, (5, 5), (250, 40), (0, 0, 0), -1)
                frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
                
                # Texto do timestamp
                cv2.putText(
                    frame, 
                    timestamp_text,
                    (10, 28), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, 
                    (0, 255, 0), 
                    2,
                    cv2.LINE_AA
                )
                
                self.frames.append(frame)
                
                # Aguarda intervalo baseado no FPS
                time.sleep(1.0 / self.fps)
                
            except Exception as e:
                print(f"[VIDEO] Erro ao capturar frame: {e}")
                time.sleep(0.5)  # Aguarda antes de tentar novamente
                
    def stop_recording(self, save=True):
        """
        Para a gravação e opcionalmente salva o vídeo.
        
        Args:
            save (bool): Se True, salva o vídeo. Se False, descarta.
            
        Returns:
            bool: True se vídeo foi salvo, False caso contrário
        """
        self.recording = False
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=3)
            
        if save and self.frames:
            try:
                self._save_video()
                print(f"[VIDEO] Vídeo salvo com sucesso: {Path(self.output_path).name}")
                return True
            except Exception as e:
                print(f"[VIDEO] ERRO ao salvar vídeo: {e}")
                return False
        else:
            print(f"[VIDEO] Gravação descartada ({len(self.frames)} frames)")
            return False
            
    def _save_video(self):
        """Salva os frames capturados como arquivo de vídeo MP4"""
        if not self.frames:
            print("[VIDEO] Nenhum frame para salvar")
            return
        
        # Garante que o diretório existe
        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Obtém dimensões do primeiro frame
        height, width, _ = self.frames[0].shape
        
        # Tenta usar codecs nativos e compatíveis com navegadores
        # Forçar uso de codecs que funcionam bem em navegadores
        fourcc_options = [
            ('mp4v', '.mp4'),  # MPEG-4 - MUITO compatível com navegadores
            ('MJPG', '.mp4'),  # Motion JPEG em MP4 - Funciona em navegadores
            ('avc1', '.mp4'),  # H.264 (AVC1) - Melhor compatibilidade mas pode falhar
            ('H264', '.mp4'),  # H.264 alternativo - Nativo no Windows
        ]
        
        # Usa context manager para suprimir stderr durante criação do VideoWriter
        # Isso evita mensagens assustadoras sobre codecs não disponíveis
        with _suprimir_stderr_contexto():
            out = None
            codec_usado = None
            
            for fourcc_str, ext in fourcc_options:
                try:
                    # Ajusta extensão do arquivo se necessário
                    output_path_adjusted = str(self.output_path)
                    if not output_path_adjusted.endswith(ext):
                        output_path_adjusted = output_path_adjusted.rsplit('.', 1)[0] + ext
                    
                    fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
                    out = cv2.VideoWriter(output_path_adjusted, fourcc, self.fps, (width, height))
                    
                    if out.isOpened():
                        codec_usado = fourcc_str
                        self.output_path = output_path_adjusted
                        break
                    else:
                        out.release()
                        out = None
                except Exception:
                    # Ignora erros silenciosamente durante a tentativa de codecs
                    if out:
                        out.release()
                    out = None
            
            # Se nenhum codec funcionou, tenta criar VideoWriter sem fourcc
            if out is None or not out.isOpened():
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (width, height))
                codec_usado = 'mp4v (padrão)'
        
        # Após sair do context manager (stderr restaurado), verifica se deu certo
        if not out.isOpened():
            raise Exception("Não foi possível criar o arquivo de vídeo")
        
        # Escreve todos os frames
        for frame in self.frames:
            out.write(frame)
            
        out.release()
        
        # Informa qual codec foi usado com sucesso
        if codec_usado:
            print(f"[VIDEO] Codec selecionado: {codec_usado} | Frames: {len(self.frames)} | FPS: {self.fps}")
        
    def delete_video(self):
        """
        Deleta o arquivo de vídeo do disco.
        
        Returns:
            bool: True se vídeo foi deletado, False caso contrário
        """
        try:
            video_path = Path(self.output_path)
            if video_path.exists():
                video_path.unlink()
                print(f"[VIDEO] Vídeo deletado: {video_path.name}")
                return True
            else:
                print(f"[VIDEO] Vídeo não encontrado para deletar: {video_path.name}")
                return False
        except Exception as e:
            print(f"[VIDEO] Erro ao deletar vídeo: {e}")
            return False
            
    def get_duration(self):
        """
        Retorna a duração do vídeo em segundos.
        
        Returns:
            float: Duração em segundos
        """
        if self.frames:
            return len(self.frames) / self.fps
        return 0.0
        
    def get_frame_count(self):
        """
        Retorna o número de frames capturados.
        
        Returns:
            int: Número de frames
        """
        return len(self.frames)

