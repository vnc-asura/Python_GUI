import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText as SText, ScrolledFrame as SFrame
from ttkbootstrap import Style
from comportamento import JanelaControl as JControl
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs import Messagebox as Msg
from registro import Registro as Reg
from configuracao import TopCategorias as TCategorias, TopLocais as TLocais



class ComponentesCadastro:
    def widget_custom(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget['font'] = 'helvetica, 14 bold'
                widget.grid_configure(sticky='w')
            elif isinstance(widget, ttk.Entry):
                widget['font'] = 'helvetica, 14'
                widget.grid_configure(sticky='ew')
            widget.grid_configure(padx=5, pady=5)

    def desabilitar_entry(self, checks):
        if len(checks):
            entrys = {'1': self.ent_nome, 
                      '2': self.ent_marca, 
                      '3': self.ent_modelo, 
                      '4': self.ent_nserie, 
                      '5': self.cbb_local, 
                      '6': self.cbb_cat, 
                      '7': self.ent_aquisicao, 
                      '8': self.ent_valor, 
                      '9': self.stxt_carac}
            for i in checks:
                if i == '9':
                    entrys[i].text['state'] = 'disabled'
                    entrys[i].config(bootstyle=DANGER)
                else:
                    entrys[i].config(state=DISABLED) 
                    entrys[i].config(bootstyle=DANGER)

    def ativos(self):
        widgets = {'nome': self.ent_nome, 
                   'marca': self.ent_marca, 
                   'aquisicao': self.ent_aquisicao, 
                   'modelo': self.ent_modelo, 
                   'local': self.cbb_local, 
                   'categoria': self.cbb_cat, 
                   'nserie': self.ent_nserie, 
                   'valor': self.ent_valor, 
                   'caracteristica': self.stxt_carac}
        ativos = []
        for nome, widget in widgets.items():
            if isinstance(widget, SText):
                if str(widget.text['state']) == 'normal':
                    ativos.append(nome)
            else:
                if str(widget['state']) in ['normal', 'readonly']:
                    ativos.append(nome)
        return ativos

    def desativados(self):
        widgets = {'nome': self.ent_nome, 
                   'marca': self.ent_marca, 
                   'aquisicao': self.ent_aquisicao, 
                   'modelo': self.ent_modelo, 
                   'local': self.cbb_local, 
                   'categoria': self.cbb_cat, 
                   'nserie': self.ent_nserie, 
                   'valor': self.ent_valor, 
                   'caracteristica': self.stxt_carac}
        desativados = []
        for nome, widget in widgets.items():
            if isinstance(widget, SText):
                if str(widget.text['state']) == 'disabled':
                    desativados.append(nome)
            else:
                if str(widget['state']) == 'disabled':
                    desativados.append(nome)
        return desativados

    def ativar_status(self):
        self.status_values = {1: 'Normal', 
                              0: 'Quebrado', 
                              2: 'Em conserto',
                              3: 'Erro Cadastro', 
                              4: 'Perdido'}
        self.stat_var = ttk.StringVar()
        self.lbl_status = ttk.Label(self.frame, text='Status', font='helvetica, 14 bold')
        self.lbl_status.grid(row=4, column=2, sticky='w')
        self.cbb_status = ttk.Combobox(self.frame, 
                                       textvariable=self.stat_var, 
                                       values=list(self.status_values.values()), 
                                       font='helvetica, 14', 
                                       state='readonly', 
                                       bootstyle=SUCCESS)
        self.cbb_status.grid(row=5, column=2, sticky='ew', padx=5, pady=5)
        self.cbb_status.bind('<MouseWheel>', lambda e: 'break')

    def config_acesso(self, campos):
        def desativar_widgets():
            widgets = [self.ent_aquisicao, 
                    self.ent_nome, 
                    self.ent_marca, 
                    self.ent_modelo, 
                    self.ent_nserie, 
                    self.ent_valor, 
                    self.cbb_cat]
            for widget in widgets:
                widget['state'] = 'disabled'
            self.stxt_carac.text['state'] = 'disabled'

        def destacar():
            self.cbb_local.config(bootstyle=SUCCESS)
        
        def formatar_categoria(value):
            sql = f'''  select printf("%s", id), nome from categorias where id = {value} ;'''
            c = JControl.ref.crud.get(sql)
            return '-'.join(c[0])
        
        def formatar_locais(value):
            sql = f'''  select printf("%s", id), nome from locais where id = {value} ;'''
            return '-'.join(JControl.ref.crud.get(sql)[0])

        def formatar_data(value):
            return '/'.join(value.split('-')[::-1])

        def inserir_dados(dados):
            status = {1: 'Normal', 
                      0: 'Quebrado', 
                      2: 'Em conserto',
                      3: 'Erro Cadastro', 
                      4: 'Perdido'}
            self.nome_var.set(str(dados[0]))
            self.marca_var.set(dados[1] if dados[1] else '') 
            self.modelo_var.set(dados[2] if dados[2] else '')
            self.nserie_var.set(dados[3] if dados[3] else '') 
            self.cat_var.set(formatar_categoria(dados[4])) 
            self.local_var.set(formatar_locais(dados[5])) 
            self.aquisicao_var.set(formatar_data(dados[6]) if dados[6] else ''), 
            self.valor_var.set(str(dados[7]) if dados[7] else ''), 
            self.stxt_carac.text['state'] = 'normal'
            self.stxt_carac.insert('end', dados[8].replace('\\n', '\n') if dados[8] else '')
            self.stxt_carac.text['state'] = 'disabled'
            self.stat_var.set(status[dados[9]])

        def carregar_dados():
            sql =  f''' select nome_item, marca, modelo, n_serie, id_categ, id_local, d_aquisicao, valor, carac, status 
            from patrimonios where id = {campos[0]} ;'''
            dados = JControl.ref.crud.get(sql)
            if dados:
                inserir_dados(dados[0])
                return dados[0]

        # -----------------------------------------------------
        desativar_widgets()
        destacar()
        self.ativar_status()
        self.id = campos[0]
        self.dados = carregar_dados()

    def carregar_combobox(self):
        sql1 = ''' select printf('%s', id), nome  from locais l where l.status != 0;'''
        sql2 = ''' select printf('%s', id), nome  from categorias c where c.status != 0;'''
        self.lista_locais = list(map('-'.join, JControl.ref.crud.get(sql1))) + ['CADASTRAR LOCAL']
        self.lista_categorias = list(map('-'.join, JControl.ref.crud.get(sql2))) + ['CADASTRAR CATEGORIA']
        try:
            self.cbb_local['values'] = self.lista_locais
            self.cbb_cat['values'] = self.lista_categorias
        except:
            pass

    def aquisicao_trace(self):
        data = [x for x in self.aquisicao_var.get() if x.isdigit()]
        data = data[:8] if len(data) > 8 else data
        tam = [2, 4]
        for i in tam:
            if len(data) >= i:
                data[i-1] = data[i-1] + '/'
        self.aquisicao_var.set(value=''.join(data))
        self.ent_aquisicao.icursor(END)
    
    def valor_trace(self):
        self.valor_var.set(''.join([x for x in self.valor_var.get() if not x.isalpha()]))

    def verificar_entradas(self):
        def verificar_obrigatorios():
            if all([var['nome'], var['locais'], var['categoria']]):
                return 1
            else:
                return 0

        def verificar_incompleto():
            if len(var['aquisicao']) > 0:
                if len(var['aquisicao']) == 10:
                    return 1
                else:
                    return 0
            else:
                return 1

        # -----------------------------------------------------------
        var = {'nome':self.nome_var.get().strip(), 
               'marca': self.marca_var.get().strip(), 
               'modelo': self.modelo_var.get().strip(), 
               'nserie': self.nserie_var.get().strip(), 
               'categoria': self.cat_var.get().strip(), 
               'locais': self.local_var.get().strip(), 
               'aquisicao': self.aquisicao_var.get().strip(), 
               'valor': self.valor_var.get().strip(), 
               'caracteristica': self.stxt_carac.get('1.0', 'end').strip()}
        if verificar_obrigatorios() and verificar_incompleto():
            return var
        else:
            Msg.show_warning('Prencha os campos obrigatorio ou corrija a data', 'Aviso', parent=self.ref.top)
            return 0

    def acesso_atualiza(self):
            # ----------------------------------------
            s = {'Normal': 1, 
                      'Quebrado': 0, 
                      'Em conserto': 2,
                      'Erro Cadastro':3, 
                      'Perdido': 4}
            status = self.stat_var.get()
            local = self.local_var.get().split('-')[0]
            sql = f''' update patrimonios 
            set status = {s[status]}, 
            id_local = {local}
            where id = {self.id}'''
            if JControl.ref.crud.update(sql):
                Reg().reg_atualizacao(self.id, status=status, local=self.local_var.get())
                self.ref.ref.ref.att_dados()
                JControl.controle.voltar_sob()
            else: 
                Msg.show_warning('Erro na atualização, tente novamente', 'Aviso', parent=self.ref.top)

    def verificar_multi_entradas(self, campos):
        def verificar_obrigatorios():
            lista = [var[i] for i in ['nome', 'local', 'categoria'] if i in campos]
            if all(lista):
                return 1
            else:
                return 0
            
        def verificar_incompleto():
            if 'aquisicao' in campos:
                if len(var['aquisicao']) > 0:
                    if len(var['aquisicao']) == 10:
                        return 1
                    else:
                        return 0
                else:
                    return 1
            else:
                return 1
        
        # ---------------------------------------------------------------
        var = {'nome':self.nome_var.get().strip(), 
               'marca': self.marca_var.get().strip(), 
               'modelo': self.modelo_var.get().strip(), 
               'nserie': self.nserie_var.get().strip(), 
               'categoria': self.cat_var.get().strip(), 
               'local': self.local_var.get().strip(), 
               'aquisicao': self.aquisicao_var.get().strip(), 
               'valor': self.valor_var.get().strip(), 
               'caracteristica': self.stxt_carac.get('1.0', 'end').strip()}

        for nome in list(var.keys()):
            if nome not in campos:
                del var[nome]

        if verificar_incompleto() and verificar_obrigatorios():
            return var
        else:
            Msg.show_warning('Prencha os campos obrigatorio ou corrija a data', 'Aviso', parent=self.ref.top)
            return 0

    def cadastro_bind(self):
        if self.cat_var.get() == 'CADASTRAR CATEGORIA':
            self.cat_var.set('')
            self.top_cadastro_categoria()
        elif self.local_var.get() == 'CADASTRAR LOCAL':
            self.local_var.set('')
            self.top_cadastro_local()
    
    def atualiza_bind(self):
        self.carregar_combobox()

    def top_cadastro_categoria(self):
        self.top_categoria = TCategorias(self.ref.top, self)
        JControl.controle.add_top_sob(self.top_categoria.top)

    def top_cadastro_local(self):
        self.top_local = TLocais(self.ref.top, self)
        JControl.controle.add_top_sob(self.top_local.top)

    def __init__(self, frame, ref):
        self.frame = frame
        self.ref = ref
        # widget
        # nome item
        self.nome_var = ttk.StringVar()
        self.lbl_nome = ttk.Label(self.frame, text='Nome do Item *')
        self.lbl_nome.grid(row=0, column=0)
        self.ent_nome = ttk.Entry(self.frame, textvariable=self.nome_var)
        self.ent_nome.grid(row=1, column=0)
        # marca
        self.marca_var = ttk.StringVar()
        self.lbl_marca = ttk.Label(self.frame, text='Marca')
        self.lbl_marca.grid(row=0, column=1)
        self.ent_marca = ttk.Entry(self.frame, textvariable=self.marca_var)
        self.ent_marca.grid(row=1, column=1)
        # modelo
        self.modelo_var = ttk.StringVar()
        self.lbl_modelo = ttk.Label(self.frame, text='Modelo')
        self.lbl_modelo.grid(row=0, column=2)
        self.ent_modelo = ttk.Entry(self.frame, textvariable=self.modelo_var)
        self.ent_modelo.grid(row=1, column=2)
        # numero de serie/identificador
        self.nserie_var = ttk.StringVar()
        self.lbl_nserie = ttk.Label(self.frame, text='Numero de Série')
        self.lbl_nserie.grid(row=2, column=0)
        self.ent_nserie = ttk.Entry(self.frame, textvariable=self.nserie_var)
        self.ent_nserie.grid(row=3, column=0)
        # localização
        self.local_var = ttk.StringVar()
        self.lbl_local = ttk.Label(self.frame, text='Localização *')
        self.lbl_local.grid(row=2, column=1)
        self.cbb_local = ttk.Combobox(self.frame, textvariable=self.local_var, state='readonly')
        self.cbb_local.grid(row=3, column=1)
        self.cbb_local.bind('<MouseWheel>', lambda e: 'break')
        self.cbb_local.bind('<<ComboboxSelected>>', lambda e: self.cadastro_bind())
        self.cbb_local.bind('<FocusIn>', lambda e: self.atualiza_bind())
        # categoria
        self.cat_var = ttk.StringVar()
        self.lbl_cat = ttk.Label(self.frame, text='Categoria *')
        self.lbl_cat.grid(row=2, column=2)
        self.cbb_cat = ttk.Combobox(self.frame, textvariable=self.cat_var, state='readonly')
        self.cbb_cat.grid(row=3, column=2)
        self.cbb_cat.bind('<MouseWheel>', lambda e: 'break')
        self.cbb_cat.bind('<<ComboboxSelected>>', lambda e: self.cadastro_bind())
        self.cbb_cat.bind('<FocusIn>', lambda e: self.atualiza_bind())
        # data aquisição
        self.aquisicao_var = ttk.StringVar()
        self.aquisicao_var.trace_add('write', lambda *args: self.aquisicao_trace())
        self.lbl_aquisicao = ttk.Label(self.frame, text='Data aquisição')
        self.lbl_aquisicao.grid(row=4, column=0)
        self.ent_aquisicao = ttk.Entry(self.frame, textvariable=self.aquisicao_var)
        self.ent_aquisicao.grid(row=5, column=0)
        # valor
        self.valor_var = ttk.StringVar()
        self.valor_var.trace_add('write', lambda *args: self.valor_trace())
        self.lbl_valor = ttk.Label(self.frame, text='Valor')
        self.lbl_valor.grid(row=4, column=1)
        self.ent_valor = ttk.Entry(self.frame, textvariable=self.valor_var)
        self.ent_valor.grid(row=5, column=1)
        # caracteristica
        self.lbl_carac = ttk.Label(self.frame, text='Caracteristicas')
        self.lbl_carac.grid(row=8, column=0)
        self.stxt_carac = SText(self.frame, autohide=True, height=5, font=('helvetica', 14), wrap='word')
        self.stxt_carac.grid(row=9, column=0, columnspan=3, sticky='ew')
        # carregar var
        self.carregar_combobox()
        # tootips
        for i in [self.lbl_nome, self.lbl_local, self.lbl_cat]:
            ToolTip(i, 'Campo obrigatório, é essencial preenche-lo')

        # customizar widget
        self.widget_custom()


class ComponentesCamposEdit:
    def aquisicao_trace(self):
        data = [x for x in self.aquisicao_var.get() if x.isdigit()]
        data = data[:8] if len(data) > 8 else data
        tam = [2, 4]
        for i in tam:
            if len(data) >= i:
                data[i-1] = data[i-1] + '/'
        self.aquisicao_var.set(value=''.join(data))
        self.ent_aquisicao.icursor(END)

    def valor_trace(self):
        self.valor_var.set(''.join([x for x in self.valor_var.get() if not x.isalpha()]))

    def nome(self, pai):
        # frame
        self.fr_nome = ttk.Frame(pai)
        self.fr_nome.pack(side='left', padx=2, pady=2)
        # compoentes
        self.nome_var = ttk.StringVar()
        self.lbl_nome = ttk.Label(self.fr_nome, text='Nome do item', font='helveitica, 10 bold')
        self.lbl_nome.pack(anchor='w')
        self.ent_nome = ttk.Entry(self.fr_nome, textvariable=self.nome_var)
        self.ent_nome.pack(anchor='w')
        return self.nome_var

    def marca(self, pai):
        # frame
        self.fr_marca = ttk.Frame(pai)
        self.fr_marca.pack(side='left', padx=2, pady=2)
        # compoentes
        self.marca_var = ttk.StringVar()
        self.lbl_marca = ttk.Label(self.fr_marca, text='Marca', font='helveitica, 10 bold')
        self.lbl_marca.pack(anchor='w')
        self.ent_marca = ttk.Entry(self.fr_marca, textvariable=self.marca_var)
        self.ent_marca.pack(anchor='w')
        return self.marca_var

    def modelo(self, pai):
        # frame
        self.fr_modelo = ttk.Frame(pai)
        self.fr_modelo.pack(side='left', padx=2, pady=2)
        # componentes
        self.modelo_var = ttk.StringVar()
        self.lbl_modelo = ttk.Label(self.fr_modelo, text='Modelo', font='helveitica, 10 bold')
        self.lbl_modelo.pack(anchor='w')
        self.ent_modelo = ttk.Entry(self.fr_modelo, textvariable=self.modelo_var)
        self.ent_modelo.pack(anchor='w')
        return self.modelo_var

    def nserie(self, pai):
        # frame
        self.fr_nserie = ttk.Frame(pai)
        self.fr_nserie.pack(side='left', padx=2, pady=2)
        # componentes
        self.nserie_var = ttk.StringVar()
        self.lbl_nserie = ttk.Label(self.fr_nserie, text='N° de série', font='helveitica, 10 bold')
        self.lbl_nserie.pack(anchor='w')
        self.ent_nserie = ttk.Entry(self.fr_nserie, textvariable=self.nserie_var)
        self.ent_nserie.pack(anchor='w')
        return self.nserie_var

    def localizacao(self, pai):
        # frame
        self.fr_local = ttk.Frame(pai)
        self.fr_local.pack(side='left', padx=2, pady=2)
        # compoenentes
        self.local_var = ttk.StringVar()
        self.lbl_local = ttk.Label(self.fr_local, text='Local', font='helveitica, 10 bold')
        self.lbl_local.pack(anchor='w')
        self.cbb_local = ttk.Combobox(self.fr_local, textvariable=self.local_var, state='readonly', values=self.lista_locais)
        self.cbb_local.pack(anchor='w')
        return self.local_var

    def categorias(self, pai):
        # frame
        self.fr_categoria = ttk.Frame(pai)
        self.fr_categoria.pack(side='left', padx=2, pady=2)
        # compoenentes
        self.categoria_var = ttk.StringVar()
        self.lbl_categoria = ttk.Label(self.fr_categoria, text='Categoria', font='helveitica, 10 bold')
        self.lbl_categoria.pack(anchor='w')
        self.cbb_categoria = ttk.Combobox(self.fr_categoria, textvariable=self.categoria_var, state='readonly', values=self.lista_categorias)
        self.cbb_categoria.pack(anchor='w')
        return self.categoria_var

    def aquisicao(self, pai):
        # frame
        self.fr_aquisicao = ttk.Frame(pai)
        self.fr_aquisicao.pack(side='left', padx=2, pady=2)
        # componentes
        self.aquisicao_var = ttk.StringVar()
        self.aquisicao_var.trace_add('write', lambda *args: self.aquisicao_trace())
        self.lbl_aquisicao = ttk.Label(self.fr_aquisicao, text='Data Aquisição', font='helveitica, 10 bold')
        self.lbl_aquisicao.pack(anchor='w')
        self.ent_aquisicao = ttk.Entry(self.fr_aquisicao, textvariable=self.aquisicao_var)
        self.ent_aquisicao.pack(anchor='w')
        return self.aquisicao_var

    def valor(self, pai):
        # frame
        self.fr_valor = ttk.Frame(pai)
        self.fr_valor.pack(side='left', padx=2, pady=2)
        # componentes
        self.valor_var = ttk.StringVar()
        self.valor_var.trace_add('write', lambda *args: self.valor_trace())
        self.lbl_valor = ttk.Label(self.fr_valor, text='Valor', font='helveitica, 10 bold')
        self.lbl_valor.pack(anchor='w')
        self.ent_valor = ttk.Entry(self.fr_valor, textvariable=self.valor_var)
        self.ent_valor.pack(anchor='w')
        return self.valor_var

    def caracteristicas(self, pai):
        self.fr_carac = ttk.Frame(pai)
        self.fr_carac.pack(side='left', padx=2, pady=2)
        self.carac_var = ttk.StringVar()
        self.lbl_carac = ttk.Label(self.fr_carac, text='Caracteristicas', font='helveitica, 10 bold')
        self.lbl_carac.pack(anchor='w')
        self.stxt_carac = SText(self.fr_carac, autohide=True, height=4, wrap=WORD, width=20)
        self.stxt_carac.pack(anchor='w')
        return self.stxt_carac

    def gerenciar_campos(self):
        if self.campos:
            self.var = {}
            frames = {'nome': self.nome, 
                    'marca': self.marca, 
                    'aquisicao': self.aquisicao, 
                    'modelo': self.modelo, 
                    'local': self.localizacao, 
                    'categoria': self.categorias, 
                    'nserie': self.nserie, 
                    'valor': self.valor, 
                    'caracteristica': self.caracteristicas}
            if len(self.campos) <= 5:
                for campo in self.campos:
                    self.var[campo] = frames[campo](self.frame)
                    
            else:
                # frame 1
                self.fr_1 = ttk.Frame(self.frame)
                self.fr_1.pack(expand=True, fill='x')
                # frame 2
                self.fr_2 = ttk.Frame(self.frame)
                self.fr_2.pack(fill='x', expand=True)
                for i in range(len(self.campos)):
                    if i < 5:
                        self.var[self.campos[i]] = frames[self.campos[i]](self.fr_1)
                    else:
                        self.var[self.campos[i]] = frames[self.campos[i]](self.fr_2)
        else:
            self.lbl_sem_padrao = ttk.Label(self.frame, text='Não há campo(s) padrão(ões)', font='helvetica, 30 bold', bootstyle=(DANGER, INVERSE))
            self.lbl_sem_padrao.pack(fill='x', padx=10, pady=10)

    def campos_itens(self):
        if len(self.campos) <= 5:
            for fr in self.frame.winfo_children():
                fr.config(bootstyle=PRIMARY) 
                for widget in fr.winfo_children():
                    if isinstance(widget, ttk.Label):
                        widget.config(bootstyle=(PRIMARY, INVERSE))
        else:
            self.fr_1.config(bootstyle=PRIMARY)
            self.fr_2.config(bootstyle=PRIMARY)
            c = self.fr_1.winfo_children() + self.fr_2.winfo_children()
            for fr in c:
                fr.config(bootstyle=PRIMARY)
                for widget in fr.winfo_children():
                    if isinstance(widget, ttk.Label):
                        widget.config(bootstyle=(PRIMARY, INVERSE))

    def campos_padrao(self):
        if len(self.campos) <= 5:
            for fr in self.frame.winfo_children():
                for widget in fr.winfo_children():
                    if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Combobox):
                        widget['state'] =  'disabled'
                    elif isinstance(widget, SText):
                        widget.text['state'] = 'disabled'
        else:
            c = self.fr_1.winfo_children() + self.fr_2.winfo_children()
            for fr in c:
                for widget in fr.winfo_children():
                    if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Combobox):
                        widget['state'] =  'disabled'
                    elif isinstance(widget, SText):
                        widget.text['state'] = 'disabled'

    def campos_ativos(self, dados):
        # formatações
        f_strings = lambda v: '\"' + v + '\"'
        f_data = lambda v: '-'.join(v.split('/')[::-1])
        f_valor = lambda v: str(round(float(v), 2))
        f_cat_local = lambda v: str(int(v.split('-')[0]))
        # colunas
        colunas = {'nome': 'nome_item', 
                'marca': 'marca', 
                'modelo': 'modelo', 
                'nserie': 'n_serie', 
                'aquisicao': 'd_aquisicao', 
                'valor': 'valor', 
                'caracteristica': 'carac', 
                'local': 'id_local', 
                'categoria': 'id_categ'}
        campos_sql = {'coluna': [], 
                    'valor': []}
        
        for nome, valor in dados.items():
            if len(valor) > 0:
                if nome not in ['categoria', 'local', 'valor', 'aquisicao']:
                    campos_sql['coluna'].append(colunas[nome])
                    campos_sql['valor'].append(f_strings(valor))
                elif nome in ['categoria', 'local']:
                    campos_sql['coluna'].append(colunas[nome])
                    campos_sql['valor'].append(f_cat_local(valor))
                elif nome == 'valor':
                    campos_sql['coluna'].append(colunas[nome])
                    campos_sql['valor'].append(f_valor(valor))
                elif nome == 'aquisicao':
                    campos_sql['coluna'].append(colunas[nome])
                    campos_sql['valor'].append(f_strings(f_data(valor)))
        return campos_sql                        

    def inserir_campos(self, dados):
        for nome in list(self.var.keys()):
            if nome != 'caracteristica':
                self.var[nome].set(dados[nome])
            else:
                self.stxt_carac.text['state'] = 'normal'
                self.var[nome].insert('end', dados[nome])
                self.stxt_carac.text['state'] = 'disabled'


        
            
        # ------------------------------------------------
        
    def carregar_combobox(self):
        sql1 = ''' select printf('%s', id), nome  from locais l where l.status != 0;'''
        sql2 = ''' select printf('%s', id), nome  from categorias c where c.status != 0;'''
        self.lista_locais = list(map('-'.join, JControl.ref.crud.get(sql1)))
        self.lista_categorias = list(map('-'.join, JControl.ref.crud.get(sql2)))

    def verificar_entradas(self):
        def verificar_obrigatorios():
            lista = [var[i] for i in ['nome', 'local', 'categoria'] if i in list(var.keys())]
            if all(lista):
                return 1
            else:
                return 0
            
        def verificar_incompleto():
            if 'aquisicao' in list(var.keys()):
                if len(var['aquisicao']) > 0:
                    if len(var['aquisicao']) == 10:
                        return 1
                    else:
                        return 0
                else:
                    return 1
            else:
                return 1

    
        # ---------------------------------------------------------------
        var = {}
        for nome, valor in self.var.items():
            if nome != 'caracteristica':
                var[nome] = valor.get().strip()
            else:
                var[nome].get('1.0', 'end').strip()

        if verificar_incompleto() and verificar_obrigatorios():
            return var
        else:
            # Msg.show_warning(message=f'Prencha os campos obrigatorio ou corrija a data do item {item}', title='Aviso', parent=self.ref.ref.ref.top)
            return 0


    def __init__(self, frame, ref, campos):
        self.frame = frame
        self.ref = ref
        self.campos = campos
        # aplicar campos
        self.carregar_combobox()
        self.gerenciar_campos()


