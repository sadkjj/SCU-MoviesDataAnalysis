
from flask import Flask, jsonify
from flaskProject.api.Content import content_bp
from flaskProject.api.Team import team_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(content_bp)
app.register_blueprint(team_bp)


# 添加根路由
@app.route('/')
def home():
    return jsonify({
        "message": "欢迎访问电影数据API",
        "status": "running"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)