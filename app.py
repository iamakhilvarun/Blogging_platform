from flask import Flask, request
from extensions import db
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)
db.init_app(app)

from models import User, Post


@app.route("/")
def home():
    return "<p>Blog api running</p>"


@app.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()

    user_id = get_jwt_identity()

    title = data["title"]
    content = data["content"]

    post = Post(title=title, content=content, user_id=user_id)

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


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data["username"]
    email = data["email"]
    password = data["password"]

    hashed_password = generate_password_hash(password)

    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return {"message": "User not found"}, 404

    if not check_password_hash(user.password, password):
        return {"message": "Invalid password"}, 401

    token = create_access_token(identity=str(user.id))

    return {"access_token": token}, 200


@app.route("/logout", methods=[""])
@jwt_required
def logout():
    return {"message": "You have logged out"}


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
