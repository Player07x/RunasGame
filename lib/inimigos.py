import montros as mon
from lib import ataques_e_armas as atk

# =========================== [ Nulo ] ============================
nulo = mon.Monstro()
nulo.setInfo('Nulo')
nulo.setAtributos([6, 3, 6], [2, 1, 3, 1, 1, 1, 0, 6, 0])
nulo.setStatus(atual=True)
nulo.setAtaques([atk.garra, atk.chifre, atk.pancada])
nulo.setDescricao('Um nulo é uma criatura que costuma vagar por florestas ou '
                  'lugares abandonados. Sempre de cabeça baixa e pouco agressivo, '
                  'além de não gostarem de serem incomodados. Um nulo possui uma '
                  'runa verde, ou seja, são runos do elemento Natureza.')
nulo.setXP()
# ========================= [ Squonk ] =========================
squonk = mon.Monstro()
squonk.setInfo('Squonk')
squonk.setAtributos([12, 4, 10], [4, 4, 4, 0, 4, 0, 0, 8, 2])
squonk.setStatus(atual=True, RDF=6, RDM=4)
squonk.setAtaques([atk.pancada_forte, atk.espirro_acido])
squonk.setDescricao('')
squonk.setXP()
