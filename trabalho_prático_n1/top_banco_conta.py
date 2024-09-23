from tkinter import ttk
import tkinter as tk
from banco import Banco


class TopBancoConta:
    def att_tree(self):
        for x in self.tree.get_children():
            self.tree.delete(x)
        for banco in Banco.num_bancos.values():
            v = (banco.numero, banco.nome)
            self.tree.insert('', 'end', values=v)

    def item_selecionado(self, ev):
        if self.tree.focus():
            self.btt_top_add['state'] = 'normal'

    def pesquisa(self, *args):
        if len(self.pesq_var.get()) > 0:
            for x in self.tree.get_children():
                self.tree.delete(x)
            for banco in Banco.num_bancos.values():
                if self.pesq_var.get().lower() in banco.nome.lower():
                    valores = (banco.numero, banco.nome)
                    self.tree.insert('', 'end', values=valores)
        else:
            self.att_tree()

    def voltar(self):
        self.top.destroy()

    def comportamento_top(self):
        self.top.grab_set()

    def adicionar(self):
        from top_banco_acesso import TopBancoAcesso as Tba
        selecionado = [str(x) for x in self.tree.item(self.tree.focus())["values"]]
        self.ref.banco_selecionado = Banco.num_bancos[int(selecionado[0])]
        self.ref.banco_var.set(value=self.ref.banco_selecionado)
        self.voltar()
        if isinstance(self.ref, Tba):
            self.ref.verifica_mudanca()

    def add_bind(self, ev):
        if str(self.btt_top_add['state']) == 'normal':
            self.adicionar()

    def limpar_tree_selecao(self, ev):
        if str(self.btt_top_add['state']) == 'normal':
            self.tree.focus('')
            self.tree.selection_remove(self.tree.selection())
            self.btt_top_add['state'] = 'disabled'

    def __init__(self, top, ref):
        self.top = top
        self.top.title('Bancos')
        self.ref = ref
        self.top.iconbitmap('imagem/icone_capi.ico')
        # comportamento
        self.comportamento_top()
        #frame
        self.top_frame = ttk.Frame(self.top)
        self.top_frame.pack()
        # tree
        self.scr_tree = ttk.Scrollbar(self.top_frame)
        self.scr_tree.grid(row=1, column=4, sticky='ns')
        colunas = {'numero': 'Número',
                   'nome': 'Nome'}
        col_width = [60, 300]
        i = 0
        self.tree = ttk.Treeview(self.top_frame,
                                 columns=list(colunas.keys()),
                                 show='headings',
                                 selectmode='browse',
                                 yscrollcommand=self.scr_tree.set,
                                 height=10)
        self.tree.grid(row=1, column=0, columnspan=4, sticky='ew')
        self.tree.bind('<<TreeviewSelect>>', self.item_selecionado)
        # config tree
        for var, nome in colunas.items():
            self.tree.heading(var, text=nome)
            self.tree.column(var, width=col_width[i], anchor='center')
            i += 1
        self.scr_tree.config(command=self.tree.yview)
        # att tree
        self.att_tree()
        # pesquisa
        self.pesq_var = tk.StringVar()
        self.pesq_var.trace_add('write', self.pesquisa)
        self.lbl_pesq = ttk.Label(self.top_frame,
                                  text='Pesquisar:')
        self.lbl_pesq.grid(row=0, column=1, sticky='e')
        self.ent_pesq = ttk.Entry(self.top_frame,
                                  textvariable=self.pesq_var)
        self.ent_pesq.grid(row=0, column=2, sticky='ew')
        self.ent_pesq.bind('<FocusIn>', self.limpar_tree_selecao)
        self.btt_pesq_clear = ttk.Button(self.top_frame,
                                         text='X',
                                         command=lambda: self.ent_pesq.delete(0, tk.END))
        self.btt_pesq_clear.grid(row=0, column=3, sticky='w')
        # butoes
        self.btt_top_add = ttk.Button(self.top_frame,
                                      text='Adicionar',
                                      state='disabled')
        self.btt_top_add.grid(row=2, column=2, sticky='ew')
        self.btt_top_add.bind('<ButtonRelease-1>', self.add_bind)
        self.btt_top_voltar = ttk.Button(self.top_frame,
                                         text='Voltar')
        self.btt_top_voltar.grid(row=2, column=3, sticky='ew')
        self.btt_top_voltar.bind('<ButtonRelease-1>', lambda ev: self.voltar())

