import customtkinter as ctk
import random

class GerenciadorCenarios:
    def __init__(self):
        self.item_atual_tela = None

    def limpar_item_atual(self):
        """Remove o item do cenário se ele existir"""
        if self.item_atual_tela:
            try:
                self.item_atual_tela.destroy()
            except Exception:
                pass
            self.item_atual_tela = None

    def spawnar_item_na_tela(self, label_fundo, imagem_item, comando_coletar):
        """Gera o item usando as estéticas exatas originais (transparente, hover=False)"""
        self.limpar_item_atual()

        x_aleatorio = random.randint(50, 750)
        y_aleatorio = random.randint(50, 550)

        if imagem_item:
            self.item_atual_tela = ctk.CTkButton(
                label_fundo, 
                image=imagem_item, 
                text=" ", 
                font=("Segoe UI", 1),
                width=45,
                height=45,
                corner_radius=0,
                fg_color="transparent", 
                hover=False, 
                command=comando_coletar
            )
        else:
            self.item_atual_tela = ctk.CTkButton(
                label_fundo, 
                text="💾", 
                font=("Segoe UI", 20),
                width=45,
                height=45,
                corner_radius=0,
                fg_color="transparent", 
                hover=False, 
                command=comando_coletar
            )

        self.item_atual_tela.place(x=x_aleatorio, y=y_aleatorio)