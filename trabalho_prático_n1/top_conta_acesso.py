import tkinter as tk
from data import DataMixin
from tkinter import ttk, scrolledtext as sct, filedialog as fd, messagebox as msg
from conta import ContaCorrente as Cc, ContaPoupanca as Cp
from top_operacoes import TopSaqueDeposito as Tsd, TopTransferir as Tt
from geometry import GeoPlace as Geo


class TopContaAcesso(DataMixin):
    def top_saque_depo(self, tipo):
        self.top_sd = tk.Toplevel(self.top)
        self.top_sd.withdraw()
        att_top_sd = Tsd(top=self.top_sd, ref=self, tipo=tipo)
        self.top_sd.geometry(Geo.centralizar_tela(self.top_sd))
        att_top_sd.ent_valor.focus_set()

    def top_tranferir(self):
        self.top_trans = tk.Toplevel(self.top)
        self.top_trans.withdraw()
        att_top_trans = Tt(self.top_trans, self)
        self.top_trans.geometry(Geo.centralizar_tela(self.top_trans))
        att_top_trans.ent_valor.focus_set()

    def att_dados(self):
        from banco import Banco
        ct = self.conta
        self.lbl_num_content['text'] = f'{str(ct.numero).zfill(3)}'
        self.lbl_tipo_content['text'] = f'{"Corrente" if isinstance(ct, Cc) else "Poupança"}'
        self.lbl_titular_content['text'] = f'{ct.cliente.nome}'
        self.lbl_banco_content['text'] = f'{Banco.pesquisar_banco_conta(ct).nome}'
        self.lbl_data_content['text'] = f'{ct.criado}'

    def att_saldo(self):
        self.lbl_saldo['text'] = f'{self.conta.saldo:,.2f}'

    def att_transacoes(self):
        self.sct_trans['state'] = 'normal'
        self.sct_trans.delete(0.0, tk.END)
        txt = self.conta.extrato.movimentacao_datetime[::-1]
        self.sct_trans.insert(0.0, '\n'.join(txt))
        self.sct_trans['state'] = 'disabled'

    def lbl_frame_dados(self):
        self.lfr_dados = ttk.Labelframe(self.top,
                                        text='Dados')
        self.lfr_dados.grid(row=0, column=0, sticky='ew')
        # widgets
        # numero
        self.lbl_num_title = ttk.Label(self.lfr_dados,
                                       text='Número:')
        self.lbl_num_title.grid(row=0, column=0, sticky='e')
        self.lbl_num_content = ttk.Label(self.lfr_dados,
                                         justify='center')
        self.lbl_num_content.grid(row=0, column=1, padx=6)
        # tipo conta
        self.lbl_tipo_title = ttk.Label(self.lfr_dados,
                                        text='Tipo conta:')
        self.lbl_tipo_title.grid(row=0, column=2, sticky='e')
        self.lbl_tipo_content = ttk.Label(self.lfr_dados,
                                          justify='center')
        self.lbl_tipo_content.grid(row=0, column=3, padx=6)
        # titular
        self.lbl_titular_title = ttk.Label(self.lfr_dados,
                                           text='Titular:')
        self.lbl_titular_title.grid(row=1, column=0, sticky='e')
        self.lbl_titular_content = ttk.Label(self.lfr_dados, width=40,
                                             justify='center')
        self.lbl_titular_content.grid(row=1, column=1, columnspan=3, sticky='ew', padx=6)
        # banco
        self.lbl_banco_title = ttk.Label(self.lfr_dados,
                                         text='Banco:')
        self.lbl_banco_title.grid(row=2, column=0, sticky='e')
        self.lbl_banco_content = ttk.Label(self.lfr_dados,
                                           justify='center')
        self.lbl_banco_content.grid(row=2, column=1, padx=6)
        # criação conta
        self.lbl_data_title = ttk.Label(self.lfr_dados,
                                        text='Data criação:')
        self.lbl_data_title.grid(row=2, column=2, sticky='e')
        self.lbl_data_content = ttk.Label(self.lfr_dados,
                                          justify='center')
        self.lbl_data_content.grid(row=2, column=3, padx=6)
        # atualizar labels
        self.att_dados()

    def lbl_frame_saldo(self):
        self.lfr_saldo = ttk.Labelframe(self.top,
                                        text='Saldo')
        self.lfr_saldo.grid(row=0, column=1, sticky='ns')
        # widget
        self.lbl_sifrao = ttk.Label(self.lfr_saldo,
                                    text='R$')
        self.lbl_sifrao.grid(row=0, column=0, sticky='e', pady=15, padx=10)
        self.lbl_saldo = ttk.Label(self.lfr_saldo)
        self.lbl_saldo.grid(row=0, column=1, pady=15, padx=10)
        # att saldo
        self.att_saldo()

    def lbl_frame_transacoes(self):
        self.lfr_trans = ttk.Labelframe(self.top,
                                        text='Transações')
        self.lfr_trans.grid(row=1, column=0)
        # widgets
        self.sct_trans = sct.ScrolledText(self.lfr_trans, width=40, height=15, state='disabled')
        self.sct_trans.grid(row=0, column=0)
        # att transacoes
        self.att_transacoes()

    def extrato(self):
        endereco = fd.askdirectory()
        a = max([len(i) for i in self.conta.extrato.registros])
        with open(f'{endereco}/{str(self.day_now()).zfill(2)}'
                  f'{str(self.month_now()).zfill(2)}_'
                  f'{str(self.seg_now()).zfill(2)}-'
                  f'{str(self.conta.numero).zfill(3)}.txt', 'w', encoding='utf-8') as fl:

            fl.write(f'{"*" * a}\n')
            for linha in self.conta.extrato.registros:
                fl.write(linha + '\n')
            fl.write(f'{"*" * a}\n')
            fl.write(f'Saldo total : R$ {self.conta.saldo:,.2f}\n')
            fl.write(f'Movimentação: R$ {sum([abs(x) for x in self.conta.extrato.movimentacao]):,.2f}\n')
            extrato_criado = msg.showinfo('Extrato', 'Extrato criado com sucesso')

    def cancelar_conta(self):
        if self.conta.cancelar_conta():
            info_exclusao = msg.showinfo('Excluir conta!',
                                         'Conta excluída com sucesso.')
            self.ref.voltar()
        else:
            erro_exclusao = msg.showerror('Excluir conta',
                                          'Erro ao excluir conta\n'
                                          'A conta ainda possui saldo.')

    def ccancel_bind(self, ev):
        if msg.askyesno('Excluir conta',
                        'Realmente deseja excluir conta?', ):
            self.cancelar_conta()

    def lbl_frame_operacoes(self):
        def saque_bind(ev):
            self.top_saque_depo(1)

        def deposito_bind(ev):
            self.top_saque_depo(2)

        def transferencia_bind(ev):
            self.top_tranferir()

        def extrato_bind(ev):
            self.extrato()

        # ----------------------------------------------
        self.lfr_op = ttk.Labelframe(self.top,
                                     text='Operações')
        self.lfr_op.grid(row=1, column=1, sticky='ns')
        # widgets
        self.btt_deposito = ttk.Button(self.lfr_op,
                                       text='Depósito')
        self.btt_deposito.grid(row=0, column=0)
        self.btt_deposito.bind('<ButtonRelease-1>', deposito_bind)
        self.btt_saque = ttk.Button(self.lfr_op,
                                    text='Saque')
        self.btt_saque.grid(row=1, column=0)
        self.btt_saque.bind('<ButtonRelease-1>', saque_bind)
        self.btt_transferir = ttk.Button(self.lfr_op,
                                         text='Transferir')
        self.btt_transferir.grid(row=2, column=0)
        self.btt_transferir.bind('<ButtonRelease-1>', transferencia_bind)
        self.btt_extrato = ttk.Button(self.lfr_op,
                                      text='Extrato')
        self.btt_extrato.grid(row=3, column=0)
        self.btt_extrato.bind('<ButtonRelease-1>', extrato_bind)

    def att_mensal(self):
        if isinstance(self.conta, Cp):
            if self.conta.att_mensal():
                self.att_saldo()
                self.att_transacoes()
                conta_att = msg.showinfo('Atualização mensal',
                                         'Atualização realizada com sucesso!')
            else:
                erro_saldo = msg.showerror('Atualização mensal',
                                           'Não foi possível realizar a atualização!\n'
                                           'Saldo insuficiente, tente mais tarde')

    def __init__(self, top, ref, conta):
        self.top = top
        self.top.title('Conta')
        self.ref = ref
        self.conta = conta
        self.top.iconbitmap('imagem/icone_capi.ico')
        # chamada de label frames
        self.lbl_frame_dados()
        self.lbl_frame_saldo()
        self.lbl_frame_transacoes()
        self.lbl_frame_operacoes()
        # butao_top
        # voltar
        self.btt_voltar = ttk.Button(self.top,
                                     text='Voltar')
        self.btt_voltar.grid(row=2, column=1, sticky='e')
        self.btt_voltar.bind('<ButtonRelease->', lambda ev: self.ref.voltar())
        # cancelar conta
        self.btt_ccancel = ttk.Button(self.top,
                                      text='Cancelar Contar')
        self.btt_ccancel.grid(row=2, column=0, sticky='w')
        self.btt_ccancel.bind('<ButtonRelease-1>', self.ccancel_bind)
        # atualizar
        self.btt_att = ttk.Button(self.top,
                                  text='Atualizar')
        self.btt_att.bind('<ButtonRelease-1>', lambda ev: self.att_mensal())
        if isinstance(self.conta, Cp):
            self.btt_att.grid(row=2, column=0, padx=95, sticky='w')
