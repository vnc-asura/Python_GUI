import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from comportamento import JanelaControl as JControl
from frame_principal import FramePrincipal as FPrincipal
from configuracao import TopTema as TTEma, TopLocais as TLocais, TopCategorias as TCategorias
from crud import Crud
from ttkbootstrap.dialogs import Messagebox as Msg


class Tela:
    def mudar_tema(self, tema):
        self.tema = ttk.Style().theme_use(tema)
        self.customizar_tema()

    def customizar_tema(self):
        style  = Style()
        style = Style(style.theme_use())
        style.configure('TButton', font=('helvetica', 16, 'bold'))   
        style.configure('TLabelframe.Label', font=('Helvetica', 16, 'bold'))
        style.configure('Toolbutton', font=('Helvetica', 16, 'bold'))
        style.configure('TNotebook.Tab', font=('helvatica', 16, 'bold'))
        style.configure('Treeview', font=('helvetica', 12), rowheight=18)
        style.configure('Treeview.Heading', font=('helvetica', 13, 'bold'))
        style.configure('TMenubutton', font=('helvetica', 16, 'bold'))
        
    def apagar_database(self):
        opcao = Msg.show_question('Atenção caso prossiga, todos os dados armazenados serão deletados.\nTem certeza que deseja continuar?', 'Resetar dados', buttons=['Cancelar:secondary', 'Continuar:primary'])
        if opcao == 'Continuar':
            self.crud.drop_database()
            self.tela.destroy()
    
    def menu_tela(self):
        self.mnu_barra = ttk.Menu(self.tela)
        self.mnu_config = ttk.Menu(self.mnu_barra, tearoff=0)
        # add cascade mnu barra
        self.mnu_barra.add_cascade(label='Configurações', menu=self.mnu_config)
        # add command
        self.mnu_config.add_command(label='Tema', command=self.toplevel_tema)
        self.mnu_config.add_command(label='Locais', command=self.toplevel_local)
        self.mnu_config.add_command(label='Categorias', command=self.toplevel_categorias)
        self.mnu_config.add_command(label='Resetar dados', command=self.apagar_database)
        # associar barra a tela
        self.tela.config(menu=self.mnu_barra)
        
    def configurar_tela(self):
        self.tela.title('pivaraca patrimonios')
        self.tela.withdraw()
        self.tela.overrideredirect(True)
        self.tela.resizable(False, False)

    def toplevel_local(self):
        self.att_local = TLocais(self.tela, self)
        JControl.controle.add_top_sob(self.att_local.top)

    def toplevel_tema(self):
        self.att_tema = TTEma(self.tela, self)
        JControl.controle.add_top_sob(self.att_tema.top)

    def toplevel_categorias(self):
        self.att_categorias = TCategorias(self.tela, self)
        JControl.controle.add_top_sob(self.att_categorias.top)

    def carregar_tema(self):
        sql = """select nome 
        from tema 
        where id = 1;"""

        tema = self.crud.get(sql)
        self.mudar_tema(tema[0][0])
        
    def __init__(self, m): 
        self.tela = m
        # configura tela
        self.configurar_tela()
        self.janela_control = JControl(self.tela, self)
        # conexão ao banco
        self.crud = Crud()
        # selecionar tema
        self.carregar_tema()
        # customizar tema
        self.customizar_tema()
        # adiciona menu a tela
        self.menu_tela()
        # frame tela
        self.frame = ttk.Frame(self.tela)
        self.frame.pack(expand=True, fill='both')
        # atualizar frame
        self.att_frame = FPrincipal(self.frame, self)
        # centraliza reaparece tela
        self.janela_control.centralizar_janela(self.tela)


app = ttk.Window()
att_app = Tela(app)
app.mainloop()