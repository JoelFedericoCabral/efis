from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required 
from marshmallow import ValidationError

from app import db
from app.schemas import post_schema 
from app.models import Post

bp = Blueprint('posts', __name__)

class PostAPI(MethodView):

    def get(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return jsonify(error=f'Post {post_id} not found.'), 404
        return post_schema.dump(post), 200

    @jwt_required()
    def post(self):
        # Crear nuevo post
        print('end1')
        post_data = request.json
        if not post_data:
            return jsonify(error='Not input data provided.'), 400
        print('end2')

        try:
            post = post_schema.load(post_data)
            post.user_id = current_user.id
            print('end3')
            db.session.add(post)
            db.session.commit()
            return post_schema.dump(post), 201
        except ValidationError as err:
            return jsonify(err.messages), 400

    @jwt_required()
    def delete(self, post_id):
        # Eliminar un post
        post = Post.query.get(post_id)
        if not post:
            return jsonify(error=f'Post {post_id} not found.'), 404

        # Verifica si es dueño
        if post.user_id != current_user.id:
            return jsonify(error='Forbidden'), 403

        db.session.delete(post)
        db.session.commit()

        return jsonify(message='Post delete sucesfully.'), 200

    @jwt_required()
    def put(self, post_id):
        # Actualizar una sola publicación
        post_data = request.json
        if not post_data:
            return jsonify(error='No input data provided.'), 400

        post = Post.query.get(post_id)
        if not post:
            return jsonify(error=f'Post {post_id} not found.'), 404

        # Verifica si eres dueño
        if post.user_id != current_user.id:
            return jsonify(error='Forbidden'), 403

        try:
            updated_post = post_schema.load(post_data, instance=post, partial=True)
            db.session.commit()
            return post_schema.dump(updated_post), 200
        except ValidationError as err:
            return jsonify(err.messages), 400

post_view = PostAPI.as_view('post_api')
bp.add_url_rule('/', view_func=post_view, methods=['POST',])
bp.add_url_rule('/<int:post_id>/', view_func=post_view, methods=['GET', 'PUT', 'DELETE'])