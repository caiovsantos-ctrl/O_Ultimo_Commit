import random

class GerenciadorNavegacao:
    """Gerencia as ações de navegação do jogador, incluindo custos e eventos aleatórios"""
    def __init__(self):
        self.custo_onibus = 2.25

    def viajar_a_pe(self, jogador, destino: str) -> tuple[str, bool]:
        """Calcula o tempo e energia gastos ao caminhar até o destino, considerando chuva e efeitos energéticos"""
        disparar_saguim = random.random() < 0.30            
        tempo_total = 20        
        if jogador.esta_chovendo():
            tempo_total += 15 
            jogador.modificar_energia(-15) 
            msg = f"Debaixo de um temporal, você caminhou até {destino}. A lama e as poças te atrasaram muito!"
        else:
            jogador.modificar_energia(-10)
            msg = f"Você caminhou sob o sol escaldante da Rural até {destino}."          
        if jogador.tem_efeito_energetico():
            tempo_total = max(1, tempo_total // 2)          
        jogador.passar_tempo(tempo_total)
        return msg, disparar_saguim

    def viajar_onibus(self, jogador, destino: str) -> tuple[str, bool]:
        """Calcula o tempo e energia gastos ao viajar de ônibus até o destino, considerando atrasos e chuva"""
        if jogador.dinheiro < self.custo_onibus:
            return "Sem dinheiro para o ônibus! Você vai ter que ir a pé.", False                                 
        jogador.modificar_dinheiro(-self.custo_onibus)
        jogador.modificar_energia(-2)        
        atraso = random.choice([5, 10, 20, 30])
        tempo_total = atraso      
        if jogador.esta_chovendo():
            tempo_total += 15 
            msg = f"A chuva alagou o campus. O õnibus demorou uma eternidade e atrasou {atraso + 15} minutos até {destino}."
        else:
            msg = f"O ônibus atrasou {atraso} minutos, mas você chegou ao ponto de destino: {destino}."          
        if jogador.tem_efeito_energetico():
            tempo_total = max(1, tempo_total // 2)           
        jogador.passar_tempo(tempo_total)
        return msg, True

    def mover_interno(self, jogador, destino: str) -> tuple[str, bool]:
        """Calcula o tempo e energia gastos ao se mover internamente dentro de um prédio, considerando efeitos energéticos"""
        tempo_total = 2       
        if jogador.tem_efeito_energetico():
            tempo_total = max(1, tempo_total // 2)            
        jogador.passar_tempo(tempo_total)
        jogador.modificar_energia(-1)
        disparar_veterano = "CEAGRI" in destino and random.random() < 0.30      
        msg = f"Você andou pelos corredores até {destino}."
        return msg, disparar_veterano   
     
    def usar_atalho(self, jogador) -> tuple[str, bool, int]:
        """Calcula o tempo, energia e possíveis perdas ao usar um atalho, considerando chuva, assaltos e efeitos energéticos"""
        resultado = random.randint(1, 10)     
        tempo_total = 5        
        if jogador.esta_chovendo():
            if resultado > 7:
                tempo_total += 5
                jogador.modificar_energia(-2)
                msg = "Você escorregou na lama do atalho debaixo de chuva, mas conseguiu cortar caminho!"
                sucesso, perda = True, 0
            else:
                if jogador.dinheiro >= 3.00:              
                    perda = 3.00 
                    jogador.modificar_dinheiro(-perda)
                    tempo_total += 10
                    jogador.modificar_energia(-5)
                    msg = "⚠️ ASSALTO NA CHUVA! Dois caras te pararam na lama e levaram R$ 3,00 trocado."
                    sucesso = False
                else:
                    tempo_total += 10
                    jogador.modificar_energia(-12)
                    msg = "⚠️ PERIGO! Você foi abordado, fugiu na chuva e quase torceu o pé. Perdeu muito tempo e energia!"
                    sucesso, perda = False, 0
        else:
            if resultado > 6:
                msg = "Você passou pelo atalho como um vulto! Chegou rápido."
                sucesso, perda = True, 0
            else:
                if jogador.dinheiro >= 3.00:              
                    perda = 3.00 
                    jogador.modificar_dinheiro(-perda)
                    tempo_total += 5
                    jogador.modificar_energia(-2)
                    msg = "⚠️ ASSALTO NO BECO! Dois caras saíram do mato e levaram seus R$ 3,00 trocado. Pelo menos não mexeram na sua mochila... Você correu o resto do caminho assustado."
                    sucesso = False
                else:
                    tempo_total += 5
                    jogador.modificar_energia(-8)
                    msg = "⚠️ PERIGO NO BECO! Você foi abordado, mas quando viram que sua carteira estava completamente vazia, te deram um empurrão e mandaram você sumir dali. Você correu desesperado até o RU gastando muita energia!"
                    sucesso, perda = False, 0
        if jogador.tem_efeito_energetico():
            tempo_total = max(1, tempo_total // 2)            
        jogador.passar_tempo(tempo_total)
        return msg, sucesso, perda
