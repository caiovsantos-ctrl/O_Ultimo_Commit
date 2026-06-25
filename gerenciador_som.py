import pygame
import os

class GerenciadorSom:
    """Gerencia todos os efeitos sonoros do jogo"""
    def __init__(self, pasta_audios="audios"): 
        pygame.mixer.init()
        self.pasta_audios = pasta_audios
        self.som_ru_objeto = None 
        self.som_praca_objeto = None
        self.som_andar_objeto = None
        self.som_ambiente_objeto = None
        self.som_sala_objeto = None
        self.som_abertura_objeto = None

    def tocar_efeito(self, nome_arquivo: str, volume=0.5, duracao_ms=None):
        """Toca um som rápido uma única vez"""
        try:
            caminho = os.path.join(self.pasta_audios, nome_arquivo)
            som = pygame.mixer.Sound(caminho)
            som.set_volume(volume)
            if duracao_ms:
                som.play(maxtime=duracao_ms)
            else:
                som.play()
        except Exception as e:
            print(f"Erro ao tocar {nome_arquivo}: {e}")

    def atualizar_som_clima(self, chovendo: bool):
        """Liga a música de chuva se estiver chovendo e desliga se parar"""
        try:
            if chovendo:
                if not pygame.mixer.music.get_busy(): 
                    caminho = os.path.join(self.pasta_audios, "som_chuva.wav")
                    pygame.mixer.music.load(caminho)
                    pygame.mixer.music.set_volume(0.3) 
                    pygame.mixer.music.play(-1) 
            else:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop() 
        except Exception as e:
            print(f"Erro ao gerenciar som do clima: {e}")

    def atualizar_som_ru(self, no_ru: bool):
        """Liga o som ambiente do RU ou desliga se o jogador sair"""
        try:
            if no_ru:
                if self.som_ru_objeto is None:
                    caminho = os.path.join(self.pasta_audios, "som_ru.wav")
                    self.som_ru_objeto = pygame.mixer.Sound(caminho)
                    self.som_ru_objeto.set_volume(0.4)
                    self.som_ru_objeto.play(loops=-1) 
            else:
                if self.som_ru_objeto is not None:
                    self.som_ru_objeto.stop()
                    self.som_ru_objeto = None 
        except Exception as e:
            print(f"Erro ao gerenciar som do RU: {e}")

    def atualizar_som_praca(self, na_praca: bool):
        """Liga o som ambiente da Praça ou desliga se o jogador sair"""
        try:
            if na_praca:
                if self.som_praca_objeto is None:
                    caminho = os.path.join(self.pasta_audios, "som_praca.wav")
                    self.som_praca_objeto = pygame.mixer.Sound(caminho)
                    self.som_praca_objeto.set_volume(0.4)
                    self.som_praca_objeto.play(loops=-1) 
            else:
                if self.som_praca_objeto is not None:
                    self.som_praca_objeto.stop()
                    self.som_praca_objeto = None
        except Exception as e:
            print(f"Erro ao gerenciar som da Praça: {e}")

    def atualizar_som_andar(self, andando: bool):
        """Liga o som de passos e desliga ao chegar no destino"""
        try:
            if andando:
                if self.som_andar_objeto is None:
                    caminho = os.path.join(self.pasta_audios, "som_andar.wav")
                    self.som_andar_objeto = pygame.mixer.Sound(caminho)
                    self.som_andar_objeto.set_volume(0.8)
                    self.som_andar_objeto.play(loops=-1)
            else:
                if self.som_andar_objeto is not None:
                    self.som_andar_objeto.stop()
                    self.som_andar_objeto = None
        except Exception as e:
            print(f"Erro ao gerenciar som de andar: {e}")

    def atualizar_som_ambiente(self, deve_tocar: bool):
        """Liga o som ambiente nos locais abertos ou desliga"""
        try:
            if deve_tocar:
                if self.som_ambiente_objeto is None:
                    caminho = os.path.join(self.pasta_audios, "som_ambiente.wav")
                    self.som_ambiente_objeto = pygame.mixer.Sound(caminho)
                    self.som_ambiente_objeto.set_volume(0.9) 
                    self.som_ambiente_objeto.play(loops=-1)
            else:
                if self.som_ambiente_objeto is not None:
                    self.som_ambiente_objeto.stop()
                    self.som_ambiente_objeto = None
        except Exception as e:
            print(f"Erro ao gerenciar som ambiente externo: {e}")

    def atualizar_som_sala(self, na_sala: bool):
        """Liga o som ambiente de sala fechada e desliga se o jogador sair"""
        try:
            if na_sala:
                if self.som_sala_objeto is None:
                    caminho = os.path.join(self.pasta_audios, "som_sala.wav")
                    self.som_sala_objeto = pygame.mixer.Sound(caminho)
                    self.som_sala_objeto.set_volume(0.3) 
                    self.som_sala_objeto.play(loops=-1)
            else:
                if self.som_sala_objeto is not None:
                    self.som_sala_objeto.stop()
                    self.som_sala_objeto = None
        except Exception as e:
            print(f"Erro ao gerenciar som da sala: {e}")

    def atualizar_som_abertura(self, deve_tocar: bool):
        """Liga a música tema da abertura  ou desliga """
        try:
            if deve_tocar:
                if self.som_abertura_objeto is None:
                    caminho = os.path.join(self.pasta_audios, "som_abertura.mp3")
                    self.som_abertura_objeto = pygame.mixer.Sound(caminho)
                    self.som_abertura_objeto.set_volume(0.4) 
                    self.som_abertura_objeto.play(loops=-1)
            else:
                if self.som_abertura_objeto is not None:
                    self.som_abertura_objeto.stop()
                    self.som_abertura_objeto = None
        except Exception as e:
            print(f"Erro ao gerenciar som de abertura: {e}")