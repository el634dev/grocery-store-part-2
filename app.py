from grocery_app.extensions import app, db
from grocery_app.routes import main, auth
from flask_migrate import Migrate

app.register_blueprint(main)
app.register_blueprint(auth)

migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
