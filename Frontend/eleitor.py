"""Compatibilidade para código antigo: dados de eleitores vivem no backend."""

from Backend.eleitor import eleitores


class Eleitor:
    def __init__(self):
        self.eleitores = eleitores
