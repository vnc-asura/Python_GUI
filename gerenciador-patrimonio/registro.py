from comportamento import JanelaControl as JControl

class Registro:
    def reg_criacao(self, id):
        sql = f''' insert into registros(registro, id_patrimonio)
          values ("Patrimonio registrado com sucesso", {id})  ;'''
        JControl.ref.crud.insert(sql)
        
    def reg_atualizacao(self, id, status, local):
        sql = f''' insert into registros(registro, id_patrimonio)
          values ("Patrimonio atualizado: (status = {status}), (local = {local})", {id})  ;'''
        JControl.ref.crud.insert(sql)
