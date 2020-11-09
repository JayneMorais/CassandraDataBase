from flask import Flask, request, Response
from infra.dao_reviews import review_dao
from models.review import Review
import json

app = Flask(__name__)
dao = review_dao()

@app.route("/reviews", methods=["GET"])
def listar():

    response = dao.listar_reviews()

    return Response(
        json.dumps(response), status=response["code"], mimetype="application/json"
    )


@app.route("/review", methods=["POST"])
def create():
    usuario_id = request.form["usuario_id"]
    filme_id = request.form["filme_id"]
    gostou = request.form["gostou"]
    comentario = request.form["comentario"]

    review = Review(
        usuario_id=usuario_id, filme_id=filme_id, gostou=gostou, comentario=comentario
    )

    response = dao.cria_review(review)

    return Response(
        json.dumps(response), status=response["code"], mimetype="application/json"
    )


@app.route("/review/<review_id>", methods=["PUT"])
def update(review_id):
    
    usuario_id = request.form["usuario_id"]
    filme_id = request.form["filme_id"]
    gostou = request.form["gostou"]
    comentario = request.form["comentario"]

    review = Review(
        usuario_id=usuario_id, filme_id=filme_id, gostou=gostou, comentario=comentario
    )
    response = dao.atualiza_review(review_id, review)

    return Response(
        json.dumps(response), status=response["code"], mimetype="application/json"
    )

@app.route("/review/<review_id>", methods=["DELETE"])
def delete(review_id):
       
    response = dao.remove_review(review_id)

    return Response(
        json.dumps(response), status=response["code"], mimetype="application/json"
    )


@app.route("/review/<review_id>", methods=["GET"])
def read(review_id):
    response = dao.busca_review(review_id)

    return Response(
        json.dumps(response), status=response["code"], mimetype="application/json"
    )


@app.route("/filme/<filme_id>/reviews", methods=["GET"])
def read_filmes(filme_id):
    response = dao.busca_reviews_filme(filme_id)

    return Response(
        json.dumps(response), status=response["code"], mimetype="application/json"
    )
