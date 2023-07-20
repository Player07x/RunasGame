from math import floor

import char
from random import choice
from lib import objetos as ob


class Monstro(char.Character):
    def __init__(self):
        super().__init__()
        self.ataques = []
        self.xp = int
        self.descricao = str

    def setAtaques(self, ataques: list):
        self.ataques = ataques

    @staticmethod
    def randomAlvo(jogador, *alvos):
        alvo = choice(alvos)
        return alvo

    def randomAtaque(self, alvo):
        ataque = choice(self.ataques)
        if ataque['Tipo'] in ['cortante', 'perfurante', 'concussão']:
            print(f'{alvo.info["nome"]} foi alvo de um ataque de {ataque["Nome"]}.')
            ob.combate.danoFisico(alvo, ataque['Dano'], ataque['Tipo'], dano_bonus=self.atributos_s['for'])
        else:
            print(f'{alvo.info["nome"]} foi alvo de um ataque de {ataque["Nome"]}.')
            ob.combate.danoMagico(alvo, ataque['Dano'], ataque['Tipo'], dano_bonus=self.atributos_s['pod'])

    def setXP(self):
        valor = 0
        multiplicador = 0
        for c in self.atributos_s:
            valor += self.atributos_s[c]
        for c in self.atributos_p:
            multiplicador += self.atributos_p[c]

        self.xp = floor(((valor * multiplicador)-200)/10)

    def setDescricao(self, desc):
        self.descricao = desc



