import customtkinter as ctk


class PainelHUD:
    def __init__(self, frame_pai):
        self.parent = frame_pai
        self.lbl_tempo = None
        self.lbl_energia = None
        self.lbl_dinheiro = None
        self.lbl_mensagem = None
        self.lbl_local = None

    def formatar_tempo(self, minutos_totais) -> str:
        """Converte minutos brutos para o formato de relógio HH:MM"""
        horas = minutos_totais // 60
        minutos = minutos_totais % 60
        return f"{horas:02d}:{minutos:02d}"

    def construir_hud(self, jogador, local_atual):
        """Desenha os widgets na tela"""
        ctk.CTkLabel(self.parent, text="STATUS DO ALUNO", font=("Impact", 24), text_color="#ffffff").pack(pady=(15, 5))        
        self.lbl_tempo = ctk.CTkLabel(self.parent, text=f"⏰ Tempo: {self.formatar_tempo(jogador.tempo_minutos)} / 14:00", font=("Segoe UI", 14, "bold"), text_color="#e74c3c")
        self.lbl_tempo.pack(anchor="w", padx=20, pady=2)     
        self.lbl_energia = ctk.CTkLabel(self.parent, text=f"⚡ Energia: {jogador.energia}%", font=("Segoe UI", 14, "bold"), text_color="#f1c40f")
        self.lbl_energia.pack(anchor="w", padx=20, pady=2)      
        self.lbl_dinheiro = ctk.CTkLabel(self.parent, text=f"💰 Carteira: R$ {jogador.dinheiro:.2f}", font=("Segoe UI", 14, "bold"), text_color="#2ecc71")
        self.lbl_dinheiro.pack(anchor="w", padx=20, pady=2)
        self.lbl_mensagem = ctk.CTkLabel(self.parent, text="O que você vai fazer?", font=("Segoe UI", 12, "italic"), text_color="#f39c12", wraplength=280)
        self.lbl_mensagem.pack(pady=5, padx=10)      
        ctk.CTkLabel(self.parent, text="="*30, text_color="#555555").pack(pady=2)
        ctk.CTkLabel(self.parent, text="📍 Local Atual:", font=("Segoe UI", 12)).pack()
        ctk.CTkLabel(self.parent, text=local_atual, font=("Segoe UI", 16, "bold"), text_color="#3498db").pack(pady=(0, 10))
        
    def atualizar_textos(self, jogador, mensagem=""):
        """Atualiza a tela sem alterar as cores ou fontes originais"""
        if self.lbl_tempo:
            self.lbl_tempo.configure(text=f"⏰ Tempo: {self.formatar_tempo(jogador.tempo_minutos)} / 14:00")
        if self.lbl_energia:
            self.lbl_energia.configure(text=f"⚡ Energia: {jogador.energia}%")
        if self.lbl_dinheiro:
            self.lbl_dinheiro.configure(text=f"💰 Carteira: R$ {jogador.dinheiro:.2f}")
        if mensagem and self.lbl_mensagem:
            self.lbl_mensagem.configure(text=mensagem)
