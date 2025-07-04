from flask import Blueprint, request, jsonify, session
from flaskProject.mapper.TeamMapper import TeamAnalysisMapper
team_bp = Blueprint('team', __name__)
teamMapper = TeamAnalysisMapper()
@team_bp.route('/production-ranking', methods=['GET'])
def production_rating():
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    top_N=request.args.get('top_N', type=int, default=10)
    # 调用Mapper获取原始数据
    raw_data = teamMapper.get_director_boxoffice_ranking(start_year, end_year,top_N)
    if not raw_data:
        return jsonify({"message": "error"}), 400
    # 构建符合要求的响应格式
    response = {
        "ranking": [
            {
                "rank": item["rank"],
                "name": item["name"],
                "totalMovies": item["totalMovies"],
                "totalBoxOffice": item["totalBoxOffice"]
            }
            for item in raw_data.get("ranking", [])
        ]
    }
    return jsonify(response)
@team_bp.route('/director_score', methods=['GET'])
def director_score():
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    top_n= request.args.get('top_n', type=int, default=10)
    data = teamMapper.get_top_directors(start_year, end_year, top_n)
    return jsonify({"data": data})
@team_bp.route('/director_like', methods=['GET'])
def director_like():
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    director_name= request.args.get('director_name', type=str)
    data = teamMapper.get_director_genre_stats(director_name,start_year, end_year)
    if not data:
        return jsonify({"message": "error"}), 400
    else:
        return jsonify({"data": data})
@team_bp.route('/actor', methods=['GET'])
def actor():
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    actor_name= request.args.get('actor_name', type=str)
    data = teamMapper.get_actor_stats(start_year, end_year,actor_name)
    if not data:
        return jsonify({"message": "error"}), 400
    else:
        return jsonify({"data": data})