from .dao import dao_factory
import uuid
import datetime

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return int(unix_time(dt) * 1000.0)

def to_dict_list(rows):
    result = []
    for row in rows.result():
        tmp = {
            "id": str(row.id),
            "usuario_id": row.usuario_id,
            "filme_id": row.filme_id,
            "comentario": row.comentario,
            "gostou": row.gostou
        }

        result.append(tmp)

    return result

class review_dao:
    def __init__(self):
        self.__session = None
        try:
            self.__factory = dao_factory()
            self.__session = self.__factory.get_session()
            self.create_table()

        except Exception as e:
            print("Erro de conexão: " + str(e))

    def create_table(self):
        query = """
				CREATE TABLE IF NOT EXISTS reviews_db.reviews (
                id UUID, 
                gostou INT, 
                usuario_id TEXT, 
                filme_id TEXT,
                comentario TEXT,
                criado_em TIMESTAMP,
                atualizado_em TIMESTAMP,
                PRIMARY KEY (id));
		"""
        self.__session.execute(query)

    def listar_reviews(self):
        try:
            rows = self.__session.execute_async(
                "SELECT * FROM reviews_db.reviews", 
            )

            response = to_dict_list(rows) 

            return {"code": 200, "response": "ok", "count": len(response), "data": response }
        except Exception as e:
            return {"code": 500, "response": "erro "+str(e)}

    def busca_review(self, review_id):
        
        review_id = uuid.UUID(review_id)

        try:
            rows = self.__session.execute_async(
                """
                SELECT * FROM reviews_db.reviews WHERE id=%s
                """, 
                [review_id]
            )

            return {"code": 200, "response": "ok", "data": to_dict_list(rows)}
        except Exception as e:
            return {"code": 500, "response": "erro "+str(e)}

    def cria_review(self, review):
        try:
            rows = self.__session.execute_async(
                """
                INSERT INTO reviews_db.reviews (id, usuario_id, filme_id, comentario, gostou, criado_em, atualizado_em)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    uuid.uuid1(),
                    review.usuario_id,
                    review.filme_id,
                    review.comentario,
                    review.gostou,
                    unix_time_millis(datetime.datetime.now()),
                    unix_time_millis(datetime.datetime.now())
                ),
            )

            response = to_dict_list(rows) 
            return {"code": 201, "response": "criado", "count": len(response), "data": response }
        except Exception as e:
            return {"code": 500, "response": "erro " + str(e)}

    def remove_review(self, review_id):
        
        review_id = uuid.UUID(review_id)

        try:
            rows = self.__session.execute_async(
                """
                DELETE FROM reviews_db.reviews 
                WHERE id=%s
                """,
                [review_id],
            )

            response = to_dict_list(rows)

            return {"code": 200, "response": "removido", "count": len(response), "data": response }
        except Exception as e:
            return {"code": 500, "response": "erro"}

    def atualiza_review(self, review_id, novo_review):
        
        review_id = uuid.UUID(review_id)

        try:
            rows = self.__session.execute_async(
                """
                UPDATE reviews_db.reviews 
                SET comentario = %s,
                gostou = %s,
                atualizado_em = %s
                WHERE id = %s
                """,
                (novo_review.comentario, novo_review.gostou, unix_time_millis(datetime.datetime.now()), review_id),
            )
            
            response = to_dict_list(rows) 

            return {"code": 200, "response": "atualizado", "count": len(response), "data": response }
        except Exception as e:
            return {"code": 500, "response": "erro"}

            
    def busca_reviews_filme(self, filme_id):

        try:
            rows = self.__session.execute_async(
                """
                SELECT * FROM reviews_db.reviews WHERE filme_id=%s ALLOW FILTERING
                """, 
                [filme_id]
            )

            return {"code": 200, "response": "ok", "data": to_dict_list(rows)}
        except Exception as e:
            return {"code": 500, "response": "erro "+str(e)}
