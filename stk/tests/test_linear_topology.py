import os

from ..molecular import StructUnit2, Polymer, Linear

if not os.path.exists('linear_topology_tests'):
    os.mkdir('linear_topology_tests')


def test_assembly():
    bb1 = StructUnit2.smiles_init('Nc1ccc(N)nc1', 'amine')
    bb2 = StructUnit2.smiles_init('O=CC1=CN=C(C=O)C1', 'aldehyde')
    bb3 = StructUnit2.smiles_init('OB(O)c1ccc(B(O)O)nc1', 'boronic_acid')
    bb4 = StructUnit2.smiles_init('Oc1cc2cc(O)c(O)nc2cc1O', 'diol')

    p1 = Polymer([bb1, bb2], Linear('AB', [0, 0], 3))
    p2 = Polymer([bb1, bb2], Linear('AB', [1, 1], 3, 'fg'))
    p3 = Polymer([bb3, bb4], Linear('AB', [0, 0], 3))

    path = os.path.join('linear_topology_tests', 'p1.mol')
    p1.write(path)
    p2.write(path.replace('1', '2'))
    p3.write(path.replace('1', '3'))
