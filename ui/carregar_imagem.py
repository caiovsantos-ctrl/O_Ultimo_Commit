import os
from PIL import Image, ImageFilter
import customtkinter as ctk


class GerenciadorMidia:
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
        else:
            print("❌ Erro Crítico: 'frente_rural.jpeg' não foi encontrada na pasta imagens.")
        caminho_borrado = os.path.join(self.pasta_imagens, "borrado.png")
        if os.path.exists(caminho_borrado):
            self.assets["bg_borrado"] = ctk.CTkImage(light_image=Image.open(caminho_borrado), size=(1220, 700))
        elif img_base_pil:
            img_borrada_pil = img_base_pil.filter(ImageFilter.GaussianBlur(radius=15))
            self.assets["bg_borrado"] = ctk.CTkImage(light_image=img_borrada_pil, size=(1220, 700))
        mapeamento_restante = {
            "Parada de Ônibus": "espera.jpeg",
            "RU": "fila_ru.jpeg",
            "Lanchonete": "lanchonete.jpeg",
            "item_caderno": "caderno.png",
            "item_pendrive": "pendrive.png",
            "tela_andando": "andar.jpeg",       
            "tela_onibus": "bus.jpeg",
            "item_carregador": "carregador.png",
            "CEAGRI (Entrada)": "frente_ceaagri.jpeg",       
            "CEAGRI (Sala de Aula)": "sala_ceagri.jpeg",      
            "CEAGRI (PCs)": "pc.jpeg",       
            "Ed Física (Entrada)": "base_edf.jpeg",    
            "Ed Física (Sala)": "sala_edf.jpeg",
            "A Praça": "praca_edf.jpeg",
            "vitoria": "sigaa.png",       
            "desmaio": "desmaio.jpeg",       
            "game_over": "ceu.jpeg",  
            "Prédio Central": "comeco.jpeg"          
        }
        for nome_cenario, nome_arquivo in mapeamento_restante.items():
            caminho_completo = os.path.join(self.pasta_imagens, nome_arquivo)
            try:
                if os.path.exists(caminho_completo):
                    img_pil = Image.open(caminho_completo)
                    if "item_" in nome_cenario:
                        self.assets[nome_cenario] = ctk.CTkImage(light_image=img_pil, size=(45, 45))
                    elif "tela_" in nome_cenario or nome_cenario in ["vitoria", "desmaio", "game_over"]:
                        self.assets[nome_cenario] = ctk.CTkImage(light_image=img_pil, size=(1220, 700))
                    else:
                        self.assets[nome_cenario] = ctk.CTkImage(light_image=img_pil, size=(900, 700))
                else:
                    self.assets[nome_cenario] = None
            except Exception as e:
                self.assets[nome_cenario] = None

    def obter_imagem(self, nome_cenario: str):
        return self.assets.get(nome_cenario, None)
