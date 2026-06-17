import random


class GerenciadorBuscas:
    def __init__(self):
        self.chance_sucesso = 0.80
        self.custo_tempo = 10
        self.custo_energia = -5

    def procurar_item_no_local(self, jogador, item_do_local: str) -> tuple[str, bool]:
        """Custa tempo e energia. Retorna se o item foi spawnado com sucesso"""
        jogador.passar_tempo(self.custo_tempo)
        jogador.modificar_energia(self.custo_energia)
        
        # Se o jogador já pegou esse item antes, não spawna de novo
        if item_do_local in jogador.itens_encontrados:
            return "Você revirou tudo, mas lembra que já pegou o que precisava aqui.", False
            
        # Chance de o item aparecer na tela para o jogador clicar
        if random.random() < self.chance_sucesso:
            msg = "Você examinou o local... Parece que tem algo por aqui. Clique nele!"
            return msg, True
            
        return "Você procurou atrás das cadeiras e armários, mas não achou nada útil.", False