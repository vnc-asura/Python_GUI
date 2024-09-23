from erros import ClienteCancelado


class Endereco:
    cod = 0
    __slots__ = ['_logradouro', '_numero', '_bairro', '_cidade', '_uf', '_cep', '_cod', '_complemento']

    def __init__(self, logradouro, numero, bairro, cidade, uf, cep, com=''):
        self._logradouro = logradouro
        self._numero = numero
        self._bairro = bairro
        self._cidade = cidade
        self._uf = uf
        self._cep = cep
        self._complemento = com
        self._cod = Endereco.cod
        Endereco.cod += 1

    @property
    def logradouro(self):
        return self._logradouro

    @logradouro.setter
    def logradouro(self, value):
        self._logradouro = value

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        self._numero = value

    @property
    def bairro(self):
        return self._bairro

    @bairro.setter
    def bairro(self, value):
        self._bairro = value

    @property
    def cidade(self):
        return self._cidade

    @cidade.setter
    def cidade(self, value):
        self._cidade = value

    @property
    def uf(self):
        return self._uf

    @uf.setter
    def uf(self, value):
        self._uf = value

    @property
    def cep(self):
        return self._cep

    @cep.setter
    def cep(self, value):
        self._cep = value

    @property
    def complemento(self):
        return self._complemento

    @complemento.setter
    def complemento(self, value):
        self._complemento = value

    def __str__(self):
        return f'{self.logradouro}, {self.numero}, {self.bairro}, {self.cidade} - {self.uf}'


class Cliente:
    identificador = 0
    ativos = {}
    desatvados = []
    clones = []
    __slots__ = ['_nome', '_endereco', '_cpf', '_id', '_genero', '_telefone', '_status', '_associado']

    def __init__(self, n, e, cpf, gen, tel):
        self._nome = n
        self._endereco = e
        self._cpf = cpf
        self._genero = gen
        self._telefone = tel
        self._id = Cliente.identificador
        self._status = True
        self._associado = False
        Cliente.identificador += 1
        Cliente.ativos[self._id] = self

    @property
    def telefone(self):
        return self._telefone

    @telefone.setter
    def telefone(self, value):
        self._telefone = value

    @property
    def genero(self):
        return self._genero

    @genero.setter
    def genero(self, value):
        self._genero = value

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def cpf(self):
        return self._cpf

    @property
    def endereco(self):
        return self._endereco

    @property
    def id(self):
        return self._id

    @property
    def associado(self):
        return self._associado

    @classmethod
    def registrar_cliente(cls, entrada):
        if entrada['cpf'] not in [i.cpf for i in Cliente.ativos.values()]:
            endereco = Endereco(logradouro=entrada['logradouro'],
                                numero=entrada['numero'],
                                bairro=entrada['bairro'],
                                cidade=entrada['cidade'],
                                uf=entrada['uf'],
                                cep=entrada['cep'],
                                com=entrada['complemento'])

            cliente = cls(n=entrada['nome'],
                          e=endereco,
                          cpf=entrada['cpf'],
                          gen=entrada['genero'],
                          tel=entrada['telefone'])
            return 1
        else:
            return 0

    @classmethod
    def atualizar_cliente(cls, entrada, conta):
        conta.nome = entrada['nome']
        conta.genero = entrada['genero']
        conta.telefone = entrada['telefone']
        conta.endereco.logradouro = entrada['logradouro']
        conta.endereco.numero = entrada['numero']
        conta.endereco.bairro = entrada['bairro']
        conta.endereco.cidade = entrada['cidade']
        conta.endereco.uf = entrada['uf']
        conta.endereco.cep = entrada['cep']
        conta.endereco.complemento = entrada['complemento']

    @classmethod
    def pesquisa_cliente_num(cls, num):
        return Cliente.ativos[int(num)]

    @classmethod
    def clonar_cliente(cls, cliente):
        clone = cls(n=cliente.nome,
                    e=cliente.endereco,
                    cpf=cliente.cpf,
                    gen=cliente.genero,
                    tel=cliente.telefone)
        del Cliente.ativos[clone.id]
        Cliente.clones.append(clone)

        return clone

    def verificar_status(self):
        if not self._status:
            raise ClienteCancelado(self)

    def cancelar_cliente(self):
        if not self._associado:
            self._status = False
            del Cliente.ativos[self._id]
            Cliente.desatvados.append(self)
            return 1
        else:
            return 0

    def associar_conta(self):
        self._associado = True

    def desassociar_conta(self):
        self._associado = False

    def __str__(self):
        return f'{str(self.id).zfill(3)} - {self.nome}'
