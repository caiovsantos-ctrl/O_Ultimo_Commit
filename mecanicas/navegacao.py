import random


class GerenciadorNavegacao:
    def __init__(self):
        self.custo_onibus = 2.25

    def viajar_a_pe(self, jogador, destino: str) -> tuple[str, bool]:
        """Aplica os custos de caminhar e calcula chance de evento com Saguim"""
        jogador.passar_tempo(20)
        jogador.modificar_energia(-10)
        
        # 30% de chance de encontrar o Saguim no caminho
        disparar_saguim = random.random() < 0.30
        
        msg = f"Você caminhou sob o sol escaldante da Rural até {destino}."
        return msg, disparar_saguim

    def viajar_onibus(self, jogador, destino: str) -> tuple[str, bool]:
        """Tenta viajar de ônibus cobrando a passagem e calculando o atraso"""
        if jogador.dinheiro < self.custo_onibus:
            return "Sem dinheiro para o ônibus! Você vai ter que ir a pé.", False
            
        jogador.modificar_dinheiro(-self.custo_onibus)
        jogador.modificar_energia(-2)
        
        # O ônibus na Rural é uma caixinha de surpresas
        atraso = random.choice([5, 10, 20, 30])
        jogador.passar_tempo(atraso)
        
        msg = f"O ônibus atrasou {atraso} minutos, mas você chegou ao ponto de destino: {destino}."
        return msg, True

    def mover_interno(self, jogador, destino: str) -> tuple[str, bool]:
        """Movimentação rápida dentro do mesmo prédio"""
        jogador.passar_tempo(2)
        jogador.modificar_energia(-1)
        
        # 30% de chance de topar com um Veterano se estiver no CEAGRI
        disparar_veterano = "CEAGRI" in destino and random.random() < 0.30
        
        msg = f"Você andou pelos corredores até {destino}."
        return msg, disparar_veterano
    
    def usar_atalho(self, jogador) -> tuple[str, bool, int]:
        """
        Retorna (mensagem, sucesso_bool, perda_dinheiro)
        Sucesso (6-10): Chega rápido. Falha (1-5): Perde dinheiro.
        """
        resultado = random.randint(1, 10)
        if resultado > 6:
            jogador.passar_tempo(5)
            return "Você passou pelo atalho como um vulto! Chegou rápido.", True, 0
        else:
            if jogador.dinheiro >= 3.00:              
                perda = 3.00 # Valor a ser roubado
                jogador.modificar_dinheiro(-perda)
                jogador.passar_tempo(10)
                jogador.modificar_energia(-2)
                return "⚠️ ASSALTO NO BECO! Dois caras saíram do mato e levaram seus R$ 3,00 trocado. Pelo menos não mexeram na sua mochila... Você correu o resto do caminho assustado.", False, perda
            else:
                jogador.passar_tempo(10)
                jogador.modificar_energia(-8)
                return "⚠️ PERIGO NO BECO! Você foi abordado, mas quando viram que sua carteira estava completamente vazia, te deram um empurrão e mandaram você sumir dali. Você correu desesperado até o RU gastando muita energia!", False, 0
