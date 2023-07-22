import copy

from lib import itens
from lib import inimigos, companions
from lib import objetos as ob
from lib import ataques_e_armas as atk
from lib import magias as mag


if __name__ == '__main__':

    ob.character.setAtributos([8, 6, 6], [2, 6, 2, 1, 3, 3, 4, 6, 2])
    ob.character.setStatus(atual=True, RDF=4, RDM=4)
    ob.character.setEquipamento(arma=atk.espada_longa, escudo=itens.escudo_madeira, magia=[mag.bola_de_fogo,
                                                                                           mag.raio_de_fogo,
                                                                  mag.raio_eletrico])
    ob.character.setEfeito()

    ob.menu.menuCombate(ob.character, [
                                       copy.deepcopy(inimigos.nulo)], [companions.levi])


