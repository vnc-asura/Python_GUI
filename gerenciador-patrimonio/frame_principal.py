import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.icons import Icon
from comportamento import JanelaControl as JControl
from patrimonio import TopPatrimonio as TPatrimonio, TopPatrimonioMult as TPMult, TopPatrimonioAcesso as TPAcesso


class FramePesquisar:
    def __init__(self, frame, ref):
        self.frame = frame
        self.ref = ref
        # label pesquisa
        self.lbl_pesq = ttk.Label(self.frame, text='Pesquisar:', font='helvetica, 16 bold', style=(INFO, INVERSE))
        self.lbl_pesq.pack(side='left', padx=5, pady=5)
        # entry pesquisa
        self.pesq_var = ttk.StringVar()
        # pesquisa_bind metodo padrao
        self.pesq_var.trace_add('write', lambda *args: self.ref.pesquisa_bind(self.pesq_var.get()))
        self.ent_pesq = ttk.Entry(self.frame, textvariable=self.pesq_var, font='helvetica, 16')
        self.ent_pesq.pack(side='left', padx=5, pady=5)
        # button limpar
        self.btt_clean = ttk.Button(self.frame, text='X', style=DANGER)
        self.btt_clean.pack(side='left', padx=5, pady=5)
        self.btt_clean.bind('<ButtonRelease>', lambda e: self.pesq_var.set(value=''))


class FramePatrimonios:
    def limpar_selecao(self):
        self.tree.selection_remove(self.tree.focus())
        self.tree.focus('')

    def limpar_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def att_tree(self, dados):
        # limpar treeview
        self.limpar_tree()
        # adicionar tuplas
        status_referencia = {1: 'Normal', 
                              0: 'Quebrado', 
                              2: 'Em conserto',
                              3: 'Erro Cadastro', 
                              4: 'Perdido'}
        if dados:
            for tupla in dados:
                id = tupla[0]
                n_serie = tupla[1] if tupla[1] else '-'
                descricao = f'{tupla[2]}  {tupla[3] if tupla[3] else ""}  {tupla[4] if tupla[4] else ""}'
                status = status_referencia[tupla[5]]
                valor = f'R$ {tupla[6]:,.2f}' if tupla[6] else '-'

                self.tree.insert('', 'end', values=(id, n_serie, descricao, status, valor))

    def __init__(self, frame, ref):
        self.frame = frame
        self.ref = ref
        # widgets
        # treeview and scroll
        self.scr_tree = ttk.Scrollbar(self.frame, style=ROUND)
        self.scr_tree.pack(side='right', fill='y')
        colunas = {'ID': 'id', 
                   'Nº de série': 'num_serie',
                   'Descrição': 'descricao', 
                   'Status': 'status', 
                   'Valor': 'valor'}
        colunas_tam = {'id': 80, 
                       'num_serie': 200, 
                       'descricao': 560, 
                       'status': 140, 
                       'valor': 150}
        self.tree = ttk.Treeview(self.frame, 
                                 columns=list(colunas.values()), 
                                 show='headings', 
                                 yscrollcommand=self.scr_tree.set, 
                                 selectmode='browse')
        self.tree.pack(side='right', fill='both', expand=True)
        self.tree.bind('<Double-1>', lambda e: self.ref.catch_fpatrimonio())
        self.tree.bind('<Escape>', lambda e: self.limpar_selecao())
        self.scr_tree.config(command=self.tree.yview)

        for nome, var in colunas.items():
            self.tree.heading(var, text=nome)
            self.tree.column(var, anchor='center', width=colunas_tam[var])


