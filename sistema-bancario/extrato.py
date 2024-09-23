from data import DataMixin


class Extrato(DataMixin):
    __slots__ = ['_registros', '_movimentacao', '_movimentacao_datetime']

    def __init__(self):
        self._registros = []
        self._movimentacao = []
        self._movimentacao_datetime = []

    @property
    def registros(self):
        return self._registros

    @property
    def movimentacao(self):
        return self._movimentacao

    @property
    def movimentacao_datetime(self):
        return self._movimentacao_datetime

    def registro_add(self, val, tp, conta=''):
        tipos = {'d': f'{self.datetime_now()} - Depósito realizado no valor de R${val:,.2f}',
                 't': f'{self.datetime_now()} - Transferência recebida no valor de R${val:,.2f} da conta {str(conta.numero).zfill(3) if conta else conta}'}
        self._registros.append(tipos[tp])
        self._movimentacao.append(val)
        self._movimentacao_datetime.append(f'{self.datetime_now()} | R$ +{val:,.2f}')

    def registro_sub(self, val, tp, conta=''):
        tipos = {'s': f'{self.datetime_now()} - Saque realizado no valor de R${val:,.2f}',
                 't': f'{self.datetime_now()} - Transferência realizada no valor de R${val:,.2f} para conta {str(conta.numero).zfill(3) if conta else conta}',
                 'ds': f'{self.datetime_now()} - Desconto de R${val:,.2f}',
                 'att': f'{self.datetime_now()} - Atualização mensal no valor de R${val:,.2f}'}
        self._registros.append(tipos[tp])
        self._movimentacao.append(-val)
        self._movimentacao_datetime.append(f'{self.datetime_now()} | R$ -{val:,.2f}')

    def saldo_inicial(self, valor):
        self._registros.append(f'Conta criada em {self.date_now()} com o Saldo de R$ {valor:,.2f}')
        self._movimentacao.append(valor)
        self._movimentacao_datetime.append(f'{self.datetime_now()} | R$ +{valor:,.2f}')

    def cancelamento_conta(self):
        self._registros.append(f'Conta cancelada em {self.datetime_now()}')

    def __str__(self):
        return '\n'.join(self._registros)
