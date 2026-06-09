# nó de árvore (binária) genealógica ascendente

class NooArvGenAsc:
    def __init__(self, val: str):
        self._nome: str = val
        self._mae = None
        self._pai = None

    # --- Seletores (Getters) ---
    @property
    def nome(self) -> str:
        return self._nome

    @property
    def mae(self):
        return self._mae

    @property
    def pai(self):
        return self._pai

    # --- Modificadores (Setters) ---
    @mae.setter
    def mae(self, noo):
        self._mae = noo

    @pai.setter
    def pai(self, noo):
        self._pai = noo