class ItemEdit:
    def frame_campos(self):
        # att componentes
        self.att_frame = ComponentesCamposEdit(frame=self.frame, ref=self, campos=self.ref.ref.desativados)
        self.att_frame.campos_itens()

    def frame_nitem(self):
        # frame
        self.fr_item = ttk.Frame(self.frame, bootstyle=WARNING)
        self.fr_item.pack(side='left')
        # label
        self.lbl_item = ttk.Label(self.fr_item, text=f'{self.numero}', bootstyle=(WARNING, INVERSE), anchor='center', font='helvetica, 18 bold')
        self.lbl_item.pack(fill='both', expand=True, padx=10, pady=10)

    def salvar(self, f_dados):
        sql_campos = self.att_frame.campos_ativos(self.var)
        sql = f'''  insert into patrimonios ({", ".join(sql_campos['coluna'] + f_dados['coluna'])})
         values ({", ".join(sql_campos['valor']+ f_dados['valor'])}) ;'''
        id = JControl.ref.crud.insert_id(sql)
        Reg().reg_criacao(id)
        

    def verificar(self):
        var = self.att_frame.verificar_entradas()
        if var:
            self.var = var
            return 1
        else:
            return 0
        

    def __init__(self, pai, ref, i):
        self.pai = pai
        self.ref = ref
        self.numero = i
        # frame
        self.frame = ttk.Frame(self.pai, bootstyle=PRIMARY)
        self.frame.pack(fill='x', expand=True, padx=5, pady=5)
        # chamar frames
        self.frame_nitem()
        self.frame_campos()


