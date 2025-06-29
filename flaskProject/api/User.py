from flask import Blueprint, request, jsonify, session
from mapper.UserMapper import UserMapper

user_bp = Blueprint('user', __name__)
user_mapper = UserMapper()


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')

    user = user_mapper.get_user_by_id(user_id)

    if user and user['password'] == password:
        session['user_id'] = user['user_id']
        return jsonify({'success': True, 'message': '登录成功'})

    return jsonify({'success': False, 'message': '用户ID或密码错误'}), 401


@user_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': '登出成功'})


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')

    if user_mapper.get_user_by_id(user_id):
        return jsonify({'success': False, 'message': '用户ID已存在'}), 400

    user_mapper.create_user(user_id, password)
    return jsonify({'success': True, 'message': '注册成功'})