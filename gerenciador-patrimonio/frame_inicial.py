import ttkbootstrap as ttk
from ttkbootstrap.constants import * 
from comportamento import JanelaControl as Jcontrol
from ttkbootstrap.scrolled import ScrolledFrame as SFrame, ScrolledText as SText
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox as Msg
from crud import Caminho 


class CadLocaisCategorias:
    def widget_custom(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget['font'] = 'helvetica, 16 bold'
            elif isinstance(widget, ttk.Entry):
                widget['font'] = 'helvetica, 16'
            widget.grid_configure(padx=5, pady=5)

    def checar_entradas(self):
        self.pegar_variaveis()
        if all([self.var['nome'].strip(), self.var['descricao'].strip()]):
            self.limpar_entradas()
            return self.var
        else:
            Msg.show_warning('Campos incompletos, corrija-os e tente novamente', 'Aviso cadastro', parent=self.ref.ref.top)

    def pegar_variaveis(self):
        # campos
        self.var = {'nome' : self.apelido_var.get(), 
                    'descricao': self.txt_desc.get('1.0', 'end')}

    def limpar_entradas(self):
        self.apelido_var.set(value='')
        self.txt_desc.delete('1.0', 'end')

    def desabilitar_habilitar(self, estado):
        state = ''
        if estado:
            state = 'normal'
        else:
            state = 'disabled'
        
        self.ent_apelido['state'] = state
        self.txt_desc.text['state'] = state

    def desconfig_mostrar(self):
        # habilitar
        self.desabilitar_habilitar(1)
        # limpar entradas
        self.limpar_entradas()
        # destruir voltar button
        self.btt_back.destroy()
        # realocar geometricamente o button cadastrar
        self.btt_cad.grid(row=4, column=0, sticky='e')

    def verifica_mostrar(self):
        if self.mostrado:
            self.desconfig_mostrar()
            self.mostrado = None

    def config_mostrar(self, campos):
        # verifica se existe ao já sendo mostrado
        self.verifica_mostrar()
        # limpar entradas
        self.limpar_entradas()
        # desaparecer cadastrar button
        self.btt_cad.grid_forget()
        # button voltar
        self.btt_back = ttk.Button(self.frame, text='Voltar', bootstyle=(DANGER, OUTLINE))
        self.btt_back.grid(row=4, column=0, sticky='e')
        self.btt_back.bind('<ButtonRelease-1>', lambda e: self.desconfig_mostrar())
        # inserir dados
        nome = campos[1]
        descricao = campos[2].replace('\\n', '\n')
        self.apelido_var.set(nome)
        self.txt_desc.insert('end', descricao)
        # desabilitar
        self.desabilitar_habilitar(0)
        # alter flag mostrado
        self.mostrado = 1

    def mostrar_catch(self, campos):
        self.config_mostrar(campos)
        
    def __init__(self, frame, ref):
        self.frame = frame
        self.ref = ref
        # variaveis
        self.var = None
        self.mostrado = None
        # widgets
        # label-entry
        # apelido
        self.apelido_var = ttk.StringVar()
        self.lbl_apelido = ttk.Label(self.frame, text='Nome/Apelido *')
        self.lbl_apelido.grid(row=0, column=0, sticky='w')
        self.ent_apelido = ttk.Entry(self.frame, textvariable=self.apelido_var)
        self.ent_apelido.grid(row=1, column=0, sticky='ew')
        # descrição
        self.lbl_desc = ttk.Label(self.frame, text='Descrição *')
        self.lbl_desc.grid(row=2, column=0, sticky='w')
        self.txt_desc = SText(self.frame, font=('helvetica', 16), width=30, height=10, autohide=True, wrap='word')
        self.txt_desc.grid(row=3, column=0, sticky='ew')
        # butoes
        # cadastrar
        self.btt_cad = ttk.Button(self.frame, text='Cadastrar')
        self.btt_cad.grid(row=4, column=0, sticky='e')
        self.btt_cad.bind('<ButtonRelease-1>', lambda e: self.ref.salvar_catch(self.checar_entradas()))
        # customizar widgets
        self.widget_custom()
        # tooltip
        ToolTip(self.lbl_apelido, 'Campo obrigatório, é essencial preenche-lo')
        ToolTip(self.lbl_desc, 'campos obrigatório, é essencial preenche-lo')


class ItemLocaisCategorias(Caminho): 
    def deletar_item(self):
        sql1 = f''' delete from {self.tabela} 
        where id = {self.campos[0]};'''

        sql2 = f'''  update {self.tabela} 
        set status = 0 
        where id = {self.campos[0]};'''

        if not Jcontrol.ref.crud.delete(sql1):
            Jcontrol.ref.crud.update(sql2)
        self.ref.pesq_var.set(value='')
        self.ref.ref.limpar_catch()

    def __init__(self, pai, ref, campos, tabela): # tipoo define se é local = 1 e categoria = 2
        self.pai = pai
        self.ref = ref
        self.campos = campos
        self.tabela = tabela
        self.frame = ttk.Frame(self.pai, bootstyle=DARK)
        self.frame.pack(padx=10, pady=10, fill=X, expand=True)
        # widgets 
        # nome 
        self.lbl_apelido = ttk.Label(self.frame, text=f'{self.campos[1]}', font='helvetica, 16 bold')
        self.lbl_apelido.pack(side='left', padx=5, pady=5)
        # ver
        self.img_ver = ttk.PhotoImage(file=self.resource_path('olho-aberto.png'))
        self.lbl_ver = ttk.Label(self.frame, image=self.img_ver)
        self.lbl_ver.pack(side='right', padx=2, pady=5)
        self.lbl_ver.bind('<ButtonRelease-1>', lambda e: self.ref.ref.ver_catch(self.campos))
        # apagar
        if self.campos[3] == 1:
            self.img_apagar = ttk.PhotoImage(file=self.resource_path('remover.png'))
            self.lbl_apagar = ttk.Label(self.frame, image=self.img_apagar)
            self.lbl_apagar.pack(side='right', padx=2, pady=5, before=self.lbl_ver)
            self.lbl_apagar.bind('<ButtonRelease-1>', lambda e: self.deletar_item())
            # Tooltip
            ToolTip(self.lbl_ver, text=f'Mostrar nome e descrição do item de {self.tabela}')
            ToolTip(self.lbl_apagar, text=f'Deletar o item de {self.tabela}')
        # Tooltip
        ToolTip(self.lbl_ver, text=f'Mostrar nome e descrição do item de {self.tabela}')


class ItemTemas:
    def mudar_tema(self):
        self.ref.ref.ref.mudar_tema(self.tema)
        self.ref.tema = self.tema
        self.ref.btt_concluir['state'] = 'normal'

    def __init__(self, pai, ref, tema):
        self.pai = pai
        self.ref = ref
        self.tema = tema
        # button
        self.btt_tema = ttk.Button(pai, text=self.tema.capitalize(), command=self.mudar_tema)
        self.btt_tema.pack(fill='x', expand=True, padx=15, pady=10)


class ListLocaisCategorias:
    def widget_custom(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget['font'] = 'helvetica, 16 bold'
            elif isinstance(widget, ttk.Entry):
                widget['font'] = 'helvetica, 16'
            widget.grid(padx=5, pady=5)

    def inserir_itens(self):
        sql = f'''  select * from {self.tabela} where status != 0 ;'''
        dados =  Jcontrol.ref.crud.get(sql)
        self.alocar_itens(dados)
        
    
    def alocar_itens(self, campos):
        self.limpar_itens()
        self.itens = []
        for tupla in campos:
            self.item = ItemLocaisCategorias(self.sframe, self, tupla, self.tabela)
            self.itens.append(self.item)

    def pesquisar(self):
        entrada = self.pesq_var.get()
        if len(entrada) > 0:
            sql = f'''  select * from {self.tabela} where nome like "%{entrada}%";'''
            self.alocar_itens(Jcontrol.ref.crud.get(sql))
        else:
            self.inserir_itens()


    def limpar_itens(self):
        # tenta limpar lista se existe
        try:
            self.itens.clear()
        except:
            pass
        # destroy itens
        for item in self.sframe.winfo_children():
            item.destroy()
            
    def __init__(self, frame, ref):
        self.frame = frame
        self.ref = ref
        # variaveis
        self.tabela = 'locais' if isinstance(self.ref, CadastrarLocais) else 'categorias'
        # widget
        # label-entry-button
        # pesquisar 
        self.pesq_var = ttk.StringVar()
        self.pesq_var.trace_add('write', lambda *args: self.pesquisar())
        self.lbl_pesq = ttk.Label(self.frame, text='Pesquisar')
        self.lbl_pesq.grid(row=0, column=0, sticky='e')
        self.ent_pesq = ttk.Entry(self.frame, textvariable=self.pesq_var)
        self.ent_pesq.grid(row=0, column=1, sticky='ew')
        self.btt_limpar = ttk.Button(self.frame, text='X', bootstyle=DANGER)
        self.btt_limpar.grid(row=0, column=2, sticky='w')
        self.btt_limpar.bind('<ButtonRelease-1>', lambda e: self.pesq_var.set(value=''))
        self.sep = ttk.Separator(self.frame, orient=HORIZONTAL)
        # separator
        self.sep.grid(row=1, column=0, columnspan=3, sticky='ew')
        # ScrolledFrame
        self.sframe = SFrame(self.frame, autohide=True)
        self.sframe.grid(row=2, column=0, columnspan=3, sticky='nsew')
        # customizar widget
        self.widget_custom()
        # listar 
        self.inserir_itens()


class CadastrarLocais:
    def customizar_widget(self):
        for widget in self.frame.winfo_children():
            widget.grid(padx=5, pady=5)

    def label_frame_cadastro(self):
        self.lfr_cadastro = ttk.LabelFrame(self.frame, text='Cadastro de local')
        self.lfr_cadastro.grid(row=2, column=0, sticky='nsew')
        self.lfr_cadastro.columnconfigure(0, weight=1)
        self.att_lfr_cadastro = CadLocaisCategorias(self.lfr_cadastro, self)

    def label_frame_listar(self):
        self.lfr_listar = ttk.LabelFrame(self.frame, text='Locais cadastrados')
        self.lfr_listar.rowconfigure(2, weight=1)
        self.lfr_listar.grid(row=2, column=1, sticky='nsew')
        self.att_lfr_listar = ListLocaisCategorias(self.lfr_listar, self)

    def salvar_catch(self, dados):
        if dados:
            t_dados = tuple(dados.values())
            self.salvar(t_dados)
    
    def ver_catch(self, dados):
        self.att_lfr_cadastro.config_mostrar(dados)

    def limpar_catch(self):
        if self.att_lfr_cadastro.mostrado:
            self.att_lfr_cadastro.desconfig_mostrar()

    def salvar(self, dados):
        sql = f'''  insert into locais(nome, descricao) values {dados};'''
        if Jcontrol.ref.crud.insert(sql) == 1:
            Msg.show_info('Cadastro realizado com sucesso', 'Informação cadastro', parent=self.ref.top)
            self.att_lfr_cadastro.limpar_entradas()
            self.att_lfr_listar.inserir_itens()
        else:
            Msg.show_warning('Erro no cadastro, tente novamente', 'Aviso cadastro', parent=self.ref.top)
        
    def fechar_tela(self):
        Jcontrol.controle.voltar_sob()

    def __init__(self, frame, ref):
        self.frame = frame
        self.ref = ref
        #labels
        self.lbl_titulo = ttk.Label(self.frame, 
                                    text='cadastre seus locais!!!', 
                                    font='helvetica, 30 bold', 
                                    anchor='center')
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, sticky='ew')
        # labelframe cadastro local
        self.label_frame_cadastro()
        self.label_frame_listar()
        # button
        # voltar
        self.btt_back = ttk.Button(self.frame, text='Voltar', bootstyle=DANGER)
        self.btt_back.grid(row=4, column=1, sticky='e')
        self.btt_back.bind('<ButtonRelease-1>', lambda e: Jcontrol.controle.voltar_sob())
        # customizar widgets
        self.customizar_widget()


class CadastrarCategorias:
    def customizar_widget(self):
        for widget in self.frame.winfo_children():
            widget.grid(padx=5, pady=5)

    def label_frame_cadastro(self):
        self.lfr_cadastro = ttk.LabelFrame(self.frame, text='Cadastro de categoria')
        self.lfr_cadastro.grid(row=2, column=0, sticky='nsew')
        self.lfr_cadastro.columnconfigure(0, weight=1)
        self.att_lfr_cadastro = CadLocaisCategorias(self.lfr_cadastro, self)

    def label_frame_listar(self):
        self.lfr_lista = ttk.LabelFrame(self.frame, text='Categorias')
        self.lfr_lista.grid(row=2, column=1, sticky='nsew')
        self.lfr_lista.rowconfigure(2, weight=1)
        self.att_lfr_lista = ListLocaisCategorias(self.lfr_lista, self)

    def ver_catch(self, dados):
        self.att_lfr_cadastro.config_mostrar(dados)

    def salvar_catch(self, dados):
        if dados:
            t_dados = tuple(dados.values())
            self.salvar(t_dados)

    def limpar_catch(self):
        if self.att_lfr_cadastro.mostrado:
            self.att_lfr_cadastro.desconfig_mostrar()

    def salvar(self, dados):
        sql = f'''  insert into categorias(nome, descricao) values {dados};'''
        if Jcontrol.ref.crud.insert(sql) == 1:
            Msg.show_info('Cadastro realizado com sucesso', 'Informação cadastro', parent=self.ref.top)
            self.att_lfr_cadastro.limpar_entradas()
            self.att_lfr_lista.inserir_itens()
        else:
            Msg.show_warning('Erro no cadastro, tente novamente', 'Aviso cadastro', parent=self.ref.top)

    def __init__(self, frame, ref):
        self.frame = frame
        self.ref = ref
        # label
        self.lbl_titulo = ttk.Label(self.frame, text='Cadastre as Categorias dos produtos!!!', font='helvetica, 30 bold ', anchor='center')
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, sticky='ew')
        # labelframa cadastro e listar
        self.label_frame_cadastro()
        self.label_frame_listar()
        # button
        # voltar
        self.btt_back = ttk.Button(self.frame, text='Voltar', bootstyle=DANGER)
        self.btt_back.grid(row=4, column=1, sticky='e')
        self.btt_back.bind('<ButtonRelease-1>', lambda e: Jcontrol.controle.voltar_sob())
        # customizar widgets
        self.customizar_widget()