class TopFrameMultEdicao:
    def labelframe_campos_padrao(self):
        self.lfr_padrao = ttk.LabelFrame(self.frame, text='Campos padrão')
        self.lfr_padrao.pack(fill='x', expand=True)
        # widgets
        self.att_lfr_padrao = ComponentesCamposEdit(frame=self.lfr_padrao, ref=self,campos=self.ref.ativos)
        if self.padrao:
            self.att_lfr_padrao.campos_padrao()
            self.f_dados = self.att_lfr_padrao.campos_ativos(self.padrao)
            self.att_lfr_padrao.inserir_campos(self.padrao)
        
    def labelframe_mult_edicao(self):
        self.lfr_edit = ttk.LabelFrame(self.frame, text='Edição múltipla', labelanchor='ne')
        self.lfr_edit.pack(expand=True, fill='both')
        # titulo
        self.lbl_titulo = ttk.Label(self.lfr_edit, text='Edite os campos únicos dos itens cadastrados', font='Helvetica, 25 bold', anchor='center')
        self.lbl_titulo.pack(fill='x', expand=True)
        # separator 2 
        self.sep2 = ttk.Separator(self.lfr_edit)
        self.sep2.pack(fill='x', expand=True, padx=5, pady=5)
        # scrolled frame
        self.sfr_mult_edit = SFrame(self.lfr_edit, autohide=True, height=350)
        self.sfr_mult_edit.pack(fill='both', expand=True)

    def alocar_itens(self):
        self.itens = []
        for i in range(1, self.ref.quantidade + 1):
            self.item = ItemEdit(self.sfr_mult_edit, self, i)
            self.itens.append(self.item)

    def cancelar(self):
        self.itens.clear()
        self.frame.destroy()
        self.ref.frame.pack(fill='both', expand=True)
        JControl.centralizar_janela(self.ref.top)

    def salvar(self):
        if all([x.verificar() for x in self.itens]):
            for item in self.itens:
                item.salvar(self.f_dados)
            JControl.controle.voltar_sob()
            JControl.ref.att_frame.att_dados()
        else:
            Msg.show_warning(message='Preencha o(s) campo(s) obrigatório(s) ou corrija a data ', title='Aviso', parent=self.ref.top)

    def frame_button(self):
        # frame
        self.fr_button = ttk.Frame(self.frame, bootstyle=INFO)
        self.fr_button.pack(fill='x', expand=True)
        # button
        self.btt_salvar = ttk.Button(self.fr_button, text='Concluir', bootstyle=(SUCCESS, OUTLINE))
        self.btt_salvar.pack(side='right', padx=3, pady=3)
        self.btt_salvar.bind('<ButtonRelease-1>', lambda e: self.salvar())
        self.btt_cancelar = ttk.Button(self.fr_button, text='Cancelar', bootstyle=DANGER)
        self.btt_cancelar.pack(side='right', padx=3, pady=3)
        self.btt_cancelar.bind('<ButtonRelease-1>', lambda e: self.cancelar())

    def widget_custom(self):
        for widget in self.frame.winfo_children():
            widget.pack_configure(padx=5, pady=5)        

    def __init__(self, frame, ref, padrao):
        self.frame = frame
        self.ref = ref
        self.padrao = padrao
        # label frames
        self.labelframe_campos_padrao()
        self.labelframe_mult_edicao()
        self.frame_button()
        # customizar widgets
        self.widget_custom()
        self.alocar_itens()


