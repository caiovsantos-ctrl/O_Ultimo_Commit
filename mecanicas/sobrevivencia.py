class GerenciadorSobrevivencia:
    """Gerencia as ações de sobrevivência do jogador, incluindo compra de comida"""
    def __init__(self):
        self.cardapio = {
            "RU": {"preco": 3.50, "tempo": 50, "energia": 50, "sucesso_msg": "Você mofou na fila do RU, mas conseguiu! (+50⚡, -50⏰)"},
            "Lanchonete": {"preco": 7.00, "tempo": 10, "energia": 40, "sucesso_msg": "Salgado caro na Lanchonete, mas foi rápido! (+40⚡, -10⏰)"}
        }

    def comprar_comida(self, jogador, tipo: str) -> tuple[str, bool]:
        """Permite ao jogador comprar comida para recuperar energia, aplicando custos de tempo e dinheiro"""
        if tipo not in self.cardapio:
            return "Tipo de comida inválido.", False          
        info = self.cardapio[tipo]        
        if jogador.dinheiro < info["preco"]:
            if tipo == "RU":
                return "Sem dinheiro até para o RU! A humilhação é real.", False
            return "Dinheiro insuficiente para a lanchonete! Esse salgado gourmet não é para o seu bico.", False           
        jogador.modificar_dinheiro(-info["preco"])
        jogador.passar_tempo(info["tempo"])
        jogador.modificar_energia(info["energia"])       
        return info["sucesso_msg"], True
