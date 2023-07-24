from math import ceil, floor
from random import randint
import hud


class Combate:
    @staticmethod
    def atacar(ataque, alvo, atacante):
        if ataque['Tipo'] in ['cortante', 'perfurante', 'concussão']:
            resultado = Combate.testeHabilidade('FISICO', 'des', atacante)
            # Verifica se o alvo acertou o ataque
            sem_escudo = True
            if resultado[0] == 'sucesso':
                try:
                    if alvo.equipamento['escudo'] is not None and alvo.equipamento['escudo']['PR'] > 0:
                        sem_escudo = False
                        res = hud.Hud.hudChoice('Esquiva',
                                                f"Bloqueio\n Seu Escudo: {alvo.equipamento['escudo']['Nome']} "
                                                f"({alvo.equipamento['escudo']['PR']} PRs)",
                                                texto='Como deseja se defender desse ataque?')
                        match res[0]:
                            case 1:
                                resultado = Combate.testeHabilidade('FISICO', 'des', alvo, resultado[1], defesa=True)
                                Combate.esquiva(resultado, ataque, alvo, atacante)
                            case 2:
                                Combate.bloqueio(alvo, alvo.equipamento['escudo'], ataque)
                except TypeError:
                    pass
                if sem_escudo is True:
                    # Verifica se o oponente se defendeu do ataque
                    resultado = Combate.testeHabilidade('FISICO', 'des', alvo, resultado[1], defesa=True)
                    Combate.esquiva(resultado, ataque, alvo, atacante)
            else:
                print(f'{atacante.info["nome"]} errou o ataque...\n')
        else:
            Combate.danoMagico(alvo, ataque['Dano'], ataque['Tipo'], dano_bonus=atacante.atributos_s['pod'])

    @staticmethod
    def esquiva(resultado, ataque, alvo, atacante):
        if resultado[0] == 'fracasso':
            Combate.danoFisico(alvo, ataque['Dano'], ataque['Tipo'], ataque['Efeitos'], dano_bonus=atacante.atributos_s[
                'for'])
        else:
            print(f'{alvo.info["nome"]} esquivou do ataque...\n')

    @staticmethod
    def bloqueio(bloqueador, escudo, ataque):
        dano = Combate.danoAleatorio(ataque['Dano']) - escudo['RD']
        if dano > 0:
            escudo['PR'] -= dano
            if escudo['PR'] < 0:
                escudo['PR'] = 0
        print(f'{bloqueador.info["nome"]} bloqueou o ataque...\n')

    @staticmethod
    def testeResistindo(atributo_p, atributo_s, alvo, oponente):
        res_oponente = None
        res_alvo = Combate.testeHabilidade('FISICO', 'des', alvo)
        if res_alvo[0] == 'sucesso':
            res_oponente = Combate.testeHabilidade('FISICO', 'des', oponente)
            if res_oponente[1] > res_alvo[1]:
                return 'sucesso', res_oponente, res_alvo
            else:
                return 'fracasso', res_oponente, res_alvo
        else:
            return 'fracasso', res_oponente, res_alvo

    @staticmethod
    def testeHabilidade(atributo_p, atributo_s, alvo, bonus=0, defesa=False):
        if defesa is True:
            teste = floor((alvo.atributos_s[atributo_s] + alvo.atributos_p[atributo_p])/2) + bonus

        else:
            teste = alvo.atributos_s[atributo_s] + alvo.atributos_p[atributo_p] + bonus

        resultado_teste = randint(1, 20)
        margem = resultado_teste - teste
        if teste >= resultado_teste:
            return 'sucesso', margem
        else:
            return 'fracasso', margem

    @staticmethod
    def danoGeral(alvo, dano):
        if alvo.status_atual['PA'] <= 0:
            alvo.status_atual['PV'] -= dano
        else:
            alvo.status_atual['PA'] -= dano
            dano_excedente = alvo.status_atual['PA']
            if alvo.status_atual['PA'] <= 0:
                alvo.status_atual['PA'] = 0
                alvo.status_atual['PV'] += ceil(dano_excedente / 2)

    @staticmethod
    def danoFisico(alvo, dano: list, tipo: str, efeito=None, dano_bonus=0):
        keep_life = alvo.status_atual['PV']
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
            hud.Hud.msgDano(alvo.info["nome"], dano, tipo)
        else:
            hud.Hud.msgDano(alvo.info["nome"], 0)
        if efeito is not None and efeito != []:
            match efeito[0]:
                case 'sangramento':
                    if keep_life > alvo.status_atual['PV']:
                        alvo.setEfeito(efeito)
                case _:
                    alvo.setEfeito(efeito)

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
                        alvo.status_atual['PV'] -= 2 * dano
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
                    case 'sangramento':
                        alvo.status_atual['PV'] -= efeito[1][0]
                hud.Hud.msgDano(alvo.info['nome'], efeito[1][0], efeito[1][1])
                dano = efeito[1][0] - alvo.status['RDM']
                if dano < 0:
                    dano = 0
                if efeito[2] <= 0:
                    alvo.efeitos.remove(efeito)
