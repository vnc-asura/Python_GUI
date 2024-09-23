class GeoPlace:
    __slots__ = ['_pai']

    def __init__(self, pai=None):
        self._pai = {}
        if pai:
            self.definir_pai(obj=pai)

    @property
    def pai(self):
        return self._pai

    @classmethod
    def centralizar_tela(cls, tela):
        tela.update()
        tela.deiconify()
        width = tela.winfo_width()
        height = tela.winfo_height()
        x = tela.winfo_screenwidth()
        y = tela.winfo_screenheight()
        return f'+{(x - width)//2}+{(y - height)//2}'

    @staticmethod
    def geometria_filho(obj):
        obj.update()
        largura = int(obj.winfo_width())
        altura = int(obj.winfo_height())
        return f'{largura}x{altura}'

    def definir_pai(self, obj):
        obj.update()
        largura = int(obj.winfo_width())
        altura = int(obj.winfo_height())
        self._pai = {'x': largura, 'y': altura}

    def proporcao_filho_pai(self, obj):
        if self.pai:
            filho = [int(x) for x in self.geometria_filho(obj).split('x')]
            return f'{filho[0]/self.pai["x"]:.2f}x{filho[1]/self.pai["y"]:.2f}'

    def __str__(self):
        return f'{self.pai["x"]}x{self.pai["y"]}'