class SelecionarTema:
    def listar_temas(self):
        temas = Style().theme_names()
        self.itens_tema = []
        for tema in temas:
            a = ItemTemas(self.sfr_temas, self, tema)
            self.itens_tema.append(a)

    def scrolled_temas(self):
        # label frame
        self.lfr_temas = ttk.LabelFrame(self.frame, text='Temas')
        self.lfr_temas.pack(padx=5, pady=5)
        self.sfr_temas = SFrame(self.lfr_temas, autohide=True)
        self.sfr_temas.pack(padx=5, pady=5)
        self.listar_temas()

    def salvar(self):
        if self.tema and str(self.btt_concluir['state']):
            sql = f""" update tema 
            set nome = '{self.tema}' 
            where id = 1; """

            if Jcontrol.ref.crud.update(sql) == 1:
                Jcontrol.controle.voltar_sob()
            else:
                Msg.ok('Ocorreu um erro, tente novamente!', 'Erro', parent=self.ref.top)    

    def __init__(self, frame, ref):
        self.frame = frame
        self.ref = ref
        # variavel
        self.tema = None
        # widgets
        # label
        # titulo
        self.titulo = ttk.Label(self.frame, text='Selecione o\ntema do programa', font='Helvetica, 30 bold')
        self.titulo.pack(padx=5, pady=5)
        # chamar metodo
        self.scrolled_temas()
        # button
        self.btt_concluir = ttk.Button(self.frame, text='Concluir', style=SUCCESS, state='disabled')
        self.btt_concluir.pack(side='right')
        self.btt_concluir.bind('<ButtonRelease-1>', lambda e: self.salvar())
        self.btt_back = ttk.Button(self.frame, text='Voltar', style=DANGER)
        self.btt_back.pack(side='left')
        self.btt_back.bind('<ButtonRelease-1>', lambda e: Jcontrol.controle.voltar_sob())

