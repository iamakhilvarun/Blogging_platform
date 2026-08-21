from flask import Flask, request
from extensions import db
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTMANGER(app)
db.init_app(app)

from models import User, Post


@app.route("/")
def home():
    return "<p>Blog api running</p>"


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    title = data["title"]
    content = data["content"]

    post = Post(title=title, content=content, user_id=1)

    db.session.add(post)
    db.session.commit()

    return {"message": "Post createad sucessfully", "post_id": post.id}


@app.route("/posts", methods=["GET"])
def create_get():
    posts = Post.query.all()  # we getting all the existing posts in the database

    return [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
        }
        for post in posts
    ]


# fetch the selected id posts
@app.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    post = Post.query.get(id)

    if post is None:
        return {"message": "Post not found"}, 404

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "user_id": post.user_id,
    }


# update
@app.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    post = Post.query.get(id)
    if post is None:
        return {"message": "Post not found"}, 404

    data = request.get_json()

    post.title = data["title"]
    post.content = data["content"]

    db.session.commit()

    return {"message": "Post updated sucessfully"}


# Delete
@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get(id)

    if post is None:
        return {"message": "Post not found"}, 404

    db.session.delete(post)
    db.session.commit()

    return {"message": "Post deleted sucessfully"}
@app.route("/register",methods=["POST"])
def register():
    pass

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
