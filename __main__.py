import customtkinter as ctk
import sys, random
from core.jogador import Jogador
from mecanicas.navegacao import GerenciadorNavegacao
from mecanicas.buscas import GerenciadorBuscas
from mecanicas.sobrevivencia import GerenciadorSobrevivencia
from mecanicas.eventos import GerenciadorEventos
from ui.carregar_imagem import GerenciadorMidia
from ui.transicao import TelasTransicao
from ui.interface_principal import ConstrutorTelas
from ui.hud import PainelHUD
from ui.cenarios import GerenciadorCenarios


class JogoBSI(ctk.CTk):
    """Classe principal do jogo, gerenciando a janela, o fluxo do jogo e a interação entre os componentes"""
    def __init__(self):
        super().__init__()
        self.title("Depois do Último Commit: O Sumiço na Rural")
        self.geometry("1220x700")
        self.resizable(False, False)
        self.jogador = Jogador()
        self.navegacao = GerenciadorNavegacao()
        self.busca = GerenciadorBuscas()
        self.sobrevivencia = GerenciadorSobrevivencia()
        self.eventos = GerenciadorEventos()
        self.midia = GerenciadorMidia()
        self.midia.inicializar_todos_assets()
        self.telas_transicao = TelasTransicao(self)
        self.construtor_visual = ConstrutorTelas(self)
        self.gerenciador_cenarios = GerenciadorCenarios()
        self.historia = (
            "Quinta-feira, 07:00 da manhã.\n\n"
            "Passei a madrugada inteira codando o projeto de Princípios de Programação. "
            "Sobrevivi à base de puro café do RU, e já estou acabado.\n\n"
            "Peguei o BRT lotado espremido na porta. Quando finalmente desci na frente da UFRPE, o desespero bateu: "
            "o zíper da minha mochila estourou. Meu Pendrive com o código, meu caderno e meu carregador "
            "caíram em algum lugar do campus.\n\n"
            "O professor avisou: o prazo final é às 14h em ponto. "
            "Se eu não recuperar tudo e chegar lá a tempo... é Game Over."
        )
        locais_do_campus = [
            "Parada de Ônibus", 
            "RU", 
            "Lanchonete", 
            "CEAGRI (Entrada)", 
            "CEAGRI (Sala de Aula)", 
            "CEAGRI (PCs)", 
            "Ed Física (Entrada)", 
            "Ed Física (Sala)", 
            "A Praça", 
            "Prédio Central"
        ]
        itens_para_esconder = ["Pendrive", "Caderno", "Carregador"] 
        locais_sorteados = random.sample(locais_do_campus, len(itens_para_esconder))
        self.distribuicao_itens = dict(zip(locais_sorteados, itens_para_esconder))
        
    def iniciar_jogo(self):
        """Inicia o jogo montando a tela de título e depois a introdução"""
        img_base = self.midia.obter_imagem("frente_rural")
        self.construtor_visual.montar_tela_titulo(self.carregar_intro, img_base)
        self.mainloop()

    def carregar_intro(self):
        """Carrega a tela de introdução com a história do jogo e um fundo borrado"""
        img_borrada = self.midia.obter_imagem("bg_borrado")
        self.construtor_visual.carregar_tela_introducao(img_borrada, self.historia, self.iniciar_primeira_fase)

    def iniciar_primeira_fase(self):
        """Inicia a primeira fase do jogo carregando o cenário inicial e o HUD"""
        self.carregar_cenario("Prédio Central")

    def carregar_cenario(self, local: str, item_do_local: str = None):
        """Carrega o cenário solicitado, exibindo o item camuflado e controlando o clima dinâmico."""
        if self.verificar_fim_de_jogo(): 
            return     
        if item_do_local is None:
            item_do_local = self.distribuicao_itens.get(local, None)      
        self.item_local_atual = item_do_local 
        mapa_chuva = {
            "Parada de Ônibus": "parada chuva",
            "RU": "ru chuva",
            "Lanchonete": "lanchonete chuva",
            "CEAGRI (Entrada)": "ceaagri chuva",
            "Ed Física (Entrada)": "edf chuva",
            "A Praça": "praca chuva",
            "Prédio Central": "predio chuva"
        }
        mapa_escuro = {
            "CEAGRI (Sala de Aula)": "ceagri sala escuro",
            "CEAGRI (PCs)": "ceagri pcs escuro",
            "Ed Física (Sala)": "edf sala escuro"
        }
        nome_asset_fundo = None      
        if self.jogador.esta_sem_energia():
            for sala_chave, asset_escuro in mapa_escuro.items():
                if sala_chave == local or sala_chave in local:
                    nome_asset_fundo = asset_escuro
                    break
        if nome_asset_fundo is None:
            if self.jogador.esta_chovendo() and local in mapa_chuva:
                nome_asset_fundo = mapa_chuva[local]
            else:
                nome_asset_fundo = local
        foto_fundo = self.midia.obter_imagem(nome_asset_fundo)
        locais_permitidos_venda = ["Parada de Ônibus", "Ed Física (Entrada)"]
        if local in locais_permitidos_venda and self.jogador.trufas > 0:
            comando_vender = self.acao_vender_trufa
        else:
            comando_vender = None
        foto_fundo = self.midia.obter_imagem(nome_asset_fundo)     
        self.construtor_visual.desenhar_cenario_completo(
            local, 
            item_do_local, 
            foto_fundo, 
            self.jogador, 
            self.mover_interno,
            comando_procurar=self.acao_procurar
        )

    def viajar(self, destino: str, meio: str):
        if meio == "pe":
            msg_viagem, evento = self.navegacao.viajar_a_pe(self.jogador, destino)
            texto_tela = msg_viagem + self.jogador.checar_alertas_clima()            
            img_nome = "tela pe chuva" if self.jogador.esta_chovendo() else "tela_andando"
            img = self.midia.obter_imagem(img_nome)           
            self.telas_transicao.mostrar_tela_pe(texto_tela, img, lambda: self.checar_chegada(destino, evento, "saguim"))
        else:
            msg_viagem, sucesso = self.navegacao.viajar_onibus(self.jogador, destino)
            texto_tela = msg_viagem + self.jogador.checar_alertas_clima()           
            if sucesso:
                img_nome = "tela onibus chuva" if self.jogador.esta_chovendo() else "tela_onibus"
                img = self.midia.obter_imagem(img_nome)
                self.telas_transicao.mostrar_tela_onibus(texto_tela, img, lambda: self.checar_chegada(destino))
            else:
               self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, texto_tela)

    def mover_interno(self, destino: str):
        """Processa a ação de se mover internamente dentro do mesmo local"""
        msg, disparar_veterano = self.navegacao.mover_interno(self.jogador, destino) 
        if disparar_veterano:
            img_destino = self.midia.obter_imagem(destino)
            self.telas_transicao.mostrar_evento_veterano(
                img_destino,
                lambda: self.resolver_evento_veterano("ouvir", destino),
                lambda: self.resolver_evento_veterano("ignorar", destino)
            )
        else:
            if not self.verificar_fim_de_jogo():
                self.carregar_cenario(destino)
                self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)

    def processar_atalho(self):
        msg_viagem, sucesso, valor = self.navegacao.usar_atalho(self.jogador)
        texto_tela = f"🏃 ATALHO\n\n{msg_viagem}" + self.jogador.checar_alertas_clima()      
        img_nome = "tela pe chuva" if self.jogador.esta_chovendo() else "tela_andando"
        img = self.midia.obter_imagem(img_nome)     
        self.telas_transicao.mostrar_tela_pe(
            texto_tela, 
            img, 
            lambda: self.carregar_cenario("RU")
        )

    def resolver_evento_veterano(self, escolha: str, destino: str):
        """Processa a escolha do jogador no evento do veterano e suas consequências"""
        msg = self.eventos.resolver_evento_veterano(self.jogador, escolha)
        if not self.verificar_fim_de_jogo():
            self.carregar_cenario(destino)
            self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)

    def checar_chegada(self, destino: str, tem_evento: bool = False, tipo_evento: str = "", item_local: str = None):
        """Checa se o jogador chegou ao destino e se deve disparar um evento"""
        if self.verificar_fim_de_jogo(): 
            return
        if tem_evento and tipo_evento == "saguim":
            nome_img_saguim = "tela pe chuva" if self.jogador.esta_chovendo() else "tela_andando"
            img = self.midia.obter_imagem(nome_img_saguim)
            self.telas_transicao.mostrar_evento_saguim(img, 
                lambda: self.resolver_evento("saguim", "tempo", destino, item_local),
                lambda: self.resolver_evento("saguim", "energia", destino, item_local))
            return
        self.carregar_cenario(destino, item_local)

    def resolver_evento(self, tipo, escolha, destino, item_local):
        """Processa a escolha do jogador no evento do saguim e suas consequências"""
        if tipo == "saguim":
            msg = self.eventos.resolver_evento_saguim(self.jogador, escolha)
        if not self.verificar_fim_de_jogo():
            self.checar_chegada(destino, tem_evento=False, item_local=item_local)
            self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)

    def acao_procurar(self):
        """Processa a ação de procurar o item perdido no cenário atual"""
        if not hasattr(self, 'item_local_atual') or not self.item_local_atual:
            self.jogador.passar_tempo(10)
            self.jogador.modificar_energia(-5)
            msg = "Você procurou com atenção, mas não encontrou nenhum item útil para o seu commit aqui."
            self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)
            self.verificar_fim_de_jogo()
            return
        msg, sucesso = self.busca.procurar_item_no_local(self.jogador, self.item_local_atual)        
        if sucesso:
            nome_asset = f"item_{self.item_local_atual.lower()}"
            img_item = self.midia.obter_imagem(nome_asset)
            self.gerenciador_cenarios.spawnar_item_na_tela(
            self.construtor_visual.label_fundo, 
            self.construtor_visual.label_fundo.cget("image"), 
            self.item_local_atual, 
            img_item, 
            self.coletar_item
        )            
        self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)
        self.verificar_fim_de_jogo()

    def coletar_item(self, nome_item: str):
        """Processa a ação de coletar um item encontrado"""
        self.gerenciador_cenarios.limpar_item_atual()        
        if nome_item not in self.jogador.itens_encontrados:
            self.jogador.itens_encontrados.append(nome_item)                     
            for local, item in list(self.distribuicao_itens.items()):
                if item == nome_item:
                    self.distribuicao_itens[local] = None        
            self.item_local_atual = None           
        if len(self.jogador.itens_encontrados) >= 3:
            img_vitoria = self.midia.obter_imagem("vitoria")
            self.telas_transicao.final_vitoria(img_vitoria, lambda: sys.exit())
        else:
            msg_sucesso = f"🎉 INCRÍVEL! Você encontrou: {nome_item}! ({len(self.jogador.itens_encontrados)}/3 itens recuperados)"
            self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg_sucesso)

    def comprar_comida(self, local: str):
        """Processa a ação de comprar comida"""
        msg, sucesso = self.sobrevivencia.comprar_comida(self.jogador, local)
        self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)
        self.verificar_fim_de_jogo()

    def acao_vender_trufa(self, local_venda: str):
        """Executa a ação de venda de trufas e garante que a mensagem fique na tela"""
        msg = self.jogador.vender_trufas()
        if self.verificar_fim_de_jogo():
            return
        self.carregar_cenario(local_venda)
        self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)

    def verificar_fim_de_jogo(self) -> bool:
        """Checa se o jogo chegou a um estado de vitória, derrota por desmaio ou derrota por tempo, e exibe a tela correspondente"""
        estado = self.jogador.checar_estado_jogo()
        img_vitoria = self.midia.obter_imagem("vitoria")
        img_desmaio = self.midia.obter_imagem("desmaio")
        img_game_over = self.midia.obter_imagem("game_over")     
        if estado == "VITORIA":
            self.telas_transicao.final_vitoria(img_vitoria, lambda: sys.exit())
            return True
        elif estado == "DESMAIO":
            self.telas_transicao.mostrar_tela_desmaio(img_desmaio, lambda: self.telas_transicao.mostrar_game_over("VOCÊ DESMAIOU DE EXAUSTÃO!", img_game_over))
            return True
        elif estado == "GAME_OVER_TEMPO":
            self.telas_transicao.mostrar_game_over("O PRAZO ACABOU! O PROFESSOR FECHOU O SISTEMA.", img_game_over)
            return True
        return False

if __name__ == "__main__":
    app = JogoBSI()
    app.iniciar_jogo()
