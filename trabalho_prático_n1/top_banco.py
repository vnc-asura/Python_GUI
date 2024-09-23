from tkinter import ttk
from tkinter import messagebox as msg
import tkinter as tk
from banco import Banco


class TopBanco:
    def item_selecionado(self, ev):
        if self.tree.focus():
            self.btt_editar['state'] = 'normal'
            self.btt_acessar['state'] = 'normal'

    def verifica_entradas(self):
        var = {'numero': self.num_var.get(),
               'nome': self.nome_var.get(),
               'desconto': self.desc_var.get(),
               'taxa': self.taxa_var.get()}
        n = var.copy()
        if all([True if x.strip() != '' else False for x in var.values()]):
            return var
        else:
            return 0

    def limpar_entradas(self):
        var = {'numero': self.num_var,
               'nome': self.nome_var,
               'desconto': self.desc_var,
               'taxa': self.taxa_var}
        for v in var.values():
            v.set('')

    def salvar(self):
        entradas = self.verifica_entradas()
        if entradas:
            if Banco.registrar_banco(entradas):
                self.limpar_entradas()
                self.att_tree()
            else:
                aviso_reptido = msg.showerror('Erro no cadastro',
                                              'O numero inserido já está sendo usado por outro banco.\n Tente outro!')
        else:
            aviso_incompleto = msg.showerror('Erro no cadastro',
                                             'Há campo(s) vazio(s)!\nPreencha-o(s) e tente novamente.')

    def acessar(self):
        # from banco import Banco
        banco = Banco.pesquisar_banco_num(int(self.tree.item(self.tree.focus())['values'][0]))
        self.ref.janelas_control.pop().destroy()
        self.ref.banco_acesso(banco)

    def limpar_tree(self):
        for x in self.tree.get_children():
            self.tree.delete(x)

    def att_tree(self):
        self.limpar_tree()
        for num, banco in Banco.num_bancos.items():
            v = (num, banco.nome, f'R$ {banco.desconto:,.2f}', f'R$ {banco.taxa:,.2f}')
            self.tree.insert('', 'end', values=v)

    def numero_trace(self, *args):
        self.num_var.set(value=''.join([i for i in self.num_var.get() if i.isdigit()]))

    def limpar_tree_selecao(self, ev):
        if str(self.btt_editar['state']) == 'normal':
            self.tree.focus('')
            self.tree.selection_remove(self.tree.selection())
            self.btt_editar['state'] = 'disabled'
            self.btt_acessar['state'] = 'disabled'

    def valores_trace(self, var):
        var.set(value=''.join([s for s in var.get() if not s.isalpha()]))

    def lbl_frame_cadastro(self):
        # label frame
        self.lfr_cad = ttk.Labelframe(self.top,
                                      text='Cadastrar')
        self.lfr_cad.pack(before=self.lfr_reg)
        self.lfr_cad.bind('<FocusIn>', self.limpar_tree_selecao)
        # widgets
        # numero
        self.lbl_num = ttk.Label(self.lfr_cad,
                                 text='Numero:')
        self.lbl_num.grid(row=0, column=0, sticky='e', padx=4)
        self.num_var = tk.StringVar()
        self.num_var.trace_add(mode='write', callback=self.numero_trace)
        self.ent_num = ttk.Entry(self.lfr_cad,
                                 textvariable=self.num_var)
        self.ent_num.grid(row=0, column=1)
        #nome
        self.lbl_nome = ttk.Label(self.lfr_cad,
                                  text='Nome:')
        self.lbl_nome.grid(row=1, column=0, sticky='e', padx=4)
        self.nome_var = tk.StringVar()
        self.ent_nome = ttk.Entry(self.lfr_cad,
                                  textvariable=self.nome_var)
        self.ent_nome.grid(row=1, column=1, sticky='ew')
        # desconto
        self.lbl_desc = ttk.Label(self.lfr_cad,
                                  text='Valor desconto:')
        self.lbl_desc.grid(row=2, column=0, sticky='e', padx=4)
        self.desc_var = tk.StringVar()
        self.desc_var.trace_add('write', lambda *args: self.valores_trace(self.desc_var))
        self.ent_desc = ttk.Entry(self.lfr_cad,
                                  textvariable=self.desc_var)
        self.ent_desc.grid(row=2, column=1)
        # taxa att
        self.lbl_taxa = ttk.Label(self.lfr_cad,
                                  text='Valor taxa:')
        self.lbl_taxa.grid(row=3, column=0, sticky='e', padx=4)
        self.taxa_var = tk.StringVar()
        self.taxa_var.trace_add('write', lambda *args: self.valores_trace(self.taxa_var))
        self.ent_taxa = ttk.Entry(self.lfr_cad,
                                  textvariable=self.taxa_var)
        self.ent_taxa.grid(row=3, column=1)
        self.ent_taxa.bind('<Return>', lambda ev: self.salvar())
        # butoes
        self.btt_salvar = ttk.Button(self.lfr_cad,
                                     text='Salvar',
                                     command=self.salvar)
        self.btt_salvar.grid(row=4, column=0, columnspan=2, sticky='ew')

    def lbl_frame_registros(self):
        def editar_bind(ev):
            if str(self.btt_editar['state']) == 'normal':
                mudar_frame_att()

        def acessar_bind(ev):
            if str(self.btt_acessar['state']) == 'normal':
                self.acessar()

        def mudar_frame_att():
            self.lfr_cad.destroy()
            self.lbl_frame_atualizar()

        def pesquisa(*args):
            if len(self.pesquisa_var.get()) > 0:
                self.limpar_tree()
                for num, banco in Banco.num_bancos.items():
                    if self.pesquisa_var.get().lower() in banco.nome.lower():
                        v = (num, banco.nome, f'R$ {banco.desconto:,.2f}', f'R$ {banco.taxa:,.2f}')
                        self.tree.insert('', 'end', values=v)
            else:
                self.att_tree()

        # -----------------------------------------------
        self.lfr_reg = ttk.Labelframe(self.top,
                                      text='Registros')
        self.lfr_reg.pack()
        #widgets
        self.scr_tree = ttk.Scrollbar(self.lfr_reg)
        self.scr_tree.grid(row=1, column=4, sticky='ns')
        colunas = 'numero,nome,desconto,taxa'.split(',')
        self.tree = ttk.Treeview(self.lfr_reg,
                                 columns=colunas,
                                 show='headings',
                                 yscrollcommand=self.scr_tree.set,
                                 selectmode='browse')
        self.tree.grid(row=1, column=0, columnspan=4, sticky='ew')
        self.tree.bind('<<TreeviewSelect>>', self.item_selecionado)

        for var, nome in zip(colunas, [x.capitalize() for x in colunas]):
            self.tree.heading(var, text=nome)
            self.tree.column(var, anchor='center')
        self.scr_tree.config(command=self.tree.yview)
        # pesquisa
        self.pesquisa_var = tk.StringVar()
        self.pesquisa_var.trace_add('write', pesquisa)
        self.lbl_pesquisa = ttk.Label(self.lfr_reg,
                                      text='Pesquisar')
        self.lbl_pesquisa.grid(row=0, column=1, sticky='e', padx=2)
        self.ent_pesquisar = ttk.Entry(self.lfr_reg,
                                       textvariable=self.pesquisa_var)
        self.ent_pesquisar.grid(row=0, column=2, sticky='ew', padx=2)
        self.ent_pesquisar.bind('<FocusIn>', self.limpar_tree_selecao)
        self.btt_pesquisar_clean = ttk.Button(self.lfr_reg,
                                              text='X')
        self.btt_pesquisar_clean.grid(row=0, column=3, sticky='w', padx=2)
        self.btt_pesquisar_clean.bind('<ButtonRelease-1>', lambda ev: self.pesquisa_var.set(''))
        # •butoes
        # editar
        self.btt_editar = ttk.Button(self.lfr_reg,
                                     text='Editar',
                                     state='disabled')
        self.btt_editar.grid(row=2, column=3, columnspan=2, sticky='ew')
        self.btt_editar.bind('<ButtonRelease-1>', editar_bind)
        # acessar
        self.btt_acessar = ttk.Button(self.lfr_reg,
                                      text='Acessar',
                                      state='disabled')
        self.btt_acessar.grid(row=2, column=0, sticky='ew', columnspan=2)
        self.btt_acessar.bind('<ButtonRelease-1>', acessar_bind)

    def lbl_frame_atualizar(self):
        def mudar_frame_cadastro():
            self.lfr_att.destroy()
            self.lbl_frame_cadastro()
            self.tree.config(selectmode='browse')
            self.att_tree()

        def att_banco():
            entradas = self.verifica_entradas()
            if entradas:
                atual = self.tree.item(self.tree.focus())['values'][0]
                if Banco.atualizar_banco(entradas, atual):
                    mudar_frame_cadastro()
                    aviso_att = msg.showinfo('Atualização banco', 'O banco foi atualizado com sucesso!')
                else:
                    erro_att = msg.showerror('Atualização Banco',
                                             'Erro na atualização, o número inserido já existe.\n'
                                             'Tente novamente.')
            else:
                erro_entrada = msg.showerror('Atualização Banco', 'Há campos incompletos')

        def att_entradas():
            atual = self.tree.item(self.tree.focus())['values']
            banco = Banco.num_bancos[atual[0]]
            self.num_var.set(banco.numero)
            self.nome_var.set(banco.nome)
            self.desc_var.set(banco.desconto)
            self.taxa_var.set(banco.taxa)

        def registro_config():
            self.tree.config(selectmode='none')
            self.btt_editar.config(state='disabled')
            self.btt_acessar.config(state='disabled')

        # --------------------------------------------
        registro_config()
        self.lfr_att = ttk.Labelframe(self.top,
                                      text='Atualizar')
        self.lfr_att.pack(before=self.lfr_reg)
        # widgets
        #numero
        self.lbl_num = ttk.Label(self.lfr_att,
                                 text='Numero:')
        self.lbl_num.grid(row=0, column=0, sticky='e', padx=4)
        self.num_var = tk.StringVar()
        self.num_var.trace_add('write', self.numero_trace)
        self.ent_num = ttk.Entry(self.lfr_att,
                                 textvariable=self.num_var)
        self.ent_num.grid(row=0, column=1, columnspan=3, sticky='ew')
        # nome
        self.lbl_nome = ttk.Label(self.lfr_att,
                                  text='Nome:')
        self.lbl_nome.grid(row=1, column=0, sticky='e', padx=4)
        self.nome_var = tk.StringVar()
        self.ent_nome = ttk.Entry(self.lfr_att,
                                  textvariable=self.nome_var)
        self.ent_nome.grid(row=1, column=1, sticky='ew')
        # desconto
        self.lbl_desc = ttk.Label(self.lfr_att,
                                  text='Valor desconto:')
        self.lbl_desc.grid(row=2, column=0, sticky='e', padx=4)
        self.desc_var = tk.StringVar()
        self.desc_var.trace_add('write', lambda *args: self.valores_trace(self.desc_var))
        self.ent_desc = ttk.Entry(self.lfr_att,
                                  textvariable=self.desc_var)
        self.ent_desc.grid(row=2, column=1)
        # taxa att
        self.lbl_taxa = ttk.Label(self.lfr_att,
                                  text='Valor taxa:')
        self.lbl_taxa.grid(row=3, column=0, sticky='e', padx=4)
        self.taxa_var = tk.StringVar()
        self.taxa_var.trace_add('write', lambda *args: self.valores_trace(self.taxa_var))
        self.ent_taxa = ttk.Entry(self.lfr_att,
                                  textvariable=self.taxa_var)
        self.ent_taxa.grid(row=3, column=1)
        self.ent_taxa.bind('<Return>', lambda ev: att_banco())
        # butoes
        self.btt_att = ttk.Button(self.lfr_att,
                                  text='Atualizar',
                                  command=att_banco)
        self.btt_att.grid(row=4, column=0, sticky='ew', padx=2, pady=3)
        self.btt_cancelar = ttk.Button(self.lfr_att,
                                       text='Cancelar',
                                       command=mudar_frame_cadastro)
        self.btt_cancelar.grid(row=4, column=1, sticky='ew', padx=2, pady=3)
        
        att_entradas()

    def cad_conta_bind(self, ev):
        self.ref.janelas_control.pop().destroy()
        self.ref.tela.withdraw()
        self.ref.reg_conta()

    def cad_cliente_bind(self, ev):
        self.ref.janelas_control.pop().destroy()
        self.ref.tela.withdraw()
        self.ref.reg_cliente()

    def __init__(self, top, ref):
        self.top = top
        self.top.title('Registro Banco')
        self.top.iconbitmap('imagem/icone_capi.ico')
        self.ref = ref
        # chamada de labelframe
        self.lbl_frame_registros()
        self.lbl_frame_cadastro()
        self.att_tree()
        # butao_top
        # voltar
        self.btt_voltar = ttk.Button(self.top,
                                     text='Voltar',
                                     command=ref.voltar)
        self.btt_voltar.pack(side='bottom', anchor='e')
        # cadastrar cliente
        self.btt_cad_cliente = ttk.Button(self.top,
                                          text='Cadastrar Cliente')
        self.btt_cad_cliente.pack(side='left', before=self.btt_voltar)
        self.btt_cad_cliente.bind('<ButtonRelease-1>', self.cad_cliente_bind)
        # cadastrar conta
        self.btt_cad_conta = ttk.Button(self.top,
                                        text='Cadastrar Conta')
        self.btt_cad_conta.pack(side='left', after=self.btt_cad_cliente)
        self.btt_cad_conta.bind('<ButtonRelease-1>', self.cad_conta_bind)
