# Basic.py
from flask import Blueprint, request, jsonify
from mapper.BasicMapper import BasicMapper
from decimal import Decimal
import logging

basic_bp = Blueprint('basic', __name__, url_prefix='/api/basic')
mapper = BasicMapper()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 处理 Decimal 类型数据，确保 JSON 可序列化
def decimal_to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    return value

@basic_bp.route('/production/yearly', methods=['GET'])
def yearly_production():
    """年度电影产量统计"""
    try:
        start_year = request.args.get('start_year', type=int)
        end_year = request.args.get('end_year', type=int)
        country = request.args.get('country', '').strip()

        # 验证年份范围
        if start_year > end_year:
            return jsonify({
                "success": False,
                "message": "起始年份不能大于结束年份"
            }), 400

        # 获取所有年份数据
        yearly_data = mapper.get_yearly_movie_count(start_year, end_year)

        # 获取特定国家数据（如果指定了国家）
        country_data = []
        if country:
            country_data = mapper.get_yearly_movie_count(start_year, end_year, country)

        # 准备返回数据
        # 准备标签（所有年份）
        labels = [str(year) for year in range(start_year, end_year + 1)]
        yearly_data_dict = {str(item['year']): item['count'] for item in yearly_data}  # 转换为字典方便查找

        # 生成对应的产量数据，没有的年份填0
        total_counts = [yearly_data_dict.get(year, 0) for year in labels]
        response_data = {
            "labels": labels,
            "datasets": [
                {
                    "label": "总产量",
                    "data": total_counts
                }
            ]
        }

        if country:
            country_data_dict = {str(item['year']): item['count'] for item in country_data}  # 转换为字典方便查找
            country_counts = [country_data_dict.get(year, 0) for year in labels]
            response_data['datasets'].append({
                "label": country,
                "data": country_counts
            })

        return jsonify({
            "success": True,
            "data": response_data
        }), 200

    except Exception as e:
        logger.error(f"年度产量统计错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@basic_bp.route('/production/monthly', methods=['GET'])
def monthly_production():
    """月度电影产量统计"""
    try:
        year = request.args.get('year', type=int)
        country = request.args.get('country', 'all').strip()

        if not year:
            return jsonify({
                "success": False,
                "message": "需要指定年份参数"
            }), 400

        monthly_data = mapper.get_monthly_movie_count(year, country)

        # 月份标签
        month_labels = [f"{month}月" for month in range(1, 13)]

        # 初始化每月数据为0
        month_counts = [0] * 12
        for item in monthly_data:
            month_counts[item['month'] - 1] = item['count']

        return jsonify({
            "success": True,
            "data": {
                "labels": month_labels,
                "datasets": [{
                    "label": f"{year}年产量" + (f"({country})" if country else ""),
                    "data": month_counts
                }]
            }
        }), 200

    except Exception as e:
        logger.error(f"月度产量统计错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@basic_bp.route('/production/countries', methods=['GET'])
def country_production():
    """国家/地区产量统计"""
    try:
        year = request.args.get('year', type=int)

        country_stats = mapper.get_country_movie_stats(year if year else None)

        # 转换为前端需要的格式
        data = [{
            "country": item['country'],
            "count": item['count'],
            "percentage": round(item['percentage'], 2)
        } for item in country_stats]

        return jsonify({
            "success": True,
            "data": data
        }), 200

    except Exception as e:
        logger.error(f"国家产量统计错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@basic_bp.route('/boxoffice/ranking', methods=['GET'])
def boxoffice_ranking():
    """票房总排行"""
    try:
        ranking_type = request.args.get('type', 'total')  # total/yearly/genre
        year = request.args.get('year', type=int)
        genre = request.args.get('genre', '').strip()
        if genre == '':
            genre = None
        limit = request.args.get('limit', default=10, type=int)

        genre_id = mapper.get_movie_genre_by_name(genre)

        top_movies = mapper.get_top_movies(
            limit=limit,
            year=year if year else None,
            genre_id=genre_id if genre_id else None
        )

        # 格式化返回数据
        data = []
        for idx, movie in enumerate(top_movies, 1):
            if hasattr(movie, 'asDict'):
                movie = movie.asDict()

            data.append({
                "rank": idx,
                "movie_id": movie['movie_id'],
                "title": movie['title'],
                "box_office": decimal_to_float(round(movie.get('total_box_office', 0) / 10000, 1)),  # 转换为万元
                "country": movie.get('country', ''),
                "release_year": int(movie.get('release_date')[:4])
            })

        return jsonify({
            "success": True,
            "data": data
        }), 200

    except Exception as e:
        logger.error(f"票房排行查询错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500


@basic_bp.route('/boxoffice/cost-relation', methods=['GET'])
def boxoffice_cost_relation():
    """票房和成本关系分析"""
    try:
        year = request.args.get('year', type=int)
        genre = request.args.get('genre', '').strip()

        genre_id = mapper.get_movie_genre_by_name(genre)

        cost_data = mapper.get_box_office_by_budget(
            year=year if year else None,
            genre_id=genre_id if genre_id else None
        )

        # 准备图表数据
        labels = [item['budget_range'] for item in cost_data]
        avg_box_office = [decimal_to_float(item['avg_box_office']) for item in cost_data]
        max_box_office = [decimal_to_float(item['max_box_office']) for item in cost_data]

        return jsonify({
            "success": True,
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "平均票房",
                        "data": avg_box_office
                    },
                    {
                        "label": "最高票房",
                        "data": max_box_office
                    }
                ]
            }
        }), 200

    except Exception as e:
        logger.error(f"票房成本分析错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"服务器错误: {str(e)}"
        }), 500