import random

class Jogador:
    """Representa o estado do jogador, incluindo energia, dinheiro, tempo e itens coletados"""
    def __init__(self):
        self.energia = 50
        self.dinheiro = 15.00
        self.tempo_minutos = 420  
        self.prazo_final = 840    
        self.itens_encontrados = []       
        self.trufas = 5
        self.inicio_chuva = random.randint(450, 660)
        duracao_chuva = random.choice([60, 120, 150])
        self.fim_chuva = self.inicio_chuva + duracao_chuva
        self.avisou_inicio_chuva = False
        self.avisou_fim_chuva = False
        self.vai_ter_queda = random.choice([True])
        if self.vai_ter_queda:
            self.inicio_energia = random.randint(450, 700)
            self.fim_energia = self.inicio_energia + random.choice([40, 60, 120, 150])
        else:
            self.inicio_energia = -1
            self.fim_energia = -1
        self.avisou_queda_energia = False
        self.avisou_volta_energia = False

    def esta_chovendo(self) -> bool:
        """Verifica se o relógio atual do jogo está dentro do período de chuva"""
        return self.inicio_chuva <= self.tempo_minutos <= self.fim_chuva
    
    def esta_sem_energia(self) -> bool:
        """Verifica se o relógio atual está dentro do período de apagão"""
        if not self.vai_ter_queda:
            return False
        return self.inicio_energia <= self.tempo_minutos <= self.fim_energia

    def checar_alertas_clima(self) -> str:
        """Gera as mensagens de transição para clima e energia"""
        mensagem = ""
        
        if self.esta_chovendo() and not self.avisou_inicio_chuva:
            self.avisou_inicio_chuva = True
            mensagem += "\n\n⛈️ O TEMPO FECHOU! Começou a chover forte na Rural."
        
        if self.tempo_minutos > self.fim_chuva and not self.avisou_fim_chuva:
            self.avisou_fim_chuva = True
            mensagem += "\n\n⛅ A chuva parou! O clima voltou ao normal."

        if self.esta_sem_energia() and not self.avisou_queda_energia:
            self.avisou_queda_energia = True
            mensagem += "\n\n🔌 A ENERGIA CAIU! Algumas salas estão no escuro."
            
        if self.vai_ter_queda and self.tempo_minutos > self.fim_energia and not self.avisou_volta_energia:
            self.avisou_volta_energia = True
            mensagem += "\n\n💡 A energia voltou! Tudo iluminado novamente."      
        return mensagem

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

    def vender_trufas(self) -> str:
        """Processa a tentativa de venda de trufas seguindo regras estritas de custo e sorteio"""
        if self.trufas <= 0:
            return "Você não tem mais trufas para vender!"
        limite_sorteio = min(5, self.trufas)
        quantidade_vendida = random.randint(0, limite_sorteio)
        faturamento = quantidade_vendida * 1.50
        self.modificar_dinheiro(faturamento)
        self.passar_tempo(30)
        self.modificar_energia(-10)
        self.trufas -= quantidade_vendida
        return f"Você passou 30 minutos tentando vender suas trufas.\nResultado: Vendeu {quantidade_vendida} trufas e ganhou R$ {faturamento:.2f}.\nGastou 10 de energia. Restam {self.trufas} trufas."

    def checar_estado_jogo(self) -> str:
        """Analisa os números e define o destino do jogador"""
        if len(self.itens_encontrados) >= 3:
            return "VITORIA"
        if self.energia <= 0:
            return "DESMAIO"
        if self.tempo_minutos >= self.prazo_final:
            return "GAME_OVER_TEMPO"
        return "JOGANDO"