class TopPatrimonioAcesso:
    def configurar_tela(self):
        self.top.withdraw()
        self.top.title('Acesso  patrimonio')
        self.top.overrideredirect(True)
        self.top.resizable(False, False)        

    def frame_titulo(self):
        self.fr_titulo = ttk.Frame(self.frame)
        self.fr_titulo.pack(fill='x', expand=True)
        self.lbl_titulo = ttk.Label(self.fr_titulo, text='Patrimonio', anchor='center', font='helvetica, 30 bold')
        self.lbl_titulo.pack(fill='x', expand=True)
        self.lbl_subtitulo = ttk.Label(self.fr_titulo, 
                                       text='Modifique ou atualize o patrimonio(apenas a localização e status podem ser alterados)', 
                                       font='helvetica, 14', 
                                       anchor='center')
        self.lbl_subtitulo.pack(fill='x', expand=True, padx=5, pady=5)

    def frame_campos(self):
        self.fr_campos = ttk.Frame(self.frame)
        self.fr_campos.pack(fill='x', expand=True)
        # atualizar frame
        self.att_fr_campos = ComponentesCadastro(self.fr_campos, self)
        self.att_fr_campos.config_acesso(self.campos)

    def frame_button(self):
        self.fr_button = ttk.Frame(self.frame, bootstyle=INFO)
        self.fr_button.pack(fill='x', expand=True)
        # button
        self.btt_concluir = ttk.Button(self.fr_button, text='Atualizar', bootstyle=(SUCCESS, OUTLINE))
        self.btt_concluir.pack(side='right')
        self.btt_concluir.bind('<ButtonRelease-1>', lambda e: self.att_fr_campos.acesso_atualiza())
        self.btt_cancelar = ttk.Button(self.fr_button, text='Cancelar', bootstyle=DANGER)
        self.btt_cancelar.pack(side='right')
        self.btt_cancelar.bind('<ButtonRelease>', lambda e: JControl.controle.voltar_sob())

    def __init__(self, pai, ref, campos):
        self.pai = pai
        self.ref = ref
        self.campos = campos
        # top level
        self.top = ttk.Toplevel(pai)
        # frame
        self.frame = ttk.Frame(self.top)
        self.frame.pack(fill='both', expand=True)
        self.configurar_tela()
        # chamar frames
        self.frame_titulo()
        self.frame_campos()
        self.frame_button()


