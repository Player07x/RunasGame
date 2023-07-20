import montros as mon


class Npc(mon.Monstro):
    def __init__(self):
        super().__init__()
        self.tipo = ''

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

