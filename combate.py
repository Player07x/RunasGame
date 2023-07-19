from math import ceil, floor
from random import randint
import hud


class Combate:
    @staticmethod
    def danoGeral(alvo, dano):
        if alvo.status_atual['PA'] <= 0:
            alvo.status_atual['PV'] -= dano
        else:
            alvo.status_atual['PA'] -= dano
            dano_excedente = alvo.status_atual['PA']
            if alvo.status_atual['PA'] <= 0:
                alvo.status_atual['PA'] = 0
                alvo.status_atual['PV'] += ceil(dano_excedente/2)

    @staticmethod
    def danoFisico(alvo, dano: list, tipo: str, efeito=None, dano_bonus=0):
        if len(dano) > 1:
            dano = Combate.danoAleatorio(dano)
        dano += dano_bonus
        dano -= alvo.status['RDF']
        if dano > 0:
            match tipo:
                case 'cortante':
                    Combate.danoGeral(alvo, dano)
                case 'perfurante':
                    if alvo.status_atual['PA'] > 0:
                        Combate.danoGeral(alvo, ceil(dano / 2))
                        alvo.status_atual['PV'] -= floor(dano / 2)
                    else:
                        alvo.status_atual['PV'] -= dano
                case 'concussão':
                    alvo.status_atual['PV'] -= dano
            hud.Hud.msgDano(alvo.info["nome"], tipo)
        else:
            hud.Hud.msgDano(alvo.info["nome"], 0)

    @staticmethod
    def danoMagico(alvo, dano: list, tipo: str, efeito=None, dano_bonus=0):
        if len(dano) > 1:
            dano = Combate.danoAleatorio(dano)
        else:
            dano = dano[0]
        dano += dano_bonus
        dano -= alvo.status['RDM']
        if dano > 0:
            match tipo:
                case 'ácido':
                    if alvo.status_atual['PA'] <= 0:
                        alvo.status_atual['PV'] -= 2*dano
                    else:
                        alvo.status_atual['PA'] -= dano
                        dano_excedente = alvo.status_atual['PA']
                        if alvo.status_atual['PA'] <= 0:
                            alvo.status_atual['PA'] = 0
                            alvo.status_atual['PV'] += dano_excedente
                case _:
                    Combate.danoGeral(alvo, dano)
            hud.Hud.msgDano(alvo.info["nome"], dano, tipo)
        if efeito is not None:
            alvo.setEfeito(efeito)

    @staticmethod
    def danoAleatorio(dano: list):
        dano_final = randint(dano[0], dano[1])
        return dano_final

    @staticmethod
    def aplicarEfeitos(alvo):
        for efeito in alvo.efeitos:
            if efeito[2] <= 0:
                alvo.efeitos.remove(efeito)
            else:
                print(f'{alvo.info["nome"]} foi afetado por {efeito[0]}.')
                match efeito[0]:
                    case 'incendiar':
                        if alvo.status_atual['PA'] > 0:
                            Combate.danoMagico(alvo, [efeito[1][0]], 'fogo')
                            if alvo.status_atual['PA'] == 0:
                                index = alvo.efeitos.index(efeito)
                                alvo.efeitos[index][2] = 0
                            else:
                                index = alvo.efeitos.index(efeito)
                                alvo.efeitos[index][2] -= 1
                        else:
                            Combate.danoMagico(alvo, [efeito[1][0]], 'fogo')
                    case 'eletrizar':
                        if alvo.status_atual['PA'] > 0:
                            Combate.danoMagico(alvo, [efeito[1][0]], 'elétrico')
                        else:
                            Combate.danoMagico(alvo, [efeito[1][0]], 'elétrico')
                            index = alvo.efeitos.index(efeito)
                            alvo.efeitos[index][2] = 0
                dano = efeito[1][0] - alvo.status['RDM']
                if dano < 0:
                    dano = 0
                if efeito[2] <= 0:
                    alvo.efeitos.remove(efeito)
