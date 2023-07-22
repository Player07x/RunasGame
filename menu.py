import copy
import time
from colorama import Fore, init
import combate
import hud
from lib import objetos as ob

init(convert=False)


class Menu:
    turno = 0
    inimigos = []

    @staticmethod
    def menuCombate(jogador: object, inim: list, companions: list = None):
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
            situacao = Menu.verifMorte(jogador)
            if situacao == 'morto':
                x = False
                break
            for inimigo in inimigos:
                ob.combate.aplicarEfeitos(inimigo)
            Menu.verifMorte(inimigos=inimigos)
            # Quebrar laço após todos os inimigos morrerem
            if len(inimigos) == 0:
                break

            # Varivável dos Turnos
            turno += 1

            choice = hud.Hud.escolhaAlvo(jogador, inimigos, turno)

            # Verifica se a escolha de inimigo é válida
            if 0 < choice <= len(inimigos):
                res = Menu.menuAtaque(inimigos[choice - 1], companions)
                if res == 'sucesso':
                    x = False
                    break

                Menu.turnoAliado(inimigos, companions)
                Menu.turnoInimigo(jogador, inimigos, companions)

                # Se o jogador morrer após o ataque, esse método se encerra
                situacao = Menu.verifMorte(jogador)
                if situacao == 'morto':
                    x = False
                    break
            else:
                print('Opção Inválida! Escolha novamente.')

    @staticmethod
    def verifMorte(jogador=None, inimigos=None, aliado=None):
        jog = 'vivo'
        if jogador is not None:
            if jogador.status_atual['PV'] <= 0:
                print(Fore.RED + '═' * 15 + f'╡ Você Morreu! ╞' + '═' * 15 + Fore.RESET)
                jog = 'morto'
        if inimigos is not None:
            # Se o inimigo morreu, remover da lista e pular turno de
            # combate dele
            copy_ias = inimigos.copy()
            for ia in copy_ias:
                # Se o inimigo morreu, remover da lista e pular turno de
                # combate dele
                if ia.status_atual['PV'] <= 0:
                    print(ia.info['nome'], ' morreu!')
                    inimigos.remove(ia)
        if aliado is not None:
            copy_ias = aliado.copy()
            for ia in copy_ias:
                # Se o inimigo morreu, remover da lista e pular turno de
                # combate dele
                if ia.status_atual['PV'] <= 0 and ia.tipo == 'Importante':
                    ia.setSituacao('Desmaiado')
                elif ia.status_atual['PV'] <= 0:
                    print(ia.info['nome'], ' morreu!')
                    aliado.remove(ia)
        return jog

    @staticmethod
    def turnoInimigo(alvos, atacantes, companion=None):
        Menu.verifMorte(inimigos=atacantes)
        for ia in atacantes:
            if companion is not None:
                alvo = ia.randomAlvo(alvos, companion)
                ia.randomAtaque(alvo)
            else:
                ia.randomAtaque(alvos)

    @staticmethod
    def turnoAliado(alvos, atacantes):
        Menu.verifMorte(aliado=atacantes)
        if atacantes is not None:
            for ia in atacantes:
                if ia.situacao == 'Vivo':
                    alvo = ia.randomAlvoAli(alvos)
                    ia.randomAtaque(alvo, True)

    @staticmethod
    def menuAtaque(inimigo, companions):
        global escolha, choice
        x = True
        while x:
            f = True
            while f:
                try:
                    print('═' * 20 + f'╡ Turno {turno} ╞' + '═' * 20)
                    hud.Hud.verEfeitos(inimigo)
                    hud.Hud.lifeHud(inimigo, inimigo=True)
                    if companions is None:
                        choice = hud.Hud.hudChoice('Atacar', 'Usar Item', 'Magias', 'Fugir')
                    elif len(companions) > 0:
                        choice = hud.Hud.hudChoice('Atacar', 'Usar Item', 'Magias', 'Fugir', 'Ver Aliados')
                    else:
                        companions = None
                        choice = hud.Hud.hudChoice('Atacar', 'Usar Item', 'Magias', 'Fugir')
                    f = False
                except ValueError:
                    hud.Hud.opcaoNaoExiste()

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
                case 5:
                    if companions is None:
                        print('Opção Inválida! Escolha novamente.')
                    else:
                        x = True
                        while x:
                            res = ob.hud.escolhaAlvo(None, companions)
                            if len(companions) >= res > 0:
                                print(
                                    f'{companions[int(res-1)].info["nome"].upper()} | '
                                    f'RDF: {companions[int(res-1)].status["RDF"]}, '
                                    f'RDM: {companions[int(res-1)].status["RDM"]}')
                                hud.Hud.verEfeitos(companions[int(res-1)])
                                ob.hud.lifeHud(companions[int(res-1)])
                                res = ob.hud.hudChoice('Menu de Ataque', voltar=True)
                                if res[0] == 1:
                                    x = False

                        escolha = 'voltar'
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
                        combate.Combate.atacar(arma, inimigo, ob.character)
                    case 2:
                        pass

                    case 3:
                        return 'voltar'
                f = False
            except ValueError:
                hud.Hud.opcaoNaoExiste()

    @staticmethod
    def verItens():
        f = True
        while f:
            try:
                pass
                f = False
            except ValueError:
                hud.Hud.opcaoNaoExiste()

    @staticmethod
    def verMagias(inimigo):
        global choice
        f = True
        while f:
            try:
                x = True
                magia = copy.deepcopy(ob.character.equipamento['magias'])
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
                hud.Hud.opcaoNaoExiste()

    @staticmethod
    def verInfoMagia(magia):
        f = True
        while f:
            try:
                choice = ob.hud.hudChoice('Confirmar', voltar=True,
                                          texto=f'Nome: {magia["Nome"]}\n'
                                                f'Dano: {magia["Dano"][0]} - {magia["Dano"][1]}\n'
                                                f'Tipo: {magia["Tipo"]}\n'
                                                f'Custo: {magia["Custo"]} PE\n {Fore.GREEN}'
                                                f'Seus PEs:'
                                                f' {ob.character.status_atual["PE"]} '
                                                f'{Fore.RESET}')
                f = False
                return choice[0]
            except ValueError:
                hud.Hud.opcaoNaoExiste()

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
            resultado = ob.combate.testeResistindo('FISICO', 'des', ob.character, inimigo)
            if resultado[0] == 'fracasso':
                print(Fore.RED + 'Você não conseguiu.' + Fore.RESET)
                input()
                break
        else:
            print(Fore.GREEN + 'Você conseguiu!' + Fore.RESET)

        return resultado[0]
