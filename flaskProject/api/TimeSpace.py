from flask import Blueprint, request, jsonify
from flaskProject.mapper.TimeSpaceMapper import TimeSpaceAnalysisMapper
import logging

timespace_bp = Blueprint('timespace', __name__)
timespace_mapper = TimeSpaceAnalysisMapper()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@timespace_bp.route('/timeline', methods=['GET'])
def movie_boxoffices_changes():
    try:
        movie_name = request.args.get('movie_name', type=str).strip()
        ret = timespace_mapper.get_movie_boxoffices(movie_name)
        return jsonify(ret)

    except Exception as e:
        logger.error(f"电影票房变化获取错误: {str(e)}")
        return jsonify({
            "times": [],
            "box_offices": []
        })


@timespace_bp.route('/area', methods=['GET'])
def area_type_data():
    try:
        year = request.args.get('year', type=int)
        ret = timespace_mapper.get_area_data(year)
        return jsonify(ret)

    except Exception as e:
        logger.error(f"电影类型地域统计错误: {str(e)}")
        return jsonify([])
