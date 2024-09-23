class ContaCancelada(BaseException):
    def __init__(self, conta):
        self._conta = conta

    @property
    def conta(self):
        return self.conta


class ClienteCancelado(BaseException):
    def __init__(self, cliente):
        self._cliente = cliente

    @property
    def cliente(self):
        return self._cliente