class TopPatrimonioMult:
    def configurar_tela(self):
        self.top.withdraw()
        self.top.title('Cadastro de patrimonio')
        self.top.overrideredirect(True)
        self.top.resizable(False, False)

    def frame_titulo(self):
        self.fr_titulo = ttk.Frame(self.frame)
        self.fr_titulo.pack(fill='x', expand=True)
        # widget
        self.lbl_titulo = ttk.Label(self.fr_titulo, text='Adicione seu patrimônio', font='helvetica, 30 bold', anchor='center')
        self.lbl_titulo.pack(fill='x', expand=True)
        self.lbl_subtitulo = ttk.Label(self.fr_titulo, 
                                       text='Atenção ao cadastrar seu patrimonio, não é possivel edita-lo após cadastro, exceto a localização', 
                                       font='helvetica, 12', 
                                       anchor='center')
        self.lbl_subtitulo.pack(fill='x', expand=True)

    def frame_cadastro(self):
        self.fr_cadastro = ttk.Frame(self.frame)
        self.fr_cadastro.pack(fill='x', expand=True, after=self.fr_config)
        # aplicar componentes
        self.componentes = ComponentesCadastro(self.fr_cadastro, self)

    def frame_qtd(self):
        self.fr_qtd = ttk.Frame(self.fr_config, style=SECONDARY)
        self.fr_qtd.grid(row=3, column=0, rowspan=2)
        # widget
        self.lbl_qtd = ttk.Label(self.fr_qtd, text='Quantidade', font='helvetica, 12 bold', anchor='center', style=(DANGER, INVERSE))
        self.lbl_qtd.pack(fill='x', expand=True)
        self.qtd_var = ttk.IntVar(value=1)
        self.spn_qtd = ttk.Spinbox(self.fr_qtd, textvariable=self.qtd_var, increment=1, from_=1, to=100)
        self.spn_qtd.pack(fill='both', expand=True)

    def configurar_cadastro(self):
        def widget_custom():
            s = Style()
            s.configure('Configurar.TCheckbutton', font=('helvetica', 12, 'bold'))
            for widget in self.fr_config.winfo_children():
                if isinstance(widget, ttk.Checkbutton):
                    widget['style'] = 'Configurar.TCheckbutton'
                    widget.grid_configure(padx=5, pady=2, sticky='w')
                elif isinstance(widget, ttk.Frame):
                    widget.grid_configure(padx=5, pady=2)

        # --------------------------------------------------------------
        self.fr_config = ttk.Frame(self.frame)
        self.fr_config.pack(fill='x', expand=True)
        for i in range(7):
            self.fr_config.columnconfigure(i, weight=1)
        # widgets
        # separator 1
        self.sep1 = ttk.Separator(self.fr_config)
        self.sep1.grid(row=0, column=0, columnspan=7, sticky='ew')
        # label
        self.lbl_config = ttk.Label(self.fr_config, 
                                    text='Selecione a quantidade de itens e os campos únicos a serem registrados', 
                                    anchor='center', 
                                    font='helvetica, 13 bold', 
                                    style=(WARNING, INVERSE))
        self.lbl_config.grid(row=1, column=0, columnspan=7, sticky='ew')
        # separator 2
        self.sep2 = ttk.Separator(self.fr_config)
        self.sep2.grid(row=2, column=0, columnspan=7, sticky='ew')
        # chamar labelframe quantidade
        self.frame_qtd()
        # nome item
        self.config_nome_var = ttk.StringVar()
        self.chk_nome = ttk.Checkbutton(self.fr_config, text='Nome do item', onvalue=1, variable=self.config_nome_var)
        self.chk_nome.grid(row=3, column=1, sticky='ew')
        # marca 
        self.config_marca_var = ttk.StringVar()
        self.chk_marca = ttk.Checkbutton(self.fr_config, text='Marca', onvalue=2, variable=self.config_marca_var)
        self.chk_marca.grid(row=3, column=2)
        # modelo
        self.config_modelo_var = ttk.StringVar()
        self.chk_modelo = ttk.Checkbutton(self.fr_config, text='Modelo', onvalue=3, variable=self.config_modelo_var)
        self.chk_modelo.grid(row=3, column=3)
        # numero de serie
        self.config_nserie_var = ttk.StringVar()
        self.chk_nserie = ttk.Checkbutton(self.fr_config, text='Nº de série', onvalue=4, variable=self.config_nserie_var)
        self.chk_nserie.grid(row=3, column=4)
        # localização
        self.config_local_var = ttk.StringVar()
        self.chk_local = ttk.Checkbutton(self.fr_config, text='Localização', onvalue=5, variable=self.config_local_var)
        self.chk_local.grid(row=3, column=5)
        # categoria
        self.config_cat_var = ttk.StringVar()
        self.chk_cat = ttk.Checkbutton(self.fr_config, text='Categoria', onvalue=6, variable=self.config_cat_var)
        self.chk_cat.grid(row=4, column=1)
        # data aquisição
        self.config_aquisicao_var = ttk.StringVar()
        self.chk_aquisicao = ttk.Checkbutton(self.fr_config, text='Data aquisição', onvalue=7, variable=self.config_aquisicao_var)
        self.chk_aquisicao.grid(row=4, column=2)
        # valor
        self.config_valor_var = ttk.StringVar()
        self.chk_valor = ttk.Checkbutton(self.fr_config, text='Valor', onvalue=8, variable=self.config_valor_var)
        self.chk_valor.grid(row=4, column=3)
        # caracteristica
        self.config_carac_var = ttk.StringVar()
        self.chk_carac = ttk.Checkbutton(self.fr_config, text='Caracteristicas', onvalue=9, variable=self.config_carac_var)
        self.chk_carac.grid(row=4, column=4)
        # button
        self.btt_grid = {'row': 3, 'column': 6}
        # concluir
        self.btt_concluir = ttk.Button(self.fr_config, text='Concluir', style=(SUCCESS, OUTLINE))
        self.btt_concluir.grid(row=self.btt_grid['row'], column=self.btt_grid['column'], sticky='ew', rowspan=2, padx=5, pady=5)
        self.btt_concluir.bind('<ButtonRelease>', lambda e: self.configuracao_concluir())
        # alterar
        self.btt_alterar = ttk.Button(self.fr_config, text='Alterar', style=OUTLINE)
        self.btt_alterar.bind('<ButtonRelease>', lambda e: self.configuracao_alterar())
        # separator 3
        self.sep3 = ttk.Separator(self.fr_config)
        self.sep3.grid(row=5, column=0, columnspan=7, sticky='ew')
        # customizar widget
        widget_custom()

    def estado_config(self, flag):
        if flag:
            for wdg in self.fr_config.winfo_children():
                if isinstance(wdg, ttk.Checkbutton):
                    wdg['state'] = 'normal'
            self.spn_qtd['state'] = 'normal'
        else:
            for wdg in self.fr_config.winfo_children():
                if isinstance(wdg, ttk.Checkbutton):
                    wdg['state'] = 'disabled'
            self.spn_qtd['state'] = 'disabled'

    def verifica_checks(self):
        checks = [self.config_nome_var, 
                self.config_marca_var, 
                self.config_modelo_var, 
                self.config_nserie_var, 
                self.config_local_var, 
                self.config_cat_var, 
                self.config_aquisicao_var, 
                self.config_valor_var, 
                self.config_carac_var]
        
        checks_on = [chk.get() for chk in checks if chk.get().isdigit() and int(chk.get())]
        return checks_on

    def configuracao_concluir(self):
        def att_button():
            self.btt_concluir.grid_forget()
            self.btt_alterar.grid(row=self.btt_grid['row'], 
                                  column=self.btt_grid['column'], 
                                  sticky='ew', 
                                  rowspan=2, 
                                  padx=5, 
                                  pady=5)

        # -------------------------------------
        if self.qtd_var.get() > 0:
            # carregar frames
            self.frame_cadastro()
            self.frame_button()
            # vericar checkbutton
            self.componentes.desabilitar_entry(self.verifica_checks())
            # atualizar config button
            att_button()
            # alterar estado dos componentes (disabled)
            self.estado_config(0)
            # centralizar tela
            JControl.centralizar_janela(self.top)
        else:
            Msg.show_warning('Corrija a quantidade', 'Erro quantidade', parent=self.top)

    def configuracao_alterar(self):
        def att_button():
            self.btt_alterar.grid_forget()
            self.btt_concluir.grid(row=self.btt_grid['row'], 
                                  column=self.btt_grid['column'], 
                                  sticky='ew', 
                                  rowspan=2, 
                                  padx=5, 
                                  pady=5)

        # destroy frames
        self.fr_cadastro.destroy()
        self.fr_button.destroy()
        # altera estaddo dos componentes (normal)
        self.estado_config(1)
        # atualizar config button
        att_button()
        # centralizar tela
        JControl.centralizar_janela(self.top)

    def limpar_top(self):
        self.frame.pack_forget()

    def salvar_multiplos_iguais(self):
        def formatar_strings(value):
            return '\"' + value + '\"'
        
        def formatar_data(data):
            return '-'.join(data.split('/')[::-1])

        def formatar_valor(valor):
            return str(round(float(valor), 2))

        def formatar_cat_local(value):
            return str(int(value.split('-')[0]))

        def campos_ativos():
            colunas = {'nome': 'nome_item', 
                       'marca': 'marca', 
                       'modelo': 'modelo', 
                       'nserie': 'n_serie', 
                       'aquisicao': 'd_aquisicao', 
                       'valor': 'valor', 
                       'caracteristica': 'carac', 
                       'locais': 'id_local', 
                       'categoria': 'id_categ'}
            campos_sql = {'coluna': [], 
                          'valor': []}
            for nome, valor in dados.items():
                if len(valor) > 0:
                    if nome in ['nome', 'marca', 'modelo', 'nserie', 'caracteristica']:
                        campos_sql['coluna'].append(colunas[nome])
                        campos_sql['valor'].append(formatar_strings(valor))
                    elif nome in ['categoria', 'locais']:
                        campos_sql['coluna'].append(colunas[nome])
                        campos_sql['valor'].append(formatar_cat_local(valor))
                    elif nome == 'valor':
                        campos_sql['coluna'].append(colunas[nome])
                        campos_sql['valor'].append(formatar_valor(valor))
                    elif nome == 'aquisicao':
                        campos_sql['coluna'].append(colunas[nome])
                        campos_sql['valor'].append(formatar_strings(formatar_data(valor)))
            return campos_sql                        

        # -----------------------------------------------------------
        dados = self.componentes.verificar_entradas()
        if dados:
            campos = campos_ativos()
            sql = f''' insert into patrimonios ({', '.join(campos['coluna'])})
            values ({', '.join(campos['valor'])});'''
            for i in range(self.quantidade):
                id = JControl.ref.crud.insert_id(sql)
                Reg().reg_criacao(id)
            JControl.controle.voltar_sob()
            JControl.ref.att_frame.att_dados()
        
    def top_frame_mult_edicao(self):
        # criar variáveis
        self.ativos = self.componentes.ativos()
        self.desativados = self.componentes.desativados()
        self.quantidade = int(self.qtd_var.get())
        if self.desativados:
            # recuperar padrão
            self.padrao = self.componentes.verificar_multi_entradas(self.ativos)
            if isinstance(self.padrao, dict):
                # limpar tela do top
                self.limpar_top()
                # alocar frame
                self.fr_mult_edit = ttk.Frame(self.top)
                self.fr_mult_edit.pack(fill='both', expand=True)
                self.att_fr_mult_edit = TopFrameMultEdicao(self.fr_mult_edit, self, self.padrao)
                JControl.centralizar_janela(self.top)
        else:
            self.salvar_multiplos_iguais()

    def frame_button(self):
        self.fr_button = ttk.Frame(self.frame, style=INFO)
        self.fr_button.pack(fill='x', expand=True, after=self.fr_cadastro)
        self.fr_button.grid_columnconfigure(0, weight=1)
        # widget
        self.btt_next = ttk.Button(self.fr_button, text='Avançar', style=(SUCCESS, OUTLINE))
        self.btt_next.grid(row=0, column=0, sticky='e')
        self.btt_next.bind('<ButtonRelease>', lambda e:self.top_frame_mult_edicao())

    def __init__(self, pai, ref):
        self.pai = pai
        self.ref = ref
        # toplevel
        self.top = ttk.Toplevel(pai)
        # frame
        self.frame = ttk.Frame(self.top)
        self.frame.pack(fill='both', expand=True)
        self.configurar_tela()
        # chamar frames
        self.frame_titulo()
        self.configurar_cadastro()


