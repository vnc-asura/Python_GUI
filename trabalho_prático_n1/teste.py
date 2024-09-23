from cliente import Cliente, Endereco
from conta import ContaPoupanca as Cp, ContaCorrente as Cc
from banco import Banco


class Teste:
    def __init__(self):
        self.end = Endereco(logradouro='Rua da goiaba',
                            numero='87',
                            bairro='Figueredo',
                            cidade='Rio branco',
                            uf='AC',
                            cep='69900-568')

        self.end2 = Endereco(logradouro='Rua buriti',
                             numero='14',
                             bairro='6 de agosto',
                             cidade='Rio Branco',
                             uf='AC',
                             cep='69900-000')

        self.cli1 = Cliente(n='Vinicius Caetano',
                            e=self.end,
                            cpf='777.777.777-77',
                            gen='Homem-Cis',
                            tel='68_99999-9999')
        self.cli2 = Cliente(n='José augusto',
                            e=self.end2,
                            cpf='888.888.888-88',
                            gen='Homem-Cis',
                            tel='68_99999-9999')

        self.banco = Banco(num=341,
                           nome='Itaú',
                           desc=0.2,
                           taxa=12)

