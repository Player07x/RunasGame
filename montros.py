from math import floor

from colorama import Fore

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
    def randomAlvo(jogador, alvos: list):
        list_alvos = [jogador]
        for alvo in alvos:
            if alvo.status_atual['PV'] > 0:
                list_alvos.append(alvo)
        alvo = choice(list_alvos)
        return alvo

    def randomAtaque(self, alvo, aliado=False):
        ataque = choice(self.ataques)
        cor = Fore.RED
        if aliado is True:
            cor = Fore.BLUE
        msg = cor+f'{self.info["nome"]} atacou {alvo.info["nome"]} com um ataque de' \
                              f' {ataque["Nome"]}.'+Fore.RESET

        print(msg)
        ob.combate.atacar(ataque, alvo, self)

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



