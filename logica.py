# logica.py
# ===========================================
# Lógica do Sistema de Triagem Manchester
# ===========================================

from collections import deque


# ---------------------------
# CLASSES BÁSICAS
# ---------------------------
class NodoArvore:
    """Representa um nó da árvore de decisão de triagem."""
    def __init__(self, question=None, cor=None, yes=None, no=None):
        self.question = question
        self.cor = cor
        self.yes = yes
        self.no = no

    def is_leaf(self):
        return self.cor is not None


class Fila:
    """Fila FIFO para pacientes de uma determinada cor."""
    def __init__(self):
        self._data = deque()

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        return self._data.popleft() if self._data else None

    def __len__(self):
        return len(self._data)


# ---------------------------
# MONTAR ÁRVORE DE TRIAGEM
# ---------------------------
def montar_arvore():
    """Cria a árvore de decisão simplificada do Protocolo de Manchester."""
    vermelho = NodoArvore(cor="Vermelho")
    laranja = NodoArvore(cor="Laranja")
    amarelo = NodoArvore(cor="Amarelo")
    verde = NodoArvore(cor="Verde")
    azul = NodoArvore(cor="Azul")

    nao_urgente = NodoArvore(
        "A queixa é claramente não urgente (ex.: pedido de receita, atestado)?",
        yes=azul,
        no=verde
    )

    dor_intensa = NodoArvore(
        "Está com dor intensa?",
        yes=amarelo,
        no=nao_urgente
    )

    consciente = NodoArvore(
        "Está consciente?",
        yes=dor_intensa,
        no=laranja
    )

    raiz = NodoArvore(
        "Está respirando?",
        yes=consciente,
        no=vermelho
    )

    return raiz


# ---------------------------
# FUNÇÃO DE TRIAGEM
# ---------------------------
def triagem_por_respostas(arvore, respostas):
    """
    Executa a triagem automaticamente com base em uma lista de respostas booleanas.
    True -> Sim, False -> Não
    Retorna a cor correspondente.
    """
    nodo = arvore
    for resposta in respostas:
        if nodo.is_leaf():
            break
        nodo = nodo.yes if resposta else nodo.no
    while not nodo.is_leaf():
        nodo = nodo.no  # fallback caso faltem respostas
    return nodo.cor