class TopPatrimonio:
    def configurar_tela(self):
        self.top.withdraw()
        self.top.title('Cadastro de patrimonio')
        self.top.overrideredirect(True)
        self.top.resizable(False, False)
    
    def frame_titulo(self):
        self.fr_titulo = ttk.Frame(self.top)
        self.fr_titulo.pack(fill='x', expand=True)
        # widget
        self.lbl_titulo = ttk.Label(self.fr_titulo, text='Adicione seu patrimônio', font='helvetica, 30 bold', anchor='center')
        self.lbl_titulo.pack(fill='x', expand=True)
        self.lbl_subtitulo = ttk.Label(self.fr_titulo, 
                                       text='Atenção ao cadastrar seu patrimonio, não é possivel edita-lo após cadastro, exceto a localização', 
                                       font='helvetica, 12', 
                                       anchor='center')
        self.lbl_subtitulo.pack(fill='x', expand=True)

    def frame_cadastro(self):
        self.fr_cadastro = ttk.Frame(self.top)
        self.fr_cadastro.pack(fill='x', expand=True)
        # aplicar componentes
        self.componentes = ComponentesCadastro(self.fr_cadastro, self)

    def salvar(self):
        def formatar_strings(value):
            return '\"' + value + '\"'
        
        def formatar_data(data):
            return '-'.join(data.split('/')[::-1])

        def formatar_valor(valor):
            return str(round(float(valor), 2))

        def formatar_cat_local(value):
            return str(int(value.split('-')[0]))

        def campos_ativos():
            colunas = {'nome': 'nome_item', 
                       'marca': 'marca', 
                       'modelo': 'modelo', 
                       'nserie': 'n_serie', 
                       'aquisicao': 'd_aquisicao', 
                       'valor': 'valor', 
                       'caracteristica': 'carac', 
                       'locais': 'id_local', 
                       'categoria': 'id_categ'}
            campos_sql = {'coluna': [], 
                          'valor': []}
            for nome, valor in dados.items():
                if len(valor) > 0:
                    if nome in ['nome', 'marca', 'modelo', 'nserie', 'caracteristica']:
                        campos_sql['coluna'].append(colunas[nome])
                        campos_sql['valor'].append(formatar_strings(valor))
                    elif nome in ['categoria', 'locais']:
                        campos_sql['coluna'].append(colunas[nome])
                        campos_sql['valor'].append(formatar_cat_local(valor))
                    elif nome == 'valor':
                        campos_sql['coluna'].append(colunas[nome])
                        campos_sql['valor'].append(formatar_valor(valor))
                    elif nome == 'aquisicao':
                        campos_sql['coluna'].append(colunas[nome])
                        campos_sql['valor'].append(formatar_strings(formatar_data(valor)))
            return campos_sql                        

        # -----------------------------------------------------------
        dados = self.componentes.verificar_entradas()
        if dados:
            campos = campos_ativos()
            sql = f''' insert into patrimonios ({', '.join(campos['coluna'])})
            values ({', '.join(campos['valor'])});'''
            id = JControl.ref.crud.insert_id(sql)
            Reg().reg_criacao(id)
            # fechar top
            JControl.controle.voltar_sob()
            self.ref.ref.att_dados()

    def frame_button(self):
        self.fr_button = ttk.Frame(self.top, style=INFO)
        self.fr_button.pack(fill='x', expand=True)
        self.fr_button.grid_columnconfigure(0, weight=1)
        # widget
        self.btt_add = ttk.Button(self.fr_button, text='Concluir', style=SUCCESS)
        self.btt_add.grid(row=0, column=0, sticky='e')
        self.btt_add.bind('<ButtonRelease-1>', lambda e: self.salvar())

    def __init__(self, pai, ref):
        self.pai = pai
        self.ref = ref
        # toplevel
        self.top = ttk.Toplevel(pai)
        self.configurar_tela()
        # chamar frames
        self.frame_titulo()
        self.frame_cadastro()
        self.frame_button()
