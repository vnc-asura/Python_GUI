import tkinter as tk
from tkinter import ttk


class TopBancoAcesso:
    def top_banco(self):
        from top_banco_conta import TopBancoConta as Tbc
        from geometry import GeoPlace as Geo
        self.top_bank = tk.Toplevel(self.top)
        self.top_bank.withdraw()
        att_top_bank = Tbc(self.top_bank, self)
        self.top_bank.geometry(Geo.centralizar_tela(self.top_bank))

    def limpar_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def att_tree(self):
        if self.banco_selecionado:
            self.limpar_tree()
            for conta in self.banco_selecionado.num_contas.values():
                dados = (str(conta.numero).zfill(3),
                         conta.cliente.nome,
                         f'R$ {conta.saldo:,.2f}',
                         'Ativa' if conta.status else 'Cancelada')
                self.tree.insert('', 'end', values=dados)
            self.lbl_valor['text'] = (f'Valor total: R$ '
                                      f'{sum([float(x.saldo) for x in self.banco_selecionado.num_contas.values()]):,.2f}')
            self.lbl_qtd_contas['text'] = (f'Quantidade total de contas: '
                                           f'{len(self.banco_selecionado.num_contas.values())}')
            self.lbl_desc['text'] = f'Valor desconto: R$ {self.banco_selecionado.desconto:,.2f}'
            self.lbl_taxa['text'] = f'Valor taxa: R$ {self.banco_selecionado.taxa:,.2f}'
            if not self.banco_var.get():
                self.banco_var.set(self.banco_selecionado)

    def verifica_mudanca(self):
        if self.banco_selecionado != self.banco_anterior:
            self.att_tree()
            self.banco_anterior = self.banco_selecionado

    def label_frame_contas(self):
        def pesquisa_trace(*args):
            if self.banco_selecionado:
                if len(self.pesquisa_var.get()) > 0:
                    self.limpar_tree()
                    for conta in self.banco_selecionado.num_contas.values():
                        if self.pesquisa_var.get().lower() in conta.cliente.nome.lower():
                            valores = (str(conta.numero).zfill(3),
                                       conta.cliente.nome,
                                       f'R$ {conta.saldo:,.2f}',
                                       'Ativa' if conta.status else 'Cancelada')
                            self.tree.insert('', 'end', values=valores)
                else:
                    self.att_tree()

        # --------------------------------------------------
        self.lfr_contas = ttk.Labelframe(self.top,
                                         text='Contas')
        self.lfr_contas.grid(row=1, column=0)
        #widgets
        colunas = {'numero': 'Número',
                   'titular': 'Titular',
                   'saldo': 'Saldo',
                   'status': 'Status'}
        colunas_width = [60, 250, 70, 80]
        i = 0
        self.scb_tree = ttk.Scrollbar(self.lfr_contas)
        self.scb_tree.grid(row=1, column=4, sticky='ns')
        self.tree = ttk.Treeview(self.lfr_contas,
                                 columns=list(colunas.keys()),
                                 show='headings',
                                 yscrollcommand=self.scb_tree.set)
        self.tree.grid(row=1, column=0, columnspan=4, sticky='ew')
        self.scb_tree.config(command=self.tree.yview)
        for var, nome in colunas.items():
            self.tree.heading(var, text=nome)
            self.tree.column(var, width=colunas_width[i], anchor='center')
            i += 1
        # pesquisa
        self.pesquisa_var = tk.StringVar()
        self.pesquisa_var.trace_add('write', pesquisa_trace)
        self.lbl_pesquisa = ttk.Label(self.lfr_contas,
                                      text='Pesquisar:')
        self.lbl_pesquisa.grid(row=0, column=1, sticky='e')
        self.ent_pesquisa = ttk.Entry(self.lfr_contas,
                                      textvariable=self.pesquisa_var)
        self.ent_pesquisa.grid(row=0, column=2, sticky='ew')
        self.btt_pesquisa_clean = ttk.Button(self.lfr_contas,
                                             text='X')
        self.btt_pesquisa_clean.grid(row=0, column=3, sticky='w')
        self.btt_pesquisa_clean.bind('<ButtonRelease-1>', lambda ev: self.pesquisa_var.set(''))

    def label_frame_escolha_banco(self):
        def select_bind(ev):
            self.top_banco()

        # ------------------------------------------------------
        self.lfr_banco = ttk.Labelframe(self.top,
                                        text='Escolha o Banco')
        self.lfr_banco.grid(row=0, column=0, padx=5, pady=4)
        #widgets
        # banco
        self.banco_var = tk.StringVar()
        self.lbl_banco = ttk.Label(self.lfr_banco,
                                   text='Banco:')
        self.lbl_banco.grid(row=0, column=0, padx=5, pady=4)
        self.ent_banco = ttk.Entry(self.lfr_banco,
                                   textvariable=self.banco_var,
                                   width=40,
                                   state='disabled')
        self.ent_banco.grid(row=0, column=1, padx=5, pady=4)
        # valor em banco
        self.lbl_valor = ttk.Label(self.lfr_banco)
        self.lbl_valor.grid(row=2, column=0)
        # quantidade contas
        self.lbl_qtd_contas = ttk.Label(self.lfr_banco)
        self.lbl_qtd_contas.grid(row=2, column=1)
        # valor desconto
        self.lbl_desc = ttk.Label(self.lfr_banco)
        self.lbl_desc.grid(row=3, column=0)
        # valor taxa
        self.lbl_taxa = ttk.Label(self.lfr_banco)
        self.lbl_taxa.grid(row=3, column=1)
        # separador
        self.sep = ttk.Separator(self.lfr_banco)
        self.sep.grid(row=1, column=0, columnspan=3, sticky='ew', padx=5, pady=5)
        # butao
        self.btt_select = ttk.Button(self.lfr_banco,
                                     text='Selecionar')
        self.btt_select.grid(row=0, column=2, padx=5, pady=4)
        self.btt_select.bind('<ButtonRelease-1>', select_bind)

    def __init__(self, top, ref, banco=''):
        self.top = top
        self.top.title('Banco')
        self.ref = ref
        self.top.iconbitmap('imagem/icone_capi.ico')
        # variaveis
        self.banco_selecionado = banco
        self.banco_anterior = self.banco_selecionado
        # Chamar labels frame
        self.label_frame_escolha_banco()
        self.label_frame_contas()
        self.att_tree()
        #   butao
        self.btt_voltar = ttk.Button(self.top,
                                     text='Voltar')
        self.btt_voltar.grid(row=2, column=0, sticky='e')
        self.btt_voltar.bind('<ButtonRelease-1>', lambda ev: self.ref.voltar())
