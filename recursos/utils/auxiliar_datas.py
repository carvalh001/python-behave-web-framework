from datetime import datetime, timedelta


class AuxiliarDatas:
    """
    Classe auxiliar para cálculos e manipulação de datas.
    Fornece métodos estáticos para gerar datas dinâmicas comumente usadas em testes.
    """
    
    @staticmethod
    def obter_dia_posterior():
        """
        Calcula a data do dia seguinte ao dia atual.
        Útil para campos que exigem datas futuras.
        
        Returns:
            Data do próximo dia no formato DD/MM/YYYY (ex: "16/10/2025")
        """
        data_amanha = datetime.now() + timedelta(days=1)
        return data_amanha.strftime("%d/%m/%Y")
    
    @staticmethod
    def obter_data_um_mes_e_dois_dias():
        """
        Calcula uma data com 1 mês e 2 dias a partir de hoje.
        Utiliza aproximação de 30 dias para 1 mês, totalizando 32 dias.
        
        Returns:
            Data futura no formato DD/MM/YYYY (ex: "16/11/2025")
        """
        data_futura = datetime.now() + timedelta(days=32)
        return data_futura.strftime("%d/%m/%Y")
    
    @staticmethod
    def obter_data_com_deslocamento(quantidade_dias=0, quantidade_meses=0):
        """
        Calcula uma data com deslocamento personalizado a partir de hoje.
        Permite adicionar ou subtrair dias e meses.
        
        Args:
            quantidade_dias: Número de dias a adicionar (negativo para subtrair)
            quantidade_meses: Número de meses a adicionar (aproximado: 1 mês = 30 dias)
        
        Returns:
            Data calculada no formato DD/MM/YYYY
        """
        total_dias = quantidade_dias + (quantidade_meses * 30)
        data_calculada = datetime.now() + timedelta(days=total_dias)
        return data_calculada.strftime("%d/%m/%Y")
    
    @staticmethod
    def obter_data_atual():
        """
        Retorna a data atual do sistema.
        
        Returns:
            Data de hoje no formato DD/MM/YYYY
        """
        return datetime.now().strftime("%d/%m/%Y")
    
    @staticmethod
    def obter_data_atual_com_horario():
        """
        Retorna a data e hora atual do sistema.
        
        Returns:
            Data e hora no formato DD/MM/YYYY HH:MM:SS
        """
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    @staticmethod
    def converter_data_para_formato_api(data_brasileira: str) -> str:
        """
        Converte data do formato brasileiro (DD/MM/YYYY) para formato API (YYYY-MM-DD).
        
        Args:
            data_brasileira: Data no formato DD/MM/YYYY
            
        Returns:
            Data no formato YYYY-MM-DD
        """
        data_obj = datetime.strptime(data_brasileira, "%d/%m/%Y")
        return data_obj.strftime("%Y-%m-%d")

