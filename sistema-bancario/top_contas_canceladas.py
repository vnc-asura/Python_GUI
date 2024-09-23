import tkinter as tk
from tkinter import ttk, filedialog as fd, messagebox as msg
from conta import Conta, ContaCorrente
from geometry import GeoPlace
from data import DataMixin


class ContaSelect:
    def pesquisa(self, *args):
        if len(self.pesq_var.get()) > 0:
            for x in self.tree.get_children():
                self.tree.delete(x)
            for conta in Conta.desativadas:
                if self.pesq_var.get().lower() in conta.cliente.nome.lower():
                    valores = (conta.numero,
                               conta.cliente.nome,
                               'Corrente' if isinstance(conta, ContaCorrente) else 'Poupança')
                    self.tree.insert('', 'end', values=valores)
        else:
            self.att_tree()

    def add_bind(self, ev):
        if str(self.btt_top_add['state']) == 'normal':
            self.adicionar()

    def adicionar(self):
        def retornar_conta(num):
            for conta in Conta.desativadas:
                if conta.numero == num:
                    return conta
        # ---------------------------------------------------------------------------
        selecionado = [str(x) for x in self.tree.item(self.tree.focus())["values"]]
        self.ref.conta_selecionada = retornar_conta(int(selecionado[0]))
        self.ref.conta_var.set(value=f'{str(self.ref.conta_selecionada.numero).zfill(3)} - '
                                     f'{self.ref.conta_selecionada.cliente.nome}')
        self.ref.att_dados()
        self.top.destroy()

    def item_selecionado(self, ev):
        if self.tree.focus():
            self.btt_top_add['state'] = 'normal'

    def att_tree(self):
        for x in self.tree.get_children():
            self.tree.delete(x)
        for conta in Conta.desativadas:
            v = (str(conta.numero).zfill(3),
                 conta.cliente.nome,
                 'Corrente' if isinstance(conta, ContaCorrente) else 'Poupança')
            self.tree.insert('', 'end', values=v)

    def limpar_tree_selecao(self, ev):
        if str(self.btt_top_add['state']) == 'normal':
            self.tree.focus('')
            self.tree.selection_remove(self.tree.selection())
            self.btt_top_add['state'] = 'disabled'

    def __init__(self, top, ref):
        self.top = top
        self.top.title('Seleção de conta')
        self.top.iconbitmap('imagem/icone_capi.ico')
        self.ref = ref
        # comportamento
        self.top.grab_set()
        # frame
        self.top_frame = ttk.Frame(self.top)
        self.top_frame.pack()
        # tree
        self.scr_tree = ttk.Scrollbar(self.top_frame)
        self.scr_tree.grid(row=1, column=4, sticky='ns')
        colunas = {'numero': 'Número',
                   'titular': 'Titular',
                   'tipo': 'Tipo conta'}
        col_width = [60, 300, 100]
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
        self.btt_top_voltar.bind('<ButtonRelease-1>', lambda ev: self.top.destroy())


