class Jogador:
    def __init__(self):
        self.energia = 50
        self.dinheiro = 15.00
        self.tempo_minutos = 420  # 07:00 da manhã
        self.prazo_final = 840    # 14:00 da tarde
        self.itens_encontrados = []

    def formatar_tempo(self) -> str:
        """Converte os minutos totais no formato clássico de relógio HH:MM"""
        horas = self.tempo_minutos // 60
        minutos = self.tempo_minutos % 60
        return f"{horas:02d}:{minutos:02d}"

    def modificar_energia(self, quantidade: int):
        """Altera a energia garantindo os limites entre 0% e 100%"""
        self.energia = max(0, min(100, self.energia + quantidade))

    def modificar_dinheiro(self, quantidade: float):
        """Adiciona ou subtrai dinheiro da carteira"""
        self.dinheiro += quantidade

    def passar_tempo(self, minutos: int):
        """Avança o relógio do jogo"""
        self.tempo_minutos += minutos

    def coletar_item(self, nome_item: str):
        """Adiciona um item ao inventário se ele já não foi pego"""
        if nome_item not in self.itens_encontrados:
            self.itens_encontrados.append(nome_item)

    def checar_estado_jogo(self) -> str:
        """Analisa os números e define o destino do jogador"""
        if len(self.itens_encontrados) >= 3:
            return "VITORIA"
        if self.energia <= 0:
            return "DESMAIO"
        if self.tempo_minutos >= self.prazo_final:
            return "GAME_OVER_TEMPO"
        return "JOGANDO"