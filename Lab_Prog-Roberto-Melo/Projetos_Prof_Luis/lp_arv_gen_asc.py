# árvore (binária) genealógica ascendente
from lp_noo_arv_gen_asc import NooArvGenAsc

class ArvGenAsc:
    def __init__(self, noo: NooArvGenAsc = None):
        self._raiz = noo

    # --- Travessia Em-Ordem ---
    def in_ord_trav(self) -> list:
        def em_ordem(aga: NooArvGenAsc):
            if aga is None:
                return []
            else:
                em_ordem(aga._pai)
                visit.append(aga._nome)
                em_ordem(aga._mae)

        visit: list = []
        em_ordem(self._raiz)
        return visit

    # --- Método auxiliar para procurar um nó recursivamente pelo nome ---
    def _procurar_no(self, atual: NooArvGenAsc, nome: str) -> NooArvGenAsc:
        if atual is None:
            return None
        if atual.nome == nome:
            return atual
        
        # Procura no lado do pai e da mãe
        no_pai = self._procurar_no(atual.pai, nome)
        if no_pai:
            return no_pai
        return self._procurar_no(atual.mae, nome)

    # --- Pesquisa 1: Obter nome dos pais de alguém ---
    def obter_pais(self, nome_pessoa: str) -> tuple:
        """Retorna (Nome da Mãe, Nome do Pai) ou None se não tiver pais mapeados."""
        no = self._procurar_no(self._raiz, nome_pessoa)
        if no and no.mae and no.pai:
            return (no.mae.nome, no.pai.nome)
        return None

    # --- Pesquisa 2: Obter ascendentes por Grau (Recursivo) ---
    def obter_ascendentes_por_grau(self, nome_pessoa: str, grau: int) -> list:
        """Retorna uma lista com os ascendentes de um determinado grau (1=pais, 2=avós, etc.)"""
        no_inicial = self._procurar_no(self._raiz, nome_pessoa)
        if not no_inicial:
            return []

        def buscar_por_grau(atual: NooArvGenAsc, grau_atual: int) -> list:
            if atual is None:
                return []
            if grau_atual == grau:
                return [atual.nome]
            
            # Vai subindo na árvore (grau_atual + 1)
            return buscar_por_grau(atual.pai, grau_atual + 1) + buscar_por_grau(atual.mae, grau_atual + 1)

        # Começa a busca a partir dos pais (Grau 1)
        return buscar_por_grau(no_inicial.pai, 1) + buscar_por_grau(no_inicial.mae, 1)
    
    # --- Pesquisa 3: Obter TODOS os ascendentes de uma pessoa em-ordem ---
    def obter_todos_ascendentes(self, nome_pessoa: str) -> list:
        """
        Procura uma pessoa e devolve uma lista com TODOS os seus ascendentes 
        pela ordem da travessia em-ordem (Pai -> Pessoa -> Mãe).
        """
        no_inicial = self._procurar_no(self._raiz, nome_pessoa)
        if not no_inicial:
            return []

        def recolher_em_ordem(atual: NooArvGenAsc):
            if atual is None:
                return []
            # Recolhe subárvore do pai, depois o nó atual, depois a subárvore da mãe
            return recolher_em_ordem(atual.pai) + [atual.nome] + recolher_em_ordem(atual.mae)

        # Recolhemos a árvore a partir do nó da pessoa encontrada
        resultado = recolher_em_ordem(no_inicial)
        
        # Como o método inclui o próprio nome da pessoa, podemos removê-lo 
        # para mostrar estritamente os *ascendentes*
        if nome_pessoa in resultado:
            resultado.remove(nome_pessoa)
            
        return resultado


# --- Função para Construir a Árvore a partir do Ficheiro ---
def construir_arvore_de_ficheiro(caminho_ficheiro: str) -> ArvGenAsc:
    dados = {}
    filhos = set()
    pais_e_maes = set()

    # 1. Ler o ficheiro e guardar a estrutura de dicionário
    with open(caminho_ficheiro, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            partes = [p.strip() for p in linha.split(',')]
            
            # Validar que a linha tem os 3 elementos (Grau 2 ou 0 - Sem nós de grau 1)
            if len(partes) == 3 and partes[1] != "" and partes[2] != "":
                pessoa, mae, pai = partes
                dados[pessoa] = (mae, pai)
                filhos.add(pessoa)
                pais_e_maes.add(mae)
                pais_e_maes.add(pai)

    if not dados:
        return ArvGenAsc()

    # 2. Encontrar a raiz (a pessoa que é filho(a) mas não é pai/mãe de ninguém no ficheiro)
    raiz_nome = (filhos - pais_e_maes)
    if raiz_nome:
        raiz_nome = list(raiz_nome)[0]
    else:
        raiz_nome = list(dados.keys())[0] # Fallback caso seja circular

    # 3. Construção recursiva da árvore
    def construir_no_recursivo(nome: str) -> NooArvGenAsc:
        no = NooArvGenAsc(nome)
        if nome in dados:
            mae_nome, pai_nome = dados[nome]
            # Cria recursivamente as subárvores
            no.mae = construir_no_recursivo(mae_nome)
            no.pai = construir_no_recursivo(pai_nome)
        return no

    raiz_no = construir_no_recursivo(raiz_nome)
    return ArvGenAsc(raiz_no)