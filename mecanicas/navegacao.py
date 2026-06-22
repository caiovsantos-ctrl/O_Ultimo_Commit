import random

class GerenciadorNavegacao:
    """Gerencia as ações de navegação do jogador, incluindo custos e eventos aleatórios"""
    def __init__(self):
        self.custo_onibus = 2.25

    def viajar_a_pe(self, jogador, destino: str) -> tuple[str, bool]:
        disparar_saguim = random.random() < 0.30            
        jogador.passar_tempo(20)       
        if jogador.esta_chovendo():
            jogador.passar_tempo(15) 
            jogador.modificar_energia(-15) 
            msg = f"Debaixo de um temporal, você caminhou até {destino}. A lama e as poças te atrasaram muito!"
        else:
            jogador.modificar_energia(-10)
            msg = f"Você caminhou sob o sol escaldante da Rural até {destino}."           
        return msg, disparar_saguim

    def viajar_onibus(self, jogador, destino: str) -> tuple[str, bool]:
        if jogador.dinheiro < self.custo_onibus:
            return "Sem dinheiro para o ônibus! Você vai ter que ir a pé.", False                      
        jogador.modificar_dinheiro(-self.custo_onibus)
        jogador.modificar_energia(-2)
        atraso = random.choice([5, 10, 20, 30])
        jogador.passar_tempo(atraso)       
        if jogador.esta_chovendo():
            jogador.passar_tempo(15) 
            msg = f"A chuva alagou o campus. O circular demorou uma eternidade e atrasou {atraso + 15} minutos até {destino}."
        else:
            msg = f"O ônibus atrasou {atraso} minutos, mas você chegou ao ponto de destino: {destino}."           
        return msg, True

    def mover_interno(self, jogador, destino: str) -> tuple[str, bool]:
        jogador.passar_tempo(2)
        jogador.modificar_energia(-1)
        disparar_veterano = "CEAGRI" in destino and random.random() < 0.30      
        msg = f"Você andou pelos corredores até {destino}."
        return msg, disparar_veterano
    
    def usar_atalho(self, jogador) -> tuple[str, bool, int]:
        resultado = random.randint(1, 10)     
        jogador.passar_tempo(5)        
        if jogador.esta_chovendo():
            if resultado > 7:
                jogador.passar_tempo(5)
                jogador.modificar_energia(-2)
                return "Você escorregou na lama do atalho debaixo de chuva, mas conseguiu cortar caminho!", True, 0
            else:
                if jogador.dinheiro >= 3.00:              
                    perda = 3.00 
                    jogador.modificar_dinheiro(-perda)
                    jogador.passar_tempo(10)
                    jogador.modificar_energia(-5)
                    return "⚠️ ASSALTO NA CHUVA! Dois caras te pararam na lama e levaram R$ 3,00 trocado.", False, perda
                else:
                    jogador.passar_tempo(10)
                    jogador.modificar_energia(-12)
                    return "⚠️ PERIGO! Você foi abordado, fugiu na chuva e quase torceu o pé. Perdeu muito tempo e energia!", False, 0
        else:
            if resultado > 6:
                return "Você passou pelo atalho como um vulto! Chegou rápido.", True, 0
            else:
                if jogador.dinheiro >= 3.00:              
                    perda = 3.00 
                    jogador.modificar_dinheiro(-perda)
                    jogador.passar_tempo(5)
                    jogador.modificar_energia(-2)
                    return "⚠️ ASSALTO NO BECO! Dois caras saíram do mato e levaram seus R$ 3,00 trocado. Pelo menos não mexeram na sua mochila... Você correu o resto do caminho assustado.", False, perda
                else:
                    jogador.passar_tempo(5)
                    jogador.modificar_energia(-8)
                    return "⚠️ PERIGO NO BECO! Você foi abordado, mas quando viram que sua carteira estava completamente vazia, te deram um empurrão e mandaram você sumir dali. Você correu desesperado até o RU gastando muita energia!", False, 0
