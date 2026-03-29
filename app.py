from flask import Flask
from flask_jwt_extended import JWTManager
from routes.auth import auth
from routes.file import file_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(file_bp)

if __name__ == "__main__":
    app.run(debug=True)

    from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from routes.auth import auth
from routes.file import file_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(auth)
app.register_blueprint(file_bp)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)