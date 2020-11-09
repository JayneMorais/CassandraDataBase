class Review(): 
    def __init__(self, usuario_id, filme_id, comentario, gostou):
        self.usuario_id = usuario_id
        self.filme_id = filme_id
        self.gostou  = int(gostou)
        self.comentario = comentario

    def set_usuario_id(self , novo_usuario_id):
        self.usuario_id = novo_usuario_id

    def set_filme_id(self, novo_filme_id): 
        self.filme_id = novo_filme_id
    
    def set_gostou (self, novo_gostou):
        self.gostou = novo_gostou

    def set_comentario(self, novo_comentario):
        self.comentario = novo_comentario
