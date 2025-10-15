from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import PaginaBase
import time


class PaginaRenegociacao(PaginaBase):
    """
    Página de Renegociação de Contrato.
    Permite pesquisar, editar e calcular novas condições de renegociação.
    """
    
    _CAMPO_INPUT_CPF = (By.ID, "cpf")
    _CAMPO_DROPDOWN_STATUS_RENEGOCIACAO = (By.ID, "statusRenegociacao")
    _BOTAO_PESQUISAR = (By.XPATH, "//button[@type='submit']//span[contains(text(), 'Pesquisar')]")
    
    _PRIMEIRA_LINHA_TABELA_RESULTADOS = (By.CSS_SELECTOR, "tbody tr.mat-mdc-row:first-child")
    _BOTAO_EDITAR_PRIMEIRA_LINHA = (By.CSS_SELECTOR, "tbody tr.mat-mdc-row:first-child pp-button-small[tooltip='Editar Renegociação'] button")
    
    _CAMPO_INPUT_DATA_REFERENCIA = (By.ID, "dataReferencia")
    _CAMPO_INPUT_DATA_VENCIMENTO_PRIMEIRA_PRESTACAO = (By.ID, "dataVencimentoPrimeiraPrestacao")
    _CAMPO_DROPDOWN_FORMA_PAGAMENTO = (By.ID, "formaPagamento")
    _CAMPO_INPUT_MARGEM_CONSIGNAVEL = (By.ID, "margemConsignavel")
    _CAMPO_INPUT_PRESTACAO = (By.ID, "prestacao")
    _CAMPO_INPUT_PRAZO = (By.ID, "prazo")
    _CAMPO_INPUT_TAXA_JUROS = (By.ID, "taxaJuros")
    _CAMPO_INPUT_DESCONTO = (By.ID, "desconto")
    _CAMPO_INPUT_ENTRADA_RENEGOCIACAO = (By.ID, "entradaDeRenegociacao")
    _CAMPO_INPUT_DATA_ENTRADA = (By.ID, "dataEntrada")
    _BOTAO_CALCULAR = (By.XPATH, "//button[@type='submit']//span[contains(text(), 'Calcular')]")
    
    _TABELA_OPCOES_PARCELAMENTO = (By.CSS_SELECTOR, "tbody.mdc-data-table__content")
    _PRIMEIRA_OPCAO_COLUNA_PRAZO = (By.CSS_SELECTOR, "tbody.mdc-data-table__content tr:first-child td.cdk-column-prazo")
    _PRIMEIRA_OPCAO_COLUNA_PRESTACAO = (By.CSS_SELECTOR, "tbody.mdc-data-table__content tr:first-child td.cdk-column-prestacao")
    _TODAS_LINHAS_TABELA_OPCOES = (By.CSS_SELECTOR, "tbody.mdc-data-table__content tr.mat-mdc-row")
    
    def __init__(self, driver, configuracao=None):
        super().__init__(driver)
        self.configuracao = configuracao
        self.url_pagina = configuracao.url_renegociacao if configuracao else \
            "https://sistemacreditogestaowebteste.hml.cloud.poupex/renegociacao"
    
    def carregar_pagina(self):
        """Navega para a página de Renegociação e aguarda carregar"""
        self.driver.get(self.url_pagina)
        self._encontrar_elemento(self._CAMPO_INPUT_CPF)
        print(f"[PÁGINA] Renegociação carregada: {self.url_pagina}")
    
    def preencher_campo_cpf(self, cpf_cliente):
        """
        Preenche o campo CPF no filtro de pesquisa.
        
        Args:
            cpf_cliente: CPF no formato "000.000.000-00"
        """
        self.preencher_campo_texto(self._CAMPO_INPUT_CPF, cpf_cliente)
        print(f"[FILTRO] CPF preenchido: {cpf_cliente}")
    
    def selecionar_status_da_renegociacao(self, status_renegociacao):
        """
        Seleciona o status da renegociação no dropdown.
        
        Args:
            status_renegociacao: Texto do status (ex: "Calculada", "Em Implantação")
        """
        self.selecionar_opcao_dropdown(self._CAMPO_DROPDOWN_STATUS_RENEGOCIACAO, status_renegociacao)
        print(f"[FILTRO] Status selecionado: {status_renegociacao}")
    
    def clicar_botao_pesquisar(self):
        """Aciona o botão Pesquisar e aguarda resultados"""
        self.clicar_no_elemento(self._BOTAO_PESQUISAR)
        print("[AÇÃO] Botão Pesquisar clicado")
        time.sleep(1)
    
    def buscar_renegociacao_por_filtros(self, cpf_cliente, status_renegociacao):
        """
        Realiza busca completa preenchendo CPF e status.
        
        Args:
            cpf_cliente: CPF do cliente
            status_renegociacao: Status da renegociação
        """
        self.preencher_campo_cpf(cpf_cliente)
        self.selecionar_status_da_renegociacao(status_renegociacao)
        self.clicar_botao_pesquisar()
    
    def clicar_botao_editar_primeira_renegociacao(self):
        """Abre a primeira renegociação da lista em modo de edição"""
        self._encontrar_elemento(self._PRIMEIRA_LINHA_TABELA_RESULTADOS)
        self.clicar_no_elemento(self._BOTAO_EDITAR_PRIMEIRA_LINHA)
        print("[AÇÃO] Primeira renegociação aberta para edição")
        time.sleep(2)
    
    def preencher_campo_data_referencia(self, data_referencia):
        """
        Preenche a data de referência do cálculo.
        
        Args:
            data_referencia: Data no formato DD/MM/YYYY (ex: "15/10/2025")
        """
        elemento_data = self._encontrar_elemento(self._CAMPO_INPUT_DATA_REFERENCIA)
        elemento_data.clear()
        
        for _ in range(10):
            elemento_data.send_keys(Keys.BACKSPACE)
        
        elemento_data.send_keys(data_referencia)
        print(f"[FORMULÁRIO] Data de referência: {data_referencia}")
    
    def preencher_campo_data_vencimento_primeira_prestacao(self, data_vencimento):
        """
        Preenche a data de vencimento da primeira prestação.
        
        Args:
            data_vencimento: Data no formato DD/MM/YYYY (ex: "14/11/2025")
        """
        elemento_data = self._encontrar_elemento(self._CAMPO_INPUT_DATA_VENCIMENTO_PRIMEIRA_PRESTACAO)
        elemento_data.clear()
        
        for _ in range(10):
            elemento_data.send_keys(Keys.BACKSPACE)
        
        elemento_data.send_keys(data_vencimento)
        print(f"[FORMULÁRIO] Data vencimento 1ª prestação: {data_vencimento}")
    
    def preencher_ambas_datas(self, data_referencia, data_vencimento):
        """
        Preenche data de referência e data de vencimento em sequência.
        
        Args:
            data_referencia: Data de referência (DD/MM/YYYY)
            data_vencimento: Data de vencimento da primeira prestação (DD/MM/YYYY)
        """
        self.preencher_campo_data_referencia(data_referencia)
        self.preencher_campo_data_vencimento_primeira_prestacao(data_vencimento)
    
    def selecionar_forma_de_pagamento(self, forma_pagamento):
        """
        Seleciona a forma de pagamento no dropdown.
        
        Args:
            forma_pagamento: Texto da forma (ex: "Pix", "Consignado")
        """
        self.selecionar_opcao_dropdown(self._CAMPO_DROPDOWN_FORMA_PAGAMENTO, forma_pagamento)
        print(f"[FORMULÁRIO] Forma de pagamento: {forma_pagamento}")
    
    def preencher_campo_margem_consignavel(self, valor_margem):
        """
        Preenche o valor da margem consignável.
        
        Args:
            valor_margem: Valor em formato texto (ex: "150,00")
        """
        self.preencher_campo_texto(self._CAMPO_INPUT_MARGEM_CONSIGNAVEL, valor_margem)
        print(f"[FORMULÁRIO] Margem consignável: {valor_margem}")
    
    def preencher_campo_prestacao(self, valor_prestacao):
        """
        Preenche o valor da prestação.
        
        Args:
            valor_prestacao: Valor em formato texto (ex: "1,30")
        """
        self.preencher_campo_texto(self._CAMPO_INPUT_PRESTACAO, valor_prestacao)
        print(f"[FORMULÁRIO] Prestação: {valor_prestacao}")
    
    def preencher_campo_prazo(self, quantidade_meses):
        """
        Preenche a quantidade de meses (prazo).
        
        Args:
            quantidade_meses: Número de meses em formato texto (ex: "12")
        """
        self.preencher_campo_texto(self._CAMPO_INPUT_PRAZO, quantidade_meses)
        print(f"[FORMULÁRIO] Prazo: {quantidade_meses} meses")
    
    def preencher_campo_taxa_juros(self, valor_taxa):
        """
        Preenche a taxa de juros.
        
        Args:
            valor_taxa: Taxa em formato texto (ex: "1,72")
        """
        self.preencher_campo_texto(self._CAMPO_INPUT_TAXA_JUROS, valor_taxa)
        print(f"[FORMULÁRIO] Taxa de juros: {valor_taxa}")
    
    def limpar_campo_por_nome(self, nome_campo):
        """
        Limpa um campo específico do formulário.
        
        Args:
            nome_campo: Nome do campo a ser limpo
        """
        mapeamento_campos = {
            "Desconto": self._CAMPO_INPUT_DESCONTO,
            "Entrada de Renegociação": self._CAMPO_INPUT_ENTRADA_RENEGOCIACAO,
            "Data Entrada": self._CAMPO_INPUT_DATA_ENTRADA
        }
        
        localizador_campo = mapeamento_campos.get(nome_campo)
        if not localizador_campo:
            raise ValueError(f"Campo '{nome_campo}' não mapeado para limpeza")
        
        elemento_campo = self._encontrar_elemento(localizador_campo)
        elemento_campo.clear()
        
        for _ in range(3):
            elemento_campo.send_keys(Keys.BACKSPACE)
        
        print(f"[FORMULÁRIO] Campo '{nome_campo}' limpo")
    
    def clicar_botao_calcular(self):
        """Aciona o botão Calcular e aguarda processamento"""
        self.clicar_no_elemento(self._BOTAO_CALCULAR)
        print("[AÇÃO] Botão Calcular acionado")
        time.sleep(2)
    
    def verificar_se_tabela_opcoes_esta_visivel(self):
        """
        Verifica se a tabela de opções de parcelamento está visível.
        
        Returns:
            True se visível, False caso contrário
        """
        visibilidade = self.elemento_esta_visivel(self._TABELA_OPCOES_PARCELAMENTO)
        
        if visibilidade:
            print("[VALIDACAO] [OK] Tabela de opcoes visivel")
        else:
            print("[VALIDACAO] [ERRO] Tabela de opcoes NAO visivel")
        
        return visibilidade
    
    def obter_prazo_da_primeira_opcao(self):
        """
        Obtém o prazo (em meses) da primeira opção da tabela.
        
        Returns:
            Texto do prazo (ex: "13")
        """
        prazo = self.obter_texto_do_elemento(self._PRIMEIRA_OPCAO_COLUNA_PRAZO)
        print(f"[RESULTADO] Prazo da 1ª opção: {prazo}")
        return prazo
    
    def obter_prestacao_da_primeira_opcao(self):
        """
        Obtém o valor da prestação da primeira opção da tabela.
        
        Returns:
            Texto da prestação (ex: "R$ 1,30")
        """
        prestacao = self.obter_texto_do_elemento(self._PRIMEIRA_OPCAO_COLUNA_PRESTACAO)
        print(f"[RESULTADO] Prestação da 1ª opção: {prestacao}")
        return prestacao
    
    def buscar_opcao_especifica_na_tabela(self, prazo_esperado, prestacao_esperada, taxas_esperadas):
        """
        Busca uma opção específica na tabela de parcelamento.
        
        Args:
            prazo_esperado: Prazo em meses (ex: "13")
            prestacao_esperada: Valor da prestação (ex: "R$ 1,30")
            taxas_esperadas: Valor das taxas (ex: "R$ 1,84")
            
        Returns:
            True se a opção foi encontrada, False caso contrário
        """
        time.sleep(1)
        todas_linhas = self._encontrar_elementos(self._TODAS_LINHAS_TABELA_OPCOES)
        
        prestacao_normalizada = prestacao_esperada.replace(" ", "").replace("R$", "R$\u00a0")
        taxas_normalizadas = taxas_esperadas.replace(" ", "").replace("R$", "R$\u00a0")
        
        for idx, linha in enumerate(todas_linhas, 1):
            try:
                prazo_celula = linha.find_element(By.CSS_SELECTOR, "td.cdk-column-prazo").text.strip()
                taxas_celula = linha.find_element(By.CSS_SELECTOR, "td.cdk-column-taxas").text.strip()
                prestacao_celula = linha.find_element(By.CSS_SELECTOR, "td.cdk-column-prestacao").text.strip()
                
                prazo_corresponde = (prazo_celula == prazo_esperado)
                prestacao_corresponde = (prestacao_normalizada in prestacao_celula or prestacao_esperada in prestacao_celula)
                taxas_correspondem = (taxas_normalizadas in taxas_celula or taxas_esperadas in taxas_celula)
                
                if prazo_corresponde and prestacao_corresponde and taxas_correspondem:
                    print(f"[VALIDACAO] [OK] Opcao encontrada - Prazo: {prazo_esperado}, Prestacao: {prestacao_esperada}, Taxas: {taxas_esperadas}")
                    return True
                    
            except Exception:
                continue
        
        print(f"[VALIDACAO] [ERRO] Opcao NAO encontrada - Prazo: {prazo_esperado}, Prestacao: {prestacao_esperada}, Taxas: {taxas_esperadas}")
        return False
