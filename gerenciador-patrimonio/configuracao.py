import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from frame_inicial import CadastrarLocais as CLocais, SelecionarTema as STema, CadastrarCategorias as CCategorias




class TopLocais:
    def configurar_tela(self):
        self.top.withdraw()
        self.top.title('Cadastro de locais')
        self.top.overrideredirect(True)
        self.top.resizable(False, False)
    
    def frame_cadastro(self):
        self.lfr_cadastro = ttk.Frame(self.frame)
        self.lfr_cadastro.pack(side='left', fill='x')
        self.att_fr_cadastro = CLocais(self.lfr_cadastro, self)

    def __init__(self, pai, ref):
        self.pai = pai
        self.ref = ref
        # toplevel
        self.top = ttk.Toplevel(self.pai)
        self.configurar_tela()
        # frames 
        self.frame = ttk.Frame(self.top)
        self.frame.pack(fill='both', expand=True)
        # chamar frames
        self.frame_cadastro()


class TopTema:
    def configurar_tela(self):
        self.top.withdraw()
        self.top.title('Selecionar tema')
        self.top.overrideredirect(True)
        self.top.resizable(False, False)
    
    def frame_cadastro(self):
        self.lfr_cadastro = ttk.Frame(self.frame)
        self.lfr_cadastro.pack(side='left', fill='x')
        self.att_fr_cadastro = STema(self.lfr_cadastro, self)

    def __init__(self, pai, ref):
        self.pai = pai
        self.ref = ref
        # toplevel
        self.top = ttk.Toplevel(self.pai)
        self.configurar_tela()
        # frames 
        self.frame = ttk.Frame(self.top)
        self.frame.pack(fill='both', expand=True)
        # chamar frames
        self.frame_cadastro()


class TopCategorias:
    def configurar_tela(self):
        self.top.withdraw()
        self.top.title('Selecionar tema')
        self.top.overrideredirect(True)
        self.top.resizable(False, False)

    def frame_categorias(self):
        self.fr_categorias = ttk.Frame(self.frame)
        self.fr_categorias.pack(fill='x')
        self.att_fr_categorias = CCategorias(self.fr_categorias, self)

    def __init__(self, pai, ref):
        self.pai = pai
        self.ref = ref
        # toplevel
        self.top = ttk.Toplevel(self.pai)
        self.configurar_tela()
        # frame
        self.frame = ttk.Frame(self.top)
        self.frame.pack(fill='both', expand=True)
        # chamar frames
        self.frame_categorias()
        
