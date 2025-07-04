from flask import Blueprint, request, jsonify, session
from flaskProject.mapper.ContentMapper import ContentAnalysisMapper

content_bp=Blueprint('content', __name__)
conMapper = ContentAnalysisMapper()
@content_bp.route('/type_p', methods=['GET'])
def type_p():
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    country = request.args.get('country', type=str)

    # 调用Mapper获取原始数据
    raw_data = conMapper.get_type_distribution_analysis(start_year, end_year, country)

    if not raw_data:
        return jsonify({ "message": "error"}), 400
    # 构建符合要求的响应格式
    response = {
        "code": 200,
        "message": "success",
        "data": raw_data
    }

    return jsonify(response)
@content_bp.route('/boxOffice', methods=['GET'])
def type_b():
    # 调用Mapper获取原始数据
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)

    raw_data = conMapper.get_type_boxoffice_analysis(start_year, end_year)

    # 构建符合要求的响应格式
    response = {
        "code": 200,
        "message": "success",
        "data": {
            "analysis": [
                {
                    "type": item['type'],
                    "avgBoxOffice": round(float(item['avgBoxOffice']), 1),
                    "maxBoxOffice": round(float(item['maxBoxOffice']), 1),
                    "minBoxOffice": round(float(item['minBoxOffice']), 1),
                    "totalBoxOffice": round(float(item['totalBoxOffice']), 1)
                }
                for item in raw_data
            ]
        }
    }

    return jsonify(response)
@content_bp.route('/Type_score', methods=['GET'])
def Type_score():
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    country = request.args.get('country', type=str)
    # 调用Mapper获取原始数据
    raw_data = conMapper.get_type_rating_analysis(start_year, end_year, country)
    # 构建符合要求的响应格式
    response = {
        "code": 200,
        "message": "success",
        "data": {
            "timeRange": f"{start_year}-{end_year}" if start_year and end_year else "全部年份",
            "totalMovies": raw_data.get('totalMovies', 0),
            "analysis": [
                {
                    "type": item['type'],
                    "avgRating": round(float(item['avgRating']), 1),
                    "medianRating": round(float(item['medianRating']), 1),
                    "ratingDistribution": {
                        "0-3": item['ratingDistribution'].get('0-3', 0),
                        "3-6": item['ratingDistribution'].get('3-6', 0),
                        "6-7": item['ratingDistribution'].get('6-7', 0),
                        "7-8": item['ratingDistribution'].get('7-8', 0),
                        "8-9": item['ratingDistribution'].get('8-9', 0),
                        "9-10": item['ratingDistribution'].get('9-10', 0)
                    }
                }
                for item in raw_data.get('analysis', [])
            ]
        }
    }

    return jsonify(response)


