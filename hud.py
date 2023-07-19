from colorama import Fore
from math import floor, ceil
from time import sleep
from lib import objetos as ob


class Hud:
    @staticmethod
    def lifeHud(char, inimigo=False):
        if inimigo is True:
            print(f'{char.info["nome"].upper()} | RDF: {char.status["RDF"]}, RDM: {char.status["RDM"]}')

        # =================[Barra dos PVs]===========================
        barra_var = char.status_atual['PV'] * 40 / char.status['PV']
        if barra_var > 0:
            barra_fixa = 40 - barra_var
        else:
            barra_fixa = 40
        if inimigo is True:
            cor_barra = [Fore.GREEN, Fore.WHITE]
        else:
            cor_barra = [Fore.RED, Fore.BLUE]
        print('PV: ', cor_barra[0] + '█' * floor(barra_var), end='')
        print(Fore.BLACK + '█' * ceil(barra_fixa), Fore.RESET + f'{char.status["PV"]} ({char.status_atual["PV"]})')
        # =================[Barra dos PAs]===========================
        barra_var = char.status_atual['PA'] * 40 / char.status['PA']
        barra_fixa = 40 - barra_var
        print('PA: ', cor_barra[1] + '█' * floor(barra_var), end='')
        print(Fore.BLACK + '█' * ceil(barra_fixa), Fore.RESET +
              f'{char.status["PA"]} ({char.status_atual["PA"]})' + Fore.RESET)
        # =================[Barra dos PEs]===========================
        if inimigo is False:
            barra_var = char.status_atual['PE'] * 40 / char.status['PE']
            barra_fixa = 40 - barra_var
            print('PE: ', Fore.LIGHTCYAN_EX + '█' * floor(barra_var), end='')
            print(Fore.BLACK + '█' * ceil(barra_fixa), Fore.RESET +
                  f'{char.status["PE"]} ({char.status_atual["PE"]})' + Fore.RESET)

    @staticmethod
    def hudChoice(*option, texto=None, voltar=False):
        global choice, num
        x = True
        falha = 0
        while x:
            if texto is not None:
                print(texto)
            if type(option[0]) is dict:
                option = option[0].copy()
                for num, op in enumerate(option):
                    if option[op] is None:
                        print(f'[{num + 1}] \x1B[3mEspaço Vazio' + "\x1B[0m")
                    else:
                        # Isso é para magias
                        print(f'[{num + 1}] {option[op]["Nome"]}')
            else:
                for num, op in enumerate(option):
                    print(f'[{num + 1}] {op}')
            if len(option) == 0:
                print('Não há opções disponíveis!')
                break
            if voltar is True:
                print(f'[{num + 2}] Voltar')
            choice = int(input('>> '))

            # Isso é para magias
            if choice == len(option) + 1 and voltar is True:
                x = False
            elif choice > len(option) or choice <= 0:
                print('Opção inválida!')
            else:
                x = False
        # Isso é para magias
        if type(option) is dict:
            if choice == len(option) + 1:
                return choice, 'voltar'
            else:
                return choice, list(option)[choice - 1]
        else:
            if choice == len(option) + 1:
                return choice, 'voltar'
            else:
                return choice, option[choice - 1]

    @staticmethod
    def dialogo(*text, escolha=False):
        x = True
        while x:
            try:
                for ver in text:
                    for palavra in ver:
                        sleep(0.02)
                        print(palavra, end='')
                    if escolha is False:
                        input()
                    else:
                        print()
                x = False
            except ValueError:
                print(Fore.RED+'Não existe essa opção! Selecione outra.'+Fore.RESET)

    @staticmethod
    def msgDano(alvo_nome, dano, tipo=None):
        if tipo is not None:
            print(f'{alvo_nome} sofreu {dano} de dano de {tipo}!')
        else:
            print(f'{alvo_nome} sofreu {dano} de dano!')

    @staticmethod
    def verEfeitos(criatura):
        num_efeitos = len(criatura.efeitos)
        if criatura.efeitos:
            print('EFEITOS: ', end='')

        for num, efeito in enumerate(criatura.efeitos):
            if num_efeitos == 1:
                print(f'{efeito[0]} {efeito[1][0]} por {efeito[2]} turnos')
            elif num+1 != num_efeitos:
                print(f'{efeito[0]} {efeito[1][0]} por {efeito[2]} turnos, ', end='')
            else:
                print(f'e {efeito[0]} {efeito[1][0]} por {efeito[2]} turnos')

    @staticmethod
    def iconEfeito(alvo):
        ico_efeito = []
        for efeito in alvo.efeitos:
            match efeito[0]:
                case 'incendiar':
                    ico_efeito.append('🔥')
                case 'eletrizar':
                    ico_efeito.append('⚡')
        return ico_efeito

    @staticmethod
    def escolhaAlvo(jogador, alvos, turno):
        global texto
        f = True
        while f:
            try:
                print('═' * 20 + f'╡ Turno {turno} ╞' + '═' * 20)

                # Mostra a vida do jogador e os efeitos
                ob.hud.verEfeitos(ob.character)
                Hud.lifeHud(jogador)

                # Laço de repetição da tela de seleção de inimigos
                for num, alvo in enumerate(alvos):
                    # Condição para a cor do inimigo
                    if alvo.status_atual['PV'] >= alvo.status['PV'] * 1 / 2:
                        cor = Fore.GREEN
                    elif alvo.status_atual['PV'] >= alvo.status['PV'] * 1 / 4:
                        cor = Fore.YELLOW
                    else:
                        cor = Fore.RED
                    # Condição para o emoji de aura
                    if alvo.status_atual['PA'] == 0:
                        aura = f''
                    else:
                        aura = f'🛡'
                    ico_efeitos = Hud.iconEfeito(alvo)
                    texto = f'[{num + 1}]{cor} {alvo.info["nome"]}'[:40]
                    res = 30 - len(texto) + -1*len(alvo.efeitos) + len(aura)
                    if (num + 1) % 2 == 1:
                        print(texto+Fore.BLUE+aura+Fore.RESET, end='')
                        for ico in ico_efeitos:
                            print(ico, end='')
                        print(' '.ljust(res)[:res], end='')
                    else:
                        print(texto+Fore.BLUE+aura+Fore.RESET, end='')
                        for ico in ico_efeitos:
                            print(ico, end='')
                        print(' '.ljust(res)[:res])

                if len(alvos) % 2 == 1:
                    print()
                choice = int(input('>> '))
                f = False
                return choice
            except ValueError:
                print(Fore.RED + 'Não existe essa opção! Selecione outra.' + Fore.RESET)


