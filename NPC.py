from random import choice

import montros as mon


class Npc(mon.Monstro):
    def __init__(self):
        super().__init__()
        self.tipo = ''
        self.situacao = 'Vivo'

    def setTipo(self, tipo):
        """
        :param tipo: [0:'Importante', 1:'NPC', 2:'Companion']
        :return:
        """
        tipos = ['Importante', 'NPC', 'Companion']
        if tipo in tipos:
            self.tipo = tipo
        elif type(tipo) is int:
            self.tipo = tipo[tipo]

    def setSituacao(self, situacao):
        """
        :param situacao: 'Vivo', 'Morto', 'Desmaiado'
        :return: None
        """
        self.situacao = situacao

    @staticmethod
    def randomAlvoAli(inimigos):
        if len(inimigos) > 1:
            alvo = choice(inimigos)
        else:
            alvo = inimigos[0]
        return alvo
