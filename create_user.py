from app import app
from extensions import db
from models import User

with app.app_context():
    user=User(
        username="Akhil kumar varun",
        email="imakahilvarun@gmail.com",
        password="12345"
    )

    db.session.add(user)
    db.session.commit()

    print("created!")