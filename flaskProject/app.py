# app.py
from flask import Flask, jsonify
from api.Admin import admin_bp
from api.User import user_bp
from api.Basic import basic_bp
from api.Team import team_bp
from api.Content import content_bp
from api.Preference import preference_bp
from api.TimeSpace import timespace_bp
from flask_cors import CORS

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(basic_bp)
app.register_blueprint(team_bp)
app.register_blueprint(content_bp)
app.register_blueprint(preference_bp)
app.register_blueprint(timespace_bp)
CORS(app, supports_credentials=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)