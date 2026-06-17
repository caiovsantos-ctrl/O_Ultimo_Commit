import customtkinter as ctk
import sys, random

# Core e Mecânicas
from core.jogador import Jogador
from mecanicas.navegacao import GerenciadorNavegacao
from mecanicas.buscas import GerenciadorBuscas
from mecanicas.sobrevivencia import GerenciadorSobrevivencia
from mecanicas.eventos import GerenciadorEventos

# UI
from ui.carregar_imagem import GerenciadorMidia
from ui.transicao import TelasTransicao
from ui.interface_principal import ConstrutorTelas
from ui.hud import PainelHUD
from ui.cenarios import GerenciadorCenarios


class JogoBSI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Depois do Último Commit: O Sumiço na Rural")
        self.geometry("1220x700")
        self.resizable(False, False)

        # Módulos de Estado e Regras
        self.jogador = Jogador()
        self.navegacao = GerenciadorNavegacao()
        self.busca = GerenciadorBuscas()
        self.sobrevivencia = GerenciadorSobrevivencia()
        self.eventos = GerenciadorEventos()

        # Módulos Visuais
        self.midia = GerenciadorMidia()
        self.midia.inicializar_todos_assets()
        self.telas_transicao = TelasTransicao(self)
        self.construtor_visual = ConstrutorTelas(self)
        self.gerenciador_cenarios = GerenciadorCenarios()

        self.historia = (
            "Quarta-feira, 07:00 da manhã.\n\n"
            "Passei a madrugada inteira codando o projeto de Princípios de Programação. "
            "Sobrevivi à base de puro café do RU, e já estou acabado.\n\n"
            "Peguei o BRT lotado espremido na porta. Quando finalmente desci na frente da UFRPE, o desespero bateu: "
            "o zíper da minha mochila estourou. Meu Pendrive com o código, meu caderno e meu carregador "
            "caíram em algum lugar do campus.\n\n"
            "O professor no Departamento de Computação (DC) avisou: o prazo final é às 14h em ponto. "
            "Se eu não recuperar tudo e chegar lá a tempo... é Game Over."
        )
        
        # 🔔 CORREÇÃO LÓGICA 1: "Educação Física" alterado para "Ed Física (Sala)" 
        # para dar match exato com os botões de movimentação da sua interface.
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
        img_base = self.midia.obter_imagem("frente_rural")
        self.construtor_visual.montar_tela_titulo(self.carregar_intro, img_base)
        self.mainloop()

    def carregar_intro(self):
        img_borrada = self.midia.obter_imagem("bg_borrado")
        self.construtor_visual.carregar_tela_introducao(img_borrada, self.historia, self.iniciar_primeira_fase)

    def iniciar_primeira_fase(self):
        self.carregar_cenario("Prédio Central")

    def carregar_cenario(self, local: str, item_do_local: str = None):
        if self.verificar_fim_de_jogo(): return
        
        if item_do_local is None:
            item_do_local = self.distribuicao_itens.get(local, None)
        
        self.item_local_atual = item_do_local 
        foto_fundo = self.midia.obter_imagem(local)
        
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
            msg, evento = self.navegacao.viajar_a_pe(self.jogador, destino)
            img = self.midia.obter_imagem("tela_andando")
            self.telas_transicao.mostrar_tela_pe(msg, img, lambda: self.checar_chegada(destino, evento, "saguim"))
        else:
            msg, sucesso = self.navegacao.viajar_onibus(self.jogador, destino)
            if sucesso:
                img = self.midia.obter_imagem("tela_onibus")
                self.telas_transicao.mostrar_tela_onibus(msg, img, lambda: self.checar_chegada(destino))
            else:
               self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)

    def mover_interno(self, destino: str):
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
        # Chama a mecânica
        msg, sucesso, valor = self.navegacao.usar_atalho(self.jogador)
        
        # Pega a imagem de transição (reutilizando a de caminhada)
        img = self.midia.obter_imagem("tela_andando")
        
        # Usa o sistema de transição que você já tem
        self.telas_transicao.mostrar_tela_pe(
            f"🏃 ATALHO\n\n{msg}", 
            img, 
            lambda: self.carregar_cenario("RU")
        )

    def resolver_evento_veterano(self, escolha: str, destino: str):
        msg = self.eventos.resolver_evento_veterano(self.jogador, escolha)
        if not self.verificar_fim_de_jogo():
            self.carregar_cenario(destino)
            self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)

    def checar_chegada(self, destino: str, tem_evento: bool = False, tipo_evento: str = "", item_local: str = None):
        if self.verificar_fim_de_jogo(): return

        if tem_evento and tipo_evento == "saguim":
            img = self.midia.obter_imagem("tela_andando")
            self.telas_transicao.mostrar_evento_saguim(img, 
                lambda: self.resolver_evento("saguim", "tempo", destino, item_local),
                lambda: self.resolver_evento("saguim", "energia", destino, item_local))
            return

        self.carregar_cenario(destino, item_local)

    def resolver_evento(self, tipo, escolha, destino, item_local):
        if tipo == "saguim":
            msg = self.eventos.resolver_evento_saguim(self.jogador, escolha)
        
        if not self.verificar_fim_de_jogo():
            self.checar_chegada(destino, tem_evento=False, item_local=item_local)
            self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)

    def acao_procurar(self):
        # Se o local não tem item OU se o item deste local já foi pego (virou None)
        if not hasattr(self, 'item_local_atual') or not self.item_local_atual:
            self.jogador.passar_tempo(10)
            self.jogador.modificar_energia(-5)
            
            msg = "Você procurou com atenção, mas não encontrou nenhum item útil para o seu commit aqui."
            self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)
            self.verificar_fim_de_jogo()
            return

        # Se tem item, roda a mecânica de probabilidade do seu Gerenciador de Buscas
        msg, sucesso = self.busca.procurar_item_no_local(self.jogador, self.item_local_atual)
        
        if sucesso:
            nome_asset = f"item_{self.item_local_atual.lower()}"
            img_item = self.midia.obter_imagem(nome_asset)
            self.gerenciador_cenarios.spawnar_item_na_tela(
            self.construtor_visual.label_fundo, # O frame pai
            self.construtor_visual.label_fundo.cget("image"), # A imagem do fundo
            self.item_local_atual, 
            img_item, 
            self.coletar_item
        )
            
        self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)
        self.verificar_fim_de_jogo()

    def coletar_item(self, nome_item: str):
        self.gerenciador_cenarios.limpar_item_atual()
        
        if nome_item not in self.jogador.itens_encontrados:
            self.jogador.itens_encontrados.append(nome_item)
            
            # 🔥 MELHORIA LÓGICA: Remove o item do mapa para o jogador não poder
            # achar o mesmo item duas vezes no mesmo prédio.
            # Procuramos qual local guardava esse item e limpamos ele:
            for local, item in list(self.distribuicao_itens.items()):
                if item == nome_item:
                    self.distribuicao_itens[local] = None
            
            # Atualiza a referência local para "Vazio" imediatamente
            self.item_local_atual = None 
            
        if len(self.jogador.itens_encontrados) >= 3:
            img_vitoria = self.midia.obter_imagem("vitoria")
            self.telas_transicao.final_vitoria(img_vitoria, lambda: sys.exit())
        else:
            msg_sucesso = f"🎉 INCRÍVEL! Você encontrou: {nome_item}! ({len(self.jogador.itens_encontrados)}/3 itens recuperados)"
            self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg_sucesso)

    def comprar_comida(self, local: str):
        msg, sucesso = self.sobrevivencia.comprar_comida(self.jogador, local)
        self.construtor_visual.gerenciador_hud.atualizar_textos(self.jogador, msg)
        self.verificar_fim_de_jogo()

    def verificar_fim_de_jogo(self) -> bool:
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