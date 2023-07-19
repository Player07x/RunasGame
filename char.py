"""
Essa classe é usado para criar qualquer personagem do jogo.
O personagem possui atributos_p que é um dicionário com os atributos Primários
Também possui atributos_s, que é um dicionário com os atrbutos Secundários
E também possui os status
"""


class Character:
    def __init__(self):
        self.atributos_p = {
            'FISICO': 0, 'MENTAL': 0, 'MISTICO': 0
        }
        self.atributos_s = {
            'for': 0, 'des': 0, 'vit': 0,
            'int': 0, 'con': 0, 'soc': 0,
            'fe': 0, 'pod': 0, 'sor': 0
        }
        self.status = {
            'PV': 0, 'PA': 0, 'PE': 0, 'RDF': 0, 'RDM': 0
        }
        self.status_atual = {
            'PV': 0, 'PA': 0, 'PE': 0
        }
        # 0:Nome, 1[0]:Dano, 1[1]:Tipo, 2:Duração
        # [['Efeito', [0, 'Tipo'], 0]]
        self.efeitos = []

        self.info = {'nome': 'Player'}

        self.equipamento = {'arma': None,
                            'magias': {
                                'slot1': None,
                                'slot2': None,
                                'slot3': None,
                                'slot4': None},
                            'armadura': {
                                'capacete': None,
                                'peitoral': None,
                                'manopla': None,
                                'bota': None}}

    def setAtributos(self, atributo_p: list, atributo_s: list = None):
        """
        :param atributo_p: [1, 2, 3]
        :param atributo_s: [1, 2, 3, 4, 5, 6, 7, 8, 9]
        :return: None
        """
        if atributo_s is None:
            atributo_s = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        num = 0
        for item in self.atributos_p:
            self.atributos_p[item] = atributo_p[num]
            num += 1
        num = 0
        for item in self.atributos_s:
            self.atributos_s[item] = atributo_s[num]
            num += 1

    def setStatus(self, RDF=0, RDM=0, atual=False):
        self.status['PV'] = self.atributos_p['FISICO'] + self.atributos_s['vit']
        self.status['PA'] = self.atributos_p['FISICO'] + self.atributos_s['pod']
        self.status['PE'] = self.atributos_p['MISTICO'] + self.atributos_s['pod']
        self.status['RDF'] = RDF
        self.status['RDM'] = RDM

        if atual is True:
            self.status_atual = self.status.copy()

    def setInfo(self, nome):
        self.info['nome'] = nome

    def setEquipamento(self, arma=None, magia=None, armadura=None):
        if arma is not None:
            self.equipamento['arma'] = arma
        if magia is not None:
            for num, mag in enumerate(magia):
                match num+1:
                    case 1:
                        self.equipamento['magias']['slot1'] = mag
                    case 2:
                        self.equipamento['magias']['slot2'] = mag
                    case 3:
                        self.equipamento['magias']['slot3'] = mag
                    case 4:
                        self.equipamento['magias']['slot4'] = mag
        if armadura is not None:
            self.equipamento['armadura'] = armadura

    def setEfeito(self, *efeito):
        for ef in efeito:
            self.efeitos.append(ef)