class TopContaCanceladas(DataMixin):
    def top_conta(self):
        self.top_cont = tk.Toplevel()
        self.top_cont.withdraw()
        att_top_cont = ContaSelect(self.top_cont, self)
        self.top_cont.geometry(GeoPlace.centralizar_tela(self.top_cont))

    def extrato(self):
        c = self.conta_selecionada
        endereco = fd.askdirectory()
        a = max([len(i) for i in c.extrato.registros])
        with open(f'{endereco}/'
                  f'{str(self.day_now()).zfill(2)}'
                  f'{str(self.month_now()).zfill(2)}_'
                  f'{str(self.seg_now()).zfill(2)}-'
                  f'{str(c.numero).zfill(3)}.txt', 'w', encoding='utf-8') as fl:

            fl.write(f'{"*" * a}\n')
            for linha in c.extrato.registros:
                fl.write(linha + '\n')
            fl.write(f'{"*" * a}\n')
            fl.write(f'Saldo total : R$ {c.saldo:,.2f}\n')
            fl.write(f'Movimentação: R$ {sum([abs(x) for x in c.extrato.movimentacao]):,.2f}\n')
            extrato_criado = msg.showinfo('Extrato', 'Extrato criado com sucesso')

    def att_dados(self):
        if self.flag_dados:
            self.label_frames_dados()
            self.flag_dados = 0
        a = self.conta_selecionada
        self.lbl_numero['text'] = f'Número: {str(a.numero).zfill(3)}'
        self.lbl_tipo['text'] = f'Tipo da conta: {"Corrente" if isinstance(a, ContaCorrente) else "Poupança"}'
        self.lbl_titular['text'] = f'Titular: {a.cliente.nome}'
        self.lbl_saldo['text'] = f'Saldo: R$ {a.saldo:.2f}'
        self.lbl_cpf['text'] = f'CPF: {a.cliente.cpf}'
        self.lbl_tel['text'] = f'Telefone: {a.cliente.telefone}'

    def label_frame_contas(self):
        self.lfr_contas = ttk.Labelframe(self.top,
                                         text='Contas')
        self.lfr_contas.grid(row=0, column=0)
        # widgets
        # conta
        self.conta_var = tk.StringVar()
        self.lbl_conta = ttk.Label(self.lfr_contas,
                                   text='Conta cancelada:')
        self.lbl_conta.grid(row=0, column=0)
        self.ent_conta = ttk.Entry(self.lfr_contas,
                                   textvariable=self.conta_var,
                                   state='disabled',
                                   width=40,
                                   justify='center')
        self.ent_conta.grid(row=0, column=1)
        # butao
        self.btt_select = ttk.Button(self.lfr_contas,
                                     text='Selecionar')
        self.btt_select.grid(row=0, column=2)
        self.btt_select.bind('<ButtonRelease-1>', lambda ev: self.top_conta())

    def label_frames_dados(self):
        self.lfr_dados = ttk.Labelframe(self.top,
                                        text='Dados')
        self.lfr_dados.grid(row=1, column=0, sticky='ew')
        # widgets
        # numero
        self.lbl_numero = ttk.Label(self.lfr_dados)
        self.lbl_numero.grid(row=0, column=0, sticky='w')
        # tipo conta
        self.lbl_tipo = ttk.Label(self.lfr_dados)
        self.lbl_tipo.grid(row=0, column=1, sticky='w')
        # Titular
        self.lbl_titular = ttk.Label(self.lfr_dados,
                                     width=40)
        self.lbl_titular.grid(row=1, column=0, sticky='w')
        # cpf
        self.lbl_cpf = ttk.Label(self.lfr_dados)
        self.lbl_cpf.grid(row=1, column=1, sticky='w')
        # telefone
        self.lbl_tel = ttk.Label(self.lfr_dados)
        self.lbl_tel.grid(row=2, column=0, sticky='w')
        # saldo
        self.lbl_saldo = ttk.Label(self.lfr_dados)
        self.lbl_saldo.grid(row=2, column=1, sticky='w')
        # butao
        self.btt_extrato = ttk.Button(self.lfr_dados,
                                      text='Extrato')
        self.btt_extrato.grid(row=3, column=2, sticky='e')
        self.btt_extrato.bind('<ButtonRelease-1>', lambda ev: self.extrato())

    def __init__(self, top, ref):
        self.top = top
        self.top.title('Contas canceladas')
        self.top.iconbitmap('imagem/icone_capi.ico')
        self.ref = ref
        # variaveis
        self.conta_selecionada = ''
        self.flag_dados = 1
        # chamada labels frames
        self.label_frame_contas()
        # butao top
        self.btt_voltar = ttk.Button(self.top,
                                     text='Voltar')
        self.btt_voltar.grid(row=2, column=0, sticky='se')
        self.btt_voltar.bind('<ButtonRelease-1>', lambda ev: self.ref.voltar())
