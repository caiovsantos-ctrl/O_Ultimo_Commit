import customtkinter as ctk
from PIL import Image, ImageFilter
import os, random

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class JogoBSI:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Depois do Último Commit: O Sumiço na Rural")
        self.janela.geometry("1220x700")
        self.janela.resizable(False, False)
        
        # Status do Jogador
        self.energia = 100
        self.dinheiro = 15.00
        self.tempo_minutos = 420
        self.prazo_final = 840
        self.itens_encontrados = []

        self.historia = (
            "Quarta-feira, 07:00 da manhã.\n\n"
            "Passei a madrugada inteira codando o projeto de Princípios de Programação. "
            "Sobrevivi à base de puro café do RU, e a minha bateria já está na metade.\n\n"
            "Peguei o BRT lotado espremido na porta. Quando finalmente desci na frente da UFRPE, o desespero bateu: "
            "o zíper da minha mochila estourou. Meu Pen Drive com o código, meu cartão VEM e minha Ficha do RU "
            "caíram em algum lugar do campus.\n\n"
            "O professor no Departamento de Computação (DC) avisou: o prazo final é às 14h em ponto. "
            "Se eu não recuperar tudo e chegar lá a tempo... é Game Over."
        )
        self.indice_texto = 0
        
        self.caminho_imagem = os.path.join("imagens", "base_rural.jpeg")
        self.pre_carregar_imagens()
        self.montar_tela_titulo()

    def carregar_imagem_segura(self, nome_arquivo, tamanho=(900, 700)):
        """Agora aceita tamanhos diferentes para as telas cheias ou telas divididas"""
        try:
            caminho = os.path.join("imagens", nome_arquivo)
            img = Image.open(caminho)
            return ctk.CTkImage(light_image=img, dark_image=img, size=tamanho)
        except FileNotFoundError:
            print(f"⚠️ Aviso: O arquivo '{nome_arquivo}' não foi encontrado na pasta 'imagens'.")
            return None

    def pre_carregar_imagens(self):
        try:
            self.img_original = Image.open(self.caminho_imagem)
            # A introdução ocupa a nova janela inteira (1220x700)
            self.bg_limpo = ctk.CTkImage(light_image=self.img_original, dark_image=self.img_original, size=(1220, 700))
            img_borrada = self.img_original.filter(ImageFilter.GaussianBlur(radius=6))
            self.bg_borrado = ctk.CTkImage(light_image=img_borrada, dark_image=img_borrada, size=(1220, 700))
        except FileNotFoundError:
            self.bg_limpo = None
            self.bg_borrado = None

        # FOTOS DOS LOCAIS DO JOGO (Ficam apenas do lado esquerdo = 900x700)
        self.img_ru = self.carregar_imagem_segura("ru.jpeg", (900, 700))
        self.img_lanchonete = self.carregar_imagem_segura("lanchonete.jpeg", (900, 700))
        self.img_onibus_local = self.carregar_imagem_segura("esperando.jpeg", (900, 700))
        
        # FOTOS DO CEAGRI 2
        self.img_ceagri = self.carregar_imagem_segura("ceagri.jpeg", (900, 700))
        self.img_ceagri_aula = self.carregar_imagem_segura("aula.jpeg", (900, 700))
        self.img_ceagri_pc = self.carregar_imagem_segura("computador.jpeg", (900, 700))
        
        # FOTOS DA EDUCAÇÃO FÍSICA
        self.img_edf_entrada = self.carregar_imagem_segura("frente_edf.jpeg", (900, 700))
        self.img_edf_sala = self.carregar_imagem_segura("corporal.jpeg", (900, 700))
        self.img_edf_praca = self.carregar_imagem_segura("praca.jpeg", (900, 700))
        
        # FOTOS DE TRANSIÇÃO E FINAIS (Ocupam a janela inteira = 1220x700)
        self.img_viagem_onibus = self.carregar_imagem_segura("onibus.jpeg", (1220, 700))
        self.img_viagem_pe = self.carregar_imagem_segura("andando.jpeg", (1220, 700))
        self.img_desmaio = self.carregar_imagem_segura("desmaio.jpeg", (1220, 700))
        self.img_game_over = self.carregar_imagem_segura("ceu.jpeg", (1220, 700))
        self.img_vitoria = self.carregar_imagem_segura("sigaa.png", (1220, 700))

        # SOLUÇÃO: Usamos apenas a sua função segura (que já busca na pasta "imagens")
        # Definimos o tamanho (45, 45) para ficar perfeito no clique do botão escondido
        self.img_item_pendrive = self.carregar_imagem_segura("pendrive.png", (45, 45))
        self.img_item_carregador = self.carregar_imagem_segura("carregador.png", (45, 45))
        self.img_item_caderno = self.carregar_imagem_segura("caderno.png", (45, 45))

        self.item_atual_tela = None
        

    def montar_tela_titulo(self):
        if self.bg_limpo:
            self.label_fundo = ctk.CTkLabel(self.janela, image=self.bg_limpo, text="")
        else:
            self.label_fundo = ctk.CTkLabel(self.janela, text="[Erro: Imagem principal não encontrada]", text_color="orange")
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        self.tag_jogo = ctk.CTkLabel(self.janela, text="🔍 PROCURA-SE: PEN DRIVE, VEM E FICHA DO RU 🔍", font=("Segoe UI", 12, "bold"), text_color="#2ecc71")
        self.tag_jogo.place(relx=0.5, rely=0.15, anchor="center")

        self.titulo_jogo = ctk.CTkLabel(self.janela, text="DEPOIS DO ÚLTIMO COMMIT", font=("Impact", 54), text_color="#ffffff")
        self.titulo_jogo.place(relx=0.5, rely=0.23, anchor="center")
        
        self.sub_jogo = ctk.CTkLabel(self.janela, text="O Sumiço na Rural // Um Jogo de Achados e Perdidos", font=("Segoe UI", 16, "italic", "bold"), text_color="#bdc3c7")
        self.sub_jogo.place(relx=0.5, rely=0.31, anchor="center")

        self.btn_entrar = ctk.CTkButton(self.janela, text="ENTRAR NO CAMPUS", font=("Segoe UI", 16, "bold"), fg_color="#1e4620", hover_color="#2e6f33", border_color="#2ecc71", border_width=1, corner_radius=8, width=280, height=55, command=self.carregar_tela_introducao)
        self.btn_entrar.place(relx=0.5, rely=0.52, anchor="center")

    def carregar_tela_introducao(self):
        self.tag_jogo.destroy()
        self.titulo_jogo.destroy()
        self.sub_jogo.destroy()
        self.btn_entrar.destroy()
        
        if self.bg_borrado:
            self.label_fundo.configure(image=self.bg_borrado)
            
        self.caixa_dialogo = ctk.CTkFrame(self.janela, fg_color="#0a120b", border_color="#1e4620", border_width=3, corner_radius=12, width=840, height=240)
        self.caixa_dialogo.place(relx=0.5, rely=0.78, anchor="center")
        self.caixa_dialogo.pack_propagate(False)

        self.label_autor = ctk.CTkLabel(self.caixa_dialogo, text="✍️ DIÁRIO DE BORBO // STATUS: EM DESESPERO", font=("Consolas", 12, "bold"), text_color="#2ecc71")
        self.label_autor.place(x=30, y=18)

        self.label_historia = ctk.CTkLabel(self.caixa_dialogo, text="", font=("Segoe UI", 16, "bold"), text_color="#ffffff", wraplength=780, justify="left")
        self.label_historia.place(x=30, y=50)

        self.btn_proximo = ctk.CTkButton(self.caixa_dialogo, text="AVANÇAR ▶", font=("Segoe UI", 13, "bold"), fg_color="transparent", hover_color="#1e4620", text_color="#2ecc71", width=110, height=35, corner_radius=6, command=self.proxima_fase)
        self.btn_proximo.place_forget()

        self.digitar_letra()

    def digitar_letra(self):
        if self.indice_texto < len(self.historia):
            texto_atual = self.label_historia.cget("text")
            self.label_historia.configure(text=texto_atual + self.historia[self.indice_texto])
            self.indice_texto += 1
            self.janela.after(18, self.digitar_letra)
        else:
            self.btn_proximo.place(x=700, y=185)

    def formatar_tempo(self, minutos_totais):
        horas = minutos_totais // 60
        minutos = minutos_totais % 60
        return f"{horas:02d}:{minutos:02d}"

    def proxima_fase(self):
        self.carregar_local("Entrada da UFRPE", self.bg_limpo)
        
    def carregar_local(self, nome_local, imagem_local):
        if hasattr(self, 'item_atual_tela') and self.item_atual_tela:
            self.item_atual_tela.destroy()
            self.item_atual_tela = None

        # Limpa os widgets antigos da janela
        for widget in self.janela.winfo_children():
            widget.destroy()
        for widget in self.janela.winfo_children():
            widget.destroy()

        if imagem_local:
            self.label_fundo = ctk.CTkLabel(self.janela, width=900, height=700, image=imagem_local, text="")
        else:
            self.label_fundo = ctk.CTkLabel(self.janela, width=900, height=700, text=f"[{nome_local}]", font=("Segoe UI", 24))
            
        self.label_fundo.place(x=0, y=0)

        self.painel_lateral = ctk.CTkFrame(self.janela, width=320, height=700, fg_color="#0a120b", corner_radius=0)
        self.painel_lateral.place(x=900, y=0)
        self.painel_lateral.pack_propagate(False)

        # CABEÇALHO DO PAINEL (Status)
        ctk.CTkLabel(self.painel_lateral, text="STATUS DO ALUNO", font=("Impact", 24), text_color="#ffffff").pack(pady=(15, 5))
        self.lbl_tempo = ctk.CTkLabel(self.painel_lateral, text=f"⏰ Tempo: {self.formatar_tempo(self.tempo_minutos)} / 14:00", font=("Segoe UI", 14, "bold"), text_color="#e74c3c")
        self.lbl_tempo.pack(anchor="w", padx=20, pady=2)
        self.lbl_energia = ctk.CTkLabel(self.painel_lateral, text=f"⚡ Energia: {self.energia}%", font=("Segoe UI", 14, "bold"), text_color="#f1c40f")
        self.lbl_energia.pack(anchor="w", padx=20, pady=2)
        self.lbl_dinheiro = ctk.CTkLabel(self.painel_lateral, text=f"💰 Carteira: R$ {self.dinheiro:.2f}", font=("Segoe UI", 14, "bold"), text_color="#2ecc71")
        self.lbl_dinheiro.pack(anchor="w", padx=20, pady=2)

        self.lbl_mensagem = ctk.CTkLabel(self.painel_lateral, text="O que você vai fazer?", font=("Segoe UI", 12, "italic"), text_color="#f39c12", wraplength=280)
        self.lbl_mensagem.pack(pady=5, padx=10)
        ctk.CTkLabel(self.painel_lateral, text="="*30, text_color="#555555").pack(pady=2)
        
        # NOME DO LOCAL ATUAL
        ctk.CTkLabel(self.painel_lateral, text="📍 Local Atual:", font=("Segoe UI", 12)).pack()
        ctk.CTkLabel(self.painel_lateral, text=nome_local, font=("Segoe UI", 16, "bold"), text_color="#3498db").pack(pady=(0, 10))

        # AÇÃO UNIVERSAL: Procurar
        ctk.CTkButton(self.painel_lateral, text="🔍 Procurar Itens (-15m / -10⚡)", height=32, fg_color="#1e4620", hover_color="#2e6f33", command=self.acao_procurar).pack(pady=5, padx=20, fill="x")

        # COMIDA (Só aparece no RU e Lanchonete)
        if "RU" in nome_local:
            ctk.CTkButton(self.painel_lateral, text="🍔 Comer no RU (R$ 3.50 | +30 min)", fg_color="#2980b9", command=lambda: self.comprar_comida("RU")).pack(pady=5, padx=20, fill="x")
        elif "Lanchonete" in nome_local:
            ctk.CTkButton(self.painel_lateral, text="🍔 Comprar Salgado (R$ 7.00 | +10 min)", fg_color="#2980b9", command=lambda: self.comprar_comida("Lanchonete")).pack(pady=5, padx=20, fill="x")

        # ==========================================================
        # MENU DE EXPLORAÇÃO INTERNA (Salas do mesmo prédio)
        # ==========================================================
        if "CEAGRI" in nome_local:
            ctk.CTkLabel(self.painel_lateral, text="🚪 Explorar CEAGRI 2:", font=("Segoe UI", 13, "bold"), text_color="#9b59b6").pack(pady=(10, 2))
            
            if nome_local != "CEAGRI (Entrada)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Entrada", height=25, fg_color="#8e44ad", command=lambda: self.mover_interno("CEAGRI (Entrada)", self.img_ceagri)).pack(pady=2, padx=30, fill="x")
            if nome_local != "CEAGRI (Sala de Aula)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Sala de Aula", height=25, fg_color="#8e44ad", command=lambda: self.mover_interno("CEAGRI (Sala de Aula)", self.img_ceagri_aula)).pack(pady=2, padx=30, fill="x")
            if nome_local != "CEAGRI (PCs)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Sala de PCs", height=25, fg_color="#8e44ad", command=lambda: self.mover_interno("CEAGRI (PCs)", self.img_ceagri_pc)).pack(pady=2, padx=30, fill="x")

        elif "Ed Física" in nome_local or "Praça" in nome_local:
            ctk.CTkLabel(self.painel_lateral, text="🚪 Explorar Ed. Física:", font=("Segoe UI", 13, "bold"), text_color="#e67e22").pack(pady=(10, 2))
            
            if nome_local != "Ed Física (Entrada)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Entrada", height=25, fg_color="#d35400", command=lambda: self.mover_interno("Ed Física (Entrada)", self.img_edf_entrada)).pack(pady=2, padx=30, fill="x")
            if nome_local != "Ed Física (Sala)":
                ctk.CTkButton(self.painel_lateral, text="Ir para Sala de Ed Física", height=25, fg_color="#d35400", command=lambda: self.mover_interno("Ed Física (Sala)", self.img_edf_sala)).pack(pady=2, padx=30, fill="x")
            if nome_local != "A Praça":
                ctk.CTkButton(self.painel_lateral, text="Ir para a Praça", height=25, fg_color="#d35400", command=lambda: self.mover_interno("A Praça", self.img_edf_praca)).pack(pady=2, padx=30, fill="x")

        # ==========================================================
        # MENU DE VIAGEM EXTERNA (Mudar de Prédio)
        # ==========================================================
        ctk.CTkLabel(self.painel_lateral, text="Viajar para outro Prédio:", font=("Segoe UI", 13, "bold")).pack(pady=(10, 2))
        
        # A viagem externa te leva sempre para a ENTRADA dos lugares
        locais = [
            ("RU", self.img_ru),
            ("CEAGRI (Entrada)", self.img_ceagri),
            ("Ed Física (Entrada)", self.img_edf_entrada),
            ("Lanchonete", self.img_lanchonete),
            ("Parada de Ônibus", self.img_onibus_local)
        ]

        # Para cada local externo, verifica se você já não está nele/naquele prédio
        for loc_nome, loc_img in locais:
            # Lógica para não mostrar o botão "Viajar pro CEAGRI" se você já está dentro de uma sala do CEAGRI
            predio_atual = nome_local.split(" ")[0] # Pega a primeira palavra (ex: "CEAGRI", "Ed", "RU")
            predio_destino = loc_nome.split(" ")[0]
            
            if predio_atual != predio_destino and nome_local != loc_nome:
                frame_loc = ctk.CTkFrame(self.painel_lateral, fg_color="transparent")
                frame_loc.pack(pady=2, fill="x", padx=10)
                
                # Exibe o nome do lugar formatado para caber no menu
                nome_formatado = loc_nome.replace(" (Entrada)", "").replace("Parada de ", "")
                ctk.CTkLabel(frame_loc, text=f"{nome_formatado}:", font=("Segoe UI", 11, "bold"), width=75, anchor="w").pack(side="left")
                
                ctk.CTkButton(frame_loc, text="🚶 A pé", width=50, height=22, font=("Segoe UI", 10), command=lambda n=loc_nome, i=loc_img: self.viajar(n, i, "A Pé")).pack(side="left", padx=2)
                ctk.CTkButton(frame_loc, text="🚌 Bus", width=50, height=22, font=("Segoe UI", 10), fg_color="#27ae60", command=lambda n=loc_nome, i=loc_img: self.viajar(n, i, "Ônibus")).pack(side="left", padx=2)

    def acao_procurar(self):
        """Gasta tempo/energia e tenta fazer um item aparecer na foto"""
        self.tempo_minutos += 15
        self.energia -= 10
        
        # 1. Lista com todos os itens do jogo
        todos_itens = [
            ("Pen Drive com o Código", self.img_item_pendrive), 
            ("Carregador do Notebook", self.img_item_carregador), 
            ("Caderno de Anotações", self.img_item_caderno)
        ]
        
        # 2. O SEGREDO: Cria uma lista só com os itens que o jogador AINDA NÃO TEM
        itens_possiveis = [item for item in todos_itens if item[0] not in self.itens_encontrados]
        
        # Se ele já achou os 3 itens do jogo, avisa que acabou
        if len(itens_possiveis) == 0:
            msg = "Você procurou por todo lado, mas já pegou tudo de importante que havia para achar!"
            if not self.verificar_game_over():
                self.atualizar_hud(msg)
            return

        # 3. 70% de chance de o item aparecer na foto para ele clicar
        import random
        if random.random() < 0.70:
            item_sorteado, imagem_sorteada = random.choice(itens_possiveis)
            
            self.spawnar_item_na_tela(item_sorteado, imagem_sorteada)
            msg = f"Você examinou o local... Há algo que parece ser o {item_sorteado} escondido na foto! Clique nele!"
        else:
            msg = "Você procurou debaixo das mesas, mas não viu nada de útil desta vez."

        if not self.verificar_game_over():
            self.atualizar_hud(msg)

    def viajar(self, destino, imagem_destino, transporte):
        if transporte == "A Pé":
            self.tempo_minutos += 20
            self.energia -= 15
   
            # 30% de chance do Saguim aparecer na caminhada
            if random.random() < 0.30: 
                self.mostrar_evento_saguim(destino, imagem_destino)
            else:
                msg = f"Você caminhou sob o sol escaldante até {destino}. Cansativo demais... (-15⚡, -20⏰)"
                self.mostrar_tela_transicao_pe(destino, imagem_destino, msg)
        
        elif transporte == "Ônibus":
            if self.dinheiro >= 2.25:
                self.dinheiro -= 2.25
                self.energia -= 5
                tempo_onibus = random.choice([5, 10, 20, 30]) 
                self.tempo_minutos += tempo_onibus
                msg = f"Foi de Bus! Ele demorou {tempo_onibus} minutos para passar. (-5⚡, -R$2.25)"
                
                self.mostrar_tela_transicao_onibus(destino, imagem_destino, msg)
            else:
                self.atualizar_hud("Sem dinheiro para o ônibus! Você vai ter que ir a pé.")

    def mover_interno(self, destino, imagem_destino):
        """Mover-se dentro do mesmo prédio"""
        self.tempo_minutos += 2  
        self.energia -= 1        
        
        # 30% de chance de topar com um Veterano se estiver no CEAGRI
        if "CEAGRI" in destino and random.random() < 0.30:
            self.mostrar_evento_veterano(destino, imagem_destino)
        else:
            msg = f"Você andou pelos corredores até: {destino}."
            if not self.verificar_game_over():
                self.carregar_local(destino, imagem_destino)
                self.atualizar_hud(msg)

    def mostrar_tela_transicao_onibus(self, destino, imagem_destino, msg):
        """Tela de transição para o Ônibus (Corrigida)"""
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        if self.img_viagem_onibus:
            self.label_fundo = ctk.CTkLabel(self.janela, image=self.img_viagem_onibus, text="")
        else:
            self.label_fundo = ctk.CTkLabel(self.janela, text="[🚌 Dentro do Ônibus...]", font=("Segoe UI", 24))
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        
        # CORREÇÃO: width e height passados dentro do CTkFrame!
        caixa = ctk.CTkFrame(self.janela, width=550, height=220, fg_color="#0a120b", border_color="#27ae60", border_width=2, corner_radius=12)
        caixa.place(relx=0.5, rely=0.5, anchor="center")
        caixa.pack_propagate(False) # Mantém o tamanho fixo da caixa
        
        ctk.CTkLabel(caixa, text="🚌 COLETIVO EM MOVIMENTO", font=("Impact", 28), text_color="#2ecc71").pack(pady=(15, 5))
        ctk.CTkLabel(caixa, text=msg, font=("Segoe UI", 14, "bold"), text_color="#ffffff", wraplength=500).pack(pady=10)
        
        ctk.CTkButton(caixa, text="DESCER NO PONTO ▶", font=("Segoe UI", 13, "bold"), fg_color="#27ae60", hover_color="#218c4e", command=lambda: self.concluir_viagem(destino, imagem_destino)).pack(pady=10)

    def mostrar_tela_transicao_pe(self, destino, imagem_destino, msg):
        """Tela de transição para Caminhada a Pé (Corrigida)"""
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        if self.img_viagem_pe:
            self.label_fundo = ctk.CTkLabel(self.janela, image=self.img_viagem_pe, text="")
        else:
            self.label_fundo = ctk.CTkLabel(self.janela, text="[🚶 Caminhando pelo campus...]", font=("Segoe UI", 24))
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        
        # CORREÇÃO: width e height passados dentro do CTkFrame!
        caixa = ctk.CTkFrame(self.janela, width=550, height=220, fg_color="#0a120b", border_color="#e67e22", border_width=2, corner_radius=12)
        caixa.place(relx=0.5, rely=0.5, anchor="center")
        caixa.pack_propagate(False) # Mantém o tamanho fixo da caixa
        
        ctk.CTkLabel(caixa, text="🚶 CAMINHANDO SOB O SOL...", font=("Impact", 28), text_color="#e67e22").pack(pady=(15, 5))
        ctk.CTkLabel(caixa, text=msg, font=("Segoe UI", 14, "bold"), text_color="#ffffff", wraplength=500).pack(pady=10)
        
        ctk.CTkButton(caixa, text="CHEGAR AO DESTINO ▶", font=("Segoe UI", 13, "bold"), fg_color="#d35400", hover_color="#a84300", command=lambda: self.concluir_viagem(destino, imagem_destino)).pack(pady=10)

    def concluir_viagem(self, destino, imagem_destino):
        """Chama a verificação final: se ele sobreviveu à viagem, carrega o local."""
        if not self.verificar_game_over():
            self.carregar_local(destino, imagem_destino)

    def comprar_comida(self, tipo):
        if tipo == "RU":
            if self.dinheiro >= 3.50:
                self.dinheiro -= 3.50
                self.tempo_minutos += 30 
                self.energia = min(100, self.energia + 50) 
                self.atualizar_hud("Você mofou na fila do RU, mas comeu! (+50⚡, -30⏰)")
            else:
                self.atualizar_hud("Sem dinheiro até para o RU!")
        elif tipo == "Lanchonete":
            if self.dinheiro >= 7.00:
                self.dinheiro -= 7.00
                self.tempo_minutos += 10 
                self.energia = min(100, self.energia + 40)
                self.atualizar_hud("Salgado caro da Lanchonete, mas foi rápido! (+40⚡, -10⏰)")
            else:
                self.atualizar_hud("Dinheiro insuficiente para a lanchonete!")
        self.verificar_game_over()

    def atualizar_hud(self, mensagem=''):
        try:
            self.lbl_tempo.configure(text=f"⏰ Tempo: {self.formatar_tempo(self.tempo_minutos)} / 14:00")
            self.lbl_energia.configure(text=f"⚡ Energia: {self.energia}%")
            self.lbl_dinheiro.configure(text=f"💰 Carteira: R$ {self.dinheiro:.2f}")
            if mensagem:
                self.lbl_mensagem.configure(text=mensagem)
        except:
            pass

    def mostrar_evento_saguim(self, destino, imagem_destino):
        """O jogador encontra o Saguim e faz uma escolha rápida"""
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        self.label_fundo = ctk.CTkLabel(self.janela, width=1220, height=700, image=self.img_viagem_pe, text="")
        self.label_fundo.place(x=0, y=0)
        
        caixa = ctk.CTkFrame(self.janela, width=600, height=280, fg_color="#0a120b", border_color="#f1c40f", border_width=3, corner_radius=12)
        caixa.place(relx=0.5, rely=0.5, anchor="center")
        caixa.pack_propagate(False)
        
        ctk.CTkLabel(caixa, text="🐒 UM SAGUIM BLOQUEIA O CAMINHO!", font=("Impact", 28), text_color="#f1c40f").pack(pady=(20, 10))
        ctk.CTkLabel(caixa, text="Ele cruza os braços e começa a pular na sua frente querendo atenção. Como você reage?", font=("Segoe UI", 15, "bold"), text_color="white", wraplength=550).pack(pady=10)
        
        # Opção 1: Gasta tempo para despistar com calma
        ctk.CTkButton(caixa, text="Despistar com paciência (-15⏰)", font=("Segoe UI", 14, "bold"), fg_color="#2980b9", height=40, command=lambda: self.resolver_evento_saguim("tempo", destino, imagem_destino)).pack(pady=5)
        
        # Opção 2: Passa correndo e perde energia
        ctk.CTkButton(caixa, text="Passar correndo (-15⚡)", font=("Segoe UI", 14, "bold"), fg_color="#e74c3c", height=40, command=lambda: self.resolver_evento_saguim("energia", destino, imagem_destino)).pack(pady=5)

    def resolver_evento_saguim(self, escolha, destino, imagem_destino):
        if escolha == "tempo":
            self.tempo_minutos += 15
            msg = "Você perdeu um bom tempo brincando e despistando o saguim, mas ele te deixou em paz. (-15⏰)"
        else:
            self.energia -= 15
            msg = "Você correu com tudo! O saguim te deu um susto e você ficou exausto. (-15⚡)"
            
        self.mostrar_tela_transicao_pe(destino, imagem_destino, msg)

    def mostrar_evento_veterano(self, destino, imagem_destino):
        """O jogador encontra o Veterano no CEAGRI"""
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        self.label_fundo = ctk.CTkLabel(self.janela, width=1220, height=700, image=imagem_destino, text="")
        self.label_fundo.place(x=0, y=0)
        
        caixa = ctk.CTkFrame(self.janela, width=600, height=280, fg_color="#0a120b", border_color="#9b59b6", border_width=3, corner_radius=12)
        caixa.place(relx=0.5, rely=0.5, anchor="center")
        caixa.pack_propagate(False)
        
        ctk.CTkLabel(caixa, text="👨‍💻 VETERANO NO CORREDOR", font=("Impact", 28), text_color="#9b59b6").pack(pady=(20, 10))
        ctk.CTkLabel(caixa, text="Um veterano do curso te para: 'E aí calouro! Quer ouvir umas verdades sobre a prova de programação?'", font=("Segoe UI", 15, "bold"), text_color="white", wraplength=550).pack(pady=10)
        
        # Opção 1: Ouve e gasta tempo
        ctk.CTkButton(caixa, text="Ouvir as 'dicas' (-20⏰)", font=("Segoe UI", 14, "bold"), fg_color="#2980b9", height=40, command=lambda: self.resolver_evento_veterano("ouvir", destino, imagem_destino)).pack(pady=5)
        
        # Opção 2: Foge e perde energia (estresse)
        ctk.CTkButton(caixa, text="Ignorar e sair andando (-10⚡)", font=("Segoe UI", 14, "bold"), fg_color="#e74c3c", height=40, command=lambda: self.resolver_evento_veterano("ignorar", destino, imagem_destino)).pack(pady=5)

    def resolver_evento_veterano(self, escolha, destino, imagem_destino):
        if escolha == "ouvir":
            self.tempo_minutos += 20
            msg = "Ele falou por 20 minutos seguidos sem respirar... Pelo menos você descobriu que não cai Python na prova! (-20⏰)"
        else:
            self.energia -= 10
            msg = "Você virou as costas. Ele gritou 'VOCÊ VAI REPROVAR!', o que te deixou super estressado... (-10⚡)"
            
        # Vai direto para o local depois do evento interno
        if not self.verificar_game_over():
            self.carregar_local(destino, imagem_destino)
            self.atualizar_hud(msg)    

    def spawnar_item_na_tela(self, nome_item, imagem_item):
        """Gera o item usando um botão invisível com hover desativado corretamente"""
        if hasattr(self, 'item_atual_tela') and self.item_atual_tela:
            try:
                self.item_atual_tela.destroy()
            except Exception:
                pass
            self.item_atual_tela = None

        import random
        x_aleatorio = random.randint(50, 750)
        y_aleatorio = random.randint(50, 550)

        # CORREÇÃO: Removemos o hover_color="transparent" e colocamos hover=False!
        # Mantemos text=" " e a font pequena para evitar o bug interno do _font.
        if imagem_item:
            self.item_atual_tela = ctk.CTkButton(
                self.label_fundo, 
                image=imagem_item, 
                text=" ", 
                font=("Segoe UI", 1),
                width=45,
                height=45,
                corner_radius=0,
                fg_color="transparent", 
                hover=False, # DESLIGA o efeito do mouse sem dar erro no CustomTkinter!
                command=lambda: self.item_encontrado(nome_item)
            )
        else:
            self.item_atual_tela = ctk.CTkButton(
                self.label_fundo, 
                text="💾", 
                font=("Segoe UI", 20),
                width=45,
                height=45,
                corner_radius=0,
                fg_color="transparent", 
                hover=False, # DESLIGA o efeito do mouse aqui também
                command=lambda: self.item_encontrado(nome_item)
            )

        self.item_atual_tela.place(x=x_aleatorio, y=y_aleatorio)

    def item_encontrado(self, nome_item):
        """Função chamada quando o jogador clica com sucesso no item escondido"""
        if self.item_atual_tela:
            self.item_atual_tela.destroy()
            self.item_atual_tela = None

        # Adiciona o item à lista do jogador
        if hasattr(self, 'itens_encontrados'):
            if nome_item not in self.itens_encontrados:
                self.itens_encontrados.append(nome_item)
        
        # VERIFICA A VITÓRIA (Se ele pegou os 3 itens)
        if len(self.itens_encontrados) >= 3:
            # Chama a tela do SIGAA e encerra a jogabilidade!
            self.final_vitoria()
        else:
            # Se ainda faltam itens, o jogo segue normalmente
            msg_sucesso = f"🎉 INCRÍVEL! Você encontrou: {nome_item}! ({len(self.itens_encontrados)}/3 itens recuperados)"
            self.atualizar_hud(msg_sucesso)

    def verificar_game_over(self):
        if self.energia <= 0:
            self.mostrar_tela_desmaio()
            return True
        elif self.tempo_minutos >= self.prazo_final:
            self.mostrar_game_over("O PRAZO ACABOU! O PROFESSOR FECHOU O SISTEMA.", self.img_game_over)
            return True
        return False

    def mostrar_tela_desmaio(self):
        """Exibe a foto de desmaio com o tamanho do CTkFrame corrigido"""
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        if self.img_desmaio:
            self.label_fundo = ctk.CTkLabel(self.janela, image=self.img_desmaio, text="")
        else:
            self.label_fundo = ctk.CTkLabel(self.janela, text="[💥 Você apagou de exaustão...]", font=("Segoe UI", 24))
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        
        # CORREÇÃO AQUI: width=650 e height=120 movidos para dentro do CTkFrame
        caixa = ctk.CTkFrame(self.janela, width=650, height=120, fg_color="#0a120b", border_color="#e74c3c", border_width=2, corner_radius=12)
        caixa.place(relx=0.5, rely=0.8, anchor="center")
        caixa.pack_propagate(False) # Garante que a caixa mantenha o tamanho fixo
        
        ctk.CTkLabel(caixa, text="💥 SUA ENERGIA CHEGOU A 0%! TUDO GIRA E VOCÊ DESMAIA DE EXAUSTÃO NO MEIO DO CAMPUS...", font=("Segoe UI", 13, "bold"), text_color="#e74c3c", wraplength=600).pack(pady=(15, 5))
        ctk.CTkButton(caixa, text="CONTINUAR ▶", font=("Segoe UI", 12, "bold"), fg_color="#e74c3c", hover_color="#c0392b", command=lambda: self.mostrar_game_over("VOCÊ DESMAIOU DE EXAUSTÃO!", self.img_game_over)).pack(pady=5)

    def mostrar_game_over(self, motivo, imagem_fundo):
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        if imagem_fundo:
            self.label_fundo = ctk.CTkLabel(self.janela, image=imagem_fundo, text="")
        else:
            self.label_fundo = ctk.CTkLabel(self.janela, text="", fg_color="black")
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
        
        ctk.CTkLabel(self.janela, text="GAME OVER", font=("Impact", 80), text_color="#e74c3c").place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(self.janela, text=motivo, font=("Segoe UI", 24, "bold"), text_color="#ffffff").place(relx=0.5, rely=0.55, anchor="center")

    def final_vitoria(self):
        """Tela de vitória exibida quando o jogador encontra os 3 itens"""
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        # Coloca a foto do SIGAA no fundo, ocupando a tela toda
        if self.img_vitoria:
            self.label_fundo = ctk.CTkLabel(self.janela, width=1220, height=700, image=self.img_vitoria, text="")
        else:
            self.label_fundo = ctk.CTkLabel(self.janela, width=1220, height=700, text="[FOTO DO SIGAA]", font=("Segoe UI", 30))
        self.label_fundo.place(x=0, y=0)
        
        # Cria uma caixa de texto bonitona na parte de baixo da tela
        caixa = ctk.CTkFrame(self.janela, width=800, height=220, fg_color="#0a120b", border_color="#2ecc71", border_width=4, corner_radius=15)
        caixa.place(relx=0.5, rely=0.8, anchor="center") # Fica mais para baixo para não tapar a nota!
        caixa.pack_propagate(False)
        
        ctk.CTkLabel(caixa, text="💻 COMMIT REALIZADO COM SUCESSO!", font=("Impact", 32), text_color="#2ecc71").pack(pady=(20, 10))
        
        texto_historia = "Você reuniu o Pen Drive, o Carregador e o Caderno a tempo! Você correu para o CEAGRI, compilou o código sem erros e o professor aprovou. Finalmente a nota saiu no SIGAA! Você sobreviveu a mais um dia na UFRPE."
        ctk.CTkLabel(caixa, text=texto_historia, font=("Segoe UI", 16, "bold"), text_color="white", wraplength=700).pack(pady=10)
        
        ctk.CTkButton(caixa, text="Sair do Jogo", font=("Segoe UI", 16, "bold"), fg_color="#e74c3c", height=40, command=self.janela.quit).pack(pady=10)

    def rodar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = JogoBSI()
    app.rodar()