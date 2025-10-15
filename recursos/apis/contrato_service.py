import requests
import copy
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ServicoContrato:
    """
    Serviço para interagir com a API de Contratos.
    Permite criar, consultar e manipular contratos via chamadas HTTP.
    Suporta modo mock para testes sem dependência da API real.
    """
    
    def __init__(self, configuracao=None, modo_mock=None):
        """
        Inicializa o serviço de contratos.
        
        Args:
            configuracao: Instância de GerenciadorDeConfiguracao (opcional)
            modo_mock: Sobrescreve configuração de modo mock (opcional)
        """
        if configuracao:
            self.url_base_api = configuracao.url_api_base
            self.modo_mock = modo_mock if modo_mock is not None else configuracao.api_modo_mock
            self.verificar_ssl = configuracao.api_verificar_ssl
            self.token_autenticacao = configuracao.api_token
        else:
            self.url_base_api = "https://sistemacreditogestaowebteste.hml.cloud.poupex/api"
            self.modo_mock = modo_mock if modo_mock is not None else True
            self.verificar_ssl = False
            self.token_autenticacao = ""
        
        self.sessao_http = requests.Session()
        self.sessao_http.verify = self.verificar_ssl
        
        if self.token_autenticacao:
            self.sessao_http.headers.update({
                'Authorization': f'Bearer {self.token_autenticacao}'
            })
        
        print(f"[API] Serviço inicializado - Modo Mock: {self.modo_mock}")

    def obter_payload_padrao_contrato(self):
        """
        Retorna um payload padrão válido para criação de contrato via API.
        Este payload contém todos os campos necessários com valores de exemplo.
        
        Returns:
            Dicionário com estrutura completa do contrato
        """
        return {
            "idPessoa": 1,
            "idMatriculaFuncional": 1,
            "dataContratacao": "08/01/2025",
            "dataLiberacao": "10/01/2025",
            "dataPrimeiraPrestacao": "05/03/2025",
            "valorCredito": 10500,
            "valorIOF": 39.9,
            "valorFinanciamento": 39.9,
            "valorTotalJuros": 50,
            "valorProRata": 40,
            "taxaJuros": 1.79,
            "prazo": 72,
            "valorPrestacao": 450.5,
            "valorCET": 60,
            "diaVencimento": 5,
            "formaLiberacao": 2,
            "subProduto": {"id": 1},
            "tipoAssociado": "Militares Ativos",
            "segmento": {"codigoSegmento": 3},
            "formaPagamento": {"id": 1},
            "classificacaoRisco": "A",
            "situacaoContrato": 1, # 1 = Normal, conforme Gherkin
            "origemContrato": 3,
            "origemCanalVenda": 3,
            "usuarioImplatacao": "AutomacaoBehave",
            "utaUsuarioImplantacao": "AUT",
            "numeroContratoAnterior": None,
            "rubrica": "Rubrica Teste",
            "codigoGrupoHomogeneo": 1,
            "scoreGrupoHomogeneo": 100.2
        }

    def criar_contrato(self, **campos_personalizados):
        """
        Cria um novo contrato via API (ou retorna mock se configurado).
        
        Args:
            **campos_personalizados: Campos do payload a serem sobrescritos
                Exemplo: criar_contrato(situacaoContrato=4, prazo=36)
        
        Returns:
            Dicionário com resposta da API ou dados mockados
            
        Raises:
            requests.exceptions.RequestException: Em caso de erro na chamada HTTP
        """
        if self.modo_mock:
            return self._criar_contrato_mockado(**campos_personalizados)
        else:
            return self._criar_contrato_real(**campos_personalizados)
    
    def _criar_contrato_mockado(self, **campos_personalizados):
        """Retorna dados mockados sem chamar a API"""
        print("[API-MOCK] Retornando dados mockados (API não será chamada)")
        
        resposta_mock = {
            "id": 1,
            "cpf": "015.107.737-11",
            "numeroContrato": "00000001-8",
            "situacaoContrato": campos_personalizados.get("situacaoContrato", 1),
            "status": "Contrato mockado com sucesso"
        }
        
        print(f"[API-MOCK] ✓ Contrato mockado - ID: {resposta_mock['id']}, CPF: {resposta_mock['cpf']}")
        return resposta_mock
    
    def _criar_contrato_real(self, **campos_personalizados):
        """Cria contrato via chamada real à API"""
        endpoint_completo = f"{self.url_base_api}/contrato"
        payload_base = self.obter_payload_padrao_contrato()
        payload_final = copy.deepcopy(payload_base)
        payload_final.update(campos_personalizados)
        
        print(f"[API] POST {endpoint_completo}")
        print(f"[API] Payload: {payload_final}")
        
        try:
            resposta = self.sessao_http.post(endpoint_completo, json=payload_final)
            resposta.raise_for_status()
            
            dados_resposta = resposta.json()
            print(f"[API] ✓ Contrato criado - ID: {dados_resposta.get('id')}")
            
            return dados_resposta
            
        except requests.exceptions.RequestException as erro:
            print(f"[API] ✗ Erro ao criar contrato: {erro}")
            
            if hasattr(erro, 'response') and erro.response is not None:
                print(f"[API] Resposta do servidor: {erro.response.text}")
            
            raise
