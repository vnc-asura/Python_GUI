import tkinter as tk
from tkinter import ttk, messagebox as msg


class TopSaqueDeposito:
    def tipo_op(self):
        if self.tp == 1:
            return {'titulo': 'Saque',
                    'butao': 'Sacar',
                    'operacao': self.ref.conta.saque}
        elif self.tp == 2:
            return {'titulo': 'Depósito',
                    'butao': 'Depositar',
                    'operacao': self.ref.conta.deposito}

    def verifica_entrada(self):
        if self.valor_var.get() and self.valor_var.get().strip() != '':
            return self.valor_var.get()
        else:
            return 0

    def op_bind(self, ev):
        valor = self.verifica_entrada()
        if valor:
            if self.var['operacao'](float(valor)):
                self.ref.att_saldo()
                self.ref.att_transacoes()
                self.top.destroy()
            else:
                erro_operacao = msg.showerror(f'Erro {self.var["titulo"]}',
                                              'Não foi possível realizar a operação\n'
                                              'Verifique o valor inserido e tente novamente')
        else:
            erro_incompleto = msg.showerror('Erro entrada',
                                            'Há um campo vazio!\n'
                                            'Preencha-o e tente novamente')

    def valor_trace(self, *args):
        self.valor_var.set(''.join([x for x in self.valor_var.get() if not x.isalpha()]))

    def __init__(self, top, ref, tipo):
        self.ref = ref
        self.tp = tipo
        self.var = self.tipo_op()
        self.top = top
        self.top.title(self.var['titulo'])
        self.top.iconbitmap('imagem/icone_capi.ico')
        # comportamento
        self.top.grab_set()
        # widgets
        # valor
        self.valor_var = tk.StringVar()
        self.valor_var.trace_add('write', self.valor_trace)
        self.lbl_valor = ttk.Label(self.top,
                                   text='Valor:')
        self.lbl_valor.grid(row=0, column=0)
        self.ent_valor = ttk.Entry(self.top,
                                   textvariable=self.valor_var)
        self.ent_valor.grid(row=0, column=1)
        self.ent_valor.bind('<Return>', self.op_bind)
        # butao
        self.btt_op = ttk.Button(self.top,
                                 text=self.var['butao'])
        self.btt_op.grid(row=0, column=2)
        self.btt_op.bind('<ButtonRelease-1>', self.op_bind)
        self.btt_voltar = ttk.Button(self.top,
                                     text='Voltar')
        self.btt_voltar.grid(row=0, column=3)
        self.btt_voltar.bind('<ButtonRelease-1>', lambda ev: self.top.destroy())


class TopTransferir:
    def verifica_entradas(self):
        var = {'valor': self.valor_var.get(),
               'numero': self.num_var.get()}
        if all([True if x.strip() != '' else False for x in var.values()]):
            return var
        else:
            return 0

    def transferir_bind(self, ev):
        from conta import Conta
        from erros import ContaCancelada as Ccancel
        var = self.verifica_entradas()
        if var:
            conta = Conta.pesquisar_conta_num(var['numero'])
            if conta:
                trans = self.ref.conta.transferencia(float(var['valor']), conta)
                if not isinstance(trans, Ccancel):
                    if trans:
                        self.ref.att_saldo()
                        self.ref.att_transacoes()
                        self.top.destroy()
                    else:
                        erro_op = msg.showerror('Erro Transferência',
                                                'Não foi possível realizar a operação\n'
                                                'Verifique o valor inserido e tente novamente')
                else:
                    erro_conta_cancelada = msg.showerror('Erro conta',
                                                         f'A conta {str(trans.conta.numero).zfill(3)} está cancelada!\n'
                                                         f'Impossivel de realizar a operação')
            else:
                erro_conta_errada = msg.showerror('Erro conta',
                                                  'O numero da conta inserida não existe!\n'
                                                  'Corrija-o ou tente outro numero')
        else:
            erro_incompleto = msg.showerror('Erro entradas',
                                            'Há campo(s) vazio(s)!\n'
                                            'Preencha-o(s) e tente novamente')

    def __init__(self, top, ref):
        self.top = top
        self.top.title('Transferir')
        self.ref = ref
        self.top.iconbitmap('imagem/icone_capi.ico')
        # comportamento
        self.top.grab_set()
        # frame
        self.frame = ttk.Frame(self.top)
        self.frame.pack()
        # widgets
        # valor
        self.valor_var = tk.StringVar()
        self.lbl_valor = ttk.Label(self.frame,
                                   text='Valor:')
        self.lbl_valor.grid(row=0, column=0)
        self.ent_valor = ttk.Entry(self.frame,
                                   textvariable=self.valor_var)
        self.ent_valor.grid(row=0, column=1)
        # numero
        self.num_var = tk.StringVar()
        self.lbl_num = ttk.Label(self.frame,
                                 text='Número da conta:')
        self.lbl_num.grid(row=0, column=2)
        self.ent_num = ttk.Entry(self.frame,
                                 textvariable=self.num_var)
        self.ent_num.grid(row=0, column=3)
        self.ent_num.bind('<Return>', self.transferir_bind)
        # butao
        self.btt_trans = ttk.Button(self.frame,
                                    text='Transferir')
        self.btt_trans.grid(row=0, column=4)
        self.btt_trans.bind('<ButtonRelease-1>', self.transferir_bind)
        self.btt_voltar = ttk.Button(self.frame,
                                     text='Voltar')
        self.btt_voltar.grid(row=0, column=5)
        self.btt_voltar.bind('<ButtonRelease-1>', lambda ev: self.top.destroy())


