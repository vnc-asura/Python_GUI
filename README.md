# Projetos GUI
---
__Conteúdos:__
* [__1. Sistema bancário__](https://github.com/vnc-asura/Python_GUI/tree/main?tab=readme-ov-file#1-sistema-banc%C3%A1rio)
   * [1.1. Instruções](https://github.com/vnc-asura/Python_GUI/tree/main?tab=readme-ov-file#11-instru%C3%A7%C3%B5es)
   * [1.2. Resultados](https://github.com/vnc-asura/Python_GUI/tree/main?tab=readme-ov-file#12-resultado)
* [__2. Gerenciador patrimonial__](https://github.com/vnc-asura/Python_GUI#2-gerenciador-patrimonial)
   * [2.1. Funcionalidades](https://github.com/vnc-asura/Python_GUI?tab=readme-ov-file#21-funcionalidades)
   * [2.2. Banco de dados](https://github.com/vnc-asura/Python_GUI?tab=readme-ov-file#22-banco-de-dados)
     * [2.2.1. DER](https://github.com/vnc-asura/Python_GUI?tab=readme-ov-file#221-der)
     * [2.2.2. Dump](https://github.com/vnc-asura/Python_GUI?tab=readme-ov-file#222-dump)
   * [2.3. Resultado](https://github.com/vnc-asura/Python_GUI?tab=readme-ov-file#23-resultado)
---
## 1. Sistema bancário
Trabalho prático em python aplicando conceitos de __GUI__ e __OOP__ na criação de um sistema bancário com o pacote tkinter e o modulo ttk(ThemedTk).
### 1.1. Instruções
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

### 1.2. Resultado

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

## 2. Gerenciador patrimonial
Trabalho prático em python aplicando conceitos de __GUI__ , __OOP__ e __DB__ na criação de um sistema para gerenciamento de patrimônios com o pacote ttkbootstrap e sqlite3.
### 2.1. Funcionalidades
* Cadastro de categorias dos itens;
* Cadastro de locais;
* Cadastro de patrimônios (único e múltiplo);
* Atualização de patrimônios;
* Registro de Atualizações;
* Mudança de Tema;
### 2.2. Banco de dados
#### 2.2.1. DER
|Diagrama entidade-relacionamento|
|:---:|
|![Conceitual_patrimonio](https://github.com/user-attachments/assets/df562a67-deeb-474e-a359-7bad68c5fce7)|
#### 2.2.2. Dump
```sql
create table patrimonios(
    id integer not null primary key autoincrement, 
    nome_item varchar(255) not null, 
    marca varchar(255) null, 
    modelo varchar(255) null, 
    n_serie varchar(255) null,
    carac text null, 
    valor double null, 
    d_aquisicao date null, 
    d_registro date default (date('now')),
    status integer default 1, 
    id_local integer not null, 
    id_categ integer not null, 
    constraint fk_pat_local foreign key (id_local) references locais(id), 
    constraint fk_pat_categ foreign key (id_categ) references categorias(id)
);

create table locais(
    id integer not null primary key autoincrement, 
    nome varchar(255) not null, 
    descricao text not null, 
    status integer default 1
);

create table categorias(
    id integer not null primary key autoincrement, 
    nome varchar(255) not null, 
    descricao text not null, 
    status integer default 1
);

create table registros(
    id integer not null primary key autoincrement,
    registro varchar(255) not null, 
    d_registro date default (date('now')),
    id_patrimonio integer not null, 
    constraint fk_reg_patrimonio foreign key (id_patrimonio) references patrimonios(id)
);

create table tema(
    id integer not null primary key autoincrement, 
    nome varchar(255) not null
);

insert into locais(nome, descricao, status)
values ('Sem local', 'Categoria padrão do sistema', 2);

insert into categorias(nome, descricao, status)
values ('Sem categoria', 'Categoria padrão do sistema', 2);

insert into tema(id, nome)
values (1, 'litera');
```

### 2.3. Resultado
|Tela inicial do gerenciador patrimonial|
|:---:|
|![inicial](https://github.com/user-attachments/assets/dabb96eb-80e9-4172-b56f-c6f5df793404)|

|Tela inicial do gerenciador patrimonial - registros|
|:---:|
|![registros](https://github.com/user-attachments/assets/adaf5834-fa8e-4828-bdc6-e27efaa7a186)|

|Tela seleção de tema|
|:---:|
|![tema](https://github.com/user-attachments/assets/2a63ce50-ebec-49b2-9dfc-80a746e98541)|

|Tela cadastro locais|
|:---:|
|![locais](https://github.com/user-attachments/assets/3a7d70f6-8ac5-492e-9708-420580c3cf35)|

|Tela cadastro categorias|
|:---:|
|![cate](https://github.com/user-attachments/assets/6128d0a9-ae9d-40e6-85fa-7d57cdf1307d)|

|Tela cadastro patrimônio - único|
|:---:|
|![cad](https://github.com/user-attachments/assets/f4843703-fab1-4479-a6d0-3c204b21b502)|

|Tela cadastro patrimônios - múltiplos|
|:---:|
|![mult-cadastro](https://github.com/user-attachments/assets/3ffe6191-9a38-4dd6-b3ea-d43f52c8f7c8)|

|Tela edição mútipla|
|:---:|
|![mult-edicao](https://github.com/user-attachments/assets/decd80db-2d95-4b2a-a4ae-a215c060d263)|

|Tela acessso e atualização de patrimônio|
|:---:|
|![att](https://github.com/user-attachments/assets/6b7b1b67-815a-4cc5-b2fd-46f749a582a7)|



