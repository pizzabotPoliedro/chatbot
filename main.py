from flask import Flask
from src.modules.health.health_controller import health_bp
from src.modules.chat.chat_controller import chat_bp
from src.modules.users.users_controller import users_bp
from src.shared.infra.environments import Environments

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# health check
app.register_blueprint(health_bp)

# chat
app.register_blueprint(chat_bp)

# users
app.register_blueprint(users_bp)

if __name__ == '__main__':
    Environments()
    app.run(debug=True)