class FrameNotebookPatrimonio:
    def frame_pesquisar(self):
        # frame pesquisa
        self.fr_pesquisa = ttk.Frame(self.frame, style=INFO)
        self.fr_pesquisa.pack(fill='x', padx=5, pady=5)
        self.att_fr_pesquisa = FramePesquisar(self.fr_pesquisa, self)

    # captura o interação com a Classe FramePatrimonio (método padrão de acesso)
    def catch_fpatrimonio(self):
        # captura componente da classe
        self.tree = self.att_fr_patri.tree
        # chama metodo
        if self.tree.focus():
            self.toplevel_acesso()

    def frame_patrimonios(self):
        self.fr_patri = ttk.Frame(self.frame)
        self.fr_patri.pack(fill='x', expand=True, padx=5, pady=5)
        self.att_fr_patri = FramePatrimonios(self.fr_patri, self)
        
    def frame_button(self):
        self.fr_button = ttk.Frame(self.frame, style=INFO)
        self.fr_button.pack(fill='x', padx=5, pady=5)
        self.fr_button.columnconfigure(0, weight=1)
        # menubutton
        self.mbt_add = ttk.Menubutton(self.fr_button, text='Adicionar +', direction='above', style=(SUCCESS, OUTLINE))
        self.mbt_add.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        # menu 
        self.mnu_add = ttk.Menu(self.mbt_add, tearoff=0, font='helvetica, 16')
        # associar menu no menubutton
        self.mbt_add.config(menu=self.mnu_add)
        # adicionar commands no menu
        self.mnu_add.add_command(label='Adição única', command=self.top_add_patrimonio)
        self.mnu_add.add_command(label='Adição múltipla', command=self.top_add_mult_patrimonio)
        # info
        self.img = ttk.PhotoImage(data=Icon.info)
        self.btt_info = ttk.Button(self.fr_button, image=self.img)
        self.btt_info.grid(row=0, column=0, sticky='w', padx=5, pady=5) 
        self.btt_tip = ToolTip(self.btt_info, 'Para acessar e atualizar um patrimonio, basta clicar duas vezes sobre o mesmo')

    def toplevel_acesso(self):
        campo = self.tree.item(self.tree.focus(), 'values')
        self.top_acesso = TPAcesso(JControl.pai, self, campo)
        JControl.controle.add_top_sob(self.top_acesso.top)

    def pesquisa_bind(self, entrada):
        if len(entrada) > 0:
            sql = f''' select id, n_serie, nome_item, marca, modelo, status, valor  
            from patrimonios
            where id like "%{entrada}%"
            or n_serie like "%{entrada}%"
            or nome_item like "%{entrada}%"
            or marca like "%{entrada}%" 
            or modelo like "%{entrada}%" ;'''
            dados = JControl.ref.crud.get(sql)
            self.att_fr_patri.att_tree(dados)
        else:
            self.ref.att_patrimonios()

    def top_add_patrimonio(self):
        self.top_patrimonio = TPatrimonio(JControl.pai, self)
        JControl.controle.add_top_sob(self.top_patrimonio.top)

    def top_add_mult_patrimonio(self):
        self.top_mult = TPMult(JControl.pai, self)
        JControl.controle.add_top_sob(self.top_mult.top)


    def __init__(self, note, ref):
        self.note = note
        self.ref = ref
        # frame
        self.frame = ttk.Frame(self.note)
        # chamar componentes
        self.frame_pesquisar()
        self.frame_patrimonios()
        self.frame_button()
        # adicionar frame no notebook
        self.note.add(self.frame, text='Patrimonios')


class FrameNotebookRegistro:
    def frame_pesquisar(self):
        self.fr_pesquisa = ttk.Frame(self.frame, style=INFO)
        self.fr_pesquisa.pack(fill='x')
        FramePesquisar(self.fr_pesquisa, self)

    def pesquisa_bind(self, entrada):
        if len(entrada) > 0:
            sql = f''' select * from registros 
            where id like "%{entrada}%" 
            or id_patrimonio like "%{entrada}%";'''
            dados = JControl.ref.crud.get(sql)
            self.att_tree(dados)
        else:
            self.ref.att_registros()

    def frame_registros(self):
        self.fr_reg = ttk.Frame(self.frame)
        self.fr_reg.pack(fill='both', expand=True, padx=5, pady=5)
        # treeview and scroll
        self.scr_tree = ttk.Scrollbar(self.fr_reg, style=ROUND)
        self.scr_tree.pack(side='right', fill='y', expand=True)
        colunas = {'ID': 'id',
                   'Data': 'data', 
                   'Patrimônio': 'patrimonio',
                   'Registro': 'registro'}
        colunas_tam = {'id': 80,
                      'data': 120, 
                      'patrimonio': 150,
                      'registro': 760}
        self.tree = ttk.Treeview(self.fr_reg, 
                                 columns=list(colunas.values()), 
                                 show='headings', 
                                 yscrollcommand=self.scr_tree.set)
        self.tree.pack(side='left', fill='both', expand=True)

        for nome, var in colunas.items():
            self.tree.heading(var, text=nome)
            self.tree.column(var, anchor='center', width=colunas_tam[var])

    def limpar_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def att_tree(self, dados):
        # limpar treeview
        self.limpar_tree()
        # adicionar tuplas
        f_data = lambda data: '/'.join(data.split('-')[::-1])
        for tupla in dados:
            id = tupla[0]
            registro = tupla[1]
            data = f_data(tupla[2])
            id_patrimonio = tupla[3]
            self.tree.insert('', 'end', values=(id, data, id_patrimonio, registro))

    def __init__(self, note, ref):
        self.note = note
        self.ref = ref
        # frame 
        self.frame = ttk.Frame(self.note)
        # chamar componentes
        self.frame_pesquisar()
        self.frame_registros()
        # adicionar frame no notebook
        self.note.add(self.frame, text='Registros')


