import os
from PIL import Image, ImageFilter
import customtkinter as ctk


class GerenciadorMidia:
    """Gerencia o carregamento e acesso às imagens do jogo"""
    def __init__(self):
        self.assets = {}
        self.pasta_imagens = "imagens" 

    def inicializar_todos_assets(self):
        """Carrega e processa todas as imagens do jogo garantindo os tamanhos corretos"""       
        caminho_base = os.path.join(self.pasta_imagens, "frente_rural.jpeg")
        img_base_pil = None        
        if os.path.exists(caminho_base):
            img_base_pil = Image.open(caminho_base)
            self.assets["frente_rural"] = ctk.CTkImage(light_image=img_base_pil, size=(1220, 700))
        caminho_borrado = os.path.join(self.pasta_imagens, "borrado.png")
        if os.path.exists(caminho_borrado):
            self.assets["bg_borrado"] = ctk.CTkImage(light_image=Image.open(caminho_borrado), size=(1220, 700))
        elif img_base_pil:
            img_borrada_pil = img_base_pil.filter(ImageFilter.GaussianBlur(radius=15))
            self.assets["bg_borrado"] = ctk.CTkImage(light_image=img_borrada_pil, size=(1220, 700))
        mapeamento_restante = {
            "Parada de Ônibus": "espera.jpeg",
            "parada chuva": "espera_chuva.png",
            "RU": "fila_ru.jpeg",
            "ru chuva": "ru_chuva.png",
            "Lanchonete": "lanchonete.jpeg",
            "lanchonete chuva": "lanchonete_chuva.png",
            "item_caderno": "caderno.png",
            "item_pendrive": "pendrive.png",
            "tela_andando": "andar.jpeg", 
            "tela pe chuva": "andar_chuva.png",
            "tela_onibus": "bus.jpeg",
            "tela onibus chuva": "bus_chuva.png",
            "item_carregador": "carregador.png",
            "CEAGRI (Entrada)": "frente_ceaagri.jpeg",  
            "ceaagri chuva": "frente_ceagri_chuva.png",    
            "CEAGRI (Sala de Aula)": "sala_ceagri.jpeg",      
            "CEAGRI (PCs)": "pc.jpeg",       
            "Ed Física (Entrada)": "base_edf.jpeg", 
            "edf chuva": "base_edf_chuva.png",
            "Ed Física (Sala)": "sala_edf.jpeg",
            "A Praça": "praca_edf.jpeg",
            "praca chuva": "praca_edf_chuva.png",
            "vitoria": "sigaa.png",       
            "desmaio": "desmaio.jpeg",       
            "game_over": "ceu.jpeg",  
            "Prédio Central": "comeco.jpeg", 
            "predio chuva": "comeco_chuva.png"        
        }
        for nome_cenario, nome_arquivo in mapeamento_restante.items():
            caminho_completo = os.path.join(self.pasta_imagens, nome_arquivo)
            try:
                if os.path.exists(caminho_completo):
                    img_pil = Image.open(caminho_completo)
                    if "item_" in nome_cenario:
                        self.assets[nome_cenario] = ctk.CTkImage(light_image=img_pil, size=(45, 45))
                    elif "tela" in nome_cenario or nome_cenario in ["vitoria", "desmaio", "game_over"]:
                        self.assets[nome_cenario] = ctk.CTkImage(light_image=img_pil, size=(1220, 700))
                    else:
                        self.assets[nome_cenario] = ctk.CTkImage(light_image=img_pil, size=(900, 700))
                else:
                    self.assets[nome_cenario] = None
            except Exception as e:
                self.assets[nome_cenario] = None

    def obter_imagem(self, nome_cenario: str):
        """Retorna a imagem processada para o cenário solicitado, ou None se não estiver disponível"""
        return self.assets.get(nome_cenario, None)
