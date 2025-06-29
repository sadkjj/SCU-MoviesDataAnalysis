from flask import Flask, render_template, session
from api.User import user_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(user_bp, url_prefix='/api/user')

@app.route('/')
def home():
    if 'user_id' in session:
        return f"欢迎, 用户 {session['user_id']}! <a href='/logout'>登出</a>"
    return "<a href='/login'>登录</a>"

@app.route('/login')
def login_page():
    return render_template('index.html')

@app.route('/logout')
def logout_page():
    session.clear()
    return "已登出 <a href='/login'>重新登录</a>"

if __name__ == '__main__':
    app.run(debug=True)