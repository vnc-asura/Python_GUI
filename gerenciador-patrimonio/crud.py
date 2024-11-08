import sqlite3
from sqlite3 import Error
import os, sys


class Caminho:
    def resource_path(self, relativo):
        try: 
            base = sys._MEIPASS
        except Exception:
            base = os.path.abspath('.')
        return os.path.join(base, relativo)



class Conexao(Caminho):
    def verificar_banco(self, cursor):
        tabelas = cursor.execute('select name from sqlite_master where type="table" ;').fetchall()
        if len(tabelas) > 1:
            return 1
        else:
            return 0
          
    def dump(self, conexao, vazio):
        if not vazio:
            with open(self.resource_path('dump.txt'), 'r', encoding='utf-8') as dump:
                cursor = conexao.cursor().executescript(dump.read())
               
    def get_conexao(self):
        caminho = (os.path.abspath('patrimonios.db'))
        conexao = None
        try:
            conexao = sqlite3.connect(caminho)
            self.dump(conexao, self.verificar_banco(conexao.cursor()))
            conexao.cursor().execute('PRAGMA foreign_keys = ON;')
        except Error as er:
            print(er)
        return conexao 
    

class Crud:
    def __init__(self):
        self.conexao = Conexao()

    #inserir
    def insert(self, sql):
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            if cursor.rowcount == 1:
                con.commit()
            con.close()
            return cursor.rowcount
        except Error as er:
            print(er)

    #inserir retorna id
    def insert_id(self, sql):
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            id = None
            if cursor.rowcount == 1:
                id = cursor.execute('select last_insert_rowid()').fetchone()[0]
                con.commit()
            con.close()
            return id
        except Error as er:
            print(er)

    #listar
    def get(self, sql):
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()
            con.close()
            return resultado
        except Error as er:
            print(er)

    def update(self, sql):
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            if cursor.rowcount == 1:
                con.commit()
            con.close()
            return cursor.rowcount
        except Error as er:
            print(er)

    def update_id(self, sql):
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            if cursor.rowcount == 1:
                con.commit()
            con.close()
            return cursor.rowcount
        except Error as er:
            print(er)

    #excluir
    def delete(self, sql):
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            if cursor.rowcount == 1:
                con.commit()
            con.close()
            return cursor.rowcount
        except Error as er:
            print(er)

    def drop_database(self):
        sql = ''' select name from sqlite_master where type="table" ;'''
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute('PRAGMA foreign_keys = OFF;')
            tabelas = cursor.execute(sql).fetchall()
            if tabelas:
                for tabela in tabelas:
                    nome_tabela = tabela[0]
                    if nome_tabela != 'sqlite_sequence':
                        sql1 = f''' drop table if exists {nome_tabela} ;'''
                        sql2 = f''' delete from sqlite_sequence where name = "{nome_tabela}" ;'''
                        cursor.execute(sql1)
                        cursor.execute(sql2)
            con.commit()
            con.close()

        except Error as er:
            print(er)
