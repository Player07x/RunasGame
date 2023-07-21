import NPC
from lib import ataques_e_armas as atk

levi = NPC.Npc()
levi.setInfo('Levi')
levi.setAtributos([7, 7, 10], [0, 3, 4, 1, 3, 3, 0, 8, 2])
levi.setStatus(atual=True, RDM=8)
levi.setAtaques([atk.pancada])
