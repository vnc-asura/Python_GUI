# Projetos GUI
---
__Conteúdos:__
* [__1. Sistema bancário__](https://github.com/vnc-asura/Python_GUI/blob/main/README.md#1-sistema-banc%C3%A1rio)
   * [1.1 Instruções](https://github.com/vnc-asura/Python_GUI/blob/main/README.md#11-instru%C3%A7%C3%B5es)
   * [1.2 Resultados](https://github.com/vnc-asura/Python_GUI/blob/main/README.md#12-resultado)
---
## 1. Sistema bancário
Trabalho prático em python aplicando conceitos de __GUI__ e __OOP__ na criação de um sistema bancário com o pacote tkinter e o modulo ttk(ThemedTk).
### 1.1 Instruções:
1. Implemente uma interface gráfica para o sistema bancário que permita instanciar outras
janelas do sistema por meio do widget Menu?

2. Implemente interfaces gráficas para cadastrar, mostrar e atualizar as informações de uma
instância da classe banco.

3. Crie subclasses para a classe Conta: ContaPoupanca e ContaCorrente. As contas do tipo
poupança devem ter seu saldo atualizado mensalmente de acordo com uma taxa de juros do
banco. As contas do tipo corrente devem ter um desconto no seu saldo, fixado pelo banco,
sempre que acontecer um saque ou um depósito.

4. As instâncias das classes Conta e Cliente deve ter um identificador de valor único e
automático para cada instância.

5. Implemente interfaces gráficas para listar e incluir instâncias das classes ContaPoupanca,
ContaCorrente e Cliente.

6. Crie uma funcionalidade para encerrar uma conta. Uma conta só pode ser encerrada se o seu
saldo estiver zerado.

7. Crie uma funcionalidade para remover uma instância da classe Cliente. Um cliente só pode
ser removido se não estiver vinculado a uma conta no banco.

8. Implemente uma interface gráfica para atualizar os dados de uma instância da classe Cliente.

9. Implemente interfaces gráficas para realizar as operações de saque e depósito em instâncias
das classes ContaCorrente e ContaPoupanca. Uma conta encerrada não pode realizar saques e
depósitos.

10. Crie uma funcionalidade para gerar um relatório (extrato de operações com saques e
depósitos) de uma conta e salve em um arquivo cujo o nome será o número da conta e conteúdo
deve conter a data, o tipo de operação e o valor (separados por vírgulas), além do saldo final da
conta.

__Considere as seguintes classes:__
```Python
class Banco:
  def __init__(self, numero, nome):
    self.__num = num
    self.__nome = nome
    self.__contas = []
  //Métodos
```
```Python
class Conta:
  def __init__(self, n, cli, sal):
    self.__numero = n
    self.__titular = cli
    self.__saldo = sal
  //Métodos
```
```Python
class Cliente:
  def __init__(self, n, e, cpf):
    self.__nome = n    
    self.__endereco = e
    self.__CPF = cpf
  //Métodos
```

### 1.2 Resultado:

|Tela inicial do sistema bancário|
|:---:|
|![Tela inicial do sistema bancário](https://github.com/user-attachments/assets/01f39e0c-e98d-416a-bd6a-16d6ba5babe4)|

|Tela de registro, listagem e edição de bancos|
|:---:|
|![Tela de registro, listagem e edição de bancos](https://github.com/user-attachments/assets/b3a38bc6-9da7-4bb0-a286-355b2138f7c7)|

|Tela de registro, listagem e edição de clientes|
|:---:|
|![Tela de registro, listagem e edição de clientes](https://github.com/user-attachments/assets/61f339bb-19b0-4e4a-9070-ab24f2c04f33)|

|Tela de acesso a conta|
|:---:|
|![Tela de acesso a conta](https://github.com/user-attachments/assets/5d790974-c248-4d5d-9090-f554abe4e043)|

|Tela para consulta de contas canceladas|
|:---:|
|![Tela para consulta de contas canceladas](https://github.com/user-attachments/assets/07e07240-759d-4f64-b962-7bbbe4631437)|

|Tela para consulta ao banco|
|:---:|
|![Tela para consulta ao banco](https://github.com/user-attachments/assets/1797a69d-f14a-4460-b200-6e5ebac50344)|

