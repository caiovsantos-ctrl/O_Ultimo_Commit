import customtkinter as ctk


class TelasTransicao:
    def __init__(self, janela_principal):
        self.janela = janela_principal

    def limpar_tela(self):
        """Destrói todos os widgets atuais da janela principal"""
        for widget in self.janela.winfo_children():
            widget.destroy()
    
    def mostrar_tela_onibus(self, msg, imagem_fundo, comando_continuar):
        self.limpar_tela()      
        if imagem_fundo:
            ctk.CTkLabel(self.janela, image=imagem_fundo, text="").place(x=0, y=0, relwidth=1, relheight=1)
        else:
            ctk.CTkLabel(self.janela, text="[🚌 Dentro do Ônibus...]", font=("Segoe UI", 24)).place(x=0, y=0, relwidth=1, relheight=1)
        caixa = ctk.CTkFrame(self.janela, width=550, height=220, fg_color="#0a120b", border_color="#27ae60", border_width=2, corner_radius=12)
        caixa.place(relx=0.5, rely=0.95, anchor="s")
        caixa.pack_propagate(False)       
        ctk.CTkLabel(caixa, text="🚌 ÔNIBUS EM MOVIMENTO", font=("Impact", 28), text_color="#2ecc71").pack(pady=(15, 5))
        ctk.CTkLabel(caixa, text=msg, font=("Segoe UI", 14, "bold"), text_color="#ffffff", wraplength=500).pack(pady=10)       
        ctk.CTkButton(caixa, text="DESCER NO PONTO ▶", font=("Segoe UI", 13, "bold"), fg_color="#27ae60", hover_color="#218c4e", command=comando_continuar).pack(pady=10)

    def mostrar_tela_pe(self, msg, imagem_fundo, comando_continuar):
        self.limpar_tela()        
        if imagem_fundo:
            ctk.CTkLabel(self.janela, image=imagem_fundo, text="").place(x=0, y=0, relwidth=1, relheight=1)
        else:
            ctk.CTkLabel(self.janela, text="[🚶 Caminhando pelo campus...]", font=("Segoe UI", 24)).place(x=0, y=0, relwidth=1, relheight=1)      
        caixa = ctk.CTkFrame(self.janela, width=550, height=240, fg_color="#0a120b", border_color="#e67e22", border_width=2, corner_radius=12)
        caixa.place(relx=0.5, rely=0.5, anchor="center")
        caixa.pack_propagate(False)      
        ctk.CTkLabel(caixa, text="🚶 CAMINHANDO SOB O SOL...", font=("Impact", 28), text_color="#e67e22").pack(pady=(15, 5))
        ctk.CTkLabel(caixa, text=msg, font=("Segoe UI", 14, "bold"), text_color="#ffffff", wraplength=500).pack(pady=10)      
        ctk.CTkButton(caixa, text="CHEGAR AO DESTINO ▶", font=("Segoe UI", 13, "bold"), fg_color="#d35400", hover_color="#a84300", command=comando_continuar).pack(pady=10)

    def mostrar_evento_saguim(self, imagem_fundo, comando_tempo, comando_energia):
        self.limpar_tela()       
        if imagem_fundo:
            ctk.CTkLabel(self.janela, width=1220, height=700, image=imagem_fundo, text="").place(x=0, y=0)        
        caixa = ctk.CTkFrame(self.janela, width=600, height=280, fg_color="#0a120b", border_color="#f1c40f", border_width=3, corner_radius=12)
        caixa.place(relx=0.5, rely=0.5, anchor="center")
        caixa.pack_propagate(False)        
        ctk.CTkLabel(caixa, text="🐒 UM SAGUIM BLOQUEIA O CAMINHO!", font=("Impact", 28), text_color="#f1c40f").pack(pady=(20, 10))
        ctk.CTkLabel(caixa, text="Ele cruza os braços e começa a pular na sua frente querendo atenção. Como você reage?", font=("Segoe UI", 15, "bold"), text_color="white", wraplength=550).pack(pady=10)        
        ctk.CTkButton(caixa, text="Despistar com paciência (-15⏰)", font=("Segoe UI", 14, "bold"), fg_color="#2980b9", height=40, command=comando_tempo).pack(pady=5)
        ctk.CTkButton(caixa, text="Passar correndo (-15⚡)", font=("Segoe UI", 14, "bold"), fg_color="#e74c3c", height=40, command=comando_energia).pack(pady=5)

    def mostrar_evento_veterano(self, imagem_fundo, comando_ouvir, comando_ignorar):
        self.limpar_tela()      
        if imagem_fundo:
            img_pil = imagem_fundo._light_image 
            imagem_tela_cheia = ctk.CTkImage(light_image=img_pil, size=(1220, 700))       
            fundo = ctk.CTkLabel(self.janela, text="", width=1220, height=700, image=imagem_tela_cheia)
            fundo.place(x=0, y=0)      
        caixa = ctk.CTkFrame(self.janela, width=600, height=280, fg_color="#0a120b", border_color="#9b59b6", border_width=3, corner_radius=12)
        caixa.place(relx=0.5, rely=0.5, anchor="center")
        caixa.pack_propagate(False)      
        ctk.CTkLabel(caixa, text="👨‍💻 VETERANO NO CORREDOR", font=("Impact", 28), text_color="#9b59b6").pack(pady=(20, 10))
        ctk.CTkLabel(caixa, text="Um veterano do curso te para: 'E aí calouro! Quer ouvir umas verdades sobre a prova de programação?'", font=("Segoe UI", 15, "bold"), text_color="white", wraplength=550).pack(pady=10)      
        ctk.CTkButton(caixa, text="Ouvir as 'dicas' (-20⏰)", font=("Segoe UI", 14, "bold"), fg_color="#2980b9", height=40, command=comando_ouvir).pack(pady=5)
        ctk.CTkButton(caixa, text="Ignorar e sair andando (-10⚡)", font=("Segoe UI", 14, "bold"), fg_color="#e74c3c", height=40, command=comando_ignorar).pack(pady=5)

    def mostrar_tela_desmaio(self, imagem_fundo, comando_continuar):
        self.limpar_tela()       
        if imagem_fundo:
            ctk.CTkLabel(self.janela, width=1220, height=700, image=imagem_fundo, text="").place(x=0, y=0)
        else:
            ctk.CTkLabel(self.janela, width=1220, height=700, text="[💥 Você apagou de exaustão...]", font=("Segoe UI", 24)).place(x=0, y=0)
        caixa = ctk.CTkFrame(self.janela, width=650, height=120, fg_color="#0a120b", border_color="#e74c3c", border_width=2, corner_radius=12)
        caixa.place(relx=0.5, rely=0.8, anchor="center")
        caixa.pack_propagate(False)        
        ctk.CTkLabel(caixa, text="💥 SUA ENERGIA CHEGOU A 0%! TUDO GIRA E VOCÊ DESMAIA DE EXAUSTÃO NO MEIO DO CAMPUS...", font=("Segoe UI", 13, "bold"), text_color="#e74c3c", wraplength=600).pack(pady=(15, 5))
        ctk.CTkButton(caixa, text="CONTINUAR ▶", font=("Segoe UI", 12, "bold"), fg_color="#e74c3c", hover_color="#c0392b", command=comando_continuar).pack(pady=5)
        
    def mostrar_game_over(self, motivo, imagem_fundo):
        self.limpar_tela()       
        if imagem_fundo:
            ctk.CTkLabel(self.janela, width=1220, height=700, image=imagem_fundo, text="").place(x=0, y=0)
        else:
            ctk.CTkLabel(self.janela, width=1220, height=700, text="", fg_color="black").place(x=0, y=0)
        ctk.CTkLabel(self.janela, text="GAME OVER", font=("Impact", 80), text_color="#e74c3c").place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(self.janela, text=motivo, font=("Segoe UI", 24, "bold"), text_color="#ffffff").place(relx=0.5, rely=0.55, anchor="center")

    def final_vitoria(self, imagem_fundo, comando_sair):
        self.limpar_tela()        
        if imagem_fundo:
            ctk.CTkLabel(self.janela, width=1220, height=700, image=imagem_fundo, text="").place(x=0, y=0)
        else:
            ctk.CTkLabel(self.janela, width=1220, height=700, text="[FOTO DO SIGAA]", font=("Segoe UI", 30)).place(x=0, y=0)      
        caixa = ctk.CTkFrame(self.janela, width=800, height=220, fg_color="#0a120b", border_color="#2ecc71", border_width=4, corner_radius=15)
        caixa.place(relx=0.5, rely=0.8, anchor="center")
        caixa.pack_propagate(False)      
        ctk.CTkLabel(caixa, text="💻 COMMIT REALIZADO COM SUCESSO!", font=("Impact", 32), text_color="#2ecc71").pack(pady=(20, 10))
        texto_historia = "Você reuniu o Pen Drive, o Carregador e o Caderno a tempo! Você correu para o CEAGRI, compilou o código sem erros e o professor aprovou. Finalmente a nota saiu no SIGAA! Você sobreviveu a mais um dia na UFRPE."
        ctk.CTkLabel(caixa, text=texto_historia, font=("Segoe UI", 16, "bold"), text_color="white", wraplength=700).pack(pady=10)        
        ctk.CTkButton(caixa, text="Sair do Jogo", font=("Segoe UI", 16, "bold"), fg_color="#e74c3c", height=40, command=comando_sair).pack(pady=10)
