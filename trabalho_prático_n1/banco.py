class Banco:
    num_bancos = {}

    __slots__ = ['_numero', '_nome', '_contas_pass', '_num_contas', '_desconto', '_taxa']

    def __init__(self, num, nome, desc, taxa):
        self._numero = num
        self._nome = nome
        self._num_contas = {}
        self._desconto = desc
        self._taxa = taxa
        Banco.num_bancos[self._numero] = self

    @property
    def taxa(self):
        return self._taxa

    @taxa.setter
    def taxa(self, value):
        self._taxa = value

    @property
    def desconto(self):
        return self._desconto

    @desconto.setter
    def desconto(self, value):
        self._desconto = value

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        self._numero = value

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def num_contas(self):
        return self._num_contas

    @classmethod
    def registrar_banco(cls, entradas):
        if int(entradas['numero']) not in cls.num_bancos.keys():
            cls(num=int(entradas['numero']),
                nome=entradas['nome'],
                desc=float(entradas['desconto']),
                taxa=float(entradas['taxa']))
            return 1
        else:
            return 0

    @classmethod
    def atualizar_banco(cls, entradas, num_atual):
        banco = cls.pesquisar_banco_num(int(num_atual))
        if int(entradas['numero']) == int(num_atual) or int(entradas['numero']) not in list(cls.num_bancos.keys()):
            banco.nome = entradas['nome']
            banco.desconto = float(entradas['desconto'])
            banco.taxa = float(entradas['taxa'])
            if int(num_atual) not in cls.num_bancos.keys():
                del cls.num_bancos[int(num_atual)]
                cls.num_bancos[int(num_atual)] = banco
            return 1
        else:
            return 0

    @classmethod
    def pesquisar_banco_conta(cls, conta):
        for k in cls.num_bancos.values():
            if conta in k.num_contas.values():
                return k
        return 0

    @classmethod
    def pesquisar_banco_num(cls, num):
        return cls.num_bancos[int(num)]

    def __str__(self):
        return f'{self._numero} - {self._nome}'

    def registrar_conta(self, conta, senha):
        from conta import Conta
        if conta not in self._num_contas.values():
            self._num_contas[conta.numero] = conta
            Conta.senhas[conta] = senha
            return 1
        else:
            return 0
