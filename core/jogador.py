import random

class Jogador:
    """Representa o estado do jogador, incluindo energia, dinheiro, tempo e itens coletados"""
    def __init__(self):
        self.energia = 50
        self.dinheiro = 15.00
        self.tempo_minutos = 420  
        self.prazo_final = 840    
        self.itens_encontrados = []
        
        # Sorteia o início da chuva para algum momento entre 07:30 (450) e 11:00 (660)
        self.inicio_chuva = random.randint(450, 660)
        
        # Sorteia a duração exata da chuva com base nos períodos definidos
        duracao_chuva = random.choice([30, 60, 120, 150])
        self.fim_chuva = self.inicio_chuva + duracao_chuva
        
        # Controle de mensagens de transição do clima
        self.avisou_inicio_chuva = False
        self.avisou_fim_chuva = False

    def esta_chovendo(self) -> bool:
        """Verifica se o relógio atual do jogo está dentro do período de chuva"""
        return self.inicio_chuva <= self.tempo_minutos <= self.fim_chuva

    def checar_alertas_clima(self) -> str:
        """Gera uma mensagem extra caso o clima tenha acabado de mudar"""
        if self.esta_chovendo() and not self.avisou_inicio_chuva:
            self.avisou_inicio_chuva = True
            return "\n\n⛈️ O TEMPO FECHOU! Começou a chover forte na Rural."
        
        if self.tempo_minutos > self.fim_chuva and not self.avisou_fim_chuva:
            self.avisou_fim_chuva = True
            return "\n\n⛅ A chuva parou! O clima voltou ao normal."
            
        return ""

    def formatar_tempo(self) -> str:
        """Converte os minutos totais no formato relógio"""
        horas = self.tempo_minutos // 60
        minutos = self.tempo_minutos % 60
        return f"{horas:02d}:{minutos:02d}"

    def modificar_energia(self, quantidade: int):
        """Altera a energia garantindo os limites entre 0% e 100%"""
        self.energia = max(0, min(100, self.energia + quantidade))

    def modificar_dinheiro(self, quantidade: float):
        """Adiciona ou subtrai dinheiro da carteira"""
        self.dinheiro += float(quantidade)

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
