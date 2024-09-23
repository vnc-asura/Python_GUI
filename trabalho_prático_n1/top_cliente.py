import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from cliente import Cliente


class TopCliente:
    def item_selecionado(self, ev):
        if self.tree.focus():
            self.btt_editar['state'] = 'normal'
            self.btt_apagar['state'] = 'normal'

    def verifica_entradas(self):
        def verifica_tam():
            var = {'cpf': self.cpf_var.get(),
                   'telefone': self.tel_var.get(),
                   'cep': self.cep_var.get()}

            var_tam = {'cpf': 14,
                       'telefone': 13,
                       'cep': 9}
            if all([True if len(ent) == var_tam[item] else False for item, ent in var.items()]):
                return 1
            else:
                return 0

        # -----------------------------------------
        var = {'nome': self.nome_var.get(),
               'cpf': self.cpf_var.get(),
               'genero': self.gen_var.get(),
               'telefone': self.tel_var.get(),
               'logradouro': self.log_var.get(),
               'numero': self.num_var.get(),
               'cidade': self.cida_var.get(),
               'bairro': self.bairro_var.get(),
               'uf': self.uf_var.get(),
               'cep': self.cep_var.get()}

        if all([True if x.strip() != '' else False for x in var.values()]) and verifica_tam():
            var['complemento'] = self.com_var.get() if self.com_var.get().strip() != '' else ''
            return var
        else:
            return 0

    def limpar_entradas(self):
        var = {'nome': self.nome_var,
               'cpf': self.cpf_var,
               'genero': self.gen_var,
               'telefone': self.tel_var,
               'logradouro': self.log_var,
               'numero': self.num_var,
               'cidade': self.cida_var,
               'bairro': self.bairro_var,
               'uf': self.uf_var,
               'cep': self.cep_var,
               'complemento': self.com_var}
        for v in var.values():
            v.set('')

    def att_tree(self):
        for x in self.tree.get_children():
            self.tree.delete(x)
        for cliente in Cliente.ativos.values():
            v = (str(cliente.id).zfill(3), cliente.nome, cliente.cpf, cliente.endereco)
            self.tree.insert('', 'end', values=v)

    def apagar(self):
        cliente = Cliente.pesquisa_cliente_num(self.tree.item(self.tree.focus())['values'][0])
        if cliente.cancelar_cliente():
            info_exclusao = msg.showinfo('Excluir cliente',
                                         'Cliente excluido com sucesso!')
            self.att_tree()
        else:
            erro_exclusao = msg.showerror('Excluir cliente',
                                          'Erro ao excluir cliente\n'
                                          'O cliente ainda está associado a uma conta')

    def atualizar(self):
        entrada = self.verifica_entradas()
        if entrada:
            conta = Cliente.pesquisa_cliente_num(int(self.tree.item(self.tree.focus())['values'][0]))
            Cliente.atualizar_cliente(entrada, conta)
            self.att_tree()
            self.limpar_entradas()
            return 1
        else:
            erro_incompleto = msg.showerror('Erro na atualização',
                                            'Há campo(s) vazio(s) ou incompleto(s)!\n'
                                            'Preencha-o(s) e tente novamente')
            return 0

    def salvar(self):
        var = self.verifica_entradas()
        if var:
            if Cliente.registrar_cliente(var):
                self.att_tree()
                self.limpar_entradas()
            else:
                erro_conflito_cpf = msg.showerror('Erro no cadastro',
                                                  'O cpf inserido já existe!\n'
                                                  'Tente outro')
        else:
            erro_incompleto = msg.showerror('Erro no cadastro',
                                            'Há campo(s) vazio(s) ou imcompleto(s)!\n'
                                            'Preencha-o(s) e tente novamente')

    def limpar_tree_selecao(self, ev):
        if str(self.btt_apagar['state']) == 'normal':
            self.tree.focus('')
            self.tree.selection_remove(self.tree.selection())
            self.btt_editar['state'] = 'disabled'
            self.btt_apagar['state'] = 'disabled'

    def lbl_frame_cadastro(self):
        def att_bind(ev):
            if self.atualizar():
                edit_desconfig()
                aviso_sucesso = msg.showinfo('Atualização cliente',
                                             'O cliente foi atualizado com sucesso!')

        def edit_desconfig():
            self.limpar_entradas()
            # config label_frame cadastro
            self.lfr_cadastro['text'] = 'Cadastrar'
            self.ent_cpf['state'] = 'normal'
            # config label_frame registro
            self.tree['selectmode'] = 'browse'
            self.tree.focus('')
            self.tree.selection_remove(self.tree.selection())
            # mostrar butao
            self.btt_salvar.grid(row=self.salvar_grid['row'],
                                 column=self.salvar_grid['column'],
                                 columnspan=self.salvar_grid['columnspan'],
                                 sticky=self.salvar_grid['sticky'],
                                 pady=self.salvar_grid['pady'],
                                 padx=self.salvar_grid['padx'])
            # desaparecer butoes
            self.btt_atualizar.grid_forget()
            self.btt_cancelar.grid_forget()

        def cpf_trace(*args):
            pont = {2: '.', 5: '.', 8: '-'}
            valor = [i for i in self.cpf_var.get() if i not in ['.', '-']]
            self.cpf_var.set(''.join([f'{y}{pont[x]}' if x in pont.keys() else y for x, y in enumerate(valor) if y.isdigit()]))
            self.ent_cpf.icursor(tk.END)
            if len(valor) >= 11:
                self.ent_cpf.delete(14, tk.END)

        def tel_trace(*args):
            pont = {1: '_', 6: '-'}
            valor = [i for i in self.tel_var.get() if i not in ['_', '-']]
            self.tel_var.set(''.join([f'{y}{pont[x]}' if x in pont.keys() else y for x, y in enumerate(valor) if y.isdigit()]))
            self.ent_tel.icursor(tk.END)
            if len(valor) > 11:
                self.ent_tel.delete(13, tk.END)

        def cep_trace(*args):
            valor = [i for i in self.cep_var.get() if i != '-']
            self.cep_var.set(''.join([f'{y}-' if x == 4 else y for x, y in enumerate(valor) if y.isdigit()]))
            self.ent_cep.icursor(tk.END)
            if len(valor) > 8:
                self.ent_cep.delete(9, tk.END)

        # ------------------------------------------------------------------------------------
        self.lfr_cadastro = ttk.Labelframe(self.top, text='Cadastrar')
        self.lfr_cadastro.pack()
        self.lfr_cadastro.bind('<FocusIn>', self.limpar_tree_selecao)
        # widgets
        # nome
        self.nome_var = tk.StringVar()
        self.lbl_nome = ttk.Label(self.lfr_cadastro, text='Nome:')
        self.lbl_nome.grid(row=0, column=0, sticky='e')
        self.ent_nome = ttk.Entry(self.lfr_cadastro,
                                  width=50,
                                  justify='center',
                                  textvariable=self.nome_var)
        self.ent_nome.grid(row=0, column=1, pady=4, padx=3)
        # cpf
        self.cpf_var = tk.StringVar()
        self.cpf_var.trace_add('write', cpf_trace)
        self.lbl_cpf = ttk.Label(self.lfr_cadastro,
                                 text='CPF:')
        self.lbl_cpf.grid(row=0, column=2, sticky='e')
        self.ent_cpf = ttk.Entry(self.lfr_cadastro,
                                 textvariable=self.cpf_var,
                                 justify='center')
        self.ent_cpf.grid(row=0, column=3, pady=4, padx=3, columnspan=3, sticky='ew')
        # genero
        generos = ('Homem-Cis', 'Mulher-Cis', 'Homem-Trans', 'Mulher-Trans', 'Não binário')
        self.gen_var = tk.StringVar()
        self.lbl_gen = ttk.Label(self.lfr_cadastro,
                                 text='Genero:')
        self.lbl_gen.grid(row=1, column=0, sticky='e')
        self.cbb_gen = ttk.Combobox(self.lfr_cadastro,
                                    values=generos,
                                    state='readonly',
                                    justify='center',
                                    textvariable=self.gen_var)
        self.cbb_gen.grid(row=1, column=1, sticky='w', pady=4, padx=3)
        # telefone
        self.tel_var = tk.StringVar()
        self.tel_var.trace_add('write', tel_trace)
        self.lbl_tel = ttk.Label(self.lfr_cadastro,
                                 text='Telefone:')
        self.lbl_tel.grid(row=1, column=2, sticky='e')
        self.ent_tel = ttk.Entry(self.lfr_cadastro,
                                 textvariable=self.tel_var,
                                 justify='center')
        self.ent_tel.grid(row=1, column=3, pady=4, padx=3, columnspan=3, sticky='ew')
        # separador
        self.separator = ttk.Separator(self.lfr_cadastro,
                                       orient=tk.HORIZONTAL)
        self.separator.grid(row=2, column=0, columnspan=6, sticky='ew', pady=10)
        # logradouro
        self.log_var = tk.StringVar()
        self.lbl_log = ttk.Label(self.lfr_cadastro,
                                 text='Logradouro:')
        self.lbl_log.grid(row=3, column=0, sticky='e')
        self.ent_log = ttk.Entry(self.lfr_cadastro,
                                 width=50,
                                 justify='center',
                                 textvariable=self.log_var)
        self.ent_log.grid(row=3, column=1, pady=4, padx=3)
        # numero
        self.num_var = tk.StringVar()
        self.lbl_num = ttk.Label(self.lfr_cadastro,
                                 text='Número:')
        self.lbl_num.grid(row=3, column=2, sticky='e')
        self.ent_num = ttk.Entry(self.lfr_cadastro,
                                 width=8,
                                 justify='center',
                                 textvariable=self.num_var)
        self.ent_num.grid(row=3, column=3, sticky='w', pady=4, padx=3)
        # cidade
        self.cida_var = tk.StringVar()
        self.lbl_cida = ttk.Label(self.lfr_cadastro,
                                  text='Cidade:')
        self.lbl_cida.grid(row=4, column=0, sticky='e')
        self.ent_cida = ttk.Entry(self.lfr_cadastro,
                                  width=40,
                                  justify='center',
                                  textvariable=self.cida_var)
        self.ent_cida.grid(row=4, column=1, pady=4, padx=3, sticky='w')
        # bairro
        self.bairro_var = tk.StringVar()
        self.lbl_bairro = ttk.Label(self.lfr_cadastro,
                                    text='Bairro:')
        self.lbl_bairro.grid(row=4, column=2, sticky='e')
        self.ent_bairro = ttk.Entry(self.lfr_cadastro,
                                    justify='center',
                                    textvariable=self.bairro_var)
        self.ent_bairro.grid(row=4, column=3, pady=4, padx=3)
        # uf
        estados = sorted('AC,AL,AP,AM,BA,CE,DF,ES,GO,MA,MT,MS,MG,PA,PB,PR,PE,PI,RJ,RN,RS,RO,RR,SC,SP,SE,TO'.split(','))
        self.uf_var = tk.StringVar()
        self.lbl_uf = ttk.Label(self.lfr_cadastro,
                                text='UF:')
        self.lbl_uf.grid(row=4, column=4, sticky='e')
        self.cbb_uf = ttk.Combobox(self.lfr_cadastro,
                                   values=estados,
                                   state='readonly',
                                   width=8,
                                   justify='center',
                                   textvariable=self.uf_var)
        self.cbb_uf.grid(row=4, column=5, pady=4, padx=3)
        # cep
        self.cep_var = tk.StringVar()
        self.cep_var.trace_add('write', cep_trace)
        self.lbl_cep = ttk.Label(self.lfr_cadastro, text='CEP:')
        self.lbl_cep.grid(row=5, column=0, sticky='e')
        self.ent_cep = ttk.Entry(self.lfr_cadastro,
                                 textvariable=self.cep_var,
                                 justify='center')
        self.ent_cep.grid(row=5, column=1, pady=4, padx=3, sticky='w')
        # complemento
        self.com_var = tk.StringVar()
        self.lbl_com = ttk.Label(self.lfr_cadastro, text='Complemento:')
        self.lbl_com.grid(row=5, column=2, sticky='e')
        self.ent_com = ttk.Entry(self.lfr_cadastro,
                                 textvariable=self.com_var,
                                 justify='center')
        self.ent_com.grid(row=5, column=3, pady=4, padx=3)
        # butao
        self.btt_salvar = ttk.Button(self.lfr_cadastro, text='Salvar')
        self.btt_salvar.grid(row=6, column=0, columnspan=6, sticky='ew', pady=15, padx=5)
        self.salvar_grid = self.btt_salvar.grid_info()
        self.btt_salvar.bind('<ButtonRelease-1>', lambda ev: self.salvar())
        # butao não alocado geometricamente
        # atualizar
        self.btt_atualizar = ttk.Button(self.lfr_cadastro,
                                        text='Atualizar')
        self.btt_atualizar.grid(row=6, column=0, columnspan=2, sticky='ew')
        self.btt_atualizar.bind('<ButtonRelease-1>', att_bind)
        self.att_grid = self.btt_atualizar.grid_info()
        self.btt_atualizar.grid_forget()
        # cancelar
        self.btt_cancelar = ttk.Button(self.lfr_cadastro,
                                       text='Cancelar')
        self.btt_cancelar.grid(row=6, column=2, columnspan=4, sticky='ew')
        self.btt_cancelar.bind('<ButtonRelease-1>', lambda ev: edit_desconfig())
        self.cancelar_grid = self.btt_cancelar.grid_info()
        self.btt_cancelar.grid_forget()

    def lbl_frame_registros(self):
        def pesquisa(*args):
            if len(self.pesq_var.get()) > 0:
                for x in self.tree.get_children():
                    self.tree.delete(x)
                for cliente in Cliente.ativos.values():
                    if self.pesq_var.get().lower() in cliente.nome.lower():
                        valores = (str(cliente.id).zfill(3), cliente.nome, cliente.cpf, cliente.endereco)
                        self.tree.insert('', 'end', values=valores)
            else:
                self.att_tree()

        def editar_config():
            self.limpar_entradas()
            # config label_frame cadastro
            self.lfr_cadastro['text'] = 'Atualizar'
            self.ent_cpf['state'] = 'disabled'
            # desaparecer butão
            self.btt_salvar.grid_forget()
            # config label_frame registro
            self.tree['selectmode'] = 'none'
            self.btt_editar['state'] = 'disabled'
            self.btt_apagar['state'] = 'disabled'
            # att_entradas
            att_entradas()
            # mostrar butoes
            self.btt_atualizar.grid(row=self.att_grid['row'],
                                    column=self.att_grid["column"],
                                    columnspan=self.att_grid['columnspan'],
                                    sticky=self.att_grid['sticky'])
            self.btt_cancelar.grid(row=self.cancelar_grid['row'],
                                   column=self.cancelar_grid["column"],
                                   columnspan=self.cancelar_grid['columnspan'],
                                   sticky=self.cancelar_grid['sticky'])

        def apagar_config():
            # configuração lfr_registro
            self.btt_apagar['state'] = 'disabled'
            self.btt_editar['state'] = 'disabled'

        def att_entradas():
            cliente = Cliente.pesquisa_cliente_num(self.tree.item(self.tree.focus())['values'][0])
            dados = {'nome': cliente.nome,
                     'cpf': cliente.cpf,
                     'genero': cliente.genero,
                     'telefone': cliente.telefone,
                     'logradouro': cliente.endereco.logradouro,
                     'numero': cliente.endereco.numero,
                     'cidade': cliente.endereco.cidade,
                     'bairro': cliente.endereco.bairro,
                     'uf': cliente.endereco.uf,
                     'cep': cliente.endereco.cep,
                     'complemento': cliente.endereco.complemento}
            cliente_var = {'nome': self.nome_var,
                           'cpf': self.cpf_var,
                           'genero': self.gen_var,
                           'telefone': self.tel_var,
                           'logradouro': self.log_var,
                           'numero': self.num_var,
                           'cidade': self.cida_var,
                           'bairro': self.bairro_var,
                           'uf': self.uf_var,
                           'cep': self.cep_var,
                           'complemento': self.com_var}

            for item, dado in dados.items():
                cliente_var[item].set(dado)

        def editar_bind(ev):
            if str(self.btt_editar['state']) == 'normal':
                editar_config()

        def apagar_bind(ev):
            if str(self.btt_apagar['state']) == 'normal':
                apagar_config()
                self.apagar()
                self.tree.focus('')
                self.tree.selection_remove(self.tree.selection())

        # -------------------------------------------------------------
        self.lfr_registros = ttk.Labelframe(self.top, text='Registros')
        self.lfr_registros.pack()
        # widgets
        # treeview
        self.scr_tree = ttk.Scrollbar(self.lfr_registros)
        self.scr_tree.grid(row=1, column=4, sticky='ns')
        colunas = {'id': 'Id',
                   'nome': 'Nome',
                   'cpf': 'CPF',
                   'endereco': 'Endereco'}
        col_width = [60, 300, 120, 300]
        i = 0
        self.tree = ttk.Treeview(self.lfr_registros,
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
            self.tree.column(var, width=col_width[i])
            i += 1
        self.scr_tree.config(command=self.tree.yview)
        # pesquisa
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
        # butao
        # apagar
        self.btt_apagar = ttk.Button(self.lfr_registros,
                                     text='Apagar',
                                     state='disabled')
        self.btt_apagar.grid(row=2, column=3, sticky='e')
        self.btt_apagar.bind('<ButtonRelease-1>', apagar_bind)
        # atualizar
        self.btt_editar = ttk.Button(self.lfr_registros,
                                     text='Editar',
                                     state='disabled')
        self.btt_editar.grid(row=2, column=2, sticky='e', columnspan=2, padx=80)
        self.btt_editar.bind('<ButtonRelease-1>', editar_bind)

    def cad_conta_bind(self, ev):
        self.ref.janelas_control.pop().destroy()
        self.ref.tela.withdraw()
        self.ref.reg_conta()

    def cad_banco_bind(self, ev):
        self.ref.janelas_control.pop().destroy()
        self.ref.tela.withdraw()
        self.ref.reg_banco()

    def __init__(self, top, ref):
        self.top = top
        self.top.title('Registro Cliente')
        self.ref = ref
        self.top.iconbitmap('imagem/icone_capi.ico')
        # chamada de labelframes
        self.lbl_frame_cadastro()
        self.lbl_frame_registros()
        self.att_tree()
        # butao_top
        # voltar
        self.btt_voltar = ttk.Button(self.top,
                                     text='voltar',
                                     command=ref.voltar)
        self.btt_voltar.pack(side='bottom', anchor='se')
        # cadastrar conta
        self.btt_cad_conta = ttk.Button(self.top,
                                        text='Cadastrar Conta')
        self.btt_cad_conta.pack(side='left', before=self.btt_voltar)
        self.btt_cad_conta.bind('<ButtonRelease-1>', self.cad_conta_bind)
        # cadastrar banco
        self.btt_cad_banco = ttk.Button(self.top,
                                        text='Cadastrar Banco')
        self.btt_cad_banco.pack(side='left', after=self.btt_cad_conta)
        self.btt_cad_banco.bind('<ButtonRelease-1>', self.cad_banco_bind)