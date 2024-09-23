import abc
from extrato import Extrato as Ex
from erros import ContaCancelada, ClienteCancelado
from data import DataMixin


class Conta(abc.ABC, DataMixin):
    ativas = {}
    senhas = {}
    desativadas = []
    id_numero = 0
    __slots__ = ['_cliente', '_saldo', '_numero', '_status', '_banco']

    def __init__(self, cli, sal, banco):
        try:
            cli.verificar_status()
            self._cliente = cli
            self._saldo = sal
            self._numero = self.id_numero
            self._extrato = Ex()
            self._status = True
            self._criado = self.date_now()
            self._banco = banco
            # ----------------------------------
            Conta.id_numero += 1
            Conta.ativas[self._numero] = self
            cli.associar_conta()
            self._extrato.saldo_inicial(sal)
        except ClienteCancelado:
            self._status = False

    @property
    def criado(self):
        return self._criado

    @property
    def banco(self):
        return self._banco

    @property
    def cliente(self):
        return self._cliente

    @property
    def extrato(self):
        return self._extrato

    @property
    def numero(self):
        return self._numero


    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        self._saldo = value

    @property
    def status(self):
        return self._status


    @classmethod
    def pesquisar_conta_num(cls, num):
        if int(num) in cls.ativas.keys():
            return cls.ativas[int(num)]
        else:
            return 0

    @classmethod
    def pesquisar_conta_cpf(cls, cpf):
        for conta in cls.ativas.values():
            if conta.cliente.cpf == cpf:
                return conta
        return 0

    @classmethod
    def verificar_senha(cls, conta, senha):
        try:
            if cls.senhas[conta] == senha:
                return 1
            else:
                return 0
        except KeyError:
            return 0

    @abc.abstractmethod
    def saque(self, valor):
        pass

    @abc.abstractmethod
    def deposito(self, valor):
        pass

    def subtrair_saldo(self, valor, tipo, cont=''):
        try:
            self.verifica_status()
            self._saldo = round(self._saldo - valor, 4)
            self._extrato.registro_sub(val=valor, tp=tipo, conta=cont)
        except ContaCancelada:
            pass

    def add_saldo(self, valor, tipo, cont=''):
        try:
            self.verifica_status()
            self._saldo = round(self._saldo + valor, 4)
            self._extrato.registro_add(val=valor, tp=tipo, conta=cont)
        except ContaCancelada:
            pass

    def transferencia(self, valor, cont):
        try:
            self.verifica_status()
            cont.verifica_status()
            tp = 't'
            if self._saldo >= valor >= 0:
                self.subtrair_saldo(valor, tp, cont=cont)
                cont.add_saldo(valor, tp, cont=self)
                return 1
            else:
                return 0
        except ContaCancelada:
            pass

    def verifica_status(self):
        if not self._status:
            raise ContaCancelada(self)

    def cancelar_conta(self):
        from cliente import Cliente
        try:
            if not self._saldo:
                self._status = False
                del Conta.ativas[self._numero]
                Conta.desativadas.append(self)
                self.cliente.desassociar_conta()
                self._cliente = Cliente.clonar_cliente(self.cliente)
                self.cliente.associar_conta()
                self.cliente.cancelar_cliente()
                self.extrato.cancelamento_conta()
                return 1
            else:
                return 0
        except ContaCancelada:
            pass


class ContaCorrente(Conta):
    def __init__(self, cli, sal, banco):
        super().__init__(cli, sal, banco)

    @classmethod
    def att_desconto(cls, valor):
        cls.valor_desconto = valor

    @classmethod
    def registrar_conta(cls, entradas):
        conta_c = cls(cli=entradas['cliente'],
                      sal=float(entradas['saldo']),
                      banco=entradas['banco'])
        try:
            conta_c.verifica_status()
        except ContaCancelada:
            return 0
        entradas['banco'].registrar_conta(conta_c, entradas['senha'])
        return 1

    def saque(self, valor):
        try:
            self.verifica_status()
            tp_saque = 's'
            tp_desconto = 'ds'
            if self._saldo >= (valor + self.banco.desconto) > 0 and valor > 0:
                self.subtrair_saldo(valor, tp_saque)
                self.subtrair_saldo(self.banco.desconto, tp_desconto)
                return 1
            else:
                return 0
        except ContaCancelada:
            pass

    def deposito(self, valor):
        try:
            self.verifica_status()
            tp = 'd'
            tp_desconto = 'ds'
            if (valor - self.banco.desconto) >= 0:
                self.add_saldo(valor, tp)
                self.subtrair_saldo(self.banco.desconto, tp_desconto)
                return 1
            else:
                return 0
        except ContaCancelada:
            pass


class ContaPoupanca(Conta):
    def __init__(self, cli, sal, banco):
        super().__init__(cli, sal, banco)

    @classmethod
    def registrar_conta(cls, entradas):
        conta_p = cls(cli=entradas['cliente'],
                      sal=float(entradas['saldo']),
                      banco=entradas['banco'])
        try:
            conta_p.verifica_status()
        except ContaCancelada:
            return 0
        entradas['banco'].registrar_conta(conta_p, entradas['senha'])
        return 1

    def saque(self, valor):
        try:
            self.verifica_status()
            tp = 's'
            if self._saldo >= valor > 0:
                self.subtrair_saldo(valor, tp)
                return 1
            else:
                return 0
        except ContaCancelada:
            pass

    def deposito(self, valor):
        try:
            self.verifica_status()
            tp = 'd'
            if valor > 0:
                self.add_saldo(valor, tp)
                return 1
            else:
                return 0
        except ContaCancelada:
            pass

    def att_mensal(self):
        try:
            tp = 'att'
            if self.banco.taxa <= self.saldo:
                self.subtrair_saldo(self.banco.taxa, tp)
                return 1
            else:
                return 0
        except ContaCancelada:
            pass
