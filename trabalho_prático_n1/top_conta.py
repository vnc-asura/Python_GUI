from tkinter import ttk, messagebox as msg
import tkinter as tk
from conta import Conta, ContaPoupanca as Cp, ContaCorrente as Cc
from geometry import GeoPlace as Geo


class TopConta:
    def item_selecionado(self, ev):
        if self.tree.focus():
            self.btt_apagar['state'] = 'normal'

    def limpar_entradas(self):
        self.tipo_conta_var.set(0)
        self.saldo_var.set('0')
        self.senha_var.set('')
        self.cliente_var.set('')
        self.cliente_selecionado = ''
        self.banco_var.set('')
        self.banco_selecionado = ''

    def verificar_entradas(self):
        var = {'tipo_conta': self.tipo_conta_var.get(),
               'saldo': self.saldo_var.get(),
               'senha': self.senha_var.get(),
               'cliente': self.cliente_selecionado,
               'banco': self.banco_selecionado}
        if all(var.values()) and all([True if x.strip() != '' else False for x in var.values() if isinstance(x, str)]):
            return var
        else:
            return None

    def salvar(self):
        var = self.verificar_entradas()
        if var:
            if var['tipo_conta'] == 1:
                Cc.registrar_conta(entradas=var)
            elif var['tipo_conta'] == 2:
                Cp.registrar_conta(entradas=var)
            self.limpar_entradas()
            self.att_tree()
        else:
            erro_incompleto = msg.showerror('Erro no cadastro',
                                            'Há campo(s) vazio(s)!\n'
                                            'Preencha-o(s) e tente novamente')

    def att_tree(self):
        for x in self.tree.get_children():
            self.tree.delete(x)
        for conta in Conta.ativas.values():
            tipo = 'Corrente' if isinstance(conta, Cc) else 'Poupança'
            v = (str(conta.numero).zfill(3), conta.cliente, f'R$ {conta.saldo:,.2f}', tipo)
            self.tree.insert('', 'end', values=v)

    def lbl_frame_tipo_conta(self):
        self.lfr_tipo_conta = ttk.Labelframe(self.lfr_cadastro, text='Tipo de conta')
        self.lfr_tipo_conta.grid(row=0, column=0, pady=4, padx=3, rowspan=3, sticky='ns')
        # widgets
        self.tipo_conta_var = tk.IntVar(value=0)
        self.rd_corrente = ttk.Radiobutton(self.lfr_tipo_conta,
                                           text='Conta Corrente',
                                           value=1,
                                           variable=self.tipo_conta_var)
        self.rd_corrente.pack()
        self.rd_poupanca = ttk.Radiobutton(self.lfr_tipo_conta,
                                           text='Conta Poupança',
                                           value=2,
                                           variable=self.tipo_conta_var)
        self.rd_poupanca.pack()

    def top_banco(self):
        from top_banco_conta import TopBancoConta as Tbc
        self.top_bank = tk.Toplevel(self.top)
        self.top_bank.withdraw()
        att_top_bank = Tbc(self.top_bank, self)
        self.top_bank.geometry(Geo.centralizar_tela(self.top_bank))

    def top_cliente(self):
        from top_cliente_conta import TopClienteConta as Tcc
        self.top_cli = tk.Toplevel(self.top)
        self.top_cli.withdraw()
        att_top_cli = Tcc(self.top_cli, self)
        self.top_cli.geometry(Geo.centralizar_tela(self.top_cli))

    def apagar(self):
        conta = Conta.pesquisar_conta_num(self.tree.item(self.tree.focus())['values'][0])
        if conta.cancelar_conta():
            info_exclusao = msg.showinfo('Excluir conta!',
                                         'Conta excluida com sucesso!')
            self.att_tree()
        else:
            erro_exclusao = msg.showerror('Excluir conta',
                                          'Erro ao excluir conta!\n'
                                          'A conta ainda possui saldo.')

    def limpar_tree_selecao(self, ev):
        if str(self.btt_apagar['state']) == 'normal':
            self.tree.focus('')
            self.tree.selection_remove(self.tree.selection())
            self.btt_apagar['state'] = 'disabled'

    def lbl_frame_cadastro(self):
        def saldo_trace(*args):
            if len(self.saldo_var.get()):
                self.saldo_var.set(value=''.join([x for x in self.saldo_var.get() if not x.isalpha()]))

        def saldo_bind_in(ev):
            if self.saldo_var.get() == '0':
                self.saldo_var.set('')

        def saldo_bind_out(ev):
            if not self.saldo_var.get():
                self.saldo_var.set('0')

        def mostrar():
            if self.mostrar_var.get() > 0:
                self.ent_pass['show'] = ''
            else:
                self.ent_pass['show'] = '*'

        # --------------------------------------------------------------
        self.lfr_cadastro = ttk.Labelframe(self.top, text='cadastrar')
        self.lfr_cadastro.pack()
        self.lfr_cadastro.bind('<FocusIn>', self.limpar_tree_selecao)
        self.cliente_selecionado = ''
        self.banco_selecionado = ''
        #chamar label frame
        self.lbl_frame_tipo_conta()
        # widgets
        # saldo
        self.saldo_var = tk.StringVar(value='0')
        self.saldo_var.trace_add('write', saldo_trace)
        self.lbl_saldo = ttk.Label(self.lfr_cadastro,
                                   text='Saldo inicial:')
        self.lbl_saldo.grid(row=0, column=1, pady=4, padx=3, sticky='e')
        self.ent_saldo = ttk.Entry(self.lfr_cadastro,
                                   textvariable=self.saldo_var,
                                   justify='center')
        self.ent_saldo.grid(row=0, column=2, pady=4, padx=3)
        self.ent_saldo.bind('<FocusIn>', saldo_bind_in)
        self.ent_saldo.bind('<FocusOut>', saldo_bind_out)
        # cliente
        self.cliente_var = tk.StringVar()
        self.lbl_cliente = ttk.Label(self.lfr_cadastro,
                                     text='Cliente:')
        self.lbl_cliente.grid(row=0, column=3, pady=4, padx=3, sticky='e')
        self.ent_cliente = ttk.Entry(self.lfr_cadastro,
                                     state='disabled',
                                     textvariable=self.cliente_var,
                                     width=50,
                                     justify='center')
        self.ent_cliente.grid(row=0, column=4, pady=4, padx=3)
        # banco
        self.banco_var = tk.StringVar()
        self.lbl_banco = ttk.Label(self.lfr_cadastro,
                                   text='Banco:')
        self.lbl_banco.grid(row=1, column=3, pady=4, padx=3, sticky='e')
        self.ent_banco = ttk.Entry(self.lfr_cadastro,
                                   textvariable=self.banco_var,
                                   state='disabled',
                                   width=50,
                                   justify='center')
        self.ent_banco.grid(row=1, column=4, pady=4, padx=3)
        # senha
        self.senha_var = tk.StringVar()
        self.lbl_pass = ttk.Label(self.lfr_cadastro,
                                  text='Senha:')
        self.lbl_pass.grid(row=1, column=1, sticky='e', pady=4, padx=3)
        self.ent_pass = ttk.Entry(self.lfr_cadastro,
                                  justify='center',
                                  show='*',
                                  textvariable=self.senha_var)
        self.ent_pass.grid(row=1, column=2, pady=4, padx=3)
        self.mostrar_var = tk.IntVar()
        self.chk_mostrar = ttk.Checkbutton(self.lfr_cadastro,
                                           text='Mostrar',
                                           variable=self.mostrar_var,
                                           command=mostrar)
        self.chk_mostrar.grid(row=2, column=2, pady=4, padx=3, sticky='e')
        # butoes
        # salvar
        self.btt_salvar = ttk.Button(self.lfr_cadastro,
                                     text='Salvar')
        self.btt_salvar.grid(row=3, column=0, columnspan=6, sticky='ew', pady=4, padx=3)
        self.btt_salvar.bind('<ButtonRelease-1>', lambda ev: self.salvar())
        # adicionar
        # cliente
        self.btt_add1 = ttk.Button(self.lfr_cadastro,
                                   text='Adicionar')
        self.btt_add1.grid(row=0, column=5, pady=4, padx=3)
        self.btt_add1.bind('<ButtonRelease-1>', lambda ev: self.top_cliente())
        # banco
        self.btt_add2 = ttk.Button(self.lfr_cadastro,
                                   text='Adicionar')
        self.btt_add2.grid(row=1, column=5, padx=3, pady=4)
        self.btt_add2.bind('<ButtonRelease-1>', lambda ev: self.top_banco())

    def lbl_frame_registros(self):
        def pesquisa(*args):
            if len(self.pesq_var.get()) > 0:
                for x in self.tree.get_children():
                    self.tree.delete(x)
                for conta in Conta.ativas.values():
                    if self.pesq_var.get().lower() in conta.cliente.nome.lower():
                        tipo = 'Corrente' if isinstance(conta, Cc) else 'Poupança'
                        valores = (str(conta.numero).zfill(3), conta.cliente, f'R$ {conta.saldo:.2f}', tipo)
                        self.tree.insert('', 'end', values=valores)
            else:
                self.att_tree()

        def apagar_config():
            self.btt_apagar['state'] = 'disabled'

        def apagar_bind(ev):
            if str(self.btt_apagar['state']) == 'normal':
                if msg.askyesno('Excluir conta',
                                'Realmente deseja excluir conta?', ):
                    apagar_config()
                    self.apagar()
                    self.tree.focus('')
                    self.tree.selection_remove(self.tree.selection())
                else:
                    apagar_config()
                    self.tree.focus('')
                    self.tree.selection_remove(self.tree.selection())

        # -----------------------------------------------
        self.lfr_registros = ttk.Labelframe(self.top,
                                            text='Registros')
        self.lfr_registros.pack()
        # widgets
        # tree
        self.scr_tree = ttk.Scrollbar(self.lfr_registros)
        self.scr_tree.grid(row=1, column=4, sticky='ns')
        colunas = {'numero': 'Número',
                   'cliente': 'Cliente',
                   'saldo': 'Saldo',
                   'tipo': 'Tipo Conta'}
        self.tree = ttk.Treeview(self.lfr_registros,
                                 columns=list(colunas.keys()),
                                 show='headings',
                                 selectmode='browse')
        self.tree.grid(row=1, column=0, sticky='ew', columnspan=4)
        self.tree.bind('<<TreeviewSelect>>', self.item_selecionado)
        # config tree
        for var, nome in colunas.items():
            self.tree.heading(var, text=nome)
            self.tree.column(var, anchor='center')
        #pesquisa
        self.pesq_var = tk.StringVar()
        self.pesq_var.trace_add('write', pesquisa)
        self.lbl_pesq = ttk.Label(self.lfr_registros,
                                  text='Pesquisar:')
        self.lbl_pesq.grid(row=0, column=1, sticky='e')
        self.ent_pesq = ttk.Entry(self.lfr_registros,
                                  textvariable=self.pesq_var)
        self.ent_pesq.grid(row=0, column=2, sticky='ew')
        self.ent_pesq.bind('<FocusIn>', self.limpar_tree_selecao)
        self.btt_pesq_clear = ttk.Button(self.lfr_registros,
                                         text='X',
                                         command=lambda: self.ent_pesq.delete(0, tk.END))
        self.btt_pesq_clear.grid(row=0, column=3, sticky='w')

        # butoes
        self.btt_apagar = ttk.Button(self.lfr_registros,
                                     text='Apagar',
                                     state='disabled')
        self.btt_apagar.grid(row=2, column=3, sticky='e')
        self.btt_apagar.bind('<ButtonRelease-1>', apagar_bind)

    def cad_cliente_bind(self, ev):
        self.ref.janelas_control.pop().destroy()
        self.ref.tela.withdraw()
        self.ref.reg_cliente()

    def cad_banco_bind(self, ev):
        self.ref.janelas_control.pop().destroy()
        self.ref.tela.withdraw()
        self.ref.reg_banco()

    def __init__(self, top, ref):
        self.top = top
        self.ref = ref
        self.top.title('Registro Conta')
        self.top.iconbitmap('imagem/icone_capi.ico')
        # chamada de labelframes
        self.lbl_frame_cadastro()
        self.lbl_frame_registros()
        self.att_tree()
        # butao_top
        # voltar
        self.btt_voltar = ttk.Button(self.top,
                                     text='Voltar')
        self.btt_voltar.pack(side='bottom', anchor='se')
        self.btt_voltar.bind('<ButtonRelease-1>', lambda ev: self.ref.voltar())
        # cadastrar cliente
        self.btt_cad_cliente = ttk.Button(self.top,
                                          text='Cadastrar Cliente')
        self.btt_cad_cliente.pack(side='left', before=self.btt_voltar)
        self.btt_cad_cliente.bind('<ButtonRelease-1>', self.cad_cliente_bind)
        # cadastrar banco
        self.btt_cad_banco = ttk.Button(self.top,
                                        text='Cadastrar Banco')
        self.btt_cad_banco.pack(side='left', after=self.btt_cad_cliente)
        self.btt_cad_banco.bind('<ButtonRelease-1>', self.cad_banco_bind)

