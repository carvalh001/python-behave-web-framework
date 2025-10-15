#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gravador de Vídeo para Evidência de Testes
Captura apenas a janela do navegador com timestamp overlay
"""
import cv2
import numpy as np
import pyautogui
from datetime import datetime
from pathlib import Path
import threading
import time


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
                print(f"[VIDEO] Vídeo salvo com sucesso: {Path(self.output_path).name} ({len(self.frames)} frames)")
                return True
            except Exception as e:
                print(f"[VIDEO] Erro ao salvar vídeo: {e}")
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
        
        # Tenta usar H264 (melhor compatibilidade com navegadores)
        # Se não funcionar, usa XVID como fallback
        fourcc_options = [
            ('avc1', '.mp4'),  # H.264 - Melhor para web
            ('H264', '.mp4'),  # H.264 alternativo
            ('X264', '.mp4'),  # x264
            ('XVID', '.avi'),  # Xvid - Fallback
            ('mp4v', '.mp4'),  # MP4V - Último recurso
        ]
        
        out = None
        for fourcc_str, ext in fourcc_options:
            try:
                # Ajusta extensão do arquivo se necessário
                output_path_adjusted = str(self.output_path)
                if not output_path_adjusted.endswith(ext):
                    output_path_adjusted = output_path_adjusted.rsplit('.', 1)[0] + ext
                
                fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
                out = cv2.VideoWriter(output_path_adjusted, fourcc, self.fps, (width, height))
                
                if out.isOpened():
                    print(f"[VIDEO] Usando codec: {fourcc_str}")
                    self.output_path = output_path_adjusted
                    break
                else:
                    out.release()
                    out = None
            except Exception as e:
                print(f"[VIDEO] Codec {fourcc_str} não disponível: {e}")
                if out:
                    out.release()
                out = None
        
        # Se nenhum codec funcionou, tenta criar VideoWriter sem fourcc
        if out is None or not out.isOpened():
            print("[VIDEO] AVISO: Nenhum codec preferencial disponível, usando padrão do sistema")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (width, height))
        
        if not out.isOpened():
            raise Exception("Não foi possível criar o arquivo de vídeo")
        
        # Escreve todos os frames
        for frame in self.frames:
            out.write(frame)
            
        out.release()
        
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

