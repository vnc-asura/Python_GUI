from crud import Caminho
import ttkbootstrap as ttk


class JanelaControl(Caminho):
    controle = None
    pai = None
    ref = None

    def __init__(self, pai, ref):
        self._janelas = [pai]
        pai.iconbitmap(self.resource_path('icone.ico'))
        JanelaControl.controle = self
        JanelaControl.pai = pai
        JanelaControl.ref = ref

    @classmethod
    def centralizar_janela(cls, janela):
        janela.position_center()
        if not janela.winfo_ismapped():
            janela.deiconify()
            janela.overrideredirect(False)

    def comportamento_top(self, top, tp):
        if tp == 1:
            top.protocol('WM_DELETE_WINDOW', self.voltar)
        elif tp == 2:
            top.protocol('WM_DELETE_WINDOW', self.voltar_sob)

    def add_top(self, top):
        self._janelas[-1].withdraw()
        self._janelas.append(top)
        self.comportamento_top(top, 1)
        self.centralizar_janela(top)
        top.iconbitmap(self.resource_path('icone.ico'))

    def add_top_sob(self, top):
        self._janelas.append(top)
        self.comportamento_top(top, 2)
        top.grab_set()
        self.centralizar_janela(top)
        top.iconbitmap(self.resource_path('icone.ico'))

    def voltar(self):
        self._janelas.pop().destroy()
        self._janelas[-1].deiconify()

    def voltar_sob(self):
        self._janelas.pop().destroy()

