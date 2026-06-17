import customtkinter as ctk
from .hud import PainelHUD
from PIL import Image

class ConstrutorTelas:
    def __init__(self, janela_principal):
        # self.janela guarda a instância da sua Main (JogoBSI), dando acesso às mecânicas
        self.janela = janela_principal 
        self.label_fundo = None
        self.indice_texto = 0
        self.historia_texto = ""
        
        # Referências dos elementos do HUD para atualização em tempo real
        self.lbl_tempo = None
        self.lbl_energia = None
        self.lbl_dinheiro = None
        self.lbl_mensagem = None

    def limpar_janela(self):
        """Remove todos os elementos da janela para evitar sobreposição"""
        for widget in self.janela.winfo_children():
            widget.destroy()

    def formatar_tempo(self, minutos_totais) -> str:
        """Converte minutos brutos para o formato de relógio HH:MM"""
        horas = minutos_totais // 60
        minutos = minutos_totais % 60
        return f"{horas:02d}:{minutos:02d}"

    # -------------------------------------------------------------------------
    # FLUXO INICIAL: TÍTULO E INTRODUÇÃO
    # -------------------------------------------------------------------------

    def montar_tela_titulo(self, comando_entrar, img_fundo):
        self.limpar_janela()

        if img_fundo:
            self.label_fundo = ctk.CTkLabel(self.janela, image=img_fundo, text="", width=1220, height=700)
        else:
            self.label_fundo = ctk.CTkLabel(self.janela, text="[Erro: Imagem 'frente_rural' não encontrada]", text_color="orange")
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        # 🔔 CORREÇÃO: Vinculados ao 'self.label_fundo' e atualizado o texto dos itens
        self.tag_jogo = ctk.CTkLabel(self.label_fundo, text="🔍 PROCURA-SE: PEN DRIVE, CADERNO E CARREGADOR 🔍", font=("Segoe UI", 12, "bold"), text_color="#2ecc71")
        self.tag_jogo.place(relx=0.5, rely=0.15, anchor="center")

        self.titulo_jogo = ctk.CTkLabel(self.label_fundo, text="DEPOIS DO ÚLTIMO COMMIT", font=("Impact", 54), text_color="#ffffff")
        self.titulo_jogo.place(relx=0.5, rely=0.24, anchor="center")
        
        self.sub_jogo = ctk.CTkLabel(self.label_fundo, text="O Sumiço na Rural // Um Jogo de Achados e Perdidos", font=("Segoe UI", 16, "italic", "bold"), text_color="#bdc3c7")
        self.sub_jogo.place(relx=0.5, rely=0.33, anchor="center")

        # 🔔 CORREÇÃO: Vinculado ao 'self.label_fundo' e adicionado o .place() que faltava no final!
        self.btn_entrar = ctk.CTkButton(
            self.label_fundo, 
            text="ENTRAR NO CAMPUS", 
            font=("Segoe UI", 16, "bold"), 
            fg_color="#1e4620", 
            hover_color="#2e6f33", 
            border_color="#2ecc71", 
            border_width=1, 
            corner_radius=8, 
            width=280, 
            height=55, 
            command=comando_entrar
        )
        self.btn_entrar.place(relx=0.5, rely=0.6, anchor="center")

    def carregar_tela_introducao(self, img_fundo_borrada, historia_completa, comando_proximo):
        self.tag_jogo.destroy()
        self.titulo_jogo.destroy()
        self.sub_jogo.destroy()
        self.btn_entrar.destroy()
        
        if img_fundo_borrada:
            self.label_fundo.configure(image=img_fundo_borrada)
            
        self.caixa_dialogo = ctk.CTkFrame(self.janela, fg_color="#0a120b", border_color="#1e4620", border_width=3, corner_radius=12, width=840, height=240)
        self.caixa_dialogo.place(relx=0.5, rely=0.78, anchor="center")
        self.caixa_dialogo.pack_propagate(False)

        self.label_autor = ctk.CTkLabel(self.caixa_dialogo, text="✍️ DIÁRIO DE BORBO // STATUS: EM DESESPERO", font=("Consolas", 12, "bold"), text_color="#2ecc71")
        self.label_autor.place(x=30, y=18)

        self.label_historia = ctk.CTkLabel(self.caixa_dialogo, text="", font=("Segoe UI", 16, "bold"), text_color="#ffffff", wraplength=780, justify="left")
        self.label_historia.place(x=30, y=50)

        self.btn_proximo = ctk.CTkButton(self.caixa_dialogo, text="AVANÇAR ▶", font=("Segoe UI", 13, "bold"), fg_color="transparent", hover_color="#1e4620", text_color="#2ecc71", width=110, height=35, corner_radius=6, command=comando_proximo)
        self.btn_proximo.place_forget()

        self.historia_texto = historia_completa
        self.indice_texto = 0
        self.digitar_letra()

    def digitar_letra(self):
        if self.indice_texto < len(self.historia_texto):
            texto_atual = self.label_historia.cget("text")
            self.label_historia.configure(text=texto_atual + self.historia_texto[self.indice_texto])
            self.indice_texto += 1
            self.janela.after(18, self.digitar_letra)
        else:
            self.btn_proximo.place(x=700, y=185)

    # -------------------------------------------------------------------------
    # LAYOUT PRINCIPAL: GAMEPLAY E HUD (Sua função carregar_local restaurada)
    # -------------------------------------------------------------------------

    def desenhar_cenario_completo(self, local: str, item_do_local: str, foto_fundo, jogador, comando_mover_interno, comando_procurar):
        """Monta a divisão de tela original: Cenário (900x700) e Painel Lateral (320x700)"""
        self.limpar_janela()

        # 1. IMAGEM DO CENÁRIO (Lado Esquerdo - 900x700)
        if foto_fundo:
            self.label_fundo = ctk.CTkLabel(self.janela, width=900, height=700, image=foto_fundo, text="")
        else:
            self.label_fundo = ctk.CTkLabel(self.janela, width=900, height=700, text=f"[{local}]", font=("Segoe UI", 24))
        self.label_fundo.place(x=0, y=0)

        # 2. PAINEL LATERAL DE STATUS E EXPLORAÇÃO (Lado Direito - 320x700)
        self.painel_lateral = ctk.CTkFrame(self.janela, width=320, height=700, fg_color="#0a120b", corner_radius=0)
        self.painel_lateral.place(x=900, y=0)
        self.painel_lateral.pack_propagate(False)

        # Cabeçalho de Status (Obtendo dados do objeto jogador da Main)
        self.gerenciador_hud = PainelHUD(self.painel_lateral)
        self.gerenciador_hud.construir_hud(jogador, local)

        # AÇÃO UNIVERSAL: Procurar itens (Chama o gerenciador de buscas da main)
        # Se passar um item específico do local, usamos ele, senão passa o nome do local
        item_alvo = item_do_local if item_do_local else local
        # Certifique-se de passar 'comando_procurar' nos argumentos de desenhar_cenario_completo
        ctk.CTkButton(self.painel_lateral, text="🔍 Procurar Itens (-10m / -5⚡)", height=32, fg_color="#1e4620", hover_color="#2e6f33", command=comando_procurar).pack(pady=5, padx=20, fill="x")

        # SISTEMA DE COMIDA (Apenas em locais de alimentação)
        if "RU" in local:
            ctk.CTkButton(self.painel_lateral, text="🍔 Comer no RU (R$ 3.50 | +50 min)", fg_color="#2980b9", command=lambda: self.janela.comprar_comida("RU")).pack(pady=5, padx=20, fill="x")
        elif "Lanchonete" in local:
            ctk.CTkButton(self.painel_lateral, text="🍔 Comprar Salgado (R$ 7.00 | +10 min)", fg_color="#2980b9", command=lambda: self.janela.comprar_comida("Lanchonete")).pack(pady=5, padx=20, fill="x")

        # ---------------------------------------------------------------------
        # REQUISITO RESTRITO: EXPLORAÇÃO INTERNA (Mover-se dentro de prédios)
        # ---------------------------------------------------------------------
        if "CEAGRI" in local:
            ctk.CTkLabel(self.painel_lateral, text="🚪 Explorar CEAGRI 2:", font=("Segoe UI", 13, "bold"), text_color="#9b59b6").pack(pady=(10, 2))
            
            if local != "CEAGRI (Entrada)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Entrada", height=25, fg_color="#8e44ad", command=lambda: self.janela.mover_interno("CEAGRI (Entrada)")).pack(pady=2, padx=30, fill="x")
            if local != "CEAGRI (Sala de Aula)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Sala de Aula", height=25, fg_color="#8e44ad", command=lambda: self.janela.mover_interno("CEAGRI (Sala de Aula)")).pack(pady=2, padx=30, fill="x")
            if local != "CEAGRI (PCs)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Sala de PCs", height=25, fg_color="#8e44ad", command=lambda: self.janela.mover_interno("CEAGRI (PCs)")).pack(pady=2, padx=30, fill="x")

        elif "Ed Física" in local or "Praça" in local:
            ctk.CTkLabel(self.painel_lateral, text="🚪 Explorar Ed. Física:", font=("Segoe UI", 13, "bold"), text_color="#e67e22").pack(pady=(10, 2))
            
            if local != "Ed Física (Entrada)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Entrada", height=25, fg_color="#d35400", command=lambda: self.janela.mover_interno("Ed Física (Entrada)")).pack(pady=2, padx=30, fill="x")
            if local != "Ed Física (Sala)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Sala de Ed Física", height=25, fg_color="#d35400", command=lambda: self.janela.    mover_interno("Ed Física (Sala)")).pack(pady=2, padx=30, fill="x")
            if local != "A Praça":
                ctk.CTkButton(self.painel_lateral, text="Ir para a Praça", height=25, fg_color="#d35400", command=lambda: self.janela.mover_interno("A Praça")).pack(pady=2, padx=30, fill="x")

        # ---------------------------------------------------------------------
        # REQUISITO RESTRITO: VIAGEM EXTERNA (Trocar de Prédio)
        # ---------------------------------------------------------------------
        ctk.CTkLabel(self.painel_lateral, text="Viajar para outro Prédio:", font=("Segoe UI", 13, "bold")).pack(pady=(10, 2))
        
        locais_externos = ["RU", "Prédio Central", "CEAGRI (Entrada)", "Ed Física (Entrada)", "Lanchonete", "Parada de Ônibus"]

        for loc_nome in locais_externos:
            # Lógica para não exibir o próprio prédio onde o jogador está
            predio_atual = local.split(" ")[0]
            predio_destino = loc_nome.split(" ")[0]
            
            if predio_atual != predio_destino and local != loc_nome:
                frame_loc = ctk.CTkFrame(self.painel_lateral, fg_color="transparent")
                frame_loc.pack(pady=2, fill="x", padx=10)
                
                nome_formatado = loc_nome.replace(" (Entrada)", "").replace("Parada de ", "")
                ctk.CTkLabel(frame_loc, text=f"{nome_formatado}:", font=("Segoe UI", 11, "bold"), width=75, anchor="w").pack(side="left")
                
                # Vincula as ações de viagem da sua main passando o destino e o meio correto
                ctk.CTkButton(frame_loc, text="🚶 A pé", width=50, height=22, font=("Segoe UI", 10), command=lambda n=loc_nome: self.janela.viajar(n, "pe")).pack(side="right", padx=2)
                ctk.CTkButton(frame_loc, text="🚌 Ônibus", width=50, height=22, font=("Segoe UI", 10), fg_color="#27ae60", command=lambda n=loc_nome: self.janela.viajar(n, "onibus")).pack(side="right", padx=2)
                if loc_nome == "RU" and ("Lanchonete" in local or "CEAGRI (Entrada)" in local):
                    ctk.CTkButton(
                        frame_loc, 
                        text="🏃 Atalho", 
                        width=45, 
                        height=22, 
                        font=("Segoe UI", 10, "bold"), 
                        fg_color="#c0392b", 
                        hover_color="#962d22",
                        command=self.janela.processar_atalho # Chamando a nova função na main
                    ).pack(side="right", padx=2)
    