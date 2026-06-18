import customtkinter as ctk
from PIL import Image
import random


class GerenciadorCenarios:
    """Gerencia os cenários do jogo, incluindo a exibição de itens camuflados e limpeza de itens anteriores"""
    def __init__(self):
        self.item_atual_tela = None

    def limpar_item_atual(self):
        """Remove o item visualmente se o jogador mudar de cenário ou coletá-lo"""
        if hasattr(self, 'item_atual_tela') and self.item_atual_tela:
            try:
                self.item_atual_tela.destroy()
            except Exception:
                pass
            self.item_atual_tela = None

    def spawnar_item_na_tela(self, frame_pai, imagem_fundo_ctk, nome_item, imagem_item, comando_coletar):
        """Posiciona um item de forma camuflada na tela, usando a imagem de fundo para criar um efeito de esconderijo"""
        x_aleatorio = random.randint(50, 750)
        y_aleatorio = random.randint(50, 550)
        if imagem_item:
            img_fundo_pil = (imagem_fundo_ctk._dark_image or imagem_fundo_ctk._light_image).convert("RGBA")
            img_item_pil = (imagem_item._dark_image or imagem_item._light_image).convert("RGBA")
            filtro = getattr(Image, 'Resampling', Image).LANCZOS
            img_fundo_pil = img_fundo_pil.resize((1220, 700), filtro)
            img_item_pil = img_item_pil.resize((45, 45), filtro)
            caixa_recorte = (x_aleatorio, y_aleatorio, x_aleatorio + 45, y_aleatorio + 45)
            fundo_recortado = img_fundo_pil.crop(caixa_recorte)
            fundo_recortado.paste(img_item_pil, (0, 0), img_item_pil)
            imagem_camuflada = ctk.CTkImage(light_image=fundo_recortado, dark_image=fundo_recortado, size=(45, 45))
            self.item_atual_tela = ctk.CTkLabel(
                frame_pai,
                image=imagem_camuflada,
                text="",
                width=45, height=45,
                fg_color="transparent", bg_color="transparent"
            )
            self.item_atual_tela.bind("<Button-1>", lambda event: comando_coletar(nome_item))
        else:
            self.item_atual_tela = ctk.CTkLabel(
                frame_pai, text="💾", font=("Segoe UI", 20),
                width=45, height=45,
                fg_color="transparent", bg_color="transparent"
            )
            self.item_atual_tela.bind("<Button-1>", lambda event: comando_coletar(nome_item))
        self.item_atual_tela.place(x=x_aleatorio, y=y_aleatorio)
