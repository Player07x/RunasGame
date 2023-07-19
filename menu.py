import time
from random import randint
from colorama import Fore
import combate
import hud
from lib import objetos as ob


class Menu:
    turno = 0
    inimigos = []

    @staticmethod
    def menuCombate(jogador: object, inim: list):
        global turno, inimigos, choice
        inimigos = inim
        """
        Menu principal de combate, usar sempre esse menu ao invés de utilizar
        dos outros métodos.

        :param jogador: Inserir um objeto que é o jogador

        :param inimigos: Inserir uma lista com objetos, cada objeto deve ter um
        copy.deepcopy() para evitar que os inimigos compartilhem dos mesmos status,
        no caso de inimigos (objetos) idênticos.
        """

        # Variável que mudará o estado do while
        x = True
        turno = 0
        # Laço de repetição do combate
        while x:
            ob.combate.aplicarEfeitos(ob.character)
            if jogador.status_atual['PV'] <= 0:
                print(Fore.RED + '═' * 15 + f'╡ Você Morreu! ╞' + '═' * 15 + Fore.RESET)
                x = False
                break
            for inimigo in inimigos:
                ob.combate.aplicarEfeitos(inimigo)
            # Quebrar laço após todos os inimigos morrerem
            if len(inimigos) == 0:
                break

            # Varivável dos Turnos
            turno += 1

            choice = hud.Hud.escolhaAlvo(jogador, inimigos, turno)

            # Verifica se a escolha de inimigo é válida
            if 0 < choice <= len(inimigos):
                res = Menu.menuAtaque(inimigos[choice - 1])
                if res == 'sucesso':
                    x = False
                    break
                # Cria uma cópia dos inimigos para evitar que dê erros
                # no laço "for".
                copy_inimigos = inimigos.copy()
                for inimigo in copy_inimigos:
                    # Se o inimigo morreu, remover da lista e pular turno de
                    # combate dele
                    if inimigo.status_atual['PV'] <= 0:
                        print(inimigo.info['nome'], ' morreu!')
                        inimigos.remove(inimigo)
                    # Se o inimigo estiver vivo, começa o turno de combate dele
                    else:
                        inimigo.randomAtaque()
                        # Se o jogador morrer após o ataque, esse método se encerra
                        if jogador.status_atual['PV'] <= 0:
                            print(Fore.RED+'═' * 15 + f'╡ Você Morreu! ╞' + '═' * 15+Fore.RESET)
                            x = False
                            break
            else:
                print('Opção Inválida! Escolha novamente.')

    @staticmethod
    def menuAtaque(inimigo):
        global escolha, choice
        x = True
        while x:
            f = True
            while f:
                try:
                    print('═' * 20 + f'╡ Turno {turno} ╞' + '═' * 20)
                    hud.Hud.verEfeitos(inimigo)
                    hud.Hud.lifeHud(inimigo, inimigo=True)
                    choice = hud.Hud.hudChoice('Atacar', 'Usar Item', 'Magias', 'Fugir')
                    f = False
                except ValueError:
                    print(Fore.RED + 'Não existe essa opção! Selecione outra.' + Fore.RESET)

            match choice[0]:
                case 1:
                    escolha = Menu.verAtaques(inimigo)
                case 2:
                    escolha = Menu.verItens()
                case 3:
                    escolha = Menu.verMagias(inimigo)
                case 4:
                    escolha = Menu.fugir()
                    if escolha == 'sucesso':
                        return 'sucesso'
                case _:
                    print('Opção Inválida! Escolha novamente.')
            x = False
            if escolha == 'voltar':
                x = True

    @staticmethod
    def verAtaques(inimigo):
        f = True
        while f:
            try:
                arma = ob.character.equipamento['arma']
                escolha = hud.Hud.hudChoice(arma['Nome'], 'Trocar de Armas', voltar=True)
                match escolha[0]:
                    case 1:
                        combate.Combate.danoFisico(inimigo, arma['Dano'], arma['Tipo'], arma['Efeitos'],
                                                   dano_bonus=ob.character.atributos_s['for'])
                    case 2:
                        pass

                    case 3:
                        return 'voltar'
                f = False
            except ValueError:
                print(Fore.RED+'Não existe essa opção! Selecione outra.'+Fore.RESET)

    @staticmethod
    def verItens():
        f = True
        while f:
            try:
                pass
                f = False
            except ValueError:
                print(Fore.RED+'Não existe essa opção! Selecione outra.'+Fore.RESET)

    @staticmethod
    def verMagias(inimigo):
        global choice
        f = True
        while f:
            try:
                x = True
                magia = ob.character.equipamento['magias']
                while x:
                    choice = ob.hud.hudChoice(magia, voltar=True)
                    x = False
                    try:
                        if magia[choice[1]] is None and choice[0] != 5:
                            print(Fore.RED+'Nenhuma magia atribuída nesse espaço. Escolha outra!'+Fore.RESET)
                            x = True
                        elif choice[0] == 5:
                            return 'voltar'
                        else:
                            resposta = Menu.verInfoMagia(magia[choice[1]])
                            if resposta == 1:
                                if magia[choice[1]]['Custo'] <= ob.character.status_atual['PE']:
                                    ob.character.status_atual['PE'] -= magia[choice[1]]['Custo']
                                    ob.combate.danoMagico(inimigo,
                                                          magia[choice[1]]['Dano'],
                                                          magia[choice[1]]['Tipo'],
                                                          magia[choice[1]]['Efeito'],
                                                          dano_bonus=ob.character.atributos_s['pod'])
                                else:
                                    print(Fore.RED + 'O custo dessa magia é muito alta...' + Fore.RESET)
                                    x = True
                            elif resposta == 2:
                                x = True
                    # if magia[choice[1]] is None and choice[0] != 5:
                    # KeyError: 'voltar'
                    except KeyError:
                        return 'voltar'
                    f = False
            except ValueError:
                print(Fore.RED+'Não existe essa opção! Selecione outra.'+Fore.RESET)

    @staticmethod
    def verInfoMagia(magia):
        f = True
        while f:
            try:
                choice = ob.hud.hudChoice('Confirmar', voltar=True, texto=f'Nome: {magia["Nome"]}\n'
                                                                 f'Tipo: {magia["Tipo"]}\n'
                                                                 f'Custo: {magia["Custo"]} PE\n {Fore.GREEN}'
                                                                 f'Seus PEs: {ob.character.status_atual["PE"]} '
                                                                          f'{Fore.RESET}')
                f = False
                return choice[0]
            except ValueError:
                print(Fore.RED+'Não existe essa opção! Selecione outra.'+Fore.RESET)

    @staticmethod
    def fugir():
        resultado = None
        x = 1
        for inimigo in inimigos:
            print(Fore.YELLOW + 'Tentando fugir' + '.' * x + Fore.RESET)
            time.sleep(0.3)
            x += 1
            if x >= 4:
                x = 1
            res_inim = inimigo.atributos_s['des'] - randint(1, 20)
            res_jog = ob.character.atributos_s['des'] - randint(1, 20)
            if res_inim > res_jog:
                print(Fore.RED + 'Você não conseguiu.' + Fore.RESET)
                resultado = 'fracasso'
                break
        if resultado is None:
            print(Fore.GREEN + 'Você conseguiu!' + Fore.RESET)
            resultado = 'sucesso'

        return resultado