class GerenciadorEventos:
    def __init__(self):
        self.penalidade_tempo_saguim = 15
        self.penalidade_energia_saguim = -8
        self.penalidade_tempo_veterano = 20
        self.penalidade_energia_veterano = -5

    def resolver_evento_saguim(self, jogador, escolha: str) -> str:
        """Aplica o resultado da decisão com o Saguim bloqueando o caminho"""
        if escolha == "tempo":
            jogador.passar_tempo(self.penalidade_tempo_saguim)
            return "Você perdeu um bom tempo fazendo caminhos alternativos e despistando o saguim. (-15⏰)"     
        jogador.modificar_energia(self.penalidade_energia_saguim)
        return "Você correu com tudo! O saguim pulou na sua direção, te deu um susto e você ficou exausto. (-8⚡)"

    def resolver_evento_veterano(self, jogador, escolha: str) -> str:
        """Aplica o resultado da decisão com o Veterano tagarela no corredor"""
        if escolha == "ouvir":
            jogador.passar_tempo(self.penalidade_tempo_veterano)
            return "Ele falou por 20 minutos seguidos sem respirar... Pelo menos você descobriu que não cai Fluxogramas na prova! (-20⏰)"      
        jogador.modificar_energia(self.penalidade_energia_veterano)
        return "Você se afastou. Ele gritou 'VOCÊ VAI REPROVAR!', o que te deixou muito estressado... (-5⚡)"