class FramePrincipal:
    def label_frame_status(self):
        # label frame 
        self.lfr_status = ttk.LabelFrame(self.frame, text='Proporção Status')
        self.lfr_status.grid(row=0, column=2, sticky='ew')
        for i in range(3):
            self.lfr_status.columnconfigure(i, weight=1)
        # meter status
        # normal
        self.mtr_normais = ttk.Meter(self.lfr_status, 
                                     amounttotal=100, 
                                     subtext='Normal', 
                                     meterthickness=20, 
                                     subtextfont='helvetica, 20 bold' , 
                                     textright='%', 
                                     bootstyle=SUCCESS)
        self.mtr_normais.grid(row=0, column=0, padx=5, pady=5)
        # perdido
        self.mtr_perdido = ttk.Meter(self.lfr_status, 
                                     amounttotal=100, 
                                     subtext='Perdido', 
                                     meterthickness=20, 
                                     subtextfont='helvetica, 20 bold', 
                                     textright='%', 
                                     bootstyle=WARNING)
        self.mtr_perdido.grid(row=0, column=1, padx=5, pady=5)
        # quebrado
        self.mtr_quebrado = ttk.Meter(self.lfr_status, 
                                     amounttotal=100, 
                                     subtext='Quebrado', 
                                     meterthickness=20, 
                                     subtextfont='helvetica, 20 bold', 
                                     textright='%', 
                                     bootstyle=DANGER)
        self.mtr_quebrado.grid(row=0, column=2, padx=5, pady=5)

    def label_frame_qtd_total(self):
        #label frame
        self.lfr_qtotal = ttk.LabelFrame(self.frame, text='Quantidade total')
        self.lfr_qtotal.grid(row=0, column=0, sticky='nsew')
        self.lfr_qtotal.rowconfigure(0, weight=1)
        self.lfr_qtotal.columnconfigure(0, weight=1)
        # label
        self.qnt_var = ttk.IntVar()
        self.lbl_num_patri = ttk.Label(self.lfr_qtotal, textvariable=self.qnt_var, font='helvetica, 25 bold', anchor='center')
        self.lbl_num_patri.grid(row=0, column=0, sticky='nsew')

    def label_frame_valor_total(self):
        #label frame
        self.lfr_vtotal = ttk.LabelFrame(self.frame, text='Valor Total')
        self.lfr_vtotal.grid(row=0, column=1, sticky='nsew')
        self.lfr_vtotal.rowconfigure(0, weight=1)
        self.lfr_vtotal.columnconfigure(0, weight=1)
        # label
        self.valor_var = ttk.StringVar()
        self.lbl_num_patri = ttk.Label(self.lfr_vtotal, textvariable=self.valor_var, font='helvetica, 25 bold', anchor='center')
        self.lbl_num_patri.grid(row=0, column=0, sticky='nsew')

    def notebook(self):
        self.ntb = ttk.Notebook(self.frame)
        self.ntb.grid(row=1, column=0, columnspan=3, sticky='ew')
        # associar frames
        self.frame_patrimonio = FrameNotebookPatrimonio(self.ntb, self)
        self.frame_registros = FrameNotebookRegistro(self.ntb, self)

    def att_quantidade(self):
        sql = '''  select count(*) from patrimonios where status != 3;'''
        qnt = JControl.ref.crud.get(sql)
        self.qnt_var.set(value=qnt[0][0])

    def att_valor(self):
        sql = ''' select sum(valor) from patrimonios where status != 3;'''        
        valor = JControl.ref.crud.get(sql)
        valor = valor if valor[0][0] else [(0,)]
        self.valor_var.set(value=f'R$ {valor[0][0]:,.2f}')

    def att_status(self):
        total = self.qnt_var.get()
        percent = lambda qnt: round((qnt * 100)/total, 2)
        if total:
            # normal
            sql1 = ''' select count(*) 
            from patrimonios 
            where status = 1; '''
            q1 = JControl.ref.crud.get(sql1)
            self.mtr_normais.amountusedvar.set(percent(q1[0][0]))
            # perdido
            sql2 = ''' select count(*) 
            from patrimonios 
            where status = 4; '''
            q2 = JControl.ref.crud.get(sql2)
            self.mtr_perdido.amountusedvar.set(percent(q2[0][0]))
            # quebrado
            sql3 = ''' select count(*) 
            from patrimonios 
            where status in (0, 2); '''
            q3 = JControl.ref.crud.get(sql3)
            self.mtr_quebrado.amountusedvar.set(percent(q3[0][0]))
        else:
            self.mtr_normais.amountusedvar.set(0.00)
            self.mtr_perdido.amountusedvar.set(0.00)
            self.mtr_quebrado.amountusedvar.set(0.00)

    def att_patrimonios(self):
        sql = ''' select id, n_serie, nome_item, marca, modelo, status, valor  
        from patrimonios;'''
        dados = JControl.ref.crud.get(sql)
        self.frame_patrimonio.att_fr_patri.att_tree(dados)

    def att_registros(self):
        sql = ''' select * from registros ;'''
        dados = JControl.ref.crud.get(sql)
        self.frame_registros.att_tree(dados)

    def att_dados(self):
        # att qtd
        self.att_quantidade()
        # att valor
        self.att_valor()
        # att status
        self.att_status()
        # patrimonios
        self.att_patrimonios()
        # registros
        self.att_registros()

    def __init__(self, frame, ref):
        self.frame = frame
        self.ref = ref
        # ativar menu
        self.ref.menu_tela()
        # labelframe quantidade patrimonios
        self.label_frame_qtd_total()
        # labelframe valor total patrimonios
        self.label_frame_valor_total()
        # labelframe status proporção
        self.label_frame_status()
        # notebook 
        self.notebook()
        # atualizar dados
        self.att_dados()
        # centralizar
        JControl.centralizar_janela(JControl.pai)

