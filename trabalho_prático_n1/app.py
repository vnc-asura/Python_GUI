import tkinter as tk
from tkinter import ttk, messagebox as msg
from geometry import GeoPlace as Geo
from teste import Teste


class Tela:
    def voltar(self):
        # self.janelas_control[0].destroy()
        self.janelas_control.pop().destroy()
        self.janelas_control[-1].deiconify()

    def banco_acesso(self, banco=''):
        from top_banco_acesso import TopBancoAcesso as Tba
        self.top_banco_acesso = tk.Toplevel(self.tela)
        self.top_banco_acesso.withdraw()
        att_top_banco_acesso = Tba(top=self.top_banco_acesso, ref=self, banco=banco)
        # comportamento
        self.top_banco_acesso.geometry(Geo.centralizar_tela(self.top_banco_acesso))
        self.janelas_control[-1].withdraw()
        self.janelas_control.append(self.top_banco_acesso)
        self.top_banco_acesso.protocol('WM_DELETE_WINDOW', self.voltar)
        self.limpar_entradas()

    def contas_canceladas(self):
        from top_contas_canceladas import TopContaCanceladas as Tcc
        self.top_contas_cancel = tk.Toplevel(self.tela)
        self.top_contas_cancel.withdraw()
        att = Tcc(self.top_contas_cancel, self)
        # Ccomportamento
        self.top_contas_cancel.geometry(Geo.centralizar_tela(self.top_contas_cancel))
        self.janelas_control[-1].withdraw()
        self.janelas_control.append(self.top_contas_cancel)
        self.top_contas_cancel.protocol('WM_DELETE_WINDOW', self.voltar)
        self.limpar_entradas()

    def conta_acesso(self, conta):
        from top_conta_acesso import TopContaAcesso as Tca
        self.top_conta_acesso = tk.Toplevel(self.tela)
        self.top_conta_acesso.withdraw()
        att_top_conta_acesso = Tca(self.top_conta_acesso, self, conta)
        # comportamento
        self.top_conta_acesso.geometry(Geo.centralizar_tela(self.top_conta_acesso))
        self.janelas_control[-1].withdraw()
        self.janelas_control.append(self.top_conta_acesso)
        self.top_conta_acesso.protocol('WM_DELETE_WINDOW', self.voltar)

    def checar_entradas(self):
        var = {'cpf': self.cpf_var.get(),
               'senha': self.pass_var.get()}
        if all([True if x.strip() != '' else False for x in  var.values()]) and len(var['cpf']) == 14:
            return var
        else:
            return None

    def limpar_entradas(self):
        var = [self.cpf_var, self.pass_var]
        for x in var:
            x.set('')
        self.mostrar_var.set(0)
        self.mostrar_senha()

    def acessar_conta(self):
        from conta import Conta
        var = self.checar_entradas()
        if var:
            ct = Conta.pesquisar_conta_cpf(var['cpf'])
            if ct:
                if Conta.verificar_senha(ct, var['senha']):
                    self.conta_acesso(ct)
                    self.limpar_entradas()
                else:
                    erro_senha_errada = msg.showerror('Erro acesso',
                                                      'A senha inserida está errada!')
            else:
                erro_cpf_inexistente = msg.showerror('Erro acesso',
                                                     'Não existe uma conta ativa vinculada a esse cpf!')
        else:
            erro_entrda_incompleta = msg.showerror('Erro acesso',
                                                   'Há campos vazios!\n'
                                                   'Preencha-os e tente novamente.')

    def reg_conta(self):
        from top_conta import TopConta
        self.top_conta = tk.Toplevel(self.tela)
        self.top_conta.withdraw()
        att_top_conta = TopConta(self.top_conta, self)
        # comportamento
        self.top_conta.geometry(Geo.centralizar_tela(self.top_conta))
        self.janelas_control[-1].withdraw()
        self.janelas_control.append(self.top_conta)
        self.top_conta.protocol('WM_DELETE_WINDOW', self.voltar)
        self.limpar_entradas()

    def reg_cliente(self):
        from top_cliente import TopCliente
        self.top_cliente = tk.Toplevel(self.tela)
        self.top_cliente.withdraw()
        att_top_cliente = TopCliente(self.top_cliente, self)
        # comportamento
        self.top_cliente.geometry(Geo.centralizar_tela(self.top_cliente))
        self.janelas_control[-1].withdraw()
        self.janelas_control.append(self.top_cliente)
        self.top_cliente.protocol('WM_DELETE_WINDOW', self.voltar)
        self.limpar_entradas()

    def reg_banco(self):
        from top_banco import TopBanco
        self.top_banco = tk.Toplevel(self.tela)
        self.top_banco.withdraw()
        att_top_banco = TopBanco(self.top_banco, self)
        # comportamento top
        self.top_banco.geometry(Geo.centralizar_tela(self.top_banco))
        att_top_banco.ent_num.focus_set()
        self.janelas_control[-1].withdraw()
        self.janelas_control.append(self.top_banco)
        self.top_banco.protocol('WM_DELETE_WINDOW', self.voltar)
        self.limpar_entradas()

    def mostrar_senha(self):
        if self.mostrar_var.get() == 1:
            self.ent_pass['show'] = ''
        else:
            self.ent_pass['show'] = '*'

    def interface_conta(self):
        def cpf_trace(*args):
            if len(self.cpf_var.get()) > 0:
                pont = {2: '.', 5: '.', 8: '-'}
                val = [x for x in self.cpf_var.get() if x.isdigit()]
                self.cpf_var.set(value=''.join([f'{n}{pont[cont]}' if cont in pont.keys() else n for cont, n in enumerate(val)]))
                self.ent_cpf.icursor(tk.END)
                if len(self.cpf_var.get()) > 14:
                    self.ent_cpf.delete(14, tk.END)

        # ---------------------------------------------------
        # imagem
        self.img = tk.PhotoImage(file='imagem/lg_capi.png')
        self.img = self.img.subsample(2)
        self.lbl_img = tk.Label(self.frame_tela, image=self.img)
        self.lbl_img.grid(row=0, column=0, columnspan=3, pady=20)
        # icone
        self.tela.iconbitmap('imagem/icone_capi.ico')
        # entradas
        # cpf
        self.cpf_var = tk.StringVar()
        self.cpf_var.trace_add('write', cpf_trace)
        self.lbl_cpf = ttk.Label(self.frame_tela,
                                 text='CPF:')
        self.lbl_cpf.grid(row=1, column=0, padx=5, pady=5)
        self.ent_cpf = ttk.Entry(self.frame_tela,
                                 width=30,
                                 textvariable=self.cpf_var)
        self.ent_cpf.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky='ew')
        # senha
        self.pass_var = tk.StringVar()
        self.lbl_pass = ttk.Label(self.frame_tela,
                                  text='Senha:')
        self.lbl_pass.grid(row=2, column=0, padx=5, pady=5)
        self.ent_pass = ttk.Entry(self.frame_tela,
                                  width=30,
                                  show='*',
                                  textvariable=self.pass_var)
        self.ent_pass.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky='ew')
        self.ent_pass.bind('<Return>', lambda ev: self.acessar_conta())
        # butao entrar
        self.btt_entrar = ttk.Button(self.frame_tela,
                                     text='Entrar')
        self.btt_entrar.grid(row=4, column=0, columnspan=3, sticky='ew', padx=5, pady=5)
        self.btt_entrar.bind('<ButtonRelease-1>', lambda ev: self.acessar_conta())
        # checkbox mostrar
        self.mostrar_var = tk.IntVar()
        self.chk_mostrar = ttk.Checkbutton(self.frame_tela,
                                           text='Mostrar senha',
                                           variable=self.mostrar_var,
                                           command=self.mostrar_senha)
        self.chk_mostrar.grid(row=3, column=2, sticky='e')

    def menu_tela(self):
        # cria barra
        self.mnu_barra = tk.Menu(self.tela)
        # cria cascata associada a barra
        self.mnu_registro = tk.Menu(self.mnu_barra, tearoff=0)
        # cria cascata associada a cascata registro
        self.mnu_banco = tk.Menu(self.mnu_registro, tearoff=0)
        self.mnu_conta = tk.Menu(self.mnu_registro, tearoff=0)
        # adiciona a cascata registro na barra
        self.mnu_barra.add_cascade(label='Registro', menu=self.mnu_registro)
        # adiciona a cascata banco e conta na cascata registro
        self.mnu_registro.add_cascade(label='Banco', menu=self.mnu_banco)
        self.mnu_registro.add_cascade(label='Conta', menu=self.mnu_conta)
        # adiciona comandos na cascata registro
        self.mnu_registro.add_command(label='Cliente', command=self.reg_cliente)
        self.tela.config(menu=self.mnu_barra)
        # adiciona comandos na cascata banco e conta
        self.mnu_banco.add_command(label='Registrar', command=self.reg_banco)
        self.mnu_banco.add_command(label='Acessar', command=self.banco_acesso)
        self.mnu_conta.add_command(label='Registrar', command=self.reg_conta)
        self.mnu_conta.add_command(label='Contas canceladas', command=self.contas_canceladas)

    def __init__(self, m):
        self.tela = m
        self.tela.title('Sistema Bancario Pivaraca')
        width = 720
        height = 500
        x = self.tela.winfo_screenwidth()
        y = self.tela.winfo_screenheight()
        centralizar = f'{width}x{height}+{(x-width)//2}+{(y-height)//2}'
        self.tela.geometry(centralizar)
        self.tela.resizable(False, False)
        # frame
        self.frame_tela = ttk.Frame(self.tela)
        self.frame_tela.pack()
        # menu
        self.menu_tela()
        # controle janelas
        self.janelas_control = [self.tela]
        # Interface conta
        self.interface_conta()
        # teste
        t = Teste()


app = tk.Tk()
att = Tela(app)
app.mainloop()
