# User.py
from decimal import Decimal

from flask import Blueprint, request, jsonify
from mapper.UserMapper import UserMapper
from datetime import datetime
import logging

user_bp = Blueprint('user', __name__, url_prefix='/api/user')
user_mapper = UserMapper()  # 创建UserMapper实例

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 处理 Decimal 类型数据，确保 JSON 可序列化
def decimal_to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    return value

@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    data = request.json

    # 验证必填字段
    if not all(field in data for field in ['username', 'password']):
        return jsonify({
            "success": False,
            "message": "需要用户名和密码"
        }), 400

    try:
        user = user_mapper.get_user_by_username(data['username'])

        # 明文密码比较
        if user and user['password'] == data['password']:
            if user['role_type'] == 2:
                logger.info(f"用户登录成功: {user['username']}")
                return jsonify({
                    "success": True,
                    "user_id": user['user_id'],
                    "role_type": user['role_type'],
                    "message": "登录成功"
                }), 200
            else:
                return jsonify({
                    "success": False,
                    "message": "管理员请通过管理员通道登录"
                })
        else:
            return jsonify({
                "success": False,
                "message": "用户名或密码错误"
            }), 401

    except Exception as e:
        logger.error(f"登录错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    """获取用户个人信息"""
    try:
        user = user_mapper.get_user_by_id(user_id)

        if user:
            # 移除敏感信息
            user.pop('password', None)
            user.pop('update_time', None)

            return jsonify({
                "success": True,
                "data": user,
                "message": "用户查询成功"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "用户不存在"
            }), 404

    except Exception as e:
        logger.error(f"查询用户信息错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    data = request.json

    # 验证必填字段
    if not all(field in data for field in ['username', 'password']):
        return jsonify({
            "success": False,
            "message": "需要用户名和密码"
        }), 400

    try:
        # 检查用户名是否已存在
        if user_mapper.get_user_by_username(data['username']):
            return jsonify({
                "success": False,
                "message": "用户名已存在"
            }), 400

        # 准备用户数据
        user_data = {
            "username": data['username'],
            "password": data['password'],
            "real_name": "",
            "phone": "",
            "email": "",
            "role_type": 2,  # 默认普通用户
        }
        # 调用Mapper创建用户
        result = user_mapper.create_user(user_data)

        if result:
            logger.info(f"新用户注册成功: {user_data['username']}")
            return jsonify({
                "success": True,
                "message": "注册成功",
                "data": {
                    "user_id": result,
                    "username": user_data['username']
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "注册失败"
            }), 400

    except Exception as e:
        logger.error(f"注册错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@user_bp.route('/auth/<int:user_id>', methods=['GET'])
def check_auth(user_id):
    """验证用户权限"""
    try:
        user = user_mapper.get_user_by_id(user_id)

        if not user:
            return jsonify({
                "success": False,
                "message": "用户不存在"
            }), 400

        role_type = user.get('role_type')
        role_name = "管理员" if role_type == 1 else "普通用户"

        return jsonify({
            "success": True,
            "message": f"用户为{role_name}"
        }), 200

    except Exception as e:
        logger.error(f"验证权限错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user_info(user_id):
    """修改个人信息"""
    data = request.json

    # 验证可更新字段
    updatable_fields = ['username', 'real_name', 'phone', 'email']
    if not all(field in data for field in updatable_fields):
        return jsonify({
            "success": False,
            "message": "需要提供更新字段(用户名、真实姓名、电话、邮箱)"
        }), 400

    try:

        # 检查新用户名是否已存在
        existing_user = user_mapper.get_user_by_username(data['username'])
        if existing_user and existing_user['user_id'] != user_id:
            return jsonify({
                "success": False,
                "message": "用户名已存在"
            }), 400

        # 准备更新数据
        update_data = {'username': data['username'],
                       'real_name': data['real_name'],
                       'phone': data['phone'],
                       'email': data['email']
                       }

        # 调用Mapper更新用户
        result = user_mapper.update_user(user_id, update_data)

        if result:
            logger.info(f"用户信息更新成功: user_id={user_id}")
            return jsonify({
                "success": True,
                "message": "信息更新成功"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "信息更新失败"
            }), 400

    except Exception as e:
        logger.error(f"更新用户信息错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


#
@user_bp.route('/movies', methods=['GET'])
def get_movies():
    """查询电影列表"""
    try:
        # 获取查询参数
        page = int(request.args.get('page'))
        page_size = int(request.args.get('page_size'))
        title = request.args.get('title', '').strip()
        director = request.args.get('director', '').strip()
        start_year=request.args.get('start_year')
        end_year=request.args.get('end_year')
        if director == '':
            director = None
        genre = request.args.get('genre').strip()
        if genre == '':
            genre = None
        min_rating = request.args.get('min_rating')
        if min_rating == '':
            min_rating = 0
        else:
            min_rating = float(min_rating)
        if start_year == '':
            start_year = None
        if end_year == '':
            end_year = None
        sort_field = request.args.get('sort_field', 'title')
        sort_order = request.args.get('sort_order', 'desc') == 'asc'

        genre_id = user_mapper.get_movie_genre_by_name(genre)
        director_id = user_mapper.get_movie_director_by_name(director)


        # 调用Mapper获取电影列表
        movies = user_mapper.get_movie_list(
            page=page,
            page_size=page_size,
            title=title,
            genre_id=genre_id,
            director_id=director_id,
            min_rating=min_rating,
            sort_field=sort_field,
            sort_order=sort_order,
            start_year=start_year,
            end_year=end_year
        )

        # 获取电影总数
        total = user_mapper.get_movie_count(
            title=title,
            genre_id=genre_id,
            director_id=director_id,
            min_rating=min_rating,
            start_year=start_year,
            end_year=end_year
        )
        # 批量获取关联数据
        movie_ids = [m.movie_id if hasattr(m, 'movie_id') else m['movie_id'] for m in movies]

        directors_map = user_mapper.get_movies_directors(movie_ids)
        actors_map = user_mapper.get_movies_actors(movie_ids)
        genres_map = user_mapper.get_movies_genres(movie_ids)

        # 格式化返回结果
        movie_list = []
        for movie in movies:
            movie_dict = movie.asDict() if hasattr(movie, 'asDict') else dict(movie)
            mid = movie_dict['movie_id']

            movie_list.append({
                "movie_id": mid,
                "title": movie_dict['title'],
                "release_date": movie_dict.get('release_date', ''),
                "total_box_office": decimal_to_float(movie_dict.get('total_box_office', 0)),
                "avg_ticket_price": decimal_to_float(movie_dict.get('avg_ticket_price', 0)),
                "country": movie_dict.get('country', ''),
                "overall_rating": decimal_to_float(movie_dict.get('overall_rating', 0)),
                "directors": directors_map.get(mid, []),
                "main_actors": actors_map.get(mid, []),
                "genres": genres_map.get(mid, []),
                "description": movie_dict.get('description', '')
            })

        return jsonify({
            "success": True,
            "data": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "items": movie_list
            }
        }), 200

    except Exception as e:
        logger.error(f"查询电影列表错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500
