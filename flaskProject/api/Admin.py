# Admin.py
from flask import Blueprint, request, jsonify
from mapper.AdminMapper import AdminMapper
from datetime import datetime
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
mapper = AdminMapper()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@admin_bp.route('/user', methods=['POST'])
def add_user():
    """管理员添加用户接口"""
    data = request.json

    # 验证必填字段
    required_fields = ['username', 'password', 'phone', 'email', 'role_type']
    if not all(field in data for field in required_fields):
        return jsonify({
            "success": False,
            "message": "缺少必填字段(用户名、密码、电话、邮箱、角色类型)"
        }), 400

    if mapper.get_user_by_username(data['username']):
        return jsonify({
            "success": False,
            "message": "用户名已存在"
        })

    try:
        # 准备用户数据
        user_data = {
            "username": data['username'],
            "password": data['password'],
            "real_name": data.get('real_name', ""),
            "phone": data.get('phone', ""),
            "email": data.get('email', ""),
            "role_type": int(data['role_type']),
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 调用Mapper创建用户
        result = mapper.create_user(user_data)

        if result:
            logger.info(f"管理员创建用户成功: {user_data['username']}")
            return jsonify({
                "success": True,
                "message": "用户创建成功",
                "data": {
                    "user_id": result,
                    "username": user_data['username']
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "用户创建失败"
            }), 400

    except Exception as e:
        logger.error(f"创建用户错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@admin_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """管理员修改用户信息接口"""
    data = request.json

    # 验证至少有一个可更新字段
    updatable_fields = ['username', 'real_name', 'phone', 'email', 'role_type']
    if not all(field in data for field in updatable_fields):
        return jsonify({
            "success": False,
            "message": "需要提供可更新字段(用户名、真实姓名、电话、邮箱、角色类型)"
        }), 400

    try:
        # 准备更新数据
        update_data = {'update_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'username': data['username'],
                       'real_name': data['real_name'], 'phone': data['phone'], 'email': data['email'],
                       'role_type': int(data['role_type'])}

        # 调用Mapper更新用户
        result = mapper.update_user(user_id, update_data)

        if result:
            logger.info(f"用户信息更新成功: user_id={user_id}")
            return jsonify({
                "success": True,
                "message": "用户信息已更新"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "用户信息修改失败"
            }), 400

    except Exception as e:
        logger.error(f"更新用户错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """管理员删除用户接口"""
    try:
        result = mapper.delete_user(user_id)

        if result:
            logger.info(f"用户删除成功: user_id={user_id}")
            return jsonify({
                "success": True,
                "message": "用户删除成功"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "用户删除失败"
            }), 400

    except Exception as e:
        logger.error(f"删除用户错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@admin_bp.route('/users', methods=['GET'])
def get_users():
    """查询用户列表接口"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        sort_field = request.args.get('sort_field', 'create_time')
        sort_order = request.args.get('sort_order', 'desc') == 'asc'
        search = request.args.get('search', '').strip()
        if search == '':
            search = None

        # 调用Mapper获取数据
        users = mapper.get_user_list(
            page=page,
            page_size=page_size,
            sort_field=sort_field,
            sort_order=sort_order,
            search=search
        )

        # 获取总数
        total = mapper.get_user_count(search)

        return jsonify({
            "success": True,
            "data": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "items": [user.asDict() if hasattr(user, 'asDict') else user for user in users]
            }
        }), 200

    except Exception as e:
        logger.error(f"查询用户列表错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """管理员登录接口"""
    data = request.json

    # 验证必填字段
    if not all(field in data for field in ['username', 'password']):
        return jsonify({
            "success": False,
            "message": "需要用户名和密码"
        }), 400

    try:
        # 在实际应用中应该查询数据库验证用户
        user = mapper.get_user_by_username(data['username'])

        if user and user['password'] == data['password']:
            if user['role_type'] == 1:  # 假设1是管理员角色
                logger.info(f"管理员登录成功: {user['username']}")
                return jsonify({
                    "success": True,
                    "user_id": user['user_id'],
                    "role_type": user['role_type'],
                    "message": "管理员登录成功"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "message": "非管理员账号"
                }), 401
        else:
            return jsonify({
                "success": False,
                "message": "用户名或密码错误"
            }), 400

    except Exception as e:
        logger.error(f"登录错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@admin_bp.route('/movie/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    if mapper.get_movie_by_id(movie_id) is None:
        return jsonify({
            "success": False,
            "message": "电影不存在"
        })
    try:
        result = mapper.delete_movie(movie_id)
        if result:
            logger.info(f"电影删除成功: movie_id={movie_id}")
            return jsonify({
                "success": True,
                "message": "电影删除成功"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "电影删除失败"
            }), 400

    except Exception as e:
        logger.error(f"删除电影错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